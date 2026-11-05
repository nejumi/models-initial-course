"""Tiny Hugging Face Trainer demo without external model downloads."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from course_utils import REPO_ROOT, setup_wandb, tiny_hf_trainer_objects
import os
os.chdir(REPO_ROOT)
project, entity, _ = setup_wandb(
    packages=["numpy>=1.24.0", "torch>=2.0.0", "transformers>=4.40.0,<5", "accelerate>=0.26.0"]
)
os.environ["WANDB_PROJECT"] = project
if entity:
    os.environ["WANDB_ENTITY"] = entity

import wandb
from transformers import Trainer, TrainingArguments

model, train_dataset = tiny_hf_trainer_objects()
args = TrainingArguments(
    output_dir="outputs/script_hf_trainer",
    report_to="wandb",
    run_name="script-hf-trainer-tiny-demo",
    max_steps=5,
    per_device_train_batch_size=8,
    logging_steps=1,
    save_strategy="no",
    disable_tqdm=True,
)
trainer = Trainer(model=model, args=args, train_dataset=train_dataset)
try:
    trainer.train()
finally:
    wandb.finish()
