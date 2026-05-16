"""Small helpers for the W&B Models initial course.

The notebooks keep W&B concepts visible and put setup / toy data details here.
"""

from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

_PACKAGE_IMPORTS = {
    "python-dotenv": "dotenv",
    "pillow": "PIL",
    "imageio-ffmpeg": "imageio_ffmpeg",
}


def _package_name(spec: str) -> str:
    for marker in ["[", ">=", "==", "<=", "~=", "<"]:
        if marker in spec:
            return spec.split(marker)[0]
    return spec


def ensure_packages(packages: list[str] | tuple[str, ...]) -> None:
    """Install missing packages only."""
    missing: list[str] = []
    for spec in packages:
        package = _package_name(spec)
        import_name = _PACKAGE_IMPORTS.get(package, package.replace("-", "_"))
        if importlib.util.find_spec(import_name) is None:
            missing.append(spec)

    if not missing:
        return

    print("Installing:", ", ".join(missing))
    if shutil.which("uv"):
        cmd = ["uv", "pip", "install", "--python", sys.executable, "-q", *missing]
    else:
        cmd = [sys.executable, "-m", "pip", "install", "-q", *missing]
    subprocess.check_call(cmd)


def load_wandb_env() -> None:
    """Load WANDB_* variables from Colab Secrets or local .env."""
    try:
        from google.colab import userdata  # type: ignore

        for key in ["WANDB_API_KEY", "WANDB_BASE_URL", "WANDB_ENTITY", "WANDB_PROJECT"]:
            value = userdata.get(key)
            if value:
                os.environ[key] = value.strip()
        print("Loaded W&B settings from Colab Secrets.")
    except Exception:
        from dotenv import load_dotenv

        load_dotenv(Path(".env"))
        print("Loaded W&B settings from .env if present.")

    if not os.environ.get("WANDB_BASE_URL", "").strip():
        os.environ.pop("WANDB_BASE_URL", None)


def setup_wandb(project: str = "models-initial-course", packages: list[str] | None = None):
    """Install packages, load secrets, log in, and return W&B init kwargs."""
    ensure_packages(["wandb>=0.19.0", "python-dotenv>=1.0.0", *(packages or [])])
    load_wandb_env()

    if not os.environ.get("WANDB_API_KEY"):
        raise RuntimeError("WANDB_API_KEY を Colab Secrets または .env に設定してください。")

    import wandb

    wandb.login(key=os.environ["WANDB_API_KEY"], relogin=True)

    project_name = os.environ.get("WANDB_PROJECT", project)
    entity = os.environ.get("WANDB_ENTITY") or None
    init_kwargs = {"project": project_name}
    if entity:
        init_kwargs["entity"] = entity

    print(f"W&B login OK: project={project_name}, entity={entity or '(default)'}")
    return project_name, entity, init_kwargs


def tiny_hf_trainer_objects(seed: int = 0):
    """Return a tiny model and dataset for a Trainer integration demo."""
    import numpy as np
    import torch
    from torch import nn
    from torch.utils.data import Dataset

    class TinyTextDataset(Dataset):
        def __init__(self, n: int = 32, seq_len: int = 8):
            rng = np.random.default_rng(seed)
            self.input_ids = rng.integers(0, 32, size=(n, seq_len), dtype=np.int64)
            self.labels = (self.input_ids.sum(axis=1) % 2).astype(np.int64)

        def __len__(self):
            return len(self.labels)

        def __getitem__(self, idx):
            return {
                "input_ids": torch.tensor(self.input_ids[idx]),
                "labels": torch.tensor(self.labels[idx]),
            }

    class TinyClassifier(nn.Module):
        def __init__(self, vocab_size: int = 32, hidden: int = 12):
            super().__init__()
            self.emb = nn.Embedding(vocab_size, hidden)
            self.head = nn.Linear(hidden, 2)

        def forward(self, input_ids=None, labels=None):
            logits = self.head(self.emb(input_ids).mean(dim=1))
            loss = nn.functional.cross_entropy(logits, labels) if labels is not None else None
            return {"loss": loss, "logits": logits}

    return TinyClassifier(), TinyTextDataset()


def label_image(text: str, color: str = "#ffcc33"):
    """Create a small image for the Table/media notebook."""
    from PIL import Image, ImageDraw

    image = Image.new("RGB", (360, 120), color="white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 360, 28), fill=color)
    draw.text((16, 52), text, fill="black")
    return image



def demo_image_array(size: int = 96):
    """Return an RGB NumPy array with simple geometric patterns."""
    import numpy as np

    y, x = np.mgrid[0:size, 0:size]
    arr = np.zeros((size, size, 3), dtype=np.uint8)
    arr[..., 0] = (x * 255 / max(size - 1, 1)).astype(np.uint8)
    arr[..., 1] = (y * 255 / max(size - 1, 1)).astype(np.uint8)
    arr[..., 2] = (((x - size / 2) ** 2 + (y - size / 2) ** 2) < (size / 3) ** 2) * 255
    return arr


def demo_pil_image(text: str = "wandb.Image"):
    """Return a PIL image for examples."""
    from PIL import Image, ImageDraw

    image = Image.new("RGB", (220, 140), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((12, 12, 208, 128), outline="#111111", width=3)
    draw.rectangle((20, 20, 120, 76), fill="#ffcc33")
    draw.ellipse((132, 36, 192, 96), fill="#1f77b4")
    draw.text((24, 100), text, fill="black")
    return image


def save_demo_image(path: str | Path) -> str:
    """Save and return a demo PNG path."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    demo_pil_image("file path").save(path)
    return str(path)


def demo_mask(size: int = 96):
    """Return a small integer segmentation mask."""
    import numpy as np

    mask = np.zeros((size, size), dtype=np.uint8)
    mask[16:72, 18:50] = 1
    mask[34:84, 52:86] = 2
    return mask


def save_demo_gif(path: str | Path, frames: int = 8) -> str:
    """Create a tiny animated GIF for wandb.Video(path)."""
    from PIL import Image, ImageDraw

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    images = []
    for i in range(frames):
        img = Image.new("RGB", (96, 96), "white")
        draw = ImageDraw.Draw(img)
        draw.rectangle((8, 8, 88, 88), outline="#111111", width=2)
        draw.ellipse((12 + i * 8, 36, 36 + i * 8, 60), fill="#ffcc33")
        images.append(img)
    images[0].save(path, save_all=True, append_images=images[1:], duration=180, loop=0)
    return str(path)


def demo_video_array(frames: int = 8, size: int = 64):
    """Return a uint8 video array shaped (time, channels, height, width)."""
    import numpy as np

    video = np.zeros((frames, 3, size, size), dtype=np.uint8)
    for t in range(frames):
        start = 6 + t * 5
        video[t, 0, start:start + 18, 12:42] = 255
        video[t, 1, 18:48, start:start + 18] = 180
        video[t, 2, :, :] = np.linspace(20, 120, size, dtype=np.uint8)[None, :]
    return video


def demo_audio_array(seconds: float = 1.0, sample_rate: int = 8000, freq: float = 440.0):
    """Return a sine wave and its sample rate."""
    import numpy as np

    t = np.linspace(0, seconds, int(sample_rate * seconds), endpoint=False)
    audio = 0.25 * np.sin(2 * np.pi * freq * t)
    return audio.astype(np.float32), sample_rate


def save_demo_wav(path: str | Path) -> str:
    """Save a small mono WAV file using the standard library."""
    import wave
    import numpy as np

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    audio, sample_rate = demo_audio_array()
    pcm = (audio * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(pcm.tobytes())
    return str(path)


def demo_point_cloud_rgb(n: int = 80):
    """Return an Object3D-compatible xyzrgb point cloud."""
    import numpy as np

    theta = np.linspace(0, 2 * np.pi, n)
    z = np.linspace(-1, 1, n)
    x = np.cos(theta)
    y = np.sin(theta)
    r = ((x + 1) * 127).astype(float)
    g = ((y + 1) * 127).astype(float)
    b = ((z + 1) * 127).astype(float)
    return np.stack([x, y, z, r, g, b], axis=1)


def demo_lidar_scene():
    """Return a small lidar/beta scene with points and a 3D box."""
    points = demo_point_cloud_rgb(40).tolist()
    corners = [
        [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5],
        [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5], [-0.5, 0.5, 0.5],
    ]
    return {
        "type": "lidar/beta",
        "points": points,
        "boxes": [{"corners": corners, "label": "demo object", "color": [255, 204, 51], "score": 0.9}],
    }


def write_demo_pdb(path: str | Path) -> str:
    """Write a tiny PDB molecule file and return its path."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "HEADER    W&B COURSE DEMO\\n"
        "ATOM      1  O   HOH A   1       0.000   0.000   0.000  1.00 20.00           O\\n"
        "ATOM      2  H1  HOH A   1       0.758   0.000   0.504  1.00 20.00           H\\n"
        "ATOM      3  H2  HOH A   1      -0.758   0.000   0.504  1.00 20.00           H\\n"
        "END\\n"
    )
    return str(path)


def demo_plotly_figure():
    """Return a small Plotly figure."""
    import plotly.express as px

    return px.line(x=[0, 1, 2, 3], y=[0.9, 0.6, 0.45, 0.38], markers=True, title="Demo validation loss")
