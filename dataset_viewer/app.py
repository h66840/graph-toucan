from flask import Flask, render_template, jsonify, request

import datasets
import json

app = Flask(__name__)


# 全局变量存储数据集
dataset = None
dataset_path = None  # 将通过命令行参数设置

def load_dataset():
    """加载数据集"""
    global dataset
    if dataset is None:
        if dataset_path is None:
            raise ValueError("Dataset path not set. Please provide --dataset_path argument.")
        print(f"Loading dataset from {dataset_path}...")
        dataset = datasets.load_from_disk(dataset_path)
        print(f"Dataset loaded! Total samples: {len(dataset)}")
    return dataset

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/dataset/info')
def dataset_info():
    """获取数据集基本信息"""
    try:
        ds = load_dataset()
        return jsonify({
            'success': True,
            'total': len(ds),
            'columns': ds.column_names,
            'features': str(ds.features)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/dataset/sample')
def get_sample():
    """获取单个样本"""
    try:
        ds = load_dataset()
        index = request.args.get('index', 0, type=int)

        if index < 0 or index >= len(ds):
            return jsonify({
                'success': False,
                'error': f'Index out of range. Dataset size: {len(ds)}'
            }), 400

        sample = ds[index]

        # 处理字段，将JSON字符串解析为对象
        processed_sample = {}
        for key, value in sample.items():
            if isinstance(value, str):
                # 尝试解析JSON字符串
                try:
                    parsed = json.loads(value)
                    processed_sample[key] = parsed
                except (json.JSONDecodeError, ValueError):
                    processed_sample[key] = value
            else:
                processed_sample[key] = value

        return jsonify({
            'success': True,
            'index': index,
            'total': len(ds),
            'data': processed_sample
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/dataset/search')
def search_samples():
    """搜索样本"""
    try:
        ds = load_dataset()
        query = request.args.get('query', '', type=str)
        field = request.args.get('field', 'subset_name', type=str)
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)

        # 筛选匹配的样本
        matching_indices = []
        for i in range(len(ds)):
            sample = ds[i]
            if field in sample:
                value = str(sample[field])
                if query.lower() in value.lower():
                    matching_indices.append(i)

        # 分页
        total_matches = len(matching_indices)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_indices = matching_indices[start_idx:end_idx]

        return jsonify({
            'success': True,
            'total_matches': total_matches,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_matches + page_size - 1) // page_size,
            'indices': page_indices
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/dataset/filter')
def filter_samples():
    """根据字段值过滤样本，支持多条件联合过滤"""
    try:
        ds = load_dataset()

        # 获取过滤条件 - 兼容旧的field/value参数和新的subset_name/is_modified/modified_type参数
        subset_name = request.args.get('subset_name', type=str)
        is_modified = request.args.get('is_modified', type=str)
        modified_type = request.args.get('modified_type', type=str)

        # 兼容旧的参数格式
        field = request.args.get('field', type=str)
        value = request.args.get('value', type=str)

        # 如果使用旧格式，转换到新格式
        if field and value is not None:
            if field == 'subset_name':
                subset_name = value
            elif field == 'is_modified':
                is_modified = value

        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 100, type=int)

        # 如果没有任何过滤条件，返回错误
        if subset_name is None and is_modified is None and modified_type is None:
            return jsonify({
                'success': False,
                'error': 'At least one filter parameter is required (subset_name, is_modified or modified_type)'
            }), 400

        # 筛选匹配的样本索引
        matching_indices = []
        filters_applied = []

        for i in range(len(ds)):
            sample = ds[i]
            match = True

            # 检查subset_name条件
            if subset_name:
                if 'subset_name' not in sample or str(sample['subset_name']) != subset_name:
                    match = False

            # 检查is_modified条件
            if is_modified:
                if 'is_modified' in sample:
                    expected_value = is_modified.lower() == 'true'
                    if sample['is_modified'] != expected_value:
                        match = False
                else:
                    match = False

            # 检查 modified_type 条件（依赖 modification_info 字段）
            if modified_type:
                mod_info_str = sample.get('modification_info', '')
                if not mod_info_str:
                    match = False
                else:
                    try:
                        mod_info = json.loads(mod_info_str)
                        if mod_info.get('modified_type') != modified_type:
                            match = False
                    except Exception:
                        match = False

            if match:
                matching_indices.append(i)

        # 构建过滤器描述
        if subset_name:
            filters_applied.append(f"subset_name='{subset_name}'")
        if is_modified:
            filters_applied.append(f"is_modified={is_modified}")
        if modified_type:
            filters_applied.append(f"modified_type='{modified_type}'")

        # 分页
        total_matches = len(matching_indices)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_indices = matching_indices[start_idx:end_idx]

        return jsonify({
            'success': True,
            'filters': filters_applied,
            'total_matches': total_matches,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_matches + page_size - 1) // page_size if total_matches > 0 else 0,
            'indices': page_indices
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/dataset/stats')
def get_stats():
    """获取数据集统计信息"""
    try:
        ds = load_dataset()

        # 统计subset_name分布
        subset_distribution = {}
        modified_count = 0

        for sample in ds:
            subset_name = sample.get('subset_name', 'unknown')
            subset_distribution[subset_name] = subset_distribution.get(subset_name, 0) + 1

            if sample.get('is_modified', False):
                modified_count += 1

        return jsonify({
            'success': True,
            'total_samples': len(ds),
            'subset_distribution': subset_distribution,
            'modified_samples': modified_count,
            'unmodified_samples': len(ds) - modified_count
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    import argparse

    # 设置命令行参数
    parser = argparse.ArgumentParser(description='Dataset Viewer Web Application')
    parser.add_argument('--dataset_path', type=str, required=True,
                        help='Path to the dataset directory')
    parser.add_argument('--host', type=str, default='0.0.0.0',
                        help='Host address (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5001,
                        help='Port number (default: 5001)')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode')
    args = parser.parse_args()

    # 设置全局dataset_path
    dataset_path = args.dataset_path

    # 预加载数据集
    load_dataset()

    # 启动服务器
    print("\n" + "="*60)
    print("Dataset Viewer Server Starting...")
    print("="*60)
    print(f"Dataset Path: {dataset_path}")
    print(f"Server URL: http://{args.host}:{args.port}")
    print("="*60 + "\n")

    app.run(debug=args.debug, host=args.host, port=args.port)
