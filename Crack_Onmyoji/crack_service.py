import random
import time
from threading import Thread
from Crack_Onmyoji.crack_controller import CrackController
from Crack_Onmyoji.game_detail import GameDetail


class CrackService(Thread):

    def __init__(self, index: int, task_list: list = None, onmyoji: GameDetail = None) -> None:
        super().__init__()
        self.index = index
        self.start_time = time.ctime()
        self.task_list: list = task_list
        self.onmyoji = onmyoji

    def run(self) -> None:
        while len(self.task_list) != 0:
            current_task = self.task_list.pop(0)
            if len(current_task) == 1:
                accomplish = eval("self." + current_task[0])()
            else:
                accomplish = eval("self." + current_task[0])(*current_task[1:])
            if current_task[0] in ["accept_invite", "mitama_or_awake_invite"]:
                if not accomplish:
                    self.task_list.insert(0, current_task)
                    self.start_onmyoji()
                    CrackController.random_sleep()
                    continue

    def start_onmyoji(self) -> None:
        if CrackController.is_player_running(self.index):
            CrackController.reboot_player_and_start_app(self.index, GameDetail.game_package_name)
        else:
            CrackController.launch_player_and_start_app(self.index, GameDetail.game_package_name)
        CrackController.random_sleep(10, 15)
        self.any_pages_back_to_home_page()

    def is_home_page_or_not(self) -> bool:
        return CrackController.wait_picture(self.index, 1,
                                            CrackController.share_path + "bonus.png")[0] \
               and not CrackController.wait_picture(self.index, 1,
                                                    CrackController.share_path + "yard_close.png")[0]

    def any_pages_back_to_home_page(self) -> None:
        while True:
            if self.is_home_page_or_not():
                break
            else:
                exist, page_location, _ = \
                    CrackController.check_picture_list(self.index, GameDetail.close)
                if exist:
                    CrackController.touch(self.index, CrackController.cheat(page_location))
                    CrackController.random_sleep(1.2, 1.8)
                else:
                    print("not found ...")

    def mitama_or_awake_invite(self, mode: str, addition_arg: str, column_name_list: [(str, str)],
                               count: int = 10000) -> bool:
        self._invite_friend_to_team(mode, addition_arg, column_name_list)
        CrackController.random_sleep(1.5, 3)
        accomplish = self.send_invite(column_name_list, count)
        if accomplish:
            self.leave_team()
            self.any_pages_back_to_home_page()
        return accomplish

    def send_invite(self, column_name_list: [(str, str)] = None, count: int = 10000) -> bool:
        auto_invite_flag = False
        battle_count = 0
        while True:
            exist, location, template = CrackController.check_picture_list(self.index, GameDetail.victory)
            if exist:
                if template == 'Onmyoji_images\\game_failure_victory.png':
                    return False
                if template == 'Onmyoji_images\\6_victory.png':
                    if not auto_invite_flag:
                        exist, location = CrackController.wait_picture(
                            self.index, 1,
                            CrackController.share_path + 'invite_in_default.png')
                        if exist:
                            CrackController.touch(self.index, CrackController.cheat(location))
                            exist, location = CrackController.wait_picture(
                                self.index, 1,
                                CrackController.share_path + 'invite_in_default_confirm.png')
                            if exist:
                                CrackController.touch(self.index, CrackController.cheat(location))
                                auto_invite_flag = True
                    else:
                        CrackController.touch(self.index, CrackController.cheat(location))
                if template == 'Onmyoji_images\\battle_victory.png':
                    if battle_count > count:
                        return True
                    CrackController.random_sleep(2, 3)
                    if len(column_name_list) == 2:
                        CrackController.random_sleep(3, 5)
                    if self._inviter_ready_to_begin_team_battle(column_name_list):
                        battle_count += 1
                        print('--------------invite count-------------------------------------', battle_count)
                    else:
                        self._invite(column_name_list)
                CrackController.touch(self.index, CrackController.cheat(location))

    def accept_invite(self, inviter: str, timer: int = 60 * 60 * 6) -> bool:
        accept_time = time.time()
        while True:
            if time.time() - accept_time > timer:
                return True
            screen = CrackController.screen_shot(self.index)
            _, is_team_leader = CrackController.find_single_picture(screen, CrackController.share_path +
                                                                    'battle_victory.png')
            if is_team_leader > 0:
                self.leave_team()
                continue
            inviter_location, exist = CrackController.find_single_picture(screen,
                                                                          CrackController.share_path + "invite\\check_"
                                                                          + inviter + ".png")
            if exist > 0:
                all_locations = CrackController.find_all_pictures(screen,
                                                                  CrackController.share_path + "invite2_team.png")
                if len(all_locations) > 0:
                    CrackController.touch(self.index, CrackController.cheat(all_locations[0]))
                else:
                    all_locations = CrackController.find_all_pictures(screen,
                                                                      CrackController.share_path + "invite_team.png")
                    to_click = [location for location in all_locations if
                                inviter_location[1] in range(location[1], location[1] + 50)]
                    if len(to_click) > 0:
                        CrackController.touch(self.index, CrackController.cheat(all_locations[0]))
            exist, location, template = CrackController.check_picture_list(self.index, GameDetail.victory,
                                                                           screen=screen)
            if exist:
                if template == 'Onmyoji_images\\game_failure_victory.png':
                    return False
                CrackController.touch(self.index, CrackController.cheat(location))

    def _invite_friend_to_team(self, mode: str, addition_arg: str, column_name_list: [(str, str)]):
        self.detour_to_explore_page()
        if mode == 'mitama':
            exist, location = CrackController.wait_picture(self.index, 2,
                                                           CrackController.share_path + 'mitama_icon.png')
            if exist:
                CrackController.touch(self.index, CrackController.cheat(location))
                CrackController.random_sleep(1.5, 3)
                exist, location = CrackController.wait_picture(self.index, 2,
                                                               CrackController.share_path +
                                                               'dragon_mitama.png')
                if exist:
                    CrackController.touch(self.index, CrackController.cheat(location))
                CrackController.random_sleep(1.5, 3)
                exist, location = CrackController.wait_picture(self.index, 2,
                                                               CrackController.share_path +
                                                               'mitama_level_' + addition_arg + '.png')
                if exist:
                    CrackController.touch(self.index, CrackController.cheat(location))
                CrackController.random_sleep(1.5, 3)
        if mode == 'awake':
            exist, location = CrackController.wait_picture(self.index, 1,
                                                           CrackController.share_path + 'awake_icon.png')
            if exist:
                CrackController.touch(self.index, CrackController.cheat(location))
                CrackController.random_sleep(1.5, 3)
                exist, location = CrackController.wait_picture(self.index, 1,
                                                               CrackController.share_path + addition_arg +
                                                               '_awake.png')
                if exist:
                    CrackController.touch(self.index, CrackController.cheat(location))
                CrackController.random_sleep(1.5, 3)
        exist, location = CrackController.wait_picture(self.index, 1,
                                                       CrackController.share_path + 'invite\\make_up_team.png')
        if exist:
            CrackController.touch(self.index, CrackController.cheat(location))
        CrackController.random_sleep(1.5, 3)
        exist, location = CrackController.wait_picture(self.index, 1,
                                                       CrackController.share_path + 'invite\\create_team_bar.png')
        if exist:
            CrackController.touch(self.index, CrackController.cheat(location))
        CrackController.random_sleep(1.5, 3)
        exist, location = CrackController.wait_picture(self.index, 1,
                                                       CrackController.share_path + 'invite\\not_open.png')
        if exist:
            CrackController.touch(self.index, CrackController.cheat(location))
        CrackController.random_sleep(1.5, 3)
        exist, location = CrackController.wait_picture(self.index, 1,
                                                       CrackController.share_path + 'invite\\create_bar.png')
        if exist:
            CrackController.touch(self.index, CrackController.cheat(location))
        CrackController.random_sleep(1.5, 3)
        self._invite(column_name_list)

    def _invite(self, column_name_list: [(str, str)]):
        while True:
            for column_name in column_name_list:
                exist, location = CrackController.wait_picture(self.index, 1,
                                                               CrackController.share_path + 'invite\\invite_icon.png')
                if exist:
                    CrackController.touch(self.index, CrackController.cheat(location))
                CrackController.random_sleep(1.5, 3)
                exist, location = CrackController.wait_picture(self.index, 1,
                                                               CrackController.share_path + 'invite\\' + column_name[
                                                                   0] + '_column.png')
                if exist:
                    CrackController.touch(self.index, CrackController.cheat(location))
                CrackController.random_sleep(1.5, 3)
                exist, location = CrackController.wait_picture(self.index, 1,
                                                               CrackController.share_path + 'invite\\name_' +
                                                               column_name[
                                                                   1] + '.png')
                if exist:
                    CrackController.touch(self.index, CrackController.cheat(location))
                CrackController.random_sleep(1.5, 3)
                exist, location = CrackController.wait_picture(self.index, 1,
                                                               CrackController.share_path + 'invite\\invite_bar.png')
                if exist:
                    CrackController.touch(self.index, CrackController.cheat(location))
                CrackController.random_sleep(12, 15)
            if self._inviter_ready_to_begin_team_battle(column_name_list):
                break

    def _inviter_ready_to_begin_team_battle(self, column_name_list: [(str, str)]):
        screen = CrackController.screen_shot(self.index)
        invite_icons = CrackController.find_all_pictures(screen,
                                                         CrackController.share_path + 'invite\\invite_icon.png',
                                                         0.99)
        print(invite_icons)
        if len(invite_icons) + len(column_name_list) == 2:
            return True
        else:
            CrackController.random_sleep(2, 3)
            screen = CrackController.screen_shot(self.index)
            invite_icons = CrackController.find_all_pictures(screen,
                                                             CrackController.share_path + 'invite\\invite_icon.png',
                                                             0.99)
            return len(invite_icons) + len(column_name_list) == 2

    def personal_break_through(self) -> None:
        self.detour_to_explore_page()
        exist, location = CrackController.wait_picture(self.index, 2,
                                                       CrackController.share_path + 'breakthrough_icon.png')
        if exist:
            CrackController.touch(self.index, CrackController.cheat(location))
        CrackController.random_sleep(1.5, 3)
        refresh = False
        ticket = CrackController.intercept_rectangle_from_picture(self.index,
                                                                  GameDetail.break_through_ticket_left_up,
                                                                  GameDetail.break_through_ticket_right_down)
        result = CrackController.fetch_number_from_picture(ticket)
        result = int(result[:-2])
        ticket = result
        while True:
            print('have ', ticket, 'tickets')
            if ticket <= 2:
                self.any_pages_back_to_home_page()
                break
            exist, location, template = CrackController.check_picture_list(self.index, GameDetail.victory)
            if exist:
                if template in ['Onmyoji_images\\2_victory.png', 'Onmyoji_images\\3_victory.png']:
                    CrackController.random_sleep(3, 4)
                    exist, _ = CrackController.wait_picture(self.index, 1,
                                                            CrackController.share_path
                                                            + 'break_through_money_flag.png')
                    if exist:
                        print("already beat 3 players")
                        ticket -= 3
                        refresh = True
                        CrackController.random_sleep(3, 4)
                CrackController.touch(self.index, CrackController.cheat(location))
                CrackController.random_sleep()
            screen = CrackController.screen_shot(self.index)
            click_locations = CrackController.find_all_pictures(screen,
                                                                CrackController.share_path + 'zero_star.png', 0.95)
            click_position = None
            if len(click_locations) > 0:
                exist, location, template = CrackController.check_picture_list(self.index, GameDetail.victory)
                if exist:
                    if template in ['Onmyoji_images\\2_victory.png', 'Onmyoji_images\\3_victory.png']:
                        CrackController.random_sleep(3, 4)
                        exist, _ = CrackController.wait_picture(self.index, 1,
                                                                CrackController.share_path
                                                                + 'break_through_money_flag.png')
                        if exist:
                            print("already beat 3 players")
                            ticket -= 3
                            refresh = True
                            CrackController.random_sleep(3, 4)
                    CrackController.touch(self.index, CrackController.cheat(location))
                    CrackController.random_sleep()
                screen = CrackController.screen_shot(self.index)
                locations = CrackController.find_all_pictures(
                    screen,
                    CrackController.share_path + 'broken2_flag.png', 0.7)
                print('beat' + str(len(locations)))
                if len(locations) >= 3:
                    refresh = True
                if not refresh:
                    screen = CrackController.screen_shot(self.index)
                    remove_locations = CrackController.find_all_pictures(screen,
                                                                         CrackController.share_path
                                                                         + 'break_through_fail_flag.png')
                    if len(remove_locations) > 0:
                        to_remove = []
                        for click in click_locations:
                            for remove in remove_locations:
                                if 130 >= remove[0] - click[0] >= 70 and 80 >= click[1] - remove[1] >= 40:
                                    to_remove.append(click)
                        for remove in to_remove:
                            click_locations.remove(remove)
                    print(click_locations)
                    if len(click_locations) > 0:
                        click_position = click_locations[random.randint(0, len(click_locations) - 1)]
                    else:
                        refresh = True
                if not refresh:
                    CrackController.touch(self.index, CrackController.cheat(click_position))
                    CrackController.random_sleep()
                    exist, location = CrackController.wait_picture(self.index, 10,
                                                                   CrackController.share_path + 'attack_star.png')
                    if exist:
                        CrackController.touch(self.index, CrackController.cheat(location))
                        CrackController.random_sleep(10, 12)
            if refresh:
                exist, location = CrackController.wait_picture(self.index, 1,
                                                               CrackController.share_path +
                                                               'breakthrough_refresh.png')
                if exist:
                    CrackController.touch(self.index, CrackController.cheat(location))
                    CrackController.random_sleep()
                    exist, location = CrackController.wait_picture(self.index, 10,
                                                                   CrackController.share_path +
                                                                   'breakthrough_refresh_confirm.png')
                    if exist:
                        CrackController.touch(self.index, CrackController.cheat(location))
                        CrackController.random_sleep(3, 4)
                        screen = CrackController.screen_shot(self.index)
                        locations = CrackController.find_all_pictures(screen, CrackController.share_path +
                                                                      'zero_star.png', 0.95)
                        print('zero star number: ', len(locations))
                        if len(locations) >= 3:
                            refresh = False
                else:
                    sleep_time = CrackController.intercept_rectangle_from_picture(
                        self.index,
                        GameDetail.break_through_sleep_left_up,
                        GameDetail.break_through_sleep_right_down)
                    result = CrackController.fetch_number_from_picture(sleep_time)
                    if len(result) >= 4:
                        minute = int(result[:2])
                        second = int(result[2:])
                    else:
                        minute = 0
                        second = 0
                    sleep_time = 60 * minute + second
                    print('need to sleep... ', sleep_time)
                    CrackController.random_sleep(sleep_time, sleep_time + 10)

    def detour_to_explore_page(self):
        self.any_pages_back_to_home_page()
        CrackController.random_sleep()
        CrackController.random_click(self.index, GameDetail.home_page_explore_left_up,
                                     GameDetail.home_page_explore_right_down)
        CrackController.random_sleep(1.5, 3)

    def group_break_through(self):
        self.detour_to_explore_page()
        exist, location = CrackController.wait_picture(self.index, 2,
                                                       CrackController.share_path + 'breakthrough_icon.png')
        if exist:
            CrackController.touch(self.index, CrackController.cheat(location))
        CrackController.random_sleep(1.5, 3)
        exist, location = CrackController.wait_picture(self.index, 2,
                                                       CrackController.share_path +
                                                       'group_break_through_icon.png')
        if exist:
            CrackController.touch(self.index, CrackController.cheat(location))
        CrackController.random_sleep(1.5, 3)
        scroll = False
        not_exist_times = 0
        while True:
            exist, location, template = CrackController.check_picture_list(self.index, GameDetail.victory)
            if exist:
                CrackController.touch(self.index, CrackController.cheat(location))
            exist, location = CrackController.wait_picture(self.index, 1, CrackController.share_path +
                                                           'group_break_through_flag.png')
            if exist:
                exist, location = CrackController.wait_picture(self.index, 1,
                                                               CrackController.share_path +
                                                               'group_break_through_target.png')
                if exist:
                    not_exist_times = 0
                    CrackController.touch(self.index, CrackController.cheat(location))
                    CrackController.random_sleep()
                    exist, _ = CrackController.wait_picture(self.index, 1, CrackController.share_path +
                                                            'group_tickets_not_enough.png')
                    if exist:
                        break
                    exist, location = CrackController.wait_picture(self.index, 1,
                                                                   CrackController.share_path +
                                                                   'attack_star.png')
                    if exist:
                        CrackController.touch(self.index, CrackController.cheat(location))
                else:
                    scroll = True
                    not_exist_times += 1
            if scroll:
                exist, location = CrackController.wait_picture(self.index, 2,
                                                               CrackController.share_path +
                                                               'group_break_through_scroll.png')
                if exist:
                    flag = random.uniform(self.index, 1) > 0.75
                    CrackController.swipe(0, location[:2],
                                          (location[0], location[1] - 120 if flag else location[1] + 120),
                                          1800)
                    scroll = False
            if not_exist_times >= 5:
                break
        self.any_pages_back_to_home_page()

    def solo_mode(self, mode: str, addition_arg: str, count: int = 10000) -> None:
        self.detour_to_explore_page()
        if mode == 'mitama':
            exist, location = CrackController.wait_picture(self.index, 2,
                                                           CrackController.share_path + 'mitama_icon.png')
            if exist:
                CrackController.touch(self.index, CrackController.cheat(location))
                CrackController.random_sleep(1.5, 3)
                exist, location = CrackController.wait_picture(self.index, 2,
                                                               CrackController.share_path + addition_arg +
                                                               '_mitama.png')
                if exist:
                    CrackController.touch(self.index, CrackController.cheat(location))
                CrackController.random_sleep(1.5, 3)
        if mode == 'awake':
            exist, location = CrackController.wait_picture(self.index, 2,
                                                           CrackController.share_path + 'awake_icon.png')
            if exist:
                CrackController.touch(self.index, CrackController.cheat(location))
                CrackController.random_sleep(1.5, 3)
                exist, location = CrackController.wait_picture(self.index, 2,
                                                               CrackController.share_path + addition_arg +
                                                               '_awake.png')
                if exist:
                    CrackController.touch(self.index, CrackController.cheat(location))
                CrackController.random_sleep(1.5, 3)
        if mode == 'imperial_spirit':
            exist, location = CrackController.wait_picture(self.index, 2,
                                                           CrackController.share_path + 'imperial_spirit_icon.png')
            if exist:
                CrackController.touch(self.index, CrackController.cheat(location))
                CrackController.random_sleep(1.5, 3)
                exist, location = CrackController.wait_picture(self.index, 2,
                                                               CrackController.share_path + addition_arg +
                                                               '_imperial_spirit.png')
                if exist:
                    CrackController.touch(self.index, CrackController.cheat(location))
                CrackController.random_sleep(1.5, 3)
        times = 0
        while True:
            if times > count:
                break
            exist, location, template = CrackController.check_picture_list(self.index, GameDetail.victory)
            if exist:
                CrackController.touch(self.index, CrackController.cheat(location))
                if template == 'Onmyoji_images\\challenge_victory.png':
                    times += 1
                    if mode == 'mitama':
                        CrackController.random_sleep(20, 30)
                    if mode == 'awake':
                        CrackController.random_sleep(15, 20)
                    if mode == 'imperial_spirit':
                        CrackController.random_sleep(55, 65)

    def chapter_solo(self) -> None:

        height = random.randint(*GameDetail.chapter_drag_height)
        left = random.randint(*GameDetail.chapter_drag_left)
        right = random.randint(*GameDetail.chapter_drag_right)
        drag_time = random.randint(1000, 2000)

        def drag_to_left():
            CrackController.swipe(self.index, (left, height), (right, height), drag_time)

        def drag_to_right():
            CrackController.swipe(self.index, (right, height), (left, height), drag_time)

        self.any_pages_back_to_home_page()
        CrackController.random_click(self.index, GameDetail.home_page_explore_left_up,
                                     GameDetail.home_page_explore_right_down)
        CrackController.random_sleep(1.5, 3)
        exist, location = CrackController.wait_picture(self.index, 2,
                                                       CrackController.share_path + 'chapter_28_flag.png')
        if exist:
            CrackController.touch(self.index, CrackController.cheat(location))
        CrackController.random_sleep(1.5, 3)
        exist, location = CrackController.wait_picture(self.index, 2,
                                                       CrackController.share_path + 'explore_start_icon.png')
        if exist:
            CrackController.touch(self.index, CrackController.cheat(location))
        CrackController.random_sleep(1.5, 3)
        exist, _ = CrackController.wait_picture(self.index, 1,
                                                CrackController.share_path + 'fix_team_flag.png')
        if exist:
            CrackController.random_sleep()
            while True:
                exist, location, _ = CrackController.check_picture_list(self.index, GameDetail.chapter_battle)
                if exist:
                    CrackController.touch(self.index, location[:2])
                    CrackController.random_sleep(3.5, 4.5)
                    self._in_chapter_battle()
                    CrackController.random_sleep()
                else:
                    if random.uniform(0, 1) > 0.5:
                        drag_to_right()
                    else:
                        drag_to_left()
                exist, _, template = CrackController.check_picture_list(self.index, GameDetail.out_of_chapter)
                if exist:
                    if template == 'Onmyoji_images\\gift_chapter_flag.png':
                        exist, location = CrackController.wait_picture(self.index, 1,
                                                                       CrackController.share_path +
                                                                       'backward3_close.png')
                        if exist:
                            CrackController.touch(self.index, CrackController.cheat(location))
                        CrackController.random_sleep()
                        exist, location = CrackController.wait_picture(self.index, 1,
                                                                       CrackController.share_path +
                                                                       'backward3_confirm_close.png')
                        if exist:
                            CrackController.touch(self.index, CrackController.cheat(location))
                    break
            self.any_pages_back_to_home_page()

    def _in_chapter_battle(self) -> None:
        screen = CrackController.screen_shot(self.index)
        locations = CrackController.find_all_pictures(screen, CrackController.share_path + 'max_level_flag.png')
        max_level_flag = False
        if len(locations) != 0:
            for x, y, w, h in locations:
                if x in range(*GameDetail.chapter_attendant_position_3_stand_width) and y in range(
                        *GameDetail.chapter_attendant_position_3_stand_height):
                    max_level_flag = True
            if max_level_flag:
                CrackController.random_click(self.index, GameDetail.chapter_attendant_click_left_up,
                                             GameDetail.chapter_attendant_click_right_down)
                CrackController.random_click(self.index, GameDetail.chapter_attendant_click_left_up,
                                             GameDetail.chapter_attendant_click_right_down)
                CrackController.random_sleep(1.5, 3)
                exist, location, template = CrackController.check_picture_list(self.index, GameDetail.champion_class)
                if exist:
                    if template != 'Onmyoji_images\\N_class.png':
                        CrackController.touch(self.index, CrackController.cheat(location))
                        CrackController.random_sleep()
                        exist, location = CrackController.wait_picture(self.index, 1,
                                                                       CrackController.share_path + 'N_class.png')
                        if exist:
                            CrackController.touch(self.index, CrackController.cheat(location))
                            CrackController.random_sleep()
                    while True:
                        exist, location = CrackController.wait_picture(self.index, 1,
                                                                       CrackController.share_path +
                                                                       'level_one_flag.png')
                        if exist:
                            height = random.randint(*GameDetail.chapter_attendant_position_3_drag_height)
                            width = random.randint(*GameDetail.chapter_attendant_position_3_drag_width)
                            drag_time = random.randint(1000, 2000)
                            CrackController.swipe(self.index, location, (width, height), drag_time)
                            CrackController.random_sleep()
                            break
                        else:
                            height = random.randint(*GameDetail.chapter_backup_drag_height)
                            left = random.randint(*GameDetail.chapter_backup_drag_left)
                            right = random.randint(*GameDetail.chapter_backup_drag_right)
                            drag_time = random.randint(1000, 2000)
                            CrackController.swipe(self.index, (right, height), (left, height), drag_time)
                            CrackController.random_sleep()
        CrackController.random_sleep(2, 3)
        exist, location = CrackController.wait_picture(self.index, 1,
                                                       CrackController.share_path + 'prepare_flag.png')
        if exist:
            CrackController.touch(self.index, CrackController.cheat(location))
        CrackController.random_sleep()
        while True:
            exist, location, _ = CrackController.check_picture_list(self.index, GameDetail.victory)
            if exist:
                CrackController.touch(self.index, CrackController.cheat(location))
            exist, _, _ = CrackController.check_picture_list(self.index,
                                                             [CrackController.share_path +
                                                              'fix_team_flag.png',
                                                              CrackController.share_path +
                                                              'out2_of_chapter_flag.png'])
            if exist:
                break

    def open_close_buff(self, buff_type: str, buff_option: bool) -> None:
        self.any_pages_back_to_home_page()
        exist, location = CrackController.wait_picture(self.index, 1,
                                                       CrackController.share_path + "bonus.png")
        if exist:
            CrackController.touch(self.index, CrackController.cheat(location))
        CrackController.random_sleep()
        if buff_type == 'mitama':
            mitama_flag = self._buff_check_in_location(GameDetail.mitama_buff_check_left_up,
                                                       GameDetail.mitama_buff_check_right_down)
            if mitama_flag ^ buff_option:
                CrackController.random_click(self.index, GameDetail.mitama_buff_left_up,
                                             GameDetail.mitama_buff_right_down)
        if buff_type == 'awake':
            awake_flag = self._buff_check_in_location(GameDetail.awake_buff_check_left_up,
                                                      GameDetail.awake_buff_check_right_down)
            if awake_flag ^ buff_option:
                CrackController.random_click(self.index, GameDetail.awake_buff_left_up,
                                             GameDetail.awake_buff_right_down)
        CrackController.random_sleep()
        exist, location = CrackController.wait_picture(self.index, 1,
                                                       CrackController.share_path + "bonus.png")
        if exist:
            CrackController.touch(self.index, CrackController.cheat(location))

    def _buff_check_in_location(self, left_up: (int, int), right_down: (int, int)) -> bool:
        exist, location = CrackController.wait_picture(self.index, 1,
                                                       CrackController.share_path + "buff_check.png")
        if exist:
            return location[0] in range(left_up[0], right_down[0]) and location[1] in range(left_up[1], right_down[1])
        else:
            return False

    def leave_team(self) -> None:
        while True:
            exist, location = CrackController.wait_picture(self.index, 3, CrackController.share_path +
                                                           "team_leave.png")
            if not exist:
                break
            else:
                CrackController.touch(self.index, CrackController.cheat(location))
                CrackController.random_sleep()
                _, location = CrackController.wait_picture(self.index, 3,
                                                           CrackController.share_path +
                                                           "team_confirm_leave.png")
                CrackController.touch(self.index, CrackController.cheat(location))
                CrackController.random_sleep()
        self.any_pages_back_to_home_page()

    def hundred_ghosts(self, count: int) -> None:
        self.any_pages_back_to_home_page()
        exist, location = CrackController.wait_picture(self.index, 1,
                                                       CrackController.share_path + "to_yard_icon.png")
        if exist:
            CrackController.touch(self.index, CrackController.cheat(location))
        CrackController.random_sleep(2, 3)
        exist, location = CrackController.wait_picture(self.index, 1,
                                                       CrackController.share_path + "hundred_ghosts_flag.png", 0.7)
        if exist:
            CrackController.touch(self.index, CrackController.cheat(location))
        CrackController.random_sleep()
        ticket = CrackController.intercept_rectangle_from_picture(self.index,
                                                                  GameDetail.hundred_ghosts_ticket_left_up,
                                                                  GameDetail.hundred_ghosts_ticket_right_down)
        result = CrackController.fetch_number_from_picture(ticket)
        result = int(result)
        ticket = result
        times = 0
        while ticket >= 0 and times < count:
            print('have ', ticket, ' tickets')
            exist, location, template = CrackController.check_picture_list(self.index, GameDetail.hundred_ghosts)
            if exist:
                if template == 'Onmyoji_images\\enter_hundred_ghosts.png':
                    CrackController.touch(self.index, CrackController.cheat(location))
                    print(self.index, ' begin ', times, ' hundred ghosts')
                elif template == 'Onmyoji_images\\begin_hundred_ghosts.png':
                    choose_pool = [(GameDetail.hundred_ghosts_choose_king_first_left_up,
                                    GameDetail.hundred_ghosts_choose_king_first_right_down),
                                   (GameDetail.hundred_ghosts_choose_king_second_left_up,
                                    GameDetail.hundred_ghosts_choose_king_second_right_down),
                                   (GameDetail.hundred_ghosts_choose_king_third_left_up,
                                    GameDetail.hundred_ghosts_choose_king_third_right_down)]
                    for _ in range(1):
                        random_king = random.randint(0, 2)
                        king_locations = choose_pool[random_king]
                        CrackController.random_click(self.index, *king_locations)
                        CrackController.random_sleep()
                    CrackController.random_sleep(1.8, 3)
                    CrackController.touch(self.index, CrackController.cheat(location))
                    CrackController.random_sleep(2, 3)
                    exist, location = CrackController.wait_picture(self.index, 1,
                                                                   CrackController.share_path
                                                                   + 'five_ghosts.png')
                    if exist:
                        ticket -= 1
                        times += 1
                        height = random.randint(*GameDetail.hundred_ghosts_drag_height)
                        width = random.randint(*GameDetail.hundred_ghosts_drag_width)
                        drag_time = random.randint(1000, 2000)
                        CrackController.swipe(self.index, location,
                                              (width, height), drag_time)
                        CrackController.random_sleep(0.4, 0.6)
                    else:
                        break
                    low_high = GameDetail.hundred_ghosts_throw_height
                    throw_pool = [((i * 180, low_high[0]), ((i + 1) * 180, low_high[1])) for i in range(1, 5)]
                    begin_time = time.time()
                    while True:
                        current_time = time.time()
                        if current_time - begin_time >= 40:
                            CrackController.random_sleep()
                            exist, _, _ = CrackController.check_picture_list(self.index, GameDetail.hundred_ghosts)
                            if exist:
                                break
                        CrackController.random_sleep(0.4, 0.8)
                        random_area = random.randint(0, 3)
                        area_locations = throw_pool[random_area]
                        on_fire = random.uniform(0, 1) >= 0.8
                        if on_fire:
                            for i in range(3):
                                print('on fire ', i)
                                CrackController.random_click(self.index, *area_locations)
                                CrackController.random_sleep(0.4, 0.6)
                        CrackController.random_click(self.index, *area_locations)
                else:
                    CrackController.touch(self.index, CrackController.cheat(location))
        CrackController.random_sleep()
        self.any_pages_back_to_home_page()
