# 图像搜索系统

## 核心思想

本项目基于Faiss库实现了一个高效的图像搜索系统，主要包含以下核心功能：

1. **特征提取**
   - 使用预训练的ResNet-50模型提取图像特征
   - 特征维度为2048维
   - 保持了图像的语义信息

2. **索引构建**
   - 使用Faiss库构建向量索引
   - 支持快速的相似度搜索
   - 使用FlatL2索引实现精确搜索

3. **相似度搜索**
   - 支持批量图像特征提取
   - 实时搜索相似图像
   - 返回最相似的N张图片

4. **社区互动**
   - 用户注册和登录系统
   - 为每个图片创建词条页面
   - 支持用户评分和评论
   - 实时更新评分统计

5. **Web界面**
   - 基于Flask构建的Web服务
   - 支持图片上传和预览
   - 实时显示搜索结果
   - 美观的词条页面设计

## 系统要求

- Python 3.8+
- CUDA支持（可选，用于GPU加速）
- 8GB+ RAM
- 2GB+ 磁盘空间

## 系统架构

```
FaissSearch/
├── app.py              # 主应用文件
├── templates/          # HTML模板
│   ├── index.html     # 主页界面
│   ├── login.html     # 登录页面
│   ├── register.html  # 注册页面
│   └── term.html      # 词条页面
├── utils/             # 工具函数
│   ├── faiss_search.py  # 图像搜索核心
│   └── user_metadata.py # 用户数据处理
├── data/              # 数据存储
│   ├── users.json     # 用户信息
│   └── comments.json  # 评论数据
├── uploads/           # 上传图片存储目录
├── images/            # 数据集图片目录
└── faiss_index.index  # Faiss索引文件
```

## 快速部署

### 1. 环境准备

```bash
# 克隆项目
git clone [项目地址]
cd FaissSearch

# 创建Conda环境
conda create -n AIFrameQuest python=3.12
conda activate AIFrameQuest

# 安装PyTorch和CUDA（根据您的CUDA版本选择）
conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch

# 安装其他依赖
pip install -r requirements.txt
```

### 2. 准备数据集

1. 创建必要的目录：
```bash
mkdir -p images uploads data
```

2. 将图片数据集放入`images`目录

### 3. 启动服务

```bash
python app.py
```

首次运行时，系统会自动构建索引文件，这可能需要几分钟时间。
服务启动后，访问 http://localhost:5000 即可使用。

## 使用指南

1. **用户注册与登录**
   - 访问 http://localhost:5000/register 注册新账号
   - 使用注册的账号登录系统

2. **图像搜索**
   - 在主页点击"选择图片"按钮上传要搜索的图片
   - 系统会自动处理图片并显示最相似的图片结果
   - 每个结果都会显示相似度分数

3. **词条互动**
   - 点击搜索结果中的图片进入词条页面
   - 查看图片的详细信息和社区评分
   - 发表评论分享您的见解
   - 为图片打分（1-5星）

4. **社区参与**
   - 查看其他用户的评论
   - 参与评分，影响图片的整体评分
   - 分享有趣的发现

## 性能优化

1. GPU加速
   - 安装CUDA和cuDNN
   - 使用GPU版本的PyTorch和Faiss

2. 索引优化
   - 调整`nlist`和`nprobe`参数
   - 使用IVF索引提高搜索速度

3. 内存优化
   - 减小batch_size
   - 使用图片压缩

## 常见问题

1. 内存不足
   - 减少同时处理的图片数量
   - 降低特征维度
   - 使用更小的模型

2. 索引构建慢
   - 使用SSD存储
   - 增加系统内存
   - 使用GPU加速

3. 搜索结果不准确
   - 检查图片质量
   - 调整相似度阈值
   - 优化特征提取模型

## 技术栈

- Python 3.8+
- Flask 2.x
- PyTorch 1.x
- Faiss 1.x
- ResNet-50
- Bootstrap 5.x

## 许可证

本项目采用MIT许可证。

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进项目。

1. Fork本项目
2. 创建新分支
3. 提交更改
4. 发起Pull Request

## 更新日志

### v2.0
- 添加用户系统
- 实现图片词条功能
- 添加评分和评论系统

### v1.0
- 初始版本发布
- 基本图像搜索功能
- Web界面支持
