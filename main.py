import core.crawler as cl
from extra.config import MENU,DEFAULT_SEMESTER
import getpass
import numpy as np
import time


if __name__ == "__main__":
    bot = cl.Crawler()
    username = input('Input username: ')
    password = getpass.getpass('Input password: ')
    appcode = input('Input your captcha AppCode: ')
    # bot.get_captcha()
    # captchacode = input('Input captcha code: ')
    while not bot.login_status:
        captchacode = bot.get_captcha(appcode)
        bot.login(username, password, captchacode)
    if bot.login_status:
        flag = True
        while flag:
            print(MENU)
            choice = input('Input your choice: ')
            if choice == '1':
                semester = input('Input semester(Default:2019-2020-1): ')
                if not semester:
                    semester = DEFAULT_SEMESTER
                courses = bot.get_selected_courses(semester)
                print('='*60)
                for c in courses:
                    print(c)
            elif choice == '2':
                semester = input('Input semester(Default:2019-2020-1): ')
                if not semester:
                    semester = DEFAULT_SEMESTER
                keywords = input('Input keywords(split with space):')
                courses_info = {}
                all_info = bot.search_course_info(semester)
                all_info = np.array(all_info)
                for kw in keywords.split():
                    courses_info[kw] = all_info[all_info[:,2]==kw]
                print('='*60)
                print(courses_info)
            elif choice == '3':
                semester = input('Input semester(Default:2019-2020-1): ')
                if not semester:
                    semester = DEFAULT_SEMESTER
                sleep_time = input('Input interval time(Suggest: 10): ')
                if not sleep_time:
                    sleep_time = '10'
                sleep_time = float(sleep_time)
                id1_list = []
                id2_list = []
                input_flag = True
                while input_flag:
                    input_id = input('Input course ID[split with space(example:"60510082 200")]:')
                    input_id = input_id.split()
                    id1_list.append(input_id[0])
                    id2_list.append(input_id[1])
                    continue_flag = input('Input next ID?[y/n]: ').lower()
                    if continue_flag == 'n':
                        input_flag = False
                msg = ''
                attempt_count = 1
                while id1_list:
                    for i in range(len(id1_list)):
                        try:
                            msg = bot.select_course(semester,id1_list[i],id2_list[i])
                            if '成功' in msg or '冲突' in msg or '学位课' in msg:
                                id1_list.pop(i)
                                id2_list.pop(i)
                        except:
                            msg = 'Failed'
                            bot.login_status = False
                            while not bot.login_status:
                                captchacode = bot.get_captcha(appcode)
                                bot.login(username, password, captchacode)
                        print(str(attempt_count) + ': ' + msg)
                        attempt_count += 1
                        time.sleep(sleep_time)
            else:
                print('Please input correct option!')
            choice = input('='*60 + '\nBack to menu?[y/n]: ').lower()
            if choice == 'n':
                flag = False
    else:
        exit(0)