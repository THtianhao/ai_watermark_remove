import os.path
import shutil

import cv2
import numpy as np
from ultralytics import YOLO

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
        base_name = base_name[:-8]
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

# 利用yolo打标签
def identify():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(current_dir)
    model_path = current_dir + '/yolo.pt'
    model = YOLO(model_path)  # pretrained YOLOv8n model
    results = model('/Volumes/Samsung_T5/image/汉服/all/')
    # results = model(['/Volumes/Samsung_T5/image/汉服/all/汉服_20230818_221956_451673.jpg',
    #                  '/Volumes/Samsung_T5/image/汉服/all/汉服_20230818_221956_596268.jpg',
    #                  '/Volumes/Samsung_T5/image/汉服/all/汉服_20230818_221957_222866.jpg',
    #                  '/Volumes/Samsung_T5/image/汉服/all/汉服_20230818_221958_060101.jpg',
    #                  '/Volumes/Samsung_T5/image/汉服/all/汉服_20230818_221958_376129.jpg',
    #                  '/Volumes/Samsung_T5/image/汉服/all/汉服_20230818_221959_274586.jpg',
    #                  '/Volumes/Samsung_T5/image/汉服/all/汉服_20230818_221959_627561.jpg',
    #                  '/Volumes/Samsung_T5/image/汉服/all/汉服_20230818_221959_657735.jpg',
    #                  '/Volumes/Samsung_T5/image/汉服/all/汉服_20230818_222003_159744.jpg',
    #                  '/Volumes/Samsung_T5/image/汉服/all/汉服_20230818_222004_525555.jpg',
    #                  '/Volumes/Samsung_T5/image/汉服/all/汉服_20230818_222004_525555.jpg'])
    # outputPath = "/Volumes/Samsung_T5/image/汉服/all"
    outputPath = "/Volumes/Samsung_T5/image/汉服/all_mask"
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    # Process results list
    for result in results:
        boxes = result.boxes  # Boxes object for bbox outputs
        conf = boxes.conf.tolist()
        if not conf:
            continue
        if max(conf) < 0.3:
            print(f'skip {result.path} {conf}')
            continue
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        # mask生成
        mask = np.zeros((result.orig_img.shape[0], result.orig_img.shape[1]))
        if boxes.xyxy.numel() == 0:
            continue
        box = boxes.xyxy.cpu().detach().numpy().astype(int)[0]
        x1, y1, x2, y2 = box
        if y1 < result.orig_img.shape[0] / 4 * 3:
            print(f'skip {result.path} y1 = {y1}')
            continue
        print(f'{result.path} {conf} {x1},{y1},{x2},{y2}')
        mask[y1:y2, x1:x2] = 255
        filename = os.path.basename(result.path)
        shutil.copyfile(result.path, os.path.join(outputPath, filename))
        name, extension = filename.split('.')
        filename = name + "_mask001.png"
        mask_filename = os.path.join(outputPath, filename)
        cv2.imwrite(mask_filename, mask)

import os

def rename_files_in_folder(folder_path):
    for index , filename in enumerate(os.listdir(folder_path)):
        # 构建原始文件路径
        old_filepath = os.path.join(folder_path, filename)

        # 将中文字符替换为英文字符或其他字符
        new_filename = filename.replace("汉服", "hanfu")

        # 构建新的文件路径
        new_filepath = os.path.join(folder_path, new_filename)

        # 重命名文件
        os.rename(old_filepath, new_filepath)
        print(index)


if __name__ == "__main__":
    rename_files_in_folder("/Volumes/Samsung_T5/image/汉服/all")


# if __name__ == "__main__":
#     folder_path = 'C:\\path\\to\\your\\folder'  # 指定要遍历的文件夹路径
#     rename_files_in_folder(folder_path)
#
# if __name__ == '__main__':
#     replace_png_to_target_folder('/Volumes/Samsung_T5/image/汉服/out_all_mask',
#                                  '/Volumes/Samsung_T5/image/汉服/all')
