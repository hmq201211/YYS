import base64
import collections
import json
import threading
import winsound
import win32com.client
import time
import numpy
import cv2
import requests
import glob
import configparser

# d = collections.defaultdict(int)
# d[1] = 1
# d[2] = 1
# d[3] = 1
# d[4] = 1
# d[5] = 1
# d[6] = 1
# d[7] = 1
#
# for k in d.values():
#     print(k)
#
#
# def r(s):
#     print("r" + s)
#
#
# def b(s):
#     print("b" + s)
#
#
# def t(name, params):
#     name(params)
#
#
# t(b, "123")

# access_token = "24.23d29c67210387cca93ac7c6364e429d.2592000.1563507426.282335-16564125"
# url = "https://aip.baidubce.com/rest/2.0/ocr/v1/numbers?" \
#       "access_token=24.23d29c67210387cca93ac7c6364e429d.2592000.1563507426.282335-16564125"
# headers = {
#     'Content-Type': 'application/x-www-form-urlencoded',
# }
# data = {
#     'image': base64.b64encode(cv2.imencode('.png', cv2.imread('./Onmyoji_images/test.png'))[1]).decode(),
# }
# response = requests.post(url, data=data, headers=headers)
# result = json.loads(response.text)
# print(result["words_result"][0]['words'])

# f = Factory().create('zh_CN')
# db = pymysql.connect("localhost", "test", "123456", "test")
# cursor = db.cursor()
# sql = "INSERT INTO user_test(name, \
#        password, email) \
#        VALUES ('%s', '%s', '%s')"
# for i in range(20):
#     try:
#         cursor.execute(sql % (
#             f.name(), f.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True),
#             f.email()))
#         db.commit()
#     except:
#         db.rollback()
# db.close()

# print([file[17:] for file in glob.glob(r'./Onmyoji_images/*_page*.png')])

# def fetch_player_certain_place_number(path) -> str:
#     url = "https://aip.baidubce.com/rest/2.0/ocr/v1/numbers?" \
#           "access_token=24.23d29c67210387cca93ac7c6364e429d.2592000.1563507426.282335-16564125"
#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded',
#     }
#     data = {
#         'image': base64.b64encode(cv2.imencode('.png', cv2.imread(path))[1]).decode(),
#     }
#     response = requests.post(url, data=data, headers=headers)
#     result = json.loads(response.text)
#     return result["words_result"][0]['words']
#
#
# print(fetch_player_certain_place_number('H:\\123.png'))

# url = "http://localhost:4000/users/user/delete"
# # data = {
# #     'id': 21, "name": "client", "password": "U",
# #     "email": "Q"}
# data = {
#         'id': 21
# }
# response = requests.post(url, data)
# print(response.text)
# screen_shot = cv2.imread('E:/1.png')
# template_picture = cv2.imread('E:/2.png')
# result = cv2.matchTemplate(screen_shot, template_picture, cv2.TM_CCOEFF_NORMED)
# print(numpy.where(result > 0.85))
# h, w = template_picture.shape[:-1]
# for x in zip(*numpy.where(result > 0.85)[::-1]):
#     cv2.circle(screen_shot, (x[0] + int(w / 2), x[1] + int(h / 2)), 10, (0, 0, 255), 3)
# cv2.imshow('we get', screen_shot)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# speak_out = win32com.client.Dispatch('SAPI.SPVOICE')
#
#
# def print_word(word):
#     print(word)
#
#
# def time_out(func):
#     def wrap_func(*args, **kwargs):
#         timer = threading.Timer(3, func, *args, **kwargs)
#         timer.start()
#         func(*args, **kwargs)
#         timer.cancel()
#
#     return wrap_func
#
#
# @time_out
# def speak_word(word):
#     time.sleep(4)
#     speak_out.Speak(word)
#     winsound.PlaySound(word, winsound.SND_ASYNC)
#
#
# speak_word('hello')
from Crack_Onmyoji.game_detail import GameDetail

# old_time = time.time()
# time.sleep(1)
# second_time = time.time()
# print(second_time - old_time)
# throw_pool = [
#     ((i * 180, Onmyoji.hundred_ghosts_throw_height[0]), ((i + 1) * 180, Onmyoji.hundred_ghosts_throw_height[1])) for i
#     in range(6)]
# print(throw_pool)
print(time.strftime("%Y %m %d %H:%M:%S", time.localtime()))
s = time.time()
time.sleep(1)
ss = time.time()
print(ss - s)
