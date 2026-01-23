"""
SafeExecutionContext 安全性测试脚本

测试各种绕过场景，包括：
1. 绝对路径访问外部
2. 相对路径 .. 访问父目录
3. 符号链接绕过
4. 多层嵌套路径
5. subprocess/eval/exec 禁用
"""
import os
import sys
import tempfile
import shutil
from pathlib import Path

# 添加项目路径
sys.path.insert(0, '/data/lhy/datasets/graph-Toucan/src')
from backward_to_query import SafeExecutionContext


# 创建测试环境
TEST_ROOT = "/tmp/safe_context_test"
SAFE_DIR = os.path.join(TEST_ROOT, "safe_work_dir")
UNSAFE_DIR = os.path.join(TEST_ROOT, "unsafe_dir")

def setup_test_env():
    """设置测试环境"""
    # 清理并创建测试目录
    if os.path.exists(TEST_ROOT):
        shutil.rmtree(TEST_ROOT)

    os.makedirs(SAFE_DIR, exist_ok=True)
    os.makedirs(UNSAFE_DIR, exist_ok=True)

    # 在不安全目录创建一个敏感文件
    with open(os.path.join(UNSAFE_DIR, "sensitive.txt"), 'w') as f:
        f.write("SENSITIVE DATA - Should not be accessible!")

    print(f"✅ 测试环境创建完成")
    print(f"   Safe dir: {SAFE_DIR}")
    print(f"   Unsafe dir: {UNSAFE_DIR}")
    print()


def test_case(name: str, test_func):
    """测试用例包装器"""
    print(f"{'='*70}")
    print(f"测试: {name}")
    print(f"{'='*70}")
    try:
        result = test_func()
        if result:
            print(f"✅ PASS - {name}")
        else:
            print(f"❌ FAIL - {name}")
        print()
        return result
    except Exception as e:
        print(f"⚠️  ERROR - {name}: {e}")
        print()
        return False


def test_1_basic_allowed_operations():
    """测试 1: 基本允许的操作（应该成功）"""
    with SafeExecutionContext(SAFE_DIR):
        # 写入文件
        with open("test.txt", 'w') as f:
            f.write("Hello from safe context")

        # 读取文件
        with open("test.txt", 'r') as f:
            content = f.read()

        # 创建目录
        os.makedirs("subdir", exist_ok=True)

        # 写入子目录文件
        with open("subdir/test2.txt", 'w') as f:
            f.write("Hello from subdir")

        print("✓ 在安全目录内的操作都成功")
        return True


def test_2_absolute_path_outside():
    """测试 2: 使用绝对路径访问外部（应该被阻止）"""
    try:
        with SafeExecutionContext(SAFE_DIR):
            # 尝试访问不安全目录
            with open(os.path.join(UNSAFE_DIR, "sensitive.txt"), 'r') as f:
                content = f.read()
            print("❌ SECURITY BREACH: 成功读取了外部文件！")
            return False
    except PermissionError as e:
        print(f"✓ 正确阻止了绝对路径访问外部: {e}")
        return True


def test_3_relative_path_parent():
    """测试 3: 使用 .. 访问父目录（应该被阻止）"""
    try:
        with SafeExecutionContext(SAFE_DIR):
            # 尝试使用 .. 访问父目录
            with open("../unsafe_dir/sensitive.txt", 'r') as f:
                content = f.read()
            print("❌ SECURITY BREACH: 成功使用 .. 访问了外部！")
            return False
    except PermissionError as e:
        print(f"✓ 正确阻止了 .. 路径访问: {e}")
        return True


def test_4_symlink_bypass():
    """测试 4: 符号链接绕过（这是当前实现的漏洞）"""
    # 在安全目录创建指向外部的符号链接
    symlink_path = os.path.join(SAFE_DIR, "evil_link")
    target_path = os.path.join(UNSAFE_DIR, "sensitive.txt")

    # 先清理可能存在的符号链接
    if os.path.exists(symlink_path):
        os.unlink(symlink_path)

    try:
        os.symlink(target_path, symlink_path)
        print(f"创建符号链接: {symlink_path} -> {target_path}")
    except OSError as e:
        print(f"无法创建符号链接（可能权限不足）: {e}")
        return True  # 如果无法创建符号链接，测试通过

    try:
        with SafeExecutionContext(SAFE_DIR):
            # 尝试通过符号链接读取外部文件
            with open("evil_link", 'r') as f:
                content = f.read()
            print(f"❌ CRITICAL SECURITY BREACH: 通过符号链接读取了外部文件！")
            print(f"   内容: {content}")
            return False
    except PermissionError as e:
        print(f"✓ 正确阻止了符号链接绕过: {e}")
        return True
    finally:
        # 清理符号链接
        if os.path.exists(symlink_path):
            os.unlink(symlink_path)


def test_5_complex_relative_path():
    """测试 5: 复杂的相对路径（./../../...）"""
    try:
        with SafeExecutionContext(SAFE_DIR):
            # 尝试使用复杂路径
            with open("./subdir/../../unsafe_dir/sensitive.txt", 'r') as f:
                content = f.read()
            print("❌ SECURITY BREACH: 复杂路径绕过成功！")
            return False
    except PermissionError as e:
        print(f"✓ 正确阻止了复杂相对路径: {e}")
        return True


def test_6_eval_disabled():
    """测试 6: eval 应该被禁用"""
    try:
        with SafeExecutionContext(SAFE_DIR):
            eval("1+1")
            print("❌ SECURITY BREACH: eval 仍然可用！")
            return False
    except PermissionError as e:
        print(f"✓ 正确禁用了 eval: {e}")
        return True


def test_7_exec_disabled():
    """测试 7: exec 应该被禁用"""
    try:
        with SafeExecutionContext(SAFE_DIR):
            exec("x = 1")
            print("❌ SECURITY BREACH: exec 仍然可用！")
            return False
    except PermissionError as e:
        print(f"✓ 正确禁用了 exec: {e}")
        return True


def test_8_subprocess_disabled():
    """测试 8: subprocess 应该被禁用"""
    try:
        with SafeExecutionContext(SAFE_DIR):
            import subprocess
            subprocess.run(["ls", "-la"])
            print("❌ SECURITY BREACH: subprocess 仍然可用！")
            return False
    except PermissionError as e:
        print(f"✓ 正确禁用了 subprocess: {e}")
        return True


def test_9_os_listdir_not_restricted():
    """测试 9: os.listdir 等读取操作未被限制（这是一个潜在问题）"""
    try:
        with SafeExecutionContext(SAFE_DIR):
            # os.listdir 未被 SafeExecutionContext 限制
            files = os.listdir(UNSAFE_DIR)
            print(f"⚠️  WARNING: os.listdir 可以列出外部目录: {files}")
            return False  # 这是一个安全问题
    except Exception as e:
        print(f"✓ os.listdir 被阻止: {e}")
        return True


def test_10_pathlib_operations():
    """测试 10: pathlib 操作未被限制（这是一个严重问题）"""
    try:
        with SafeExecutionContext(SAFE_DIR):
            # pathlib 完全未被限制
            p = Path(UNSAFE_DIR) / "sensitive.txt"
            content = p.read_text()
            print(f"❌ CRITICAL SECURITY BREACH: pathlib 可以读取外部文件！")
            print(f"   内容: {content}")
            return False
    except Exception as e:
        print(f"✓ pathlib 被阻止: {e}")
        return True


def test_11_os_walk_not_restricted():
    """测试 11: os.walk 未被限制"""
    try:
        with SafeExecutionContext(SAFE_DIR):
            # os.walk 未被限制
            for root, dirs, files in os.walk(UNSAFE_DIR):
                print(f"⚠️  WARNING: os.walk 可以遍历外部目录: {root}")
                break
            return False
    except Exception as e:
        print(f"✓ os.walk 被阻止: {e}")
        return True


def test_12_os_chdir_not_restricted():
    """测试 12: os.chdir 未被限制（严重问题）"""
    original_cwd = os.getcwd()
    try:
        with SafeExecutionContext(SAFE_DIR):
            # os.chdir 未被限制
            os.chdir(UNSAFE_DIR)
            current = os.getcwd()
            print(f"❌ CRITICAL SECURITY BREACH: os.chdir 可以改变到外部目录！")
            print(f"   当前目录: {current}")
            return False
    except Exception as e:
        print(f"✓ os.chdir 被阻止: {e}")
        return True
    finally:
        os.chdir(original_cwd)


def cleanup_test_env():
    """清理测试环境"""
    if os.path.exists(TEST_ROOT):
        shutil.rmtree(TEST_ROOT)
    print("✅ 测试环境已清理")


def main():
    print("\n" + "="*70)
    print("SafeExecutionContext 安全性测试")
    print("="*70 + "\n")

    # 设置测试环境
    setup_test_env()

    # 运行所有测试
    results = []

    # 基本功能测试
    results.append(("基本允许的操作", test_case("基本允许的操作", test_1_basic_allowed_operations)))

    # 安全限制测试
    results.append(("绝对路径访问外部", test_case("绝对路径访问外部", test_2_absolute_path_outside)))
    results.append((".. 访问父目录", test_case(".. 访问父目录", test_3_relative_path_parent)))
    results.append(("复杂相对路径", test_case("复杂相对路径", test_5_complex_relative_path)))

    # 危险操作禁用测试
    results.append(("eval 禁用", test_case("eval 禁用", test_6_eval_disabled)))
    results.append(("exec 禁用", test_case("exec 禁用", test_7_exec_disabled)))
    results.append(("subprocess 禁用", test_case("subprocess 禁用", test_8_subprocess_disabled)))

    # 已知漏洞测试
    results.append(("符号链接绕过 (已知漏洞)", test_case("符号链接绕过", test_4_symlink_bypass)))
    results.append(("os.listdir 未限制", test_case("os.listdir 未限制", test_9_os_listdir_not_restricted)))
    results.append(("pathlib 未限制 (严重)", test_case("pathlib 未限制", test_10_pathlib_operations)))
    results.append(("os.walk 未限制", test_case("os.walk 未限制", test_11_os_walk_not_restricted)))
    results.append(("os.chdir 未限制 (严重)", test_case("os.chdir 未限制", test_12_os_chdir_not_restricted)))

    # 清理
    cleanup_test_env()

    # 汇总结果
    print("\n" + "="*70)
    print("测试结果汇总")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f"\n通过: {passed}/{total}")
    print(f"失败: {total - passed}/{total}")

    print("\n详细结果:")
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")

    # 安全评估
    print("\n" + "="*70)
    print("安全评估")
    print("="*70)

    # 统计严重漏洞
    critical_vulns = [name for name, result in results if not result and any(
        keyword in name for keyword in ["符号链接", "pathlib", "chdir"]
    )]

    if critical_vulns:
        print("\n🚨 发现严重安全漏洞:")
        for vuln in critical_vulns:
            print(f"  - {vuln}")

    if passed == total:
        print("\n✅ SafeExecutionContext 安全性验证通过！")
    elif len(critical_vulns) > 0:
        print("\n❌ SafeExecutionContext 存在严重安全漏洞，不建议在生产环境使用！")
    else:
        print("\n⚠️  SafeExecutionContext 存在一些安全问题，需要改进")

    return passed, total


if __name__ == "__main__":
    passed, total = main()
    sys.exit(0 if passed == total else 1)
