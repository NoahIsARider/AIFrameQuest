import os
import clip
import torch
from PIL import Image
import numpy as np
from tqdm import tqdm

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

IMAGE_DIR = "images"
features = []
image_paths = []

for fname in tqdm(os.listdir(IMAGE_DIR)):
    path = os.path.join(IMAGE_DIR, fname)
    try:
        image = preprocess(Image.open(path)).unsqueeze(0).to(device)
        with torch.no_grad():
            feature = model.encode_image(image)
            feature /= feature.norm(dim=-1, keepdim=True)
        features.append(feature.cpu().numpy())
        image_paths.append(path)
    except Exception as e:
        print(f"Skipping {path}: {e}")

features = np.vstack(features)
np.save("features_clip.npy", features)
np.save("paths_clip.npy", image_paths)
