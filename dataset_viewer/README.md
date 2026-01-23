# Dataset Viewer

一个用于查看和浏览Hugging Face Datasets的Web应用。

## 功能特性

- 浏览dataset中的每个样本
- 美观的界面展示messages、tools等字段
- 支持按subset_name等字段筛选
- 显示数据集统计信息（总样本数、修改样本数等）
- 支持随机抽样查看
- 快速导航（上一条、下一条）

## 安装依赖

```bash
pip install -r requirements.txt
```

## 启动应用

### 方法1: 使用启动脚本（推荐）

```bash
./start.sh
```

### 方法2: 直接运行Python

```bash
python3 app.py
```

## 访问应用

启动后，在浏览器中访问：

```
http://localhost:5001
```

## 修改数据集路径

默认数据集路径是 `/data/lhy/datasets/Toucan-SFT`

如果需要修改，编辑 `app.py` 第13行：

```python
dataset_path = '/your/dataset/path'
```

## API接口

应用提供以下REST API接口：

- `GET /` - 主页面
- `GET /api/dataset/info` - 获取数据集基本信息
- `GET /api/dataset/sample?index=0` - 获取指定索引的样本
- `GET /api/dataset/filter?field=subset_name&value=multi-turn` - 筛选样本
- `GET /api/dataset/stats` - 获取统计信息

## 界面说明

### 顶部统计区域
显示数据集的总样本数、修改样本数、原始样本数

### 控制区域
- **Sample Index**: 输入样本索引直接跳转
- **Load Sample**: 加载当前索引的样本
- **Previous/Next**: 上一条/下一条
- **Random**: 随机查看一条样本

### 快速筛选
- 可以按subset_name或is_modified字段筛选
- 点击subset按钮快速筛选该类别的样本

### 样本展示区域
- 清晰展示每个字段的内容
- Messages以对话形式展示，不同角色用不同颜色标识
- Tools和其他JSON数据以代码块形式展示
- 显示样本是否被修改的标签

## 技术栈

- 后端: Flask + Hugging Face Datasets
- 前端: HTML + CSS + JavaScript (纯原生，无框架依赖)
- UI设计: 渐变色背景 + 卡片式布局

## 目录结构

```
dataset_viewer/
├── app.py              # Flask后端应用
├── requirements.txt    # Python依赖
├── start.sh           # 启动脚本
├── README.md          # 说明文档
└── templates/
    └── index.html     # 前端页面
```

## 注意事项

1. 首次加载会读取整个dataset到内存，如果dataset很大可能需要等待
2. 筛选操作会遍历所有样本，数据量大时可能较慢
3. 默认端口是5001，确保端口未被占用

## 故障排除

### 端口被占用
修改 `app.py` 最后一行的端口号：
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # 改成其他端口
```

### Dataset路径不存在
检查并修改 `app.py` 中的 `dataset_path` 变量

### 依赖安装失败
尝试使用国内镜像源：
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```
