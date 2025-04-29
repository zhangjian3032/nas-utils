#!/bin/python3

import os
import shutil
import argparse

def move_large_files(source_dir, target_dir, dry_run):
    # 1GB 换算成字节
    one_gb = 1024 * 1024 * 1024
    # 更丰富的常见视频文件扩展名
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.mpg', '.mpeg', '.3gp', '.rmvb', '.vob')
    try:
        # 遍历源目录下的一级子目录
        for sub_dir in os.listdir(source_dir):
            sub_dir_path = os.path.join(source_dir, sub_dir)
            if os.path.isdir(sub_dir_path):
                has_large_video = False
                # 遍历子目录下的文件
                for item in os.listdir(sub_dir_path):
                    item_path = os.path.join(sub_dir_path, item)
                    if os.path.isfile(item_path) and os.path.getsize(item_path) > one_gb and item.lower().endswith(video_extensions):
                        has_large_video = True
                        break
                if has_large_video:
                    target_sub_dir_path = os.path.join(target_dir, sub_dir)
                    if dry_run:
                        print(f"DRY RUN: 将会移动 {sub_dir_path} 到 {target_sub_dir_path}")
                    else:
                        print(f"正在移动 {sub_dir_path} 到 {target_sub_dir_path}")
                        shutil.move(sub_dir_path, target_sub_dir_path)
    except FileNotFoundError:
        print(f"错误: 未找到目录 {source_dir} 或 {target_dir}。")
    except Exception as e:
        print(f"错误: 发生未知错误: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="遍历指定目录下的一级子目录，移动包含大于 1GB 视频文件的上一层目录到特定目录。")
    parser.add_argument("source_dir", help="要遍历的源目录")
    parser.add_argument("target_dir", help="要移动目录到的目标目录")
    parser.add_argument("--dry-run", action="store_true", help="开启 dry-run 模式，仅显示将要执行的操作")
    args = parser.parse_args()

    move_large_files(args.source_dir, args.target_dir, args.dry_run)
