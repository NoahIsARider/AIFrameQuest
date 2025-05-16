import clip
import math
import torch
import numpy as np
import faiss
from PIL import Image
import matplotlib.pyplot as plt

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# 加载索引和图片路径
index = faiss.read_index("clip_index.faiss")
paths = np.load("paths_clip.npy")

# 提取查询图像特征
def extract_query_feature(image_path):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    with torch.no_grad():
        feature = model.encode_image(image)
        feature /= feature.norm(dim=-1, keepdim=True)
    return feature.cpu().numpy().astype("float32")

query_feature = extract_query_feature("query.jpg")

# 搜索最相似的图像
k = 20
distances, indices = index.search(query_feature, k)

# 展示检索结果
cols = 5  # 每行显示几张图
rows = math.ceil(k / cols)

plt.figure(figsize=(2 * cols, 2 * rows))

for i, idx in enumerate(indices[0]):
    img = Image.open(paths[idx])
    plt.subplot(rows, cols, i + 1)
    plt.imshow(img)
    plt.title(f"Top {i+1}")
    plt.axis("off")

plt.tight_layout()
plt.show()
