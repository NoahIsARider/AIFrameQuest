建议在python3.10.*下运行，其他版本可能存在兼容性问题，我不确定
你们可以建立虚拟环境，然后安装依赖，确保安全

我不太清楚windows下脚本文件怎么写，这个同一个目录下的setup.sh是mac和linux的脚本文件，你们可以自己改一下，需要的包应该如下
```shell
pip install \
    faiss-cpu \
    torch torchvision \
    ftfy regex tqdm \
    git+https://github.com/openai/CLIP.git \
    matplotlib \
    numpy \
    pillow
```

运行程序run.sh在windows应该也是运行不了的，你们也可以自己改一下，这是我自己运行的时候运行的顺序，一定要按照这个顺序运行，然后```./image```目录下的是图片库，```query.jpg```是要查询的图片。

```shell
export KMP_DUPLICATE_LIB_OK=TRUE
python3 extract_features_clip.py
python3 build_index_clip.py
python3 show.py
```

不过你们嫌麻烦的话其实可以在linux虚拟机下运行，但是在安装虚拟环境的时候可以能会报错，问一下ai，改一下shell文件的内容应该就可以。