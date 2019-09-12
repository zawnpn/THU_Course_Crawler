import requests
from PIL import Image
from io import BytesIO
import re
import os
import ast
from extra.config import *
import numpy as np
import base64
import json

class Crawler:

    def __init__(self):
        self.sess = requests.Session()
        self.login_status = False

    def get_captcha(self):
        print('Initializing and recognizing captcha code...(Wait for about 1 minute)')
        self.sess.get(LOGIN_URL, headers=HEADERS)
        captcha_resp = self.sess.get(CAPTCHA_URL)
        # img = Image.open(BytesIO(captcha_resp.content))
        # img.save('./captcha.jpg')
        # print('\n[Captcha saved to %s/captcha.jpg, please check!]\n' % os.getcwd())
        img_base64 = base64.b64encode(captcha_resp.content)
        test_url = 'http://codevirify.market.alicloudapi.com/icredit_ai_image/verify_code/v1'
        headers = {
            'Authorization': 'APPCODE %s' % APPCODE,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        data = {
            'IMAGE': img_base64,
            'IMAGE_TYPE': '0'
        }
        resp = requests.post(test_url,headers=headers,data=data)
        captchacode = json.loads(resp.text)['VERIFY_CODE_ENTITY']['VERIFY_CODE']
        print(captchacode)
        return captchacode

    
    def login(self, username, password, captchacode):
        login_post = {
            'j_username': username,
            'j_password': password,
            'captchaflag': 'login1',
            '_login_image_': captchacode
        }
        resp = self.sess.post(POST_URL,data=login_post,headers=HEADERS)
        if '选课研究生选课' in resp.text:
            self.login_status = True
            print('Login successfully!\n')
        else:
            print('Login failed!\n')

    def get_selected_courses(self, semester):
        course_post = {
            "m": "kbSearch",
            "p_xnxq":semester
        }
        resp = self.sess.post(HOME_URL,headers=HEADERS,data=course_post)
        course_html = resp.text
        course_html_strip = course_html.replace("strHTML += \"</a>\";","").replace("<b>","").replace("</b>","").replace("；","")
        pattern1 = re.compile(
            'target=\'_blank\'>";(.+?)if\(strHTML1 != ""\) {',
            re.DOTALL
        )
        pattern2 = re.compile(
            'strHTML.+?"(.+?)"',
            re.DOTALL
        )
        result = []
        result1 = pattern1.findall(course_html_strip)
        for item in result1:
            result2 = pattern2.findall(item)
            if result == [] or result2 != result[-1]:
                result.append(result2)
        return result
    
    def search_course_info(self, semester):
        result = []
        page = 1
        remain_course_post = {
            'm': 'kylSearch',
            'page': str(page),
            'p_xnxq': semester,
            # 'p_kcm': kw.encode('GB2312')
        }
        resp = self.sess.post(UTIL_URL,headers=HEADERS,data=remain_course_post, allow_redirects=True)
        pattern1 = re.compile('var gridData = (.+?);\r\n</script>',re.DOTALL)
        remain_list = pattern1.findall(resp.text)[0]
        remain_list = remain_list.replace(" ","").replace("\r","").replace("\n","").replace("\t","")
        result.extend(ast.literal_eval(remain_list))
        pattern2 = re.compile('共 (.+?) 页')
        num = int(pattern2.findall(resp.text)[0])
        for page in range(2,num+1):
            remain_course_post = {
                'm': 'kylSearch',
                'page': str(page),
                'p_xnxq': semester,
                # 'p_kcm': kw.encode('GB2312')
            }
            resp = self.sess.post(UTIL_URL,headers=HEADERS,data=remain_course_post, allow_redirects=True)
            pattern1 = re.compile('var gridData = (.+?);\r\n</script>',re.DOTALL)
            remain_list = pattern1.findall(resp.text)[0]
            remain_list = remain_list.replace(" ","").replace("\r","").replace("\n","").replace("\t","")
            result.extend(ast.literal_eval(remain_list))
        
        return result
    
    def select_course(self, semester, id1, id2):
        token_pattern = re.compile('<input type="hidden" name="token"\r\n\t\t\t\tvalue="(.+?)">')
        token_data = {
            'm':'xwkSearch',
            'p_xnxq':semester,
            'tokenPriFlag':'xwk'
        }
        resp = self.sess.post(HOME_URL,headers=HEADERS,data=token_data)
        token = token_pattern.findall(resp.text)[0]
        submit_data = {
            'm': 'saveXwKc',
            'token': token,
            'p_xnxq': semester,
            'tokenPriFlag': 'xwk',
            'p_xwk_id':'%s;%s;%s;' % (semester,id1,id2)
        }
        resp = self.sess.post(HOME_URL,headers=HEADERS,data=submit_data)
        msg_pattern = re.compile('showMsg\("(.+?)"\);')
        msg = msg_pattern.findall(resp.text)[0]
        return msg
