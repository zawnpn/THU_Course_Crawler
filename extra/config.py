APPCODE = '' # 此处填写你申请到的验证码API的 AppCode

LOGIN_URL = 'http://zhjwxk.cic.tsinghua.edu.cn/xklogin.do'
HOME_URL = 'http://zhjwxk.cic.tsinghua.edu.cn/xkYjs.vxkYjsXkbBs.do'
CAPTCHA_URL = 'http://zhjwxk.cic.tsinghua.edu.cn/login-jcaptcah.jpg?captchaflag=login1'
POST_URL = 'https://zhjwxk.cic.tsinghua.edu.cn/j_acegi_formlogin_xsxk.do'
UTIL_URL = 'http://zhjwxk.cic.tsinghua.edu.cn/xkYjs.vxkYjsJxjhBs.do'
HEADERS = {
'Access-Control-Allow-Origin': '*',
'Connection': 'Keep-Alive',
'Content-Encoding': 'gzip',
'Content-Length': '108',
'Keep-Alive': 'timeout=8, max=500',
'P3P': 'CP=CAO DSP COR CUR ADM DEV TAI PSA PSD IVAi IVDi CONi TELo OTPi OUR DELi SAMi OTRi UNRi PUBi IND PHY ONL UNI PUR FIN COM NAV INT DEM CNT STA POL HEA PRE GOV',
'Server': 'Apache/2.4.37 (Unix) Resin/3.0.28',
'Vary': 'Accept-Encoding',
}
MENU = """
-------------------\n
1.show courses\n
2.search course info\n
3.select course\n
-------------------
"""
DEFAULT_SEMESTER = '2019-2020-1'