"""
批量重命名文件：将文件名中的空格替换为横线
"""
import os
import shutil


def rename_files_with_spaces(directory: str, dry_run: bool = True):
    """
    重命名目录中文件名包含空格的文件

    Args:
        directory: 目标目录
        dry_run: True 时只预览，不实际重命名
    """
    if not os.path.exists(directory):
        print(f"❌ Directory not found: {directory}")
        return

    files = os.listdir(directory)
    files_with_spaces = [f for f in files if ' ' in f and os.path.isfile(os.path.join(directory, f))]

    if not files_with_spaces:
        print("✅ No files with spaces found!")
        return

    print(f"Found {len(files_with_spaces)} files with spaces in their names:\n")

    renamed_count = 0
    for old_name in sorted(files_with_spaces):
        new_name = old_name.replace(' ', '-')
        old_path = os.path.join(directory, old_name)
        new_path = os.path.join(directory, new_name)

        # 检查目标文件是否已存在
        if os.path.exists(new_path):
            print(f"⚠️  SKIP (target exists): {old_name}")
            print(f"   → {new_name}\n")
            continue

        if dry_run:
            print(f"[DRY RUN] {old_name}")
            print(f"       → {new_name}\n")
        else:
            try:
                shutil.move(old_path, new_path)
                print(f"✅ RENAMED: {old_name}")
                print(f"         → {new_name}\n")
                renamed_count += 1
            except Exception as e:
                print(f"❌ ERROR: {old_name}")
                print(f"   Error: {e}\n")

    if dry_run:
        print("=" * 80)
        print("🔍 DRY RUN MODE - No files were actually renamed")
        print("=" * 80)
        print(f"To execute the renaming, run this script with dry_run=False")
    else:
        print("=" * 80)
        print(f"✅ Successfully renamed {renamed_count} files!")
        print("=" * 80)


def main():
    target_dir = "/data/lhy/datasets/graph-Toucan/tool_info/generated_functions_v1"

    print("=" * 80)
    print("STEP 1: Preview (Dry Run)")
    print("=" * 80)
    rename_files_with_spaces(target_dir, dry_run=True)

    print("\n" + "=" * 80)
    print("STEP 2: Execute Renaming")
    print("=" * 80)
    user_input = input("\nProceed with renaming? (yes/no): ").strip().lower()

    if user_input in ['yes', 'y']:
        print("\n🔄 Renaming files...\n")
        rename_files_with_spaces(target_dir, dry_run=False)
    else:
        print("\n❌ Renaming cancelled.")


if __name__ == "__main__":
    main()
