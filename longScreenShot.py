#!/usr/bin/python env
# -*- coding: utf-8 -*-

import time
import subprocess
import logging


"""
# 分辨率
"adb shell wm size"
adb shell input swipe命令中的坐标值中的第一个值是x坐标，代表屏幕上的水平位置（宽度），
而第二个值是y坐标，代表垂直位置（高度）。所以，中是屏幕上的水平位置（宽度），而第二个值是y坐标，代表垂直位置（高度）
adb shell input swipe 540 1600 540 800 500。540宽度上的坐标，表示滑动的起始点和结束点的位置相同，即屏幕中间的水平位置。
这个会在屏幕中间从上到下滑动，持续500毫秒。请根据您的需求调整坐标和持续时间。
"""


# 执行ADB命令获取屏幕截图

class ScreenCapture:

    def __init__(self):
        self._running = True

    def _screen(self, y1: int, y2: int, height: int) -> None:
        if y1 < y2 < height:
            count = 1
            while self._running:
                subprocess.Popen(['adb', 'shell', 'input', 'swipe', '350', str(y2), '350', str(y1), '250'],
                                 stdout=subprocess.PIPE)
                process = subprocess.Popen(['adb', 'exec-out', 'screencap', '-p'], stdout=subprocess.PIPE)
                # 读取屏幕截图数据
                screenshot = process.stdout.read()
                # 将屏幕截图保存到本地文件
                with open(f'screenshot_{time.time()}.png', 'wb') as f:
                    f.write(screenshot)
                time.sleep(1)
                count += 1
        raise ValueError(f"y2必需大于y1,且小于{height}")

    def stop(self):
        self._running = False

    def check_drive(self):
        """adb驱动检测"""
        action = subprocess.Popen('adb version', stdout=subprocess.PIPE)
        result = action.stdout.read()
        return result.decode()

    def fund_devices(self):
        """查看手机列表"""
        action = subprocess.Popen('adb devices', stdout=subprocess.PIPE)
        result = action.stdout.read()
        return result.decode()

    def _get_phone_resolution(self):
        """获取手机分辨率"""
        action = subprocess.Popen(['adb', 'shell', 'wm', 'size'], stdout=subprocess.PIPE)
        result = action.stdout.read()
        _, size = result.decode().split(':')
        width, height = size.strip().split('x')
        logging.debug(f'获取到手机分辨率为：{width}x{height}')
        return int(width), int(height)

    def run(self):
        width, height = self._get_phone_resolution()
        y1 = int(int(height) / 2)
        y2 = y1 + (height - width)
        self._screen(y1, y2, height)