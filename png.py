import os
import numpy as np
import matplotlib.pyplot as plt
from pds4_tools import pds4_read
from skimage import exposure, img_as_float
from PIL import Image
from tqdm import tqdm
import glob

from colour_demosaicing import demosaicing_CFA_Bayer_Menon2007
from colour import cctf_encoding

def read_pds(path):
    data = pds4_read(path, quiet=True)
    img = np.array(data[0].data)
    img = img_as_float(img)
    return img

def debayer_img(img, CFA='RGGB'):
    debayered = cctf_encoding(demosaicing_CFA_Bayer_Menon2007(img, CFA))
    return debayered

def stretch_img(img):
    p2, p98 = np.percentile(img, (2, 98))
    img = exposure.rescale_intensity(img, in_range=(p2, p98))
    return img

def export_img(name, img):
    pil_img = Image.fromarray(np.uint8(img * 255))
    pil_img.save(name)

def process_directory(input_directory, output_directory):
    os.makedirs(output_directory, exist_ok=True)
    for file_path in tqdm(glob.glob(os.path.join(input_directory, '*.*L'))):
        try:
            img = read_pds(file_path)
            if img.shape == (1728, 2352):
                img = debayer_img(img)
            elif img.shape != (864, 1176):
                print(f'{file_path} has an unexpected dimension: {img.shape}')
            img = stretch_img(img)
            output_path = os.path.join(output_directory, f"{os.path.basename(file_path)}.png")
            export_img(output_path, img)
            print(f"Saved image to: {output_path}")
        except KeyError as e:
            print(f"Error processing file {file_path}: {e}")

# 示例目录路径
input_directory = r'C:\Users\xiaoyu\Desktop\Tsinghua\downloads'
output_directory = r'C:\Users\xiaoyu\Desktop\Tsinghua\IMAGE'

# 处理目录中的所有文件并保存图像
process_directory(input_directory, output_directory)
