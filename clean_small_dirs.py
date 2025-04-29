#!/usr/bin/env python3

import os
import argparse
import shutil
from pathlib import Path

def get_dir_size(path: Path) -> int:
    """递归获取目录大小（单位：字节）"""
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = Path(dirpath) / f
            try:
                total += fp.stat().st_size
            except FileNotFoundError:
                continue  # 跳过已被删除的文件
    return total

def parse_size(size_str: str) -> int:
    """将 1G, 500M, 200K 等字符串转换为字节数"""
    size_str = size_str.strip().upper()
    units = {'K': 1024, 'M': 1024**2, 'G': 1024**3}
    if size_str[-1] in units:
        return int(float(size_str[:-1]) * units[size_str[-1]])
    return int(size_str)

def clean_dirs(base_dir: Path, threshold: int, dry_run: bool):
    for child in base_dir.iterdir():
        if child.is_dir():
            size = get_dir_size(child)
            if size < threshold:
                human_readable = f"{size / 1024**2:.2f} MB"
                if dry_run:
                    print(f"[DRY-RUN] Would delete: {child} (size: {human_readable})")
                else:
                    print(f"Deleting: {child} (size: {human_readable})")
                    shutil.rmtree(child, ignore_errors=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete subdirs smaller than a size threshold")
    parser.add_argument("-d", "--dir", default=".", help="Target directory (default: current)")
    parser.add_argument("-s", "--size", default="1G", help="Size threshold (e.g., 1G, 500M, 100K)")
    parser.add_argument("--dry-run", action="store_true", help="Only print, do not delete")

    args = parser.parse_args()
    base_path = Path(args.dir).resolve()
    size_threshold = parse_size(args.size)

    if not base_path.is_dir():
        print(f"Error: {base_path} is not a valid directory")
        exit(1)

    clean_dirs(base_path, size_threshold, args.dry_run)
