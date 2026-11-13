"""Regression checks for setup, generated media, and notebook structure."""

import ast
import json
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

import nbformat

import course_utils as course


class SetupTests(unittest.TestCase):
    def test_default_saas_and_dedicated_url(self):
        for value, expected in [
            ("", "https://api.wandb.ai"),
            ("   ", "https://api.wandb.ai"),
            ("https://example.wandb.io/", "https://example.wandb.io"),
        ]:
            with self.subTest(value=value), patch.dict(os.environ, {"WANDB_BASE_URL": value}, clear=True):
                self.assertEqual(course.wandb_base_url(), expected)
        with patch.dict(os.environ, {"WANDB_BASE_URL": "https://example.wandb.io/team/project"}, clear=True):
            with self.assertRaises(ValueError):
                course.wandb_base_url()

    def test_login_uses_selected_host(self):
        fake_wandb = types.ModuleType("wandb")
        from unittest.mock import Mock
        fake_wandb.login = Mock()
        for host in ["", "https://example.wandb.io"]:
            with self.subTest(host=host), patch.dict(
                os.environ, {"WANDB_API_KEY": "test-key", "WANDB_BASE_URL": host}, clear=True
            ), patch.dict(sys.modules, {"wandb": fake_wandb}), patch.object(
                course, "ensure_packages"
            ), patch.object(course, "load_wandb_env"):
                course.setup_wandb()
                fake_wandb.login.assert_called_with(
                    key="test-key", host=host or "https://api.wandb.ai", relogin=True
                )

    def test_optional_missing_secret_does_not_skip_team_and_project(self):
        class SecretNotFoundError(Exception):
            pass

        class NotebookAccessError(Exception):
            pass

        values = {"WANDB_API_KEY": "key", "WANDB_ENTITY": "team", "WANDB_PROJECT": "project"}

        def get(key):
            if key not in values:
                raise SecretNotFoundError(key)
            return values[key]

        userdata = types.SimpleNamespace(
            get=get, SecretNotFoundError=SecretNotFoundError, NotebookAccessError=NotebookAccessError
        )
        google = types.ModuleType("google")
        google.__path__ = []
        colab = types.ModuleType("google.colab")
        colab.userdata = userdata
        google.colab = colab
        with patch.dict(sys.modules, {"google": google, "google.colab": colab}), patch.dict(
            os.environ, {}, clear=True
        ), patch("dotenv.load_dotenv"):
            course.load_wandb_env()
            self.assertEqual(os.environ["WANDB_ENTITY"], "team")
            self.assertEqual(os.environ["WANDB_PROJECT"], "project")
            self.assertNotIn("WANDB_BASE_URL", os.environ)

    def test_cached_login_is_scoped_to_the_selected_host(self):
        from unittest.mock import Mock
        fake_wandb = types.SimpleNamespace(login=Mock())
        with patch.dict(os.environ, {"WANDB_BASE_URL": "https://example.wandb.io"}, clear=True), patch.dict(
            sys.modules, {"wandb": fake_wandb}
        ), patch.object(course, "ensure_packages"), patch.object(course, "load_wandb_env"):
            course.setup_wandb()
        fake_wandb.login.assert_called_once_with(host="https://example.wandb.io")

    def test_dependency_resolver_receives_extras_even_if_wandb_exists(self):
        # Importing the base distribution must not suppress its media extras.
        with patch("course_utils.shutil.which", return_value=None), patch(
            "course_utils.subprocess.check_call"
        ) as install:
            course.ensure_packages(["wandb[media]>=0.19.0", "transformers>=4.40.0,<5"])
        args = install.call_args.args[0]
        self.assertIn("wandb[media]>=0.19.0", args)
        self.assertIn("transformers>=4.40.0,<5", args)


class ContentTests(unittest.TestCase):
    def test_lidar_scene_can_be_serialized_by_wandb(self):
        import wandb
        scene = wandb.Object3D(course.demo_lidar_scene())
        self.assertIsInstance(scene, wandb.Object3D)

    def test_generated_pdb_has_three_atoms(self):
        from rdkit import Chem
        with tempfile.TemporaryDirectory() as directory:
            path = Path(course.write_demo_pdb(Path(directory) / "water.pdb"))
            text = path.read_text()
            self.assertEqual(sum(line.startswith("ATOM") for line in text.splitlines()), 3)
            molecule = Chem.MolFromPDBFile(str(path), removeHs=False)
            self.assertIsNotNone(molecule)
            self.assertEqual(molecule.GetNumAtoms(), 3)

    def test_all_notebooks_have_valid_schema_and_python(self):
        for path in (course.REPO_ROOT / "notebooks").rglob("*.ipynb"):
            with self.subTest(path=path):
                nb = nbformat.read(path, as_version=4)
                nbformat.validate(nb)
                for index, cell in enumerate(nb.cells):
                    if cell.cell_type == "code":
                        ast.parse(cell.source, filename=f"{path}:cell-{index + 1}")

    def test_python_sources_compile(self):
        for folder in [course.REPO_ROOT, course.REPO_ROOT / "scripts", course.REPO_ROOT / "tests"]:
            for path in folder.glob("*.py"):
                with self.subTest(path=path):
                    ast.parse(path.read_text(), filename=str(path))

    def test_sweep_config_matches_notebook(self):
        import yaml
        path = course.REPO_ROOT / "notebooks/04_workflows/01_sweeps_reports_automations.ipynb"
        nb = nbformat.read(path, as_version=4)
        configs = []
        for cell in nb.cells:
            if cell.cell_type != "code":
                continue
            for node in ast.walk(ast.parse(cell.source)):
                if isinstance(node, ast.Assign) and any(
                    isinstance(target, ast.Name) and target.id == "sweep_config" for target in node.targets
                ):
                    configs.append(ast.literal_eval(node.value))
        self.assertEqual(configs, [yaml.safe_load((course.REPO_ROOT / "configs/sweep.yaml").read_text())])

    def test_segmentation_logs_metrics_and_table_to_explicit_run(self):
        """00b must keep all acceptance outputs on the run created in the notebook."""
        path = course.REPO_ROOT / "notebooks/00_setup/01_segmentation_quickstart.ipynb"
        nb = nbformat.read(path, as_version=4)
        source = "\n".join(cell.source for cell in nb.cells if cell.cell_type == "code")

        for metric in ["train/loss", "valid/loss", "valid/pixel_accuracy"]:
            self.assertIn(f'"{metric}"', source)
        self.assertIn('run.log({"predictions": table})', source)
        self.assertIn('run.define_metric("train/*"', source)
        self.assertIn('run.define_metric("valid/*"', source)
        self.assertNotIn("wandb.log(", source)


if __name__ == "__main__":
    unittest.main()
