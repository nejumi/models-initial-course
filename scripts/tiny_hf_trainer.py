"""Tiny Hugging Face Trainer demo without external model downloads."""

import os
import wandb
from transformers import Trainer, TrainingArguments

from course_utils import tiny_hf_trainer_objects

os.environ.setdefault("WANDB_PROJECT", "models-initial-course")

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
trainer.train()
wandb.finish()
