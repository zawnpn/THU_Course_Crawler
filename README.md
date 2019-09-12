# THU_Course_Crawler

强调：**本程序仅供爬虫方面的技术交流，请勿用于其他用途，概不负责。如有问题，随时联系我删掉此 repo。**

匆忙之中写出来的，仅供研究生测试使用（本科生我没法测试，应该稍微改一些链接和参数即可），功能较少，且很多地方没做逻辑测试，完善度较低，不少地方没填对就会报错。

## 功能

1. 显示当前已选课程
2. 查询课余量
3. 特殊功能，仅供技术交流和测试，勿用作其他用途

## 使用说明

### 0.前提

（首先要通过 `pip install -r requirements.txt` 安装好依赖库，然后执行 `python main.py` 来运行）

经过测试发现，该教务系统在程序提交200次申请后必定会将你的会话结束，若想再次使用需要重新登录，因此需要引入验证码自动识别程序，本人不才，来不及编写和训练出模型来，暂时使用的是网上的验证码识别API。

在使用前，请先前往[该网站](https://market.aliyun.com/products/57124001/cmapi00035185.html) (非广告，我随便找的，类似的很多)注册领取一个免费100次的验证码识别包，他会提供一个`AppCode`，填写至 `extra/config.py` 中即可使用，其他地方无需更改。

若不想使用上面说的这个API，也可修改 `core/crawler.py` 中的 `get_captcha()` 函数，自行替换为其他API或者验证码识别算法。

### 1.登录

按提示输入账号和密码即可，验证码会自动识别无需填写，可能会有个1、2次识别失败，是正常现象。此处不知道为什么会有点慢，稍等1分钟即可出现菜单选项。

### 2.显示当前已选课程

若想查询已选课程，菜单中输入选项1，即可查询当前已选课程。

### 3.查询课余量

若想查询课余量，菜单中输入选项2，按提示逐项输入学期（默认学期无需输入回车即可）和要搜索的关键词（空格分开）即可出现你要查询的课余量。

### 4.特殊功能，仅供交流测试

**再次强调，该功能仅供技术交流和测试，勿用作其他用途！本人不负责！**

按提示，逐项输入学期（默认回车即可）、course id（有两个id，空格分开，example: `60510082 200`），然后输入 `y` 来提交下一个 course id，或者输入 `n` 即可结束输入执行该功能。

`main.py` 中的 `time.sleep(10)` 表示前后两次提交的间隔为10秒，根据你的需求自行修改，建议至少控制在 3 秒以上，太快反而无效，而且会很快将你的 100 次验证码识别消耗完。

## 其他

仓促中完成的，还有很多不足之处，欢迎大佬指点和交流！