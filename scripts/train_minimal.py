"""Record five example metrics using the course connection settings."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from course_utils import setup_wandb
_, _, init_kwargs = setup_wandb()

import wandb

with wandb.init(**init_kwargs, config={"steps": 5}) as run:
    for step in range(run.config.steps):
        run.log({"train/loss": 1 / (step + 1), "step": step})
