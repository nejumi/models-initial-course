"""Execute notebooks and save outputs, including a failing cell's traceback.

Use --offline for local computation/media checks without W&B credentials.
Artifact download and Sweeps require the online service and are skipped offline.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = [
    "notebooks/00_setup/00_environment_setup.ipynb",
    "notebooks/00_setup/01_segmentation_quickstart.ipynb",
    "notebooks/01_basics/01_minimal_tracking.ipynb",
    "notebooks/01_basics/02_save_code_and_outputs.ipynb",
    "notebooks/02_integrations/01_integrations_overview.ipynb",
    "notebooks/03_core/01_artifacts.ipynb",
    "notebooks/03_core/02_tables_media.ipynb",
    "notebooks/04_workflows/01_sweeps_reports_automations.ipynb"
]
ONLINE_ONLY = {"01_artifacts.ipynb", "01_sweeps_reports_automations.ipynb"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--cpu", action="store_true", help="Hide CUDA GPUs from notebook kernels")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs" / "executed")
    parser.add_argument("--notebook", action="append", choices=NOTEBOOKS, help="Execute only the selected notebook(s)")
    args = parser.parse_args()
    if args.cpu:
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
    if args.offline:
        os.environ["WANDB_MODE"] = "offline"

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    for nb_path in args.notebook or NOTEBOOKS:
        path = ROOT / nb_path
        if args.offline and path.name in ONLINE_ONLY:
            print(f"SKIP (online required): {nb_path}", flush=True)
            continue
        print(f"Executing {nb_path}", flush=True)
        nb = nbformat.read(path, as_version=4)
        nbformat.validate(nb)
        client = NotebookClient(
            nb, timeout=600, kernel_name="python3",
            resources={"metadata": {"path": str(ROOT)}},
        )
        try:
            client.execute()
        finally:
            nbformat.write(nb, output_dir / path.name)
        print(f"OK {nb_path}", flush=True)


if __name__ == "__main__":
    main()
