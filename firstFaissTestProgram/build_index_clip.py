import numpy as np
import faiss

features = np.load("features_clip.npy").astype("float32")

index = faiss.IndexFlatIP(features.shape[1])  # 余弦相似度
index.add(features)

faiss.write_index(index, "clip_index.faiss")
