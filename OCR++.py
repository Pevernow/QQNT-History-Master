import cv2
import numpy as np


longscreenshot_path = "Screenshot_20240711_112744.jpg"

# 读取大图和小图
longscreenshot_image = cv2.imread(big_image_path)


def get_avatar_clicks(image):
    """
    Displays an image and allows the user to click on two avatars.
    Records the click coordinates for each avatar and returns them as a list.

    Args:
        image (obj): Opencv2 image object.

    Returns:
        List[tuple]: A list containing the coordinates of the two avatar clicks.
    """

    # Initialize variables to store click coordinates
    avatar_clicks = []

    # Define a mouse callback function to handle mouse clicks
    def mouse_callback(event, x, y, flags, param):
        # Check for left mouse click
        if event == cv2.EVENT_LBUTTONDOWN:
            # Append the click coordinates to the list
            avatar_clicks.append((x, y))

            # Check if two clicks have been registered
            if len(avatar_clicks) == 2:
                # Close the window
                cv2.destroyWindow("Image")

    # Set the mouse callback function for the image window
    cv2.setMouseCallback("Image", mouse_callback)

    # Display the image in a window
    cv2.imshow("Image", image)

    while True:
        if len(avatar_clicks) >= 2:  # Check for two clicks or 5 seconds timeout
            break

        # Process pending events (including window close events)
        cv2.waitKey(100)
        

    return avatar_clicks



# Read the image
image = cv2.imread(image_path)

# Check if the image was read successfully
if image is None:
    print(f"Failed to read image: {image_path}")
    return None

# Get avatar click coordinates
avatar_clicks = get_avatar_clicks(image_path)

# Check if coordinates were successfully obtained
if avatar_clicks is not None:
    print(f"Avatar click coordinates: {avatar_clicks}")
    exit()

def find_non_trash_segments_midpoints(image, start_coord, trash_color, min_segment_length=10):
  """
  从指定像素开始垂直向下遍历一列像素，并找到所有长度不小于 min_segment_length 的非垃圾像素段的中点坐标。

  参数：
    image: OpenCV 图像对象
    start_coord: 起始像素坐标 (x, y)
    trash_color: 垃圾像素 RGB 颜色值 (R, G, B)
    min_segment_length: 最小非垃圾像素段长度（默认为 10）

  返回值：
    包含所有有效非垃圾像素段中点坐标的列表 [(x, y)]。
  """

  # 获取图像高度
  image_height = image.shape[0]

  # 初始化有效非垃圾像素段列表
  valid_non_trash_segments_midpoints = []

  # 当前非垃圾像素段的起始 y 坐标
  current_segment_start_y = None

  # 当前非垃圾像素段长度
  current_segment_length = 0

  # 从起始像素开始遍历
  y = start_coord[1]
  while y < image_height:
    # 获取当前像素的 RGB 值
    current_color = image[y, start_coord[0]]

    # 判断是否为垃圾像素
    if not np.array_equal(current_color, trash_color):
      # 非垃圾像素

      if current_segment_start_y is None:
        # 新的非垃圾像素段开始
        current_segment_start_y = y
        current_segment_length = 1

      else:
        # 累计非垃圾像素段长度
        current_segment_length += 1

    else:
      # 垃圾像素

      if current_segment_start_y is not None and current_segment_length >= min_segment_length:
        # 非垃圾像素段结束且长度不小于 min_segment_length，则认为有效
        # 计算中点坐标
        segment_midpoint_y = current_segment_start_y + current_segment_length // 2
        valid_non_trash_segments_midpoints.append((start_coord[0], segment_midpoint_y))

        # 重置当前非垃圾像素段
        current_segment_start_y = None
        current_segment_length = 0

    # 下移一行
    y += 1

  # 处理最后一个非垃圾像素段
  if current_segment_start_y is not None and current_segment_length >= min_segment_length:
    segment_midpoint_y = current_segment_start_y + current_segment_length // 2
    valid_non_trash_segments_midpoints.append((start_coord[0], segment_midpoint_y))

  return valid_non_trash_segments_midpoints

# 测试代码
start_coord = (85, 1430)  # 替换为实际起始坐标

image = cv2.imread("C:\code\QQNT-History-Master\Screenshot_20240711_112744.jpg")  # 替换为实际图像路径
trash_color = (242, 237, 238)  # 替换为垃圾像素 BGR 颜色值

valid_non_trash_segments_midpoints = find_non_trash_segments_midpoints(image, start_coord, trash_color)


def get_message_rect(avatar):
    """匹配不到有bug用不了，还要手动截头像图

    # 转换为灰度图
    big_gray = cv2.cvtColor(big_image, cv2.COLOR_BGR2GRAY)
    small_gray = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)
    h, w = small_gray.shape[:2]
    # 使用模板匹配方法找到小图在大图中的位置
    res = cv2.matchTemplate(big_gray, small_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    """

    cv2.namedWindow("click your avatar")


    cv2.setMouseCallback("click your avatar", on_EVENT_LBUTTONDOWN)
    while 1:
        cv2.imshow("click your avatar", big_image)
        cv2.destroyWindow("click your avatar")
        


    small_image_top_left = min_loc
    small_image_bottom_right = (
        small_image_top_left[0] + w,
        small_image_top_left[1] + h,
    )
    # magic_offset=5
    small_image_right_center = (
        small_image_top_left[0] + 5,
        small_image_top_left[1] + int(float(h) / 2),
    )
    print(min_loc)
    cv2.imshow("", big_image[29:, :2534])
    cv2.waitKey(0)
    pad = 0
    while True:
        pad += 1
        if (
            big_image[small_image_right_center[0] + pad, small_image_right_center[1]]
            - (238, 237, 242)
        ).any():
            break
    x_start = small_image_right_center[0] + pad - 10

    pad = 0
    while True:
        pad += 1
        print(x_start + pad)
        if not (
            big_image[x_start + pad, small_image_right_center[1]] - (238, 237, 242)
        ).any():
            break
    x_end = x_start + pad + 10

    pad = 0
    while True:
        pad += 1
        if not (
            big_image[
                int(float(x_start + x_end) / 2), small_image_right_center[1] + pad
            ]
            - (238, 237, 242)
        ).any():
            break
    y_end = small_image_right_center[1] + pad + 10

    pad = 0
    while True:
        pad += 1
        if not (
            big_image[
                int(float(x_start + x_end) / 2), small_image_right_center[1] - pad
            ]
            - (238, 237, 242)
        ).any():
            break
    y_start = small_image_right_center[1] - pad - 10
    cv2.imshow("img", big_image[x_start:x_end, y_start:y_end])
    cv2.waitKey(0)
    return big_image[x_start:x_end, y_start:y_end]

get_message_rect(small_image, big_image)
