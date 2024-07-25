import longScreenShot
import os


def del_files(path):
    for root , dirs, files in os.walk(path):
        for name in files:
            if name.endswith(".png"):
                os.remove(os.path.join(root, name))
                print ("Delete File: " + os.path.join(root, name))


print("开始截屏...")

longScreenShot.ScreenCapture().run()

print("尝试合并...")

import splicing


import cv2
import numpy as np

def find_image(big_image_path, small_image_path):
  """
  在大图中找到小图的位置

  Args:
    big_image_path: 大图的路径
    small_image_path: 小图的路径

  Returns:
    小图在大图中的位置，如果没有找到则返回 None
  """

  # 读取大图和小图
  big_image = cv2.imread(big_image_path)
  small_image = cv2.imread(small_image_path)

  # 转换为灰度图
  big_gray = cv2.cvtColor(big_image, cv2.COLOR_BGR2GRAY)
  small_gray = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)

  # 使用模板匹配方法找到小图在大图中的位置
  result = cv2.matchTemplate(big_gray, small_gray, cv2.TM_CCOEFF_NORMED)

  # 获取匹配位置
  (x, y) = np.unravel_index(result.argmax(), result.shape)

  # 检查匹配度
  if result[y, x] < 0.5:
    return None

  # 返回匹配位置
  return (x, y)

if __name__ == "__main__":
  # 测试代码
  big_image_path = "big_image.jpg"
  small_image_path = "small_image.jpg"

  position = find_image(big_image_path, small_image_path)

  if position:
    (x, y) = position
    print(f"小图在大图中的位置：({x}, {y})")
  else:
    print("未找到小图")

