import os
import json
from PIL import Image
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Heiti TC'  # 替换为你选择的字体

dataset_dir = "../firstFaissTestProgram/images"  # 修改为你的数据集目录路径
# dataset_dir = r"..\firstFaissTestProgram\images" # windows应该是这个
output_json = "labels.json"

data = []

for filename in os.listdir(dataset_dir):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp')):
        img_path = os.path.join(dataset_dir, filename)
        print(f"读取文件: {img_path}")
        img = Image.open(img_path)
        plt.imshow(img)
        plt.title(filename)
        plt.axis('off')
        plt.show()
        labels_input = input(f"请输入该图像的标签（复数标签用英文逗号分隔）: ")
        label_list = [label.strip() for label in labels_input.split(',') if label.strip()]
        data.append({
            "image": img_path,
            "label": label_list
        })

with open(output_json, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"共标注 {len(data)} 张图像，已保存到 {output_json}")