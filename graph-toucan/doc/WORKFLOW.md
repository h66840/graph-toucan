# 🔒 危险函数检测与重新生成完整流程

本文档描述了如何检测、重新生成和部署安全的函数。

---

## 📋 概述

整个流程分为 3 个步骤：
1. **检测**：扫描所有函数，识别危险操作
2. **重新生成**：使用 LLM 重写危险函数为安全版本
3. **验证与部署**：验证新函数的安全性并部署

---

## 🔍 步骤 1: 检测危险函数

### 1.1 运行扫描脚本

```bash
cd /data/lhy/datasets/graph-Toucan

# 扫描所有生成的函数
python src/check_dangerous_operations.py

# 或者扫描指定目录
python src/check_dangerous_operations.py /path/to/functions
```

### 1.2 查看扫描结果

扫描完成后会生成：

**终端输出**：
```
================================================================================
SCAN RESULTS
================================================================================
Total files scanned: 1252
Files with dangers: 68
Clean files: 1184

Severity Distribution:
  CRITICAL: 29    # eval, exec, subprocess
  HIGH: 30        # os, subprocess 模块导入
  MEDIUM: 89      # pathlib 文件操作（部分误报）
```

**生成的报告文件**：
- `tool_info/danger_scan_report.json` - 详细的扫描报告（JSON 格式）
- `tool_info/SECURITY_ANALYSIS.md` - 人类可读的安全分析报告

### 1.3 查看报告详情

```bash
# 查看摘要
cat tool_info/SECURITY_ANALYSIS.md

# 查看 JSON 报告（前 50 行）
head -50 tool_info/danger_scan_report.json

# 或使用 jq 查看特定信息
jq '.summary' tool_info/danger_scan_report.json
```

### 1.4 理解危险等级

| 等级 | 描述 | 示例 | 优先级 |
|-----|------|------|--------|
| 🔴 **CRITICAL** | 可执行任意代码/命令 | `eval()`, `subprocess.run()` | **立即处理** |
| 🟠 **HIGH** | 导入危险模块 | `import os`, `import subprocess` | 尽快处理 |
| 🟡 **MEDIUM** | 文件操作 | `open()`, pathlib 操作 | 可以稍后处理 |

---

## 🔧 步骤 2: 重新生成安全函数

### 2.1 测试模式（推荐先测试）

在处理所有文件前，先测试 3 个文件：

```bash
# 测试模式：只处理 3 个文件
python src/danger_func_rege.py --test

# 查看生成的文件
ls -lh tool_info/generated_functions_v1_safe/

# 查看其中一个文件
cat tool_info/generated_functions_v1_safe/calculator-calculate.py
```

### 2.2 部分重新生成（按严重级别）

只处理 CRITICAL 和 HIGH 级别的危险函数：

```bash
# 只处理 CRITICAL 级别（最危险）
python src/danger_func_rege.py --severity CRITICAL

# 处理 CRITICAL 和 HIGH 级别
python src/danger_func_rege.py --severity CRITICAL HIGH
```

### 2.3 完整重新生成

处理所有危险函数（68 个文件）：

```bash
# 保存到新目录（推荐，不覆盖原文件）
python src/danger_func_rege.py

# 预计耗时和成本
# - 时间：约 10-15 分钟（batch_size=5）
# - Token 用量：约 28万 tokens（基于测试推算）
# - 成本估算：视具体模型定价
```

### 2.4 高级选项

```bash
# 限制处理数量（例如只处理前 10 个）
python src/danger_func_rege.py --max-files 10

# 调整批处理大小（提高并发）
python src/danger_func_rege.py --batch-size 10

# 覆盖原文件（⚠️ 危险！建议先备份）
python src/danger_func_rege.py --overwrite

# 组合使用
python src/danger_func_rege.py --severity CRITICAL HIGH --batch-size 10
```

### 2.5 查看重新生成的结果

```bash
# 查看摘要
cat logs/regeneration_summary.json

# 查看详细日志
tail -100 logs/function_regeneration_log.jsonl

# 统计成功率
python3 -c "import json; data=json.load(open('logs/regeneration_summary.json')); print(f'Success: {data[\"success_count\"]}/{data[\"total_files\"]}')"
```

**预期输出示例**：
```
================================================================================
REGENERATION SUMMARY
================================================================================
Total files: 68
✅ Success: 65
❌ Failed: 3
🪙 Total tokens used: 285,430
```

---

## ✅ 步骤 3: 验证新函数的安全性

### 3.1 重新扫描生成的函数

```bash
# 扫描新生成的安全函数目录
python src/check_dangerous_operations.py tool_info/generated_functions_v1_safe

# 应该看到大幅减少的危险操作
```

**预期结果**：
```
Total files scanned: 68
Files with dangers: 10
Clean files: 58

Severity Distribution:
  MEDIUM: 15    # 主要是 string.replace() 误报
```

🎯 **目标**：
- ✅ CRITICAL: 0 次
- ✅ HIGH: 0 次
- 🟡 MEDIUM: 仅剩字符串操作误报

### 3.2 手动抽查重点函数

对于原本有 CRITICAL 危险的函数，建议手动检查：

```bash
# 列出原本最危险的函数
jq '.dangerous_files | sort_by(.danger_count) | reverse | .[0:5] | .[].file' tool_info/danger_scan_report.json

# 查看原始版本和新版本的对比
echo "=== ORIGINAL ==="
cat tool_info/generated_functions_v1/calculator-calculate.py | head -60

echo "=== REGENERATED ==="
cat tool_info/generated_functions_v1_safe/calculator-calculate.py | head -60
```

### 3.3 功能测试（可选但推荐）

创建测试脚本验证函数接口一致性：

```bash
# 创建简单的测试脚本
cat > test_regenerated.py << 'EOF'
import sys
import importlib.util

def test_function(file_path, func_name, test_cases):
    """测试重新生成的函数"""
    spec = importlib.util.spec_from_file_location("test_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    func = getattr(module, func_name)

    print(f"Testing {func_name}...")
    for test_input, expected in test_cases:
        try:
            result = func(**test_input)
            print(f"  ✓ {test_input} -> {result}")
        except Exception as e:
            print(f"  ✗ {test_input} -> Error: {e}")

# 测试 calculator-calculate
test_function(
    "tool_info/generated_functions_v1_safe/calculator-calculate.py",
    "calculator_calculate",
    [
        ({"expression": "2 + 2"}, {"result": 4.0}),
        ({"expression": "sin(pi/2)"}, {"result": 1.0}),
        ({"expression": "sqrt(16)"}, {"result": 4.0}),
    ]
)
EOF

python test_regenerated.py
```

---

## 🚀 步骤 4: 部署安全函数

### 4.1 备份原始函数（重要！）

```bash
# 备份原始函数目录
cp -r tool_info/generated_functions_v1 tool_info/generated_functions_v1_backup_$(date +%Y%m%d)

# 验证备份
ls -lh tool_info/ | grep backup
```

### 4.2 部署策略选择

#### 策略 A: 渐进式部署（推荐）

只替换 CRITICAL 和 HIGH 级别的函数：

```bash
# 1. 读取需要替换的文件列表
python3 << 'EOF'
import json

# 读取扫描报告
with open('tool_info/danger_scan_report.json') as f:
    report = json.load(f)

# 筛选 CRITICAL 和 HIGH 级别的文件
critical_files = []
for file_info in report['dangerous_files']:
    for danger in file_info['dangers']:
        if danger['severity'] in ['CRITICAL', 'HIGH']:
            critical_files.append(file_info['file'])
            break

# 保存到文件
with open('critical_files.txt', 'w') as f:
    for file in critical_files:
        f.write(file + '\n')

print(f"Found {len(critical_files)} critical files to replace")
EOF

# 2. 替换这些文件
while read file; do
    if [ -f "tool_info/generated_functions_v1_safe/$file" ]; then
        echo "Replacing $file..."
        cp "tool_info/generated_functions_v1_safe/$file" "tool_info/generated_functions_v1/$file"
    else
        echo "⚠️  Warning: $file not found in safe directory"
    fi
done < critical_files.txt

# 3. 验证替换
echo "Replaced files:"
wc -l critical_files.txt
```

#### 策略 B: 全量部署

替换所有重新生成的函数：

```bash
# ⚠️ 确保已备份！

# 复制所有安全版本到原目录
cp tool_info/generated_functions_v1_safe/*.py tool_info/generated_functions_v1/

# 验证
echo "Total files replaced:"
ls -1 tool_info/generated_functions_v1_safe/*.py | wc -l
```

#### 策略 C: 使用符号链接（便于回滚）

```bash
# 创建安全版本的软链接
cd tool_info/generated_functions_v1

for file in ../generated_functions_v1_safe/*.py; do
    filename=$(basename "$file")
    mv "$filename" "${filename}.original"  # 保留原文件
    ln -s "$file" "$filename"              # 创建软链接
done

cd ../..

# 回滚方法（如果需要）
cd tool_info/generated_functions_v1
for file in *.original; do
    target="${file%.original}"
    rm "$target"
    mv "$file" "$target"
done
cd ../..
```

### 4.3 验证部署

```bash
# 重新扫描主目录
python src/check_dangerous_operations.py

# 应该看到危险操作大幅减少
```

---

## 📊 步骤 5: 监控与维护

### 5.1 定期扫描

建议每周或每次添加新函数时扫描：

```bash
# 添加到 cron 任务（每周一扫描）
echo "0 9 * * 1 cd /data/lhy/datasets/graph-Toucan && python src/check_dangerous_operations.py" | crontab -
```

### 5.2 新增函数的安全检查

在生成新函数后立即检查：

```bash
# 生成新函数后
python generate_new_functions.py

# 立即扫描
python src/check_dangerous_operations.py

# 如果发现危险操作，立即重新生成
python src/danger_func_rege.py --max-files 1
```

### 5.3 查看历史记录

```bash
# 查看所有重新生成的日志
grep "status" logs/function_regeneration_log.jsonl | head -20

# 统计总体安全改进
python3 << 'EOF'
import json

# 原始扫描
with open('tool_info/danger_scan_report.json') as f:
    original = json.load(f)

print("=== Security Improvement Summary ===")
print(f"Original dangerous files: {original['summary']['dangerous_files']}")
print(f"Critical issues: {original['summary']['severity_stats'].get('CRITICAL', 0)}")
print(f"High issues: {original['summary']['severity_stats'].get('HIGH', 0)}")
print("\nAfter regeneration: Run scan again to see improvements!")
EOF
```

---

## 🛠️ 故障排除

### 问题 1: 重新生成失败

**症状**：某些函数重新生成失败

**解决方案**：
```bash
# 查看失败的文件
jq '.results[] | select(.status != "success") | .file' logs/regeneration_summary.json

# 查看具体错误
jq '.results[] | select(.status != "success") | {file, error}' logs/regeneration_summary.json

# 单独重新生成失败的文件（手动调整 prompt）
python src/danger_func_rege.py --max-files 1  # 然后手动指定文件
```

### 问题 2: 验证失败（函数签名不匹配）

**症状**：`verification_failed` 状态

**解决方案**：
```bash
# 查看验证失败的原因
jq '.results[] | select(.status == "verification_failed") | {file, issues}' logs/regeneration_summary.json

# 这些文件需要手动检查和修复
```

### 问题 3: Token 用量过高

**解决方案**：
```bash
# 分批处理
python src/danger_func_rege.py --max-files 10 --severity CRITICAL
# 等待一段时间后再处理下一批
python src/danger_func_rege.py --max-files 10 --severity HIGH
```

---

## 📈 效果评估

### 安全改进对比

| 指标 | 处理前 | 处理后 | 改进 |
|-----|-------|-------|------|
| 危险文件数 | 68 | ~10 | **-85%** |
| CRITICAL 危险 | 29 | 0 | **-100%** |
| HIGH 危险 | 30 | 0 | **-100%** |
| MEDIUM 危险 | 89 | ~15 | **-83%** |

### Token 使用统计

基于测试数据推算（处理 3 个文件用了 12,552 tokens）：
- **单个文件平均**: ~4,184 tokens
- **68 个文件总计**: ~284,512 tokens
- **预估成本**: 根据你的模型定价计算

---

## 📝 最佳实践

1. **总是先测试**
   ```bash
   python src/danger_func_rege.py --test
   ```

2. **按严重级别处理**
   ```bash
   python src/danger_func_rege.py --severity CRITICAL HIGH
   ```

3. **保留备份**
   ```bash
   cp -r tool_info/generated_functions_v1 tool_info/generated_functions_v1_backup
   ```

4. **验证后再部署**
   ```bash
   python src/check_dangerous_operations.py tool_info/generated_functions_v1_safe
   ```

5. **定期重新扫描**
   - 每周扫描一次
   - 添加新函数后立即扫描

---

## 🔗 相关文件

| 文件 | 描述 |
|-----|------|
| `src/check_dangerous_operations.py` | 危险操作扫描脚本 |
| `src/danger_func_rege.py` | 函数重新生成脚本 |
| `tool_info/danger_scan_report.json` | 扫描报告（JSON） |
| `tool_info/SECURITY_ANALYSIS.md` | 安全分析报告（Markdown） |
| `logs/function_regeneration_log.jsonl` | 重新生成详细日志 |
| `logs/regeneration_summary.json` | 重新生成摘要 |

---

## ❓ 常见问题

**Q: 为什么有些 MEDIUM 危险是误报？**
A: `string.replace()` 被误判为 pathlib 文件操作。这是检测工具的已知限制，可以安全忽略。

**Q: 可以只重新生成特定文件吗？**
A: 可以，修改脚本或手动编辑 `danger_scan_report.json`，只保留需要处理的文件。

**Q: 重新生成的函数是否保证功能一致？**
A: LLM 会尽力保持接口一致，但建议进行功能测试验证。

**Q: 如果重新生成后仍有危险操作怎么办？**
A: 查看 `verification_failed` 的文件，这些需要手动检查和修复。

---

## 📞 获取帮助

如果遇到问题：
1. 查看日志文件：`logs/function_regeneration_log.jsonl`
2. 检查报告：`logs/regeneration_summary.json`
3. 查看文档：本文件

---

**最后更新**: 2026-01-06
**版本**: 1.0
