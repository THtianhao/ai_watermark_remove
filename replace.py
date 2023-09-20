import os
import shutil

def replace_png_to_target_folder(source_folder, destination_folder):
    """
    将源文件夹内的PNG文件替换到目标文件夹内的同名文件，保留目标文件夹的后缀。

    :param source_folder: 源文件夹的路径
    :param destination_folder: 目标文件夹的路径
    """
    # 获取源文件夹中的所有PNG文件
    png_files = [f for f in os.listdir(source_folder) if f.endswith('.png')]
    for png_file in png_files:
        # 构建目标文件的完整路径（假设目标文件夹中文件名和源文件名相同，但后缀可能不同）
        base_name = os.path.splitext(png_file)[0]  # 获取文件名（不包含后缀）

        # 获取目标文件夹中与源文件同名的文件
        matching_files = [f for f in os.listdir(destination_folder) if f.startswith(base_name)]

        for matching_file in matching_files:
            source_file_path = os.path.join(source_folder, png_file)
            target_file_path = os.path.join(destination_folder, matching_file)
            # 删除目标文件
            os.remove(target_file_path)
            # 复制源文件到目标文件夹
            shutil.copy2(source_file_path, target_file_path)

    print("替换完成")

# 使用示例：
# replace_png_to_target_folder('源文件夹路径', '目标文件夹路径')
