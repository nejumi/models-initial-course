"""Minimal W&B run used by the course notebooks."""

import os
import wandb

PROJECT = os.environ.get("WANDB_PROJECT", "models-initial-course")

with wandb.init(project=PROJECT, config={"lr": 0.1, "steps": 5}) as run:
    for step in range(run.config.steps):
        run.log({"train/loss": 1 / (step + 1), "step": step})
