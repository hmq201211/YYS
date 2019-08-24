import glob


class GameDetail:
    left_up_position = (0, 0)
    right_down_position = (1280, 720)
    invite = glob.glob(r'Onmyoji_images\*_invite.png')
    victory = glob.glob(r'Onmyoji_images\*_victory.png')
    close = glob.glob(r'Onmyoji_images\*close.png')
    chapter_battle = glob.glob(r'Onmyoji_images\*_battle.png')
    out_of_chapter = glob.glob(r'Onmyoji_images\*_chapter_flag.png')
    game_package_name = "com.netease.onmyoji"
    game_video_activity_name = "com.netease.onmyoji/.VideoPlayer"
    player = ["player_master", "player_attendant_one", "player_attendant_two"]
    champion_class = glob.glob(r'Onmyoji_images\*class.png')
    hundred_ghosts = glob.glob(r'Onmyoji_images\*_hundred_ghosts.png')
    chapter_drag_height = (120, 140)
    chapter_drag_left = (100, 200)
    chapter_drag_right = (1080, 1180)
    chapter_attendant_click_left_up = (360, 480)
    chapter_attendant_click_right_down = (530, 600)
    chapter_backup_drag_left = (200, 300)
    chapter_backup_drag_right = (900, 1000)
    chapter_backup_drag_height = (500, 660)
    chapter_attendant_position_3_drag_width = (1060, 1080)
    chapter_attendant_position_3_drag_height = (235, 325)
    chapter_attendant_position_3_stand_width = (240, 330)
    chapter_attendant_position_3_stand_height = (160, 320)

    # 换狗粮高视角切换低视角，固定点击矩形区域,值为对角线定点坐标
    change_attendant_click_left_up = (400, 400)
    change_attendant_click_right_down = (600, 485)
    # 高度误差补偿
    change_first_attendant_drag_middle = (50, 65)
    # 魂十第一个位置
    mitama_level_10_first_position_width = (45, 90)
    mitama_level_10_first_position_height = (306, 319)

    break_through_word_left_up = (170, 520)
    break_through_word_right_down = (320, 570)
    break_through_sleep_left_up = (1040, 523)
    break_through_sleep_right_down = (1125, 561)
    break_through_ticket_left_up = (409, 605)
    break_through_ticket_right_down = (487, 639)
    hundred_ghosts_choose_king_first_left_up = (220, 480)
    hundred_ghosts_choose_king_first_right_down = (320, 520)
    hundred_ghosts_choose_king_second_left_up = (580, 480)
    hundred_ghosts_choose_king_second_right_down = (680, 520)
    hundred_ghosts_choose_king_third_left_up = (930, 480)
    hundred_ghosts_choose_king_third_right_down = (1030, 520)
    hundred_ghosts_throw_height = (300, 450)
    hundred_ghosts_drag_width = (420, 480)
    hundred_ghosts_drag_height = (0, 720)
    hundred_ghosts_ticket_left_up = (788, 517)
    hundred_ghosts_ticket_right_down = (841, 545)
    home_page_explore_left_up = (660, 128)
    home_page_explore_right_down = (698, 197)
    awake_buff_left_up = (860, 137)
    awake_buff_right_down = (888, 170)
    mitama_buff_left_up = (860, 210)
    mitama_buff_right_down = (888, 237)
    awake_buff_check_left_up = (766, 132)
    awake_buff_check_right_down = (893, 176)
    mitama_buff_check_left_up = (768, 200)
    mitama_buff_check_right_down = (896, 244)
    group_break_through_times_left_up = (269, 545)
    group_break_through_times_right_down = (330, 585)
    all_teams_first_box_left_up = (166, 128)
    all_teams_first_box_right_down = (346, 173)

    @staticmethod
    def get_user_name_by_index(index: int) -> str:
        return GameDetail.player[index]

    def __init__(self):
        self.mitama_battle_count = 0
        self.awake_battle_count = 0
        self.personal_breakthrough_battle_count = 0
        self.group_breakthrough_battle_count = 0
        self.chapter_single_battle_count = 0
        self.chapter_boss_battle_count = 0
        self.technical_battle_count = 0

    def __str__(self):
        mitama_battle_count = self.mitama_battle_count
        awake_battle_count = self.awake_battle_count
        personal_breakthrough_battle_count = self.personal_breakthrough_battle_count
        group_breakthrough_battle_count = self.group_breakthrough_battle_count
        chapter_single_battle_count = self.chapter_single_battle_count
        chapter_boss_battle_count = self.chapter_boss_battle_count
        technical_battle_count = self.technical_battle_count
        return "\n mitama_battle_count:%d " \
               "awake_battle_count:%d " \
               " personal_breakthrough_battle_count:%d " \
               " group_breakthrough_battle_count:%d " \
               " chapter_single_battle_count:%d " \
               "chapter_boss_battle_count:%d " \
               "technical_battle_count:%d " \
               "\n" % (
                   mitama_battle_count, awake_battle_count, personal_breakthrough_battle_count,
                   group_breakthrough_battle_count,
                   chapter_single_battle_count, chapter_boss_battle_count, technical_battle_count)
