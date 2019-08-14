import base64
import configparser
import json
import os
import random
import shutil
import time
import cv2
import numpy
import requests
import win32com.client
from Crack_Onmyoji.game_detail import GameDetail
from Crack_Onmyoji.template_loader import TemplateLoader
from Crack_Onmyoji.player_detail import PlayerDetail


class CrackController:
    share_path = 'Onmyoji_images\\'
    speak_out = win32com.client.Dispatch('SAPI.SPVOICE')
    conf = configparser.ConfigParser()
    file_path = './instruction/config.txt'
    conf.read(file_path)
    api = conf.get('config', 'api')
    console = conf.get('config', 'console') + ' '
    ld = conf.get('config', 'ld') + ' '
    templates_dict = TemplateLoader.load_templates()

    # fetch all thunder simulators list
    @staticmethod
    def get_list() -> list:
        cmd = os.popen(CrackController.console + 'list2')
        text = cmd.read()
        cmd.close()
        print("fetching all thunder simulators list......")
        info = text.split('\n')
        result = list()
        for line in info:
            if len(line) > 1:
                thunder_player_info = line.split(',')
                result.append(PlayerDetail(thunder_player_info))
        return result

    # fetch all running thunder simulators list
    @staticmethod
    def get_running_list() -> list:
        result = list()
        all_players = CrackController.get_list()
        for player in all_players:
            if player.is_running() is True:
                result.append(player)
        return result

    # test the specified index player is running or not
    @staticmethod
    def is_player_running(index: int) -> bool:
        all_players = CrackController.get_list()
        if index >= len(all_players):
            raise IndexError('%d is not exist' % index)
        return all_players[index].is_running()

    # run ld cmd command on specified index player
    @staticmethod
    def ld_cmd(index: int, command: str, silence: bool = True) -> str:
        cmd = CrackController.ld + '-s %d %s' % (index, command)
        if silence:
            os.system(cmd)
            return ''
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # run console command
    @staticmethod
    def console_cmd(command: str, silence: bool = False) -> str:
        cmd = CrackController.console + " " + command
        if silence:
            os.system(cmd)
            return ''
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # install specified app, assuming the index player is running
    @staticmethod
    def install_app(index: int, path: str) -> str:
        shutil.copy(path, CrackController.share_path + str(index) + 'app_to_install.apk')
        CrackController.random_sleep()
        return CrackController.ld_cmd(index, 'pm install /sdcard/Pictures/' + str(index) + 'app_to_install.apk')

    # uninstall specified app, assuming the index player is running
    @staticmethod
    def uninstall_app(index: int, package: str) -> str:
        command = 'uninstallapp --index %d --packagename %s' % (index, package)
        return CrackController.console_cmd(command, True)

    # start specified app, assuming the index player is running
    @staticmethod
    def invoke_app(index: int, package: str) -> str:
        command = 'runapp --index %d --packagename %s' % (index, package)
        return CrackController.console_cmd(command)

    # stop specified app, assuming the index player is running
    @staticmethod
    def stop_app(index: int, package: str) -> str:
        command = 'killapp --index %d --packagename %s' % (index, package)
        return CrackController.console_cmd(command)

    # input word, assuming the index player is running
    @staticmethod
    def input_text(index: int, text: str) -> str:
        command = 'action --index %d --key call.input --value %s' % (index, text)
        return CrackController.console_cmd(command)

    # fetch installed app list, assuming the player is running
    @staticmethod
    def get_package_list(index: int) -> list:
        result = list()
        text = CrackController.ld_cmd(index, 'pm list packages', False)
        info = text.split('\n')
        for i in info:
            if len(i) > 1:
                result.append(i.strip())
        return result

    # test the specified app is installed or not, assuming the player is running
    @staticmethod
    def has_app_installed(index: int, package: str) -> bool:
        if CrackController.is_player_running(index) is False:
            return False
        return "package:" + package in CrackController.get_package_list(index)

    # start player and then start specified app, assuming the player is not running
    @staticmethod
    def launch_player_and_start_app(index: int, package: str = "null") -> str:
        command = 'launchex --index ' + str(index) + ' --packagename ' + package
        return CrackController.console_cmd(command)

    # reboot player and then start specified app, assuming the player is running
    @staticmethod
    def reboot_player_and_start_app(index: int, package: str = "null") -> str:
        command = 'action --index ' + str(index) + ' --key call.reboot --value ' + package
        return CrackController.console_cmd(command)

    # modify the player's location, assuming the player is running
    @staticmethod
    def modify_location(index: int, location: str) -> str:
        command = 'action --index ' + str(index) + ' --key call.locate --value ' + location
        return CrackController.console_cmd(command)

    # shutdown player, assuming the player is running
    @staticmethod
    def quit(index: int) -> str:
        command = 'quit --index ' + str(index)
        return CrackController.console_cmd(command)

    # modify the screen resolution, assuming the player is not running
    @staticmethod
    def set_screen_resolution(index: int, resolution: str) -> str:
        command = 'modify --index %d --resolution ' % index + resolution
        return CrackController.console_cmd(command)

    # tap or touch, assuming the player is running
    @staticmethod
    def touch(index: int, x_y: (int, int)) -> str:
        return CrackController.ld_cmd(index, 'input tap %d %d' % x_y)

    # swipe, assuming the player is running
    @staticmethod
    def swipe(index, coordinate_left_up: (int, int), coordinate_right_down: (int, int), delay: int = 0) -> str:
        x0 = coordinate_left_up[0]
        y0 = coordinate_left_up[1]
        x1 = coordinate_right_down[0]
        y1 = coordinate_right_down[1]
        if delay == 0:
            return CrackController.ld_cmd(index, 'input swipe %d %d %d %d' % (x0, y0, x1, y1))
        else:
            return CrackController.ld_cmd(index, 'input swipe %d %d %d %d %d' % (x0, y0, x1, y1, delay))

    # copy player, assuming the player is not running
    @staticmethod
    def copy(name: str, index: int = 0) -> str:
        command = 'copy --name %s --from %d' % (name, index)
        return CrackController.console_cmd(command)

    # add player, assuming the player is not running
    @staticmethod
    def add(name: str) -> str:
        command = 'add --name %s' % name
        return CrackController.console_cmd(command)

    # set auto rotate, assuming the player is not running
    @staticmethod
    def auto_rotate(index: int, auto_rate: bool = False) -> str:
        rate = 1 if auto_rate else 0
        command = 'modify --index %d --autorotate %d' % (index, rate)
        return CrackController.console_cmd(command)

    # modify player info, assuming the player is not running
    @staticmethod
    def change_device_info(index: int) -> str:
        command = 'modify --index %d --imei auto --imsi' \
                  ' auto --simserial auto --androidid auto --mac auto' % index
        return CrackController.console_cmd(command)

    # modify CPU core number, assuming the player is not running
    @staticmethod
    def change_cpu_count(index: int, number: int) -> str:
        command = 'modify --index %d --cpu %d' % (index, number)
        return CrackController.console_cmd(command)

    # fetch current activity xml, assuming the player is running
    @staticmethod
    def get_cur_activity_xml(index: int) -> str:
        CrackController.ld_cmd(index, 'uiautomator dump /sdcard/Pictures/activity.xml')
        CrackController.random_sleep()
        file = open(CrackController.share_path + 'activity.xml', 'r', encoding='utf-8')
        result = file.read()
        file.close()
        return result

    # fetch current activity, assuming the player is running
    @staticmethod
    def get_activity_name(index: int) -> str:
        text = CrackController.ld_cmd(index, '"dumpsys activity top | grep ACTIVITY"', False)
        text = text.split(' ')
        for index, word in enumerate(text):
            if len(word) == 0:
                continue
            if word == 'ACTIVITY':
                return text[index + 1]
        return ''

    # wait for specified activity, assuming the player is running
    @staticmethod
    def wait_activity(index: int, activity: str, timeout: int) -> bool:
        for i in range(timeout):
            if CrackController.get_activity_name(index) == activity:
                return True
            CrackController.random_sleep()
        return False

    # use ld_cmd to make screen shot and return the array of the picture, assuming the player is running
    @staticmethod
    def screen_shot(index: int, sleep_time_low: float = 0.4, sleep_time_high: float = 0.6) -> list:
        CrackController.ld_cmd(index, 'screencap -p /sdcard/Pictures/' + str(index) + 'apk_scr.png')
        CrackController.random_sleep(sleep_time_low, sleep_time_high)
        screen = cv2.imread(CrackController.share_path + str(index) + 'apk_scr.png')
        return screen

    # intercept picture to small picture and return small picture array
    @staticmethod
    def intercept_rectangle_from_picture(index: int, left_up: (int, int),
                                         right_down: (int, int)) -> list:
        screen = CrackController.screen_shot(index)
        rectangle = screen[left_up[1]:right_down[1], left_up[0]:right_down[0]]
        return rectangle

    # find the matched picture, assuming the player is running
    @staticmethod
    def find_all_pictures(screen_shot: list, template: str, threshold: float = 0.85, debug: bool = False) -> \
            [(int, int, int, int)]:
        locations_to_return = []
        template_picture = CrackController.templates_dict.get(template)
        result = cv2.matchTemplate(screen_shot, template_picture, cv2.TM_CCOEFF_NORMED)
        locations = numpy.where(result >= threshold)
        h, w = template_picture.shape[:-1]
        if debug:
            print(template, 'searching... ')
        for pt in zip(*locations[::-1]):
            x, y = pt[0] + int(w / 2), pt[1] + int(h / 2)
            x, y = int(x), int(y)
            locations_to_return.append((x, y, w, h))
        locations_to_return = sorted(locations_to_return, key=lambda location: location[0] + location[1])
        to_return = []
        if len(locations_to_return) != 0:
            for index in range(len(locations_to_return)):
                if index + 1 == len(locations_to_return):
                    to_return.append(locations_to_return[index])
                elif abs(locations_to_return[index][0] - locations_to_return[
                    index + 1][0]) < 20 and abs(locations_to_return[index][1]
                                                - locations_to_return[index + 1][1]) < 20:
                    continue
                else:
                    to_return.append(locations_to_return[index])
        if debug:
            for x, y, w, h in to_return:
                cv2.circle(screen_shot, (x, y), 5, (0, 0, 255), 2)
                cv2.rectangle(screen_shot, (x - int(w / 2), y - int(h / 2)), (x + int(w / 2), y + int(h / 2)),
                              (0, 0, 0), 2)
                print('found ', template, ' ,at', x, y)
            cv2.imshow('result graph: ', screen_shot)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        if len(to_return) == 0:
            print(template, 'not find')
        return to_return

    # find the matched picture, assuming the player is running
    @staticmethod
    def find_single_picture(screen_shot: list, template: str, threshold: float = 0.85, debug: bool = False) -> \
            ((int, int, int, int), float):
        template_picture = CrackController.templates_dict.get(template)
        result = cv2.matchTemplate(screen_shot, template_picture, cv2.TM_CCOEFF_NORMED)
        minimum_value, maximum_value, minimum_value_location, maximum_value_location = cv2.minMaxLoc(result)
        h, w = template_picture.shape[:-1]
        if debug:
            print(template, 'searching... ')
            print(numpy.max(result))
        if maximum_value >= threshold:
            x, y = maximum_value_location[0] + int(w / 2), maximum_value_location[1] + int(h / 2)
            if debug:
                cv2.circle(screen_shot, (x, y), 5, (0, 0, 255), 3)
                cv2.rectangle(screen_shot, (x - int(w / 2), y - int(h / 2)), (x + int(w / 2), y + int(h / 2)),
                              (0, 0, 0), 3)
                print('found ', template, ' ,at', x, y)
            x, y = int(x), int(y)
            if debug:
                cv2.imshow('result graph: ', screen_shot)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                print(x, y, w, h)
            return (x, y, w, h), maximum_value
        else:
            if debug:
                cv2.imshow("don't find: " + template, screen_shot)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            return None, -1

    # wait for specified picture, assuming the player is running
    @staticmethod
    def wait_picture(index: int, timeout: int, template: str, threshold: float = 0.85, sleep_time_low: float = 0.4,
                     sleep_time_high: float = 0.6) -> (bool, (int, int, int, int)):

        count = 0
        while count < timeout:
            screen = CrackController.screen_shot(index, sleep_time_low, sleep_time_high)
            print(str(index), ' is waiting... ', template)
            location, _ = CrackController.find_single_picture(screen, template, threshold)
            if location is None:
                CrackController.random_sleep()
                count += 1
                continue
            print(str(index), ' waiting and find... ', template)
            return True, location
        print(str(index), " waiting and DON'T find... ", template)
        return False, None

    # check the current screen for the pattern picture list, if there exists, then return it.
    # if there exist many pattern pictures then return the first one, assuming the player is running
    @staticmethod
    def check_picture_list(index: int, templates: list, threshold: float = 0.85, screen: list = None,
                           sleep_time_low: float = 0.4,
                           sleep_time_high: float = 0.6) -> (bool, (int, int, int, int), str):
        if screen is None:
            screen = CrackController.screen_shot(index, sleep_time_low, sleep_time_high)
        check_list = []
        for template_index, template in enumerate(templates):
            print(str(index), ' is checking... ', template)
            location, max_value = CrackController.find_single_picture(screen, template, threshold)
            if max_value != -1:
                print(str(index), ' has a backup template ', template)
                check_list.append((max_value, (location, template)))
        if len(check_list) >= 1:
            best_template = sorted(check_list, key=lambda one_solution: one_solution[0], reverse=True)[0]
            print(str(index), ' gets a best template ', best_template)
            return True, best_template[1][0], best_template[1][1]
        else:
            print(str(index), " is checking and DON'T find any template... ")
            return False, None, None

    # fetch the number (str) from the picture by using the api, must be png format
    @staticmethod
    def fetch_number_from_picture(picture: list) -> str:
        url = "https://aip.baidubce.com/rest/2.0/ocr/v1/numbers?access_token=" + CrackController.api
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'image': base64.b64encode(cv2.imencode('.png', picture)[1]).decode(),
        }
        response = requests.post(url, data=data, headers=headers)
        result = json.loads(response.text)
        try:
            return result["words_result"][0]['words']
        except IndexError:
            return ''

    # fetch the string (str) from the picture by using the api, must be png format
    @staticmethod
    def fetch_string_from_picture(picture: list) -> str:
        url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=" + CrackController.api
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'image': base64.b64encode(cv2.imencode('.png', picture)[1]).decode(),
        }
        response = requests.post(url, data=data, headers=headers)
        result = json.loads(response.text)
        try:
            return result["words_result"]
        except IndexError:
            return ''

    # given a rectangle and click in it randomly, assuming the player is running
    @staticmethod
    def random_click(index: int, left_up: (int, int) = GameDetail.left_up_position,
                     right_down: (int, int) = GameDetail.right_down_position) -> str:
        x = random.uniform(left_up[0], right_down[0])
        y = random.uniform(left_up[1], right_down[1])
        return CrackController.touch(index, (x, y))

    # random sleep to avoid detection
    @staticmethod
    def random_sleep(start: float = 0.8, end: float = 1.2) -> None:
        sec = random.uniform(start, end)
        time.sleep(sec)

    # use windows api to speak out some words
    @staticmethod
    def speak(word: str) -> None:
        CrackController.speak_out.Speak(word)

    # click different location to avoid game detection
    @staticmethod
    def cheat(location: (int, int, int, int)) -> (int, int):
        x, y = location[0], location[1]
        r_w, r_h = int(location[2] / 4), int(location[3] / 4)
        r_x, r_y = random.randint(-r_w, r_w), random.randint(-r_h, r_h)
        x, y = x + r_x, y + r_y
        return x, y
