import cv2
import numpy
import win32gui
import win32api
import win32con
import win32ui
import time
# import pyautogui
import random

from PIL import Image

position_enter_game = (460, 480)
fatherHandleThunder = win32gui.FindWindow("LDPlayerMainFrame", "0")
handleThunder = win32gui.FindWindowEx(fatherHandleThunder, 0, "RenderWindow", "TheRender")


# handle = win32gui.FindWindowEx(fHandle, 0, "subWin", "sub")
# handleOnmyoji = win32gui.FindWindow("Win32Window0", "阴阳师-网易游戏")
# handleOnmyojiLogin = win32gui.FindWindow("MPAY_LOGIN", "登录")


def click_it(handle, position_in_window):
    print(position_in_window)
    tmp = win32api.MAKELONG(position_in_window[0], position_in_window[1])
    win32gui.SendMessage(handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    time.sleep(random.randrange(1))
    win32gui.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, tmp)
    time.sleep(random.randrange(1))
    win32gui.SendMessage(handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, tmp)


def drag_it(handle, position_in_window, str):
    tmp1 = win32api.MAKELONG(position_in_window[0], position_in_window[1])
    if str == "up":
        tmp2 = win32api.MAKELONG(position_in_window[0], position_in_window[1] - 90)
        print(str)
    elif str == "down":
        tmp2 = win32api.MAKELONG(position_in_window[0], position_in_window[1] + 90)
        print(str)
    elif str == "left":
        tmp2 = win32api.MAKELONG(position_in_window[0] - 90, position_in_window[1])
        print(str)
    elif str == "right":
        tmp2 = win32api.MAKELONG(position_in_window[0] + 90, position_in_window[1])
        print(str)
    win32gui.SendMessage(handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    time.sleep(random.randrange(1))
    win32gui.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, tmp1)
    time.sleep(random.randrange(1))
    win32gui.SendMessage(handle, win32con.WM_MOUSEMOVE, 0, tmp2)
    time.sleep(random.randrange(1))
    win32gui.SendMessage(handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, tmp2)


def walk_it(handle, str):
    position_in_window = [480, 10]
    if str == "left":
        tmp2 = win32api.MAKELONG(position_in_window[0] - 50, position_in_window[1])
        print(str)
    elif str == "right":
        tmp2 = win32api.MAKELONG(position_in_window[0] + 50, position_in_window[1] + 90)
        print(str)
    win32gui.SendMessage(handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    time.sleep(random.randrange(1))
    win32gui.SendMessage(handle, win32con.WM_MOUSEMOVE, 0, tmp2)
    time.sleep(random.randrange(1))
    win32gui.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, tmp2)
    time.sleep(random.randrange(1))
    win32gui.SendMessage(handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, tmp2)


def random_pos():
    ranX = random.randint(0, 960)
    ranY = random.randint(0, 540)
    return ranX, ranY


def get_background_image(handle):
    if handle == 0:
        return "../images/blank.bmp"
    hwnd = handle
    w = 1280
    h = 720
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    img_dc = mfcDC
    mem_dc = saveDC
    mem_dc.BitBlt((0, 0), (w, h), img_dc, (0, 0), win32con.SRCCOPY)
    # bmpinfo = saveBitMap.GetInfo()
    # bmparray = numpy.asarray(saveBitMap.GetBitmapBits(), dtype=numpy.uint8)
    # pil_im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmparray, 'raw', 'BGRX', 0, 1)
    # pil_array = numpy.array(pil_im)
    # cv_im = cv2.cvtColor(pil_array, cv2.COLOR_RGB2BGR)
    saveBitMap.SaveBitmapFile(mem_dc, "screenShot.bmp")
    # print(saveBitMap)
    # print(cv_im)
    # cv2.imwrite('test.png',cv_im)
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    return "../images/screenShot.bmp"


def rect_to_cord(rect):
    try:
        result = int(rect[0] + rect[2] / 2.0), int(rect[1] + rect[3] / 2.0)
    except:
        result = None
    return result


def is_menu_page():
    return pyautogui.locate("../images/menupageflag.png", get_background_image(handleThunder))


def is_explore_page():
    return pyautogui.locate("../images/explorepageflag.png", get_background_image(handleThunder))


def open_scroll():
    click_scroll = rect_to_cord(pyautogui.locate("../images/scroll.png", get_background_image(handleThunder)))
    print(click_scroll)
    click_it(handleThunder, click_scroll)


def close_scroll():
    click_scroll = rect_to_cord(pyautogui.locate("../images/closeScroll.png", get_background_image(handleThunder)))
    print(click_scroll)
    click_it(handleThunder, click_scroll)


def open_explore():
    click_it(handleThunder, (482, 119))


def open_yuhun():
    click_it(handleThunder,
             rect_to_cord(pyautogui.locate("../images/mitama_icon.png", get_background_image(handleThunder))))


def open_snake():
    click_it(handleThunder,
             rect_to_cord(pyautogui.locate("../images/snakeeye.png", get_background_image(handleThunder))))


drag_it(handleThunder, (233, 567), "right")
# if is_explore_page():
#     open_yuhun()
#     time.sleep(3)
#     open_snake()
#     time.sleep(1)
#     drag_it(handleThunder, (303, 183), "up")
#     time.sleep(1)
#     drag_it(handleThunder, (303, 183), "up")
#     time.sleep(1)
#     click_it(handleThunder,
#              rect_to_cord(pyautogui.locate("../images/tenfloor.png", get_background_image(handleThunder))))
#     time.sleep(1)
#     click_it(handleThunder,
#              rect_to_cord(pyautogui.locate("../images/team.png", get_background_image(handleThunder))))
#     time.sleep(1.2)
#     click_it(handleThunder,
#              rect_to_cord(pyautogui.locate("../images/createteam.png", get_background_image(handleThunder))))
#     time.sleep(0.9)
#     click_it(handleThunder,
#              rect_to_cord(pyautogui.locate("../images/notopen.png", get_background_image(handleThunder))))
#     time.sleep(1.2)
#     click_it(handleThunder,
#              rect_to_cord(pyautogui.locate("../images/create.png", get_background_image(handleThunder))))
#     time.sleep(2)
#     while pyautogui.locate("../images/invite.png", get_background_image(handleThunder)):
#         time.sleep(1.1)
#         click_it(handleThunder,
#                  rect_to_cord(pyautogui.locate("../images/invite.png", get_background_image(handleThunder))))
#         time.sleep(1.2)
#         click_it(handleThunder,
#                  rect_to_cord(pyautogui.locate("../images/friend.png", get_background_image(handleThunder))))
#         time.sleep(1.2)
#         if pyautogui.locate("../images/jm.png", get_background_image(handleThunder)):
#             click_it(handleThunder,
#                      rect_to_cord(pyautogui.locate("../images/jm.png", get_background_image(handleThunder))))
#         time.sleep(1.3)
#         click_it(handleThunder,
#                  rect_to_cord(pyautogui.locate("../images/extendblock.png", get_background_image(handleThunder))))
#         time.sleep(1.3)
#         if pyautogui.locate("../images/mq.png", get_background_image(handleThunder)):
#             click_it(handleThunder,
#                      rect_to_cord(pyautogui.locate("../images/mq.png", get_background_image(handleThunder))))
#         time.sleep(1.2)
#         click_it(handleThunder,
#                  rect_to_cord(pyautogui.locate("../images/yuhunbegin.png", get_background_image(handleThunder))))
#         time.sleep(5)
#
#     click_it(handleThunder,
#              rect_to_cord(pyautogui.locate("../images/fight.png", get_background_image(handleThunder))))
#
get_background_image(handleThunder)
