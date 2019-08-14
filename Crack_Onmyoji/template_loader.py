import cv2
import glob


class TemplateLoader:
    @staticmethod
    def load_templates() -> dict:
        all_files = glob.glob(r'Onmyoji_images\*.png')
        to_remove_list = glob.glob(r'Onmyoji_images\*_scr.png')
        all_invite_files = glob.glob(r'Onmyoji_images\invite\*.png')
        all_files = all_files + all_invite_files
        for to_remove in to_remove_list:
            all_files.remove(to_remove)
        template_dict = {}
        for template in all_files:
            template_dict[template] = cv2.imread(template)
        return template_dict
