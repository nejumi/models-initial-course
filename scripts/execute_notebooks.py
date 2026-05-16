"""Execute course notebooks in order.

This script is intentionally small so it can be used from CI or locally after
`uv pip install --python .venv/bin/python -r requirements.txt`.
"""

from __future__ import annotations

from pathlib import Path
import nbformat
from nbclient import NotebookClient

NOTEBOOKS = [
    "notebooks/00_setup/00_environment_setup.ipynb",
    "notebooks/01_basics/01_minimal_tracking.ipynb",
    "notebooks/01_basics/02_save_code_and_outputs.ipynb",
    "notebooks/02_integrations/01_integrations_overview.ipynb",
    "notebooks/03_core/01_artifacts.ipynb",
    "notebooks/03_core/02_tables_media.ipynb",
    "notebooks/04_workflows/01_sweeps_reports_automations.ipynb",
]

for nb_path in NOTEBOOKS:
    path = Path(nb_path)
    print(f"=== Executing {path} ===", flush=True)
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=600, kernel_name="python3", resources={"metadata": {"path": "."}})
    client.execute()
    print(f"OK {path}", flush=True)
