# 代码分析及插件说明
## 1. 介绍
本说明为对修改的部分代码进行说明，及插件/修改部分代码的说明。


## 2. 插件说明
### 2.1 图像处理
- 文件名：`anylabeling/plugin/img_tools.py`
- 用途： 图片读写等接口 [被用于修改VOC转换问题]
 

 
## 3. 代码解析

### 3.1 转换部分：

- 主要转换接口： `anylabeling/views/labeling/label_converter.py`、`anylabeling/views/labeling/utils/export.py`
  - 修改说明： 修改了导入VOC类别时，对VOC类别不规范导致的错误： 
    ``` python
    image_width = int(size_width.text)          #原始代码
    image_height = int(size_height.text)
    ```
- 上传接口： `anylabeling/views/labeling/utils/upload.py`
- 文件导入接口： `anylabeling/views/labeling/label_file.py` --> `def load(self, filename)`

### 3.2 导入文件部分
- 初始化对象位置： `anylabeling/views/labeling/label_widget.py` --> `self.label_file = LabelFile(label_file, image_dir)`  

