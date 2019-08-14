import os
import re
import sys
import time
from Crack_Onmyoji.crack_service import CrackService
from Crack_Onmyoji.log_recorder import LogRecorder


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
