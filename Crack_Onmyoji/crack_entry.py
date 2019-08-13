import os
import re
import sys
import time
from threading import Thread

from Crack_Onmyoji.crack_controller import CrackController
from Crack_Onmyoji.crack_service import CrackService
from Crack_Onmyoji.log_recorder import LogRecorder


class CrackEntry:
    def __init__(self, number_of_team_members: int,
                 mode: str, addition_arg: str, inviter: int = -1, invite_members: {(str, str)} = None,
                 year_beast: bool = False, foster: bool = False, group_break_through: bool = False,
                 personal_break_through: bool = False):
        self.number_of_team_members = number_of_team_members
        self.mode = mode
        self.addition_arg = addition_arg
        self.inviter = inviter
        self.invite_members = invite_members
        self.year_beast = year_beast
        if self.year_beast:
            self.need_to_fight_year_beast = True
        self.foster = foster
        if self.foster:
            self.need_to_foster = True
        self.group_break_through = group_break_through
        if self.group_break_through:
            self.need_to_group_break_through = True
        self.personal_break_through = personal_break_through
        if self.personal_break_through:
            self.need_to_personal_break_through = True
        self.crack = []
        for i in range(number_of_team_members):
            self.crack.append(CrackService(i))

    def start(self):
        start_time = time.time()
        year_beast_timer = start_time
        foster_timer = start_time
        personal_break_through_timer = start_time
        group_break_through_timer = start_time
        while True:
            if self.year_beast and self.need_to_fight_year_beast:
                pass
            if self.foster and self.need_to_foster:
                pass
            if self.group_break_through and self.need_to_group_break_through:
                g_b_t = Thread(target=self.crack[0].group_break_through)
                g_b_t.start()
                g_b_t.join()
                self.need_to_group_break_through = False
                group_break_through_timer = time.time()
            else:
                if time.time() - group_break_through_timer >= 60 * 30:
                    self.need_to_group_break_through = True
            CrackController.random_sleep(10, 20)
            if self.personal_break_through and self.need_to_personal_break_through:
                g_b_t = Thread(target=self.crack[0].personal_break_through)
                g_b_t.start()
                g_b_t.join()
                self.need_to_personal_break_through = False
                personal_break_through_timer = time.time()
            else:
                if time.time() - personal_break_through_timer >= 60 * 30:
                    self.need_to_personal_break_through = True
            main_task_threads = []
            if self.inviter >= 0:
                for i in range(self.number_of_team_members):
                    if self.inviter == i:
                        main_task_threads.append(Thread(target=self.crack[i].mitama_or_awake_invite,
                                                        kwargs={'mode': self.mode, 'addition_arg': self.addition_arg,
                                                                'column_name_list': self.invite_members}))
                    else:
                        main_task_threads.append(Thread(target=self.crack[i].accept_invite))
            else:
                main_task_threads.append(Thread(target=self.crack[0].accept_invite))


def main():
    run_time = time.strftime("%Y %m %d %H:%M:%S", time.localtime())
    sys.stdout = LogRecorder('./logs/' + '_'.join(re.split(r'[\\ |:]', run_time)) + '_log.txt')
    c0 = CrackService(0, [['accept_invite']])
    # c1 = CrackService(1, [['accept_invite']])
    # c2 = CrackService(2,
    #                   [['mitama_or_awake_invite', 'mitama', '11', [('cross', 'ybymq'), ('cross', 'xgrcey')], 17]])
    # c0.setDaemon(True)
    # c1.setDaemon(True)
    # c0.start()
    # c1.start()
    # c2.start()
    # c2.join()
    # c2 = CrackService(2,
    #                   [['mitama_or_awake_invite', 'awake', 'fire', [('cross', 'ybymq'), ('cross', 'xgrcey')], 13
    #                     ]])
    # c2.start()
    # c2.join()
    c0.personal_break_through()
    c0.group_break_through()
    # c1 = CrackService(0, [['accept_invite']])
    # c2 = CrackService(3,
    #                   [['mitama_or_awake_invite', 'mitama', '11', [('cross', 'xgrcey')]]])
    # c1.start()
    # c2.start()
    # os.system('shutdown -s -t 10')
    # c0.accept_invite(timer=60 * 60 * 5)
    # c0.accept_invite(timer=60 * 60 * 3)
    # os.system('shutdown -s -t 60')
    # c0.hundred_ghosts(100)
    # while True:
    #     c0.hundred_ghosts(100)
    #     CrackController.random_sleep(100, 200)
    # c1 = CrackService(0, [['accept_invite']])
    # c2 = CrackService(3,
    #                   [['mitama_or_awake_invite', 'mitama', '11', [('cross', 'xgrcey')], 100]])
    # c1.start()
    # c2.start()


if __name__ == '__main__':
    main()
