import math
import random
import time
from threading import Thread
from Crack_Onmyoji.crack_controller import CrackController
from Crack_Onmyoji.game_detail import GameDetail
from collections import defaultdict


class CrackService(Thread):
    breakthrough_flag = False
    current_mode = None
    status_dict = {0: True, 1: True, 2: True, 3: True}
    dont_want_to_breakthrough_list = [1, 2, 3]

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
            # CrackController.reboot_player_and_start_app(self.index, GameDetail.game_package_name)
            CrackController.stop_app(self.index, GameDetail.game_package_name)
            CrackController.random_sleep()
            CrackController.invoke_app(self.index, GameDetail.game_package_name)
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
                               count: int = 10000, change_champion: bool = False, is_leader: bool = False) -> bool:
        count_to_breakthrough = 120
        for i in range(math.ceil(count / count_to_breakthrough)):
            while True:
                all_ready = True
                for _, value in CrackService.status_dict.items():
                    if not value:
                        all_ready = False
                        CrackController.random_sleep(10, 15)
                        break
                if all_ready:
                    break
            CrackService.current_mode = mode
            if not change_champion:
                self.open_close_buff(mode, True)
            CrackController.random_sleep(2, 3)
            self._invite_friend_to_team(mode, addition_arg, column_name_list)
            CrackController.random_sleep(1.5, 3)
            accomplish = self.send_invite(column_name_list,
                                          count_to_breakthrough if count_to_breakthrough < count else count,
                                          change_champion, is_leader)
            if accomplish:
                CrackService.breakthrough_flag = True
                self.leave_team()
                self.any_pages_back_to_home_page()
                self.open_close_buff(mode, False)
                if self.index not in CrackService.dont_want_to_breakthrough_list:
                    CrackService.current_mode = None
                    self.personal_break_through()
                else:
                    CrackService.current_mode = None
                    CrackController.random_sleep(20, 30)
                CrackService.breakthrough_flag = False
                CrackController.random_sleep()
            else:
                return False
        self.open_close_buff(mode, False)
        return True

    def send_invite(self, column_name_list: [(str, str)] = None, count: int = 10000, change_champion: bool = False,
                    is_leader: bool = False) -> bool:
        battle_count = 0
        auto_send_invite = False
        failure_count = 0
        while True:
            if failure_count >= 8:
                return True
            exist, location, template = CrackController.check_picture_list(self.index, GameDetail.victory)
            if exist:
                if template == 'Onmyoji_images\\game_failure_victory.png':
                    return False
                elif template == 'Onmyoji_images\\fail_victory.png':
                    CrackController.random_click(self.index, CrackController.cheat(location))
                    CrackController.random_sleep()
                    exist, location = CrackController.wait_picture(self.index, 1,
                                                                   CrackController.share_path + "6_victory.png")
                    if exist:
                        auto_send_invite = False
                        failure_count += 1
                        CrackController.touch(self.index, CrackController.cheat(location))
                elif template == 'Onmyoji_images\\6_victory.png':
                    if change_champion:
                        exist, location = CrackController.wait_picture(
                            self.index, 1,
                            CrackController.share_path + 'invite_in_default.png')
                        if exist:
                            exist, location = CrackController.wait_picture(
                                self.index, 1,
                                CrackController.share_path + 'invite_in_default_confirm.png')
                            if exist:
                                CrackController.touch(self.index, CrackController.cheat(location))
                    else:
                        if not auto_send_invite:
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
                                    auto_send_invite = True
                        else:
                            failure_count += 1
                            auto_send_invite = False
                            CrackController.touch(self.index, CrackController.cheat(location))
                elif template == 'Onmyoji_images\\battle_victory.png':
                    if battle_count >= count:
                        return True
                    begin = False
                    for _ in range(15):
                        begin = self._inviter_ready_to_begin_team_battle(column_name_list)
                        if begin:
                            break
                        else:
                            CrackController.random_sleep(1, 2)
                    if begin:
                        battle_count += 1
                        print('--------------invite count-------------------------------------', battle_count)
                    else:
                        self._invite(column_name_list)
                    CrackController.touch(self.index, CrackController.cheat(location))
                    CrackController.random_sleep(3, 5)
                    if change_champion:
                        self._in_chapter_battle_new(is_leader)
                        CrackController.random_sleep(90, 110)
                else:
                    CrackController.touch(self.index, CrackController.cheat(location))
            CrackController.random_sleep(1, 2)

    def accept_invite(self, inviter: str, timer: int = 60 * 60 * 6, change_champion: bool = False,
                      is_leader: bool = False, is_chapter: bool = False) -> bool:
        accept_time = time.time()
        buff_status_dict = {"mitama": False, "awake": False}
        while True:
            if CrackService.breakthrough_flag:
                self.leave_team()
                self.any_pages_back_to_home_page()
                if CrackService.current_mode is not None:
                    self.open_close_buff(CrackService.current_mode, False)
                    buff_status_dict[CrackService.current_mode] = False
                CrackService.status_dict[self.index] = False
                if self.index not in CrackService.dont_want_to_breakthrough_list:
                    self.personal_break_through()
                else:
                    CrackController.random_sleep(20, 30)
                CrackService.status_dict[self.index] = True
            else:
                if CrackService.current_mode is not None and not buff_status_dict.get(CrackService.current_mode):
                    if not change_champion:
                        self.open_close_buff(CrackService.current_mode, True)
                    buff_status_dict[CrackService.current_mode] = True
            if time.time() - accept_time > timer:
                if CrackService.current_mode is not None:
                    self.open_close_buff(CrackService.current_mode, False)
                return True
            screen = CrackController.screen_shot(self.index)
            _, exist = CrackController.find_single_picture(screen, CrackController.share_path +
                                                           'prepare_flag.png')
            if exist > 0:
                if change_champion:
                    self._in_chapter_battle_new(is_leader)
            screen = CrackController.screen_shot(self.index)
            if not is_chapter:
                _, is_team_leader = CrackController.find_single_picture(screen, CrackController.share_path +
                                                                        'battle_victory.png')
                if is_team_leader > 0:
                    self.leave_team()
                    self.any_pages_back_to_home_page()
                    continue
            else:
                _, exist_fix_flag = CrackController.find_single_picture(screen, CrackController.share_path +
                                                                        'fix_team_flag.png')
                _, exist_smile_flag = CrackController.find_single_picture(screen, CrackController.share_path +
                                                                          'smile_flag.png')
                if exist_fix_flag > 0 and exist_smile_flag < 0:
                    self.leave_team(True)
                    continue
            inviter_location, exist = CrackController.find_single_picture(screen,
                                                                          CrackController.share_path + "invite\\check_"
                                                                          + inviter + ".png")
            if exist > 0:
                all_locations = CrackController.find_all_pictures(screen,
                                                                  CrackController.share_path + "team2_invite.png")
                if not change_champion and len(all_locations) > 0:
                    CrackController.touch(self.index, CrackController.cheat(all_locations[0]))
                else:
                    all_locations = CrackController.find_all_pictures(screen,
                                                                      CrackController.share_path + "team_invite.png")
                    to_click = [location for location in all_locations if
                                inviter_location[1] in range(location[1] - 40, location[1])]
                    if len(to_click) > 0:
                        CrackController.touch(self.index, CrackController.cheat(all_locations[0]))
            exist, location, template = CrackController.check_picture_list(self.index, GameDetail.victory,
                                                                           screen=screen)
            if exist:
                if template == 'Onmyoji_images\\game_failure_victory.png':
                    return False
                CrackController.touch(self.index, CrackController.cheat(location))
            CrackController.random_sleep()

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

    def _invite(self, column_name_list: [(str, str)], is_chapter: bool = False):
        invite_counter = 0
        while True:
            if invite_counter >= 10:
                self.leave_team(is_chapter)
                invite_counter = 0
                continue
            exist, location = CrackController.wait_picture(self.index, 1,
                                                           CrackController.share_path + 'invite\\make_up_team.png')
            if exist:
                CrackController.touch(self.index, CrackController.cheat(location))
                CrackController.random_sleep()
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
                if not is_chapter:
                    CrackController.random_sleep(12, 15)
                else:
                    CrackController.random_sleep(7, 8)
                invite_counter += 1
            if not is_chapter:
                if self._inviter_ready_to_begin_team_battle(column_name_list):
                    break
            else:
                exist, _ = CrackController.wait_picture(self.index, 1,
                                                        CrackController.share_path + "fix_team_flag.png")
                if exist:
                    break

    def _inviter_ready_to_begin_team_battle(self, column_name_list: [(str, str)]) -> bool:
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
        self.any_pages_back_to_home_page()
        CrackController.random_sleep()
        CrackController.random_click(self.index, GameDetail.home_page_explore_left_up,
                                     GameDetail.home_page_explore_right_down)
        CrackController.random_sleep(1.5, 3)
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
                    if template in ['Onmyoji_images\\3_victory.png', 'Onmyoji_images\\2_victory.png']:
                        CrackController.random_sleep(2.5, 4)
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
                locations = CrackController.find_all_pictures(screen, CrackController.share_path + 'broken2_flag.png',
                                                              0.7)
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
                        ticket -= len(locations)
                        refresh = True
                if not refresh:
                    CrackController.touch(self.index, CrackController.cheat(click_position))
                    CrackController.random_sleep()
                    exist, location = CrackController.wait_picture(self.index, 10,
                                                                   CrackController.share_path + 'attack_star.png')
                    if exist:
                        CrackController.touch(self.index, CrackController.cheat(location))
                        CrackController.random_sleep(10, 12)
            # else:
            #
            #     exist, _ = CrackController.wait_picture(self.index, 1,
            #                                             CrackController.share_path +
            #                                             'group_break_through_icon.png')
            #     if exist:
            #         refresh = True

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
            CrackController.random_sleep()
            if times > count:
                break
            screen = CrackController.screen_shot(self.index)
            location, exist = CrackController.find_single_picture(screen,
                                                                  CrackController.share_path + "prepare_flag.png")
            if exist > 0:
                self._in_chapter_battle_new(True)
            exist, location, template = CrackController.check_picture_list(self.index, GameDetail.victory)
            if exist:
                CrackController.touch(self.index, CrackController.cheat(location))
                if template == 'Onmyoji_images\\challenge_victory.png':
                    times += 1
                    if mode == 'mitama':
                        CrackController.random_sleep(2, 3)
                        self._in_chapter_battle_new(True)
                    if mode == 'awake':
                        CrackController.random_sleep(15, 20)
                    if mode == 'imperial_spirit':
                        CrackController.random_sleep(55, 65)
                if template == 'Onmyoji_images\\fail_victory.png':
                    if mode == "mitama":
                        CrackController.random_sleep(3, 5)
                        exist, location = CrackController.wait_picture(self.index, 3,
                                                                       CrackController.share_path
                                                                       + "original_fire_3.png")
                        if exist:
                            CrackController.touch(self.index, CrackController.cheat(location))

    def chapter_battle(self, column_name_list: [(str, str)]) -> None:

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
        if column_name_list is None:
            exist, location = CrackController.wait_picture(self.index, 2,
                                                           CrackController.share_path + 'explore_start_icon.png')
            if exist:
                CrackController.touch(self.index, CrackController.cheat(location))
        else:
            if len(column_name_list) != 0:
                self._invite(column_name_list, True)
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
                    if column_name_list is None:
                        self._in_chapter_battle()
                    else:
                        while True:
                            exist, location, _ = CrackController.check_picture_list(self.index, GameDetail.victory)
                            if exist:
                                CrackController.touch(self.index, CrackController.cheat(location))
                            to_continue_list = [
                                CrackController.share_path + "invite2_team.png",
                                CrackController.share_path + "fix_team_flag.png"
                            ]
                            exist, location, template = CrackController.check_picture_list(self.index, to_continue_list)
                            if exist:
                                if template == 'Onmyoji_images\\fix_team_flag.png':
                                    CrackController.random_sleep()
                                    exist, _ = CrackController.wait_picture(self.index, 2,
                                                                            CrackController.share_path +
                                                                            "gift_chapter_flag.png")
                                    if exist:
                                        self.leave_team(True)
                                        CrackController.random_sleep()
                                        continue
                                    else:
                                        break
                                else:
                                    while True:
                                        CrackController.touch(self.index, CrackController.cheat(location))
                                        exist, location = CrackController.wait_picture(self.index, 1,
                                                                                       CrackController.share_path
                                                                                       + "invite2_team.png")
                                        if exist:
                                            CrackController.touch(self.index, CrackController.cheat(location))
                                            CrackController.random_sleep()
                                        else:
                                            break
                                    break
                    CrackController.random_sleep()
                else:
                    if random.uniform(0, 1) > 0.5:
                        drag_to_right()
                    else:
                        drag_to_left()
                if column_name_list is None:
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

    def leave_team(self, is_chapter: bool = False) -> None:
        if not is_chapter:
            exist, location = CrackController.wait_picture(self.index, 3, CrackController.share_path +
                                                           "team_leave.png")
        else:
            exist, location = CrackController.wait_picture(self.index, 3, CrackController.share_path +
                                                           "backward3_close.png", 0.9)
        if exist:
            CrackController.touch(self.index, CrackController.cheat(location))
            CrackController.random_sleep(1, 2)
            if is_chapter:
                exist, location = CrackController.wait_picture(self.index, 3,
                                                               CrackController.share_path + "team_confirm_leave.png")
            else:
                exist, location = CrackController.wait_picture(self.index, 3,
                                                               CrackController.share_path + "team2_confirm_leave.png")
            if exist:
                CrackController.touch(self.index, CrackController.cheat(location))
            CrackController.random_sleep()

    def detour_to_explore_page(self):
        self.any_pages_back_to_home_page()
        CrackController.random_sleep()
        CrackController.random_click(self.index, GameDetail.home_page_explore_left_up,
                                     GameDetail.home_page_explore_right_down)
        CrackController.random_sleep(1.5, 3)

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

    def _in_chapter_battle_new(self, is_leader: bool = False) -> None:
        count = 0
        while True:
            count += 1
            screen = CrackController.screen_shot(self.index)
            locations = CrackController.find_all_pictures(screen, CrackController.share_path + 'max_level_flag2.png',
                                                          0.65)
            CrackController.random_sleep()
            if len(locations) > 0 or count > 0:
                break
        if not is_leader and len(locations) > 0 or is_leader and len(locations) > 1:
            count = len(locations) if not is_leader else len(locations) - 1
            # 双击指定区域，高视角切换低视角
            CrackController.random_click(self.index, GameDetail.change_attendant_click_left_up,
                                         GameDetail.change_attendant_click_right_down)
            CrackController.random_click(self.index, GameDetail.change_attendant_click_left_up,
                                         GameDetail.change_attendant_click_right_down)
            CrackController.random_sleep(1.5, 3)
            # 筛选N卡
            exist, location, template = CrackController.check_picture_list(self.index, GameDetail.champion_class)
            if exist:
                if template != 'Onmyoji_images\\N_class.png':
                    CrackController.touch(self.index, CrackController.cheat(location))
                    CrackController.random_sleep(0.5, 0.8)
                    exist, location = CrackController.wait_picture(self.index, 1,
                                                                   CrackController.share_path + 'N_class.png')
                    if exist:
                        CrackController.touch(self.index, CrackController.cheat(location))
                        CrackController.random_sleep()

            # 低视角查询满经验式神数量
            screen = CrackController.screen_shot(self.index)
            locations_list = CrackController.find_all_pictures(screen,
                                                               CrackController.share_path + 'max_level_flag2.png', 0.65)
            locations_list = sorted(locations_list, key=lambda loc: loc[0])
            if is_leader:
                locations_list = locations_list[1:]
            else:
                if len(locations_list) != count:
                    x = random.randint(*GameDetail.mitama_level_10_first_position_width)
                    y = random.randint(*GameDetail.mitama_level_10_first_position_height)
                    locations_list.append((x, y, 0, 0))
            print(len(locations_list))
            if len(locations_list) != 0:
                for x, y, _, _ in locations_list:
                    # 默认低视角最左边为队长
                    while True:
                        screen = CrackController.screen_shot(self.index)
                        locations_list = CrackController.find_all_pictures(screen, CrackController.share_path +
                                                                           'level_one_flag.png')
                        remove_locations_list = CrackController.find_all_pictures(screen,
                                                                                  CrackController.share_path +
                                                                                  'backup_in_team_flag.png')
                        if len(remove_locations_list) > 0:
                            to_remove = []
                            for location in locations_list:
                                for remove in remove_locations_list:
                                    if location[0] in range(remove[0] - 100, remove[0]):
                                        to_remove.append(location)
                            for remove in to_remove:
                                locations_list.remove(remove)
                        if len(locations_list) > 0:
                            middle = random.randint(*GameDetail.change_first_attendant_drag_middle)
                            drag_time = random.randint(1000, 2000)
                            CrackController.swipe(self.index, CrackController.cheat(locations_list[-1]),
                                                  (x, y + middle), drag_time)
                            CrackController.random_sleep()
                            break
                        else:
                            location, exist = CrackController.find_single_picture(screen,
                                                                                  CrackController.share_path
                                                                                  + "back_up_scroll.png", 0.65)
                            if exist > 0:
                                drag_time = random.randint(1000, 2000)
                                width = random.randint(200, 300)
                                (x_n, y_n) = CrackController.cheat(location)
                                CrackController.swipe(self.index, (x_n, y_n), (x_n + width, y_n), drag_time)
                            CrackController.random_sleep()
        exist, location = CrackController.wait_picture(self.index, 1,
                                                       CrackController.share_path + 'prepare_flag.png')
        if exist:
            CrackController.touch(self.index, CrackController.cheat(location))

    def _skip_task_invite(self) -> None:
        exist, location = CrackController.wait_picture(self.index, 1, CrackController.share_path + '5_victory.png')
        if exist:
            CrackController.touch(self.index, CrackController.cheat(location))

    def monopoly(self):
        def _pick_card() -> (int, int, int, int):
            self._skip_task_invite()
            gap_line = [(200, 300), (330, 400), (460, 500), (590, 650)]
            left_right_flag = [(240, 250), (1150, 1160)]
            screen = CrackController.screen_shot(self.index)
            locations = CrackController.find_all_pictures(screen, CrackController.share_path + 'new_activity\\gap.png')
            locations.sort(key=lambda x: x[1])
            result_dict = defaultdict(list)
            for location in locations:
                for index, gap in enumerate(gap_line):
                    if location[1] in range(*gap):
                        result_dict[index].append(location)
            for k, v in result_dict.items():
                v.sort(key=lambda x: x[0])
            if len(result_dict) == 4:
                choose_row = result_dict.get(0) if len(result_dict.get(0)) < len(
                    result_dict.get(3)) else result_dict.get(3)
                to_return = choose_row[len(choose_row) - 1] if choose_row[0][0] in range(*left_right_flag[0]) else \
                    choose_row[0]
            else:
                valid_rows = len(result_dict)
                if valid_rows == 0:
                    return None
                if result_dict.get(0) is None:
                    choose_row = result_dict.get(4 - valid_rows)
                else:
                    choose_row = result_dict.get(valid_rows - 1)
                to_return = choose_row[random.randint(0, len(choose_row) - 1)]
            return to_return

        def _loot() -> None:
            check_pic_list = [CrackController.share_path + '2_victory.png',
                              CrackController.share_path + '3_victory.png',
                              CrackController.share_path + 'new_activity\\gift_box.png',
                              CrackController.share_path + 'new_activity\\gift_eye.png',
                              CrackController.share_path + 'new_activity\\gift_moon.png']
            scan_count = 0
            while True:
                self._skip_task_invite()
                CrackController.random_sleep()
                exist, location, _ = CrackController.check_picture_list(self.index, check_pic_list)
                if exist:
                    scan_count = 0
                    CrackController.touch(self.index, CrackController.cheat(location))
                else:
                    scan_count += 1
                if scan_count >= 5:
                    break

        def _buy_tickets() -> bool:
            self._skip_task_invite()
            exist, location = CrackController.wait_picture(self.index, 1,
                                                           CrackController.share_path +
                                                           'new_activity\\buy_tickets_hint.png')
            if exist:
                exist, location = CrackController.wait_picture(self.index, 1,
                                                               CrackController.share_path +
                                                               'new_activity\\buy_tickets_up_bound.png')
                if exist:
                    CrackController.touch(self.index, CrackController.cheat(location))
                    CrackController.random_sleep()
                    exist, location = CrackController.wait_picture(self.index, 1,
                                                                   CrackController.share_path +
                                                                   'new_activity\\buy_tickets_confirm.png')
                    if exist:
                        CrackController.touch(self.index, CrackController.cheat(location))
                        _loot()
                        return True
            else:
                return False

        def _choose_mitama() -> None:
            self._skip_task_invite()
            exist, location = CrackController.wait_picture(self.index, 5,
                                                           CrackController.share_path +
                                                           'new_activity\\choose_mitama.png')
            if exist:
                CrackController.touch(self.index, CrackController.cheat(location))
                CrackController.random_sleep(1, 2)
                _buy_tickets()
                exist, location = CrackController.wait_picture(self.index, 3,
                                                               CrackController.share_path +
                                                               'new_activity\\choose_mitama_hint.png')
                if exist:
                    exist, location = CrackController.wait_picture(self.index, 1,
                                                                   CrackController.share_path +
                                                                   'new_activity\\choose_mitama_confirm.png')
                    if exist:
                        CrackController.touch(self.index, CrackController.cheat(location))

        def _enter_next_level() -> None:
            self._skip_task_invite()
            exist, location = CrackController.wait_picture(self.index, 5,
                                                           CrackController.share_path +
                                                           'new_activity\\enter_next_level_hint.png')
            if exist:
                exist, location = CrackController.wait_picture(self.index, 5,
                                                               CrackController.share_path +
                                                               'new_activity\\enter_next_level_confirm.png')
                if exist:
                    CrackController.touch(self.index, CrackController.cheat(location))
                    CrackController.random_sleep(4, 5)
                    _choose_mitama()

        def _battle() -> None:
            self._skip_task_invite()
            exist, _ = CrackController.wait_picture(self.index, 1,
                                                    CrackController.share_path +
                                                    'new_activity\\ready_to_battle_flag.png')
            if exist:
                exist, click = CrackController.wait_picture(self.index, 1,
                                                            CrackController.share_path +
                                                            'new_activity\\begin_battle.png')
                if exist:
                    CrackController.touch(self.index, CrackController.cheat(click))
                    CrackController.random_sleep(2, 3)
                    bought = _buy_tickets()
                    if bought:
                        CrackController.touch(self.index, CrackController.cheat(click))
                    CrackController.random_sleep(20, 30)
                    while True:
                        exist, click, _ = CrackController.check_picture_list(self.index,
                                                                             GameDetail.victory)
                        if exist:
                            CrackController.touch(self.index, CrackController.cheat(click))
                        CrackController.random_sleep()
                        exist, _ = CrackController.wait_picture(self.index, 1,
                                                                CrackController.share_path +
                                                                'new_activity\\flip_gap_page_flag.png')
                        if exist:
                            break

        while True:
            self._skip_task_invite()
            click_loc = _pick_card()
            if click_loc is None:
                _loot()
                exist_loc, click_loc = CrackController.wait_picture(self.index, 1,
                                                                    CrackController.share_path +
                                                                    'new_activity\\next_level_door.png')
                if exist_loc:
                    CrackController.touch(self.index, CrackController.cheat(click_loc))
                    CrackController.random_sleep(2, 3)
                    _battle()
                    _enter_next_level()
            else:
                CrackController.touch(self.index, CrackController.cheat(click_loc))
                CrackController.random_sleep(2, 3)
                _battle()
