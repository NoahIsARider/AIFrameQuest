# 测试是否能够读取图片
import os

dataset_dir = "../firstFaissTestProgram/images"  # 修改为你的数据集目录路径，windows应该是下面这个
# dataset_dir = r"..\firstFaissTestProgram\images"
output_json = "labels.json"

data = []

for label in os.listdir(dataset_dir):
    print(label)