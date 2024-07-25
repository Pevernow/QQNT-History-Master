#! python3
import sys
import os
from PIL import Image
from core import find_coincide
from image import get_vertical_color
import time

ext = 'png'
# 剪裁头尾
header_height = 450
footer_height = 450
# 取 x = n 列的像素
x = 210

def get_png_paths(subfolder_path):
    # Initialize an empty list to store the paths
    png_paths = []

    # Walk through the subfolder and its subdirectories
    for root, _, filenames in os.walk(subfolder_path):
        for filename in filenames:
            # Check if the file is a PNG image
            if filename.endswith('.png'):
                # Get the absolute path of the PNG file
                png_path = os.path.join(root, filename)

                # Append the path to the list
                png_paths.append(png_path)

    return png_paths



imageList = get_png_paths("output")
allExist = True

for path in imageList:
    if not os.path.exists(path):
        print(f'Path: "{path}" does not exist!')
        allExist = False
    else:
        print(f'{os.path.basename(path)}')

if not allExist:
    sys.exit(0)

i = 0
origin_image_list = []
image_list = []

root_path = os.path.abspath(os.path.join(__file__, '../../'))
# print('root_path: ', root_path)
# sys.exit(0)

for path in imageList:
    i += 1
    img = Image.open(path)
    origin_image_list.append(img)
    # 转换为灰度图片
    img = img.convert('L')
    # 剪裁头尾, header_height & footer_height
    img = img.crop((0, header_height, img.width, img.height - footer_height))
    img.save(f'{root_path}/tmp/1-{i}.{ext}')
    image_list.append(img)


last_color_list = []
current_color_list = []


last_color_list = get_vertical_color(image_list[0], x)
last_color_list_index = 0

img1 = image_list[0]
img2 = image_list[1]

# header
origin_img1 = origin_image_list[0]
top = header_height

long_img = Image.new('RGB', (origin_img1.width, origin_img1.height * 10))
header = origin_img1.crop((0, 0, origin_img1.width, top))
long_img.paste(header, (0, 0, origin_img1.width, top))

long_img.save(f'{root_path}/tmp/2-0.{ext}')

# 第一张图
img1_content = origin_img1.crop((0, header_height, origin_img1.width, origin_img1.height - footer_height))
long_img.paste(img1_content, (0, top, img1_content.width, top + img1_content.height))
top += img1_content.height

long_img.save(f'{root_path}/tmp/2-1.{ext}')

for i in range(1, len(image_list)):
    print('i -> ', i, last_color_list_index)
    t1 = time.time()
    current_color_list = get_vertical_color(image_list[i], x)
    shift = find_coincide(last_color_list, current_color_list)
    origin_img = origin_image_list[i]
    offset = shift - origin_img.height
    top += shift
    t2 = time.time()
    print('i -> time ', t2 - t1, t2, t1)

    img_content = origin_img.crop((0, header_height, origin_img.width, origin_img.height - footer_height))
    long_img.paste(img_content, (0, top - img_content.height, img_content.width, top))

    last_color_list = current_color_list
    last_color_list_index = i

    long_img.save(f'{root_path}/tmp/2-{i + 1}.{ext}')

# footer
footer_img = origin_image_list[-1]
footer = footer_img.crop((0, footer_img.height - footer_height, footer_img.width, footer_img.height))
top += footer.height
long_img.paste(footer, (0, top - footer.height, footer.width, top))

long_img.save(f'{root_path}/tmp/2-end.{ext}')
