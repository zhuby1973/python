import time
import requests
import re
import json
from selenium import webdriver

PATH = "C:\Program Files\chromedriver.exe"
driver = webdriver.Chrome(PATH)
url = "https://pan.baidu.com/disk/home#/all?path=%2F&vmode=list"
driver.get(url)
cookies = {
  "BDUSS": "lUT1dTcXRpRHFWWFQ0RlEyM0U2R2l-MlJHMkx0dFd3QnBKY2xxTzdqUUFlUWRmRVFBQUFBJCQAAAAAAAAAAAEAAADdB6hItPPG7NOi0NtDQQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADs314A7N9eMm",
  "STOKEN": "3ba8354c922ea6ded92c05d00a618f750e7c8201e9c763a69abeec600fe37b89",
  "domain": "pan.baidu.com"
}

response_cookies_browser = [{'name':name, 'value':value} for name, value in cookies.items()]
c = [driver.add_cookie(c) for c in response_cookies_browser]

#the browser now contains the cookies generated from the authentication    
driver.get(url)
#wait 10 seconds for the popup window, so we can click the close button 
time.sleep(10)
driver.find_elements_by_xpath('.//span[@class = "dialog-icon dialog-close icon icon-close"]')[-1].click()

class BaiDuPan(object):
    def __init__(self):
        # 创建session并设置初始登录Cookie
        self.session = requests.session()
        self.session.cookies['BDUSS'] = 'lUT1dTcXRpRHFWWFQ0RlEyM0U2R2l-MlJHMkx0dFd3QnBKY2xxTzdqUUFlUWRmRVFBQUFBJCQAAAAAAAAAAAEAAADdB6hItPPG7NOi0NtDQQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADs314A7N9eMm'
        self.session.cookies['STOKEN'] = '3ba8354c922ea6ded92c05d00a618f750e7c8201e9c763a69abeec600fe37b89'
        self.headers = {
            'Host': 'pan.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        }
    def verifyShare(self, surl, bdstoken, pwd, referer):
        '''
        构造密码验证的URL：https://pan.baidu.com/share/verify?
        surl=62yUYonIFdKGdAaueOkyaQ  从重定向后的URL中获取
        &t=1572356417593  时间戳
        &channel=chunlei  固定值
        &web=1  固定值
        &app_id=250528  固定值
        &bdstoken=742aa0d6886423a5503bbc67afdb2a7d  从重定向后的页面中可以找到，有时候会为空，经过验证，不要此字段也可以
        &logid=MTU0ODU4MzUxMTgwNjAuNDg5NDkyMzg5NzAyMzY1MQ==  不知道什么作用，暂时为空或者固定值都可以
        &clienttype=0  固定值
        '''
        t = str(int(time.time()) * 1000)
        url = 'https://pan.baidu.com/share/verify?surl=%s&t=%s&channel=chunlei&web=1&app_id=250528&bdstoken=%s\
            &logid=MTU0ODU4MzUxMTgwNjAuNDg5NDkyMzg5NzAyMzY1MQ==&clienttype=0' % (surl, t, bdstoken)
        form_data = {
            'pwd': pwd,
            'vcode': '',
            'vcode_str': '',
        }
        # 设置重试机制
        is_vcode = False
        for n in range(1, 166):
            # 自动获取并识别验证码，使用pytesseract自动识别时，可加大重试次数
            if is_vcode:
                ocr_result = self.vcodeOCR()
                if (ocr_result['errno'] == 0):
                    form_data['vcode'] = ocr_result['vcode']
                    form_data['vcode_str'] = ocr_result['vcode_str']
                elif (ocr_result['errno'] == 1):
                    continue
                else:
                    return {'errno': 1, 'err_msg': '验证码获取失败：%d' % ocr_result['errno']}
            headers = self.headers
            headers['referer'] = referer
            # verify_json['errno']：-9表示提取码不正确；-62表示需要验证码/验证码不正确（不输入验证码也是此返回值）
            verify_res = self.session.post(url, headers=headers, data=form_data)
            verify_json = verify_res.json()
            if (verify_json['errno'] == 0):
                return {'errno': 0, 'err_msg': '加密分享验证通过'}
            elif (verify_json['errno'] == -9):
                return {'errno': 2, 'err_msg': '提取码不正确'}
            elif (verify_json['errno'] == -62):
                is_vcode = True
            else:
                return {'errno': 3, 'err_msg': '加密分享验证失败：%d' % verify_json['errno']}
        return {'errno': 4,
                'err_msg': '重试多次后，验证码依旧不正确：%d' % (verify_json['errno'] if ("verify_json" in locals()) else -1)}
    
    def saveShare(self, url, pwd=None, path='/'):
        share_res = self.session.get(url, headers=self.headers)
        share_page = share_res.content.decode("utf-8")
        '''
        1.如果分享链接有密码，会被重定向至输入密码的页面；
        2.如果分享链接不存在，会被重定向至404页面https://pan.baidu.com/error/404.html，但是状态码是200；
        3.如果分享链接已被删除，页面会提示：啊哦，你来晚了，分享的文件已经被删除了，下次要早点哟。
        4.如果分享链接已被取消，页面会提示：啊哦，你来晚了，分享的文件已经被取消了，下次要早点哟。
        5.如果分享链接涉及侵权，页面会提示：此链接分享内容可能因为涉及侵权、色情、反动、低俗等信息，无法访问！
        6.啊哦！链接错误没找到文件，请打开正确的分享链接!
        7.啊哦，来晚了，该分享文件已过期
        '''
        if ('error/404.html' in share_res.url):
            return {"errno": 1, "err_msg": "无效的分享链接", "extra": "", "info": ""}
        if ('你来晚了，分享的文件已经被删除了，下次要早点哟' in share_page):
            return {"errno": 2, "err_msg": "分享文件已被删除", "extra": "", "info": ""}
        if ('你来晚了，分享的文件已经被取消了，下次要早点哟' in share_page):
            return {"errno": 3, "err_msg": "分享文件已被取消", "extra": "", "info": ""}
        if ('此链接分享内容可能因为涉及侵权、色情、反动、低俗等信息，无法访问' in share_page):
            return {"errno": 4, "err_msg": "分享内容侵权，无法访问", "extra": "", "info": ""}
        if ('链接错误没找到文件，请打开正确的分享链接' in share_page):
            return {"errno": 5, "err_msg": "链接错误没找到文件", "extra": "", "info": ""}
        if ('啊哦，来晚了，该分享文件已过期' in share_page):
            return {"errno": 6, "err_msg": "分享文件已过期", "extra": "", "info": ""}
        # 提取码校验的请求中有此参数
        bdstoken = re.findall(r'bdstoken\":\"(.+?)\"', share_page)
        bdstoken = bdstoken[0] if (bdstoken) else ''
        # 如果加密分享，需要验证提取码，带上验证通过的Cookie再请求分享链接，即可获取分享文件
        if ('init' in share_res.url):
            surl = re.findall(r'surl=(.+?)$', share_res.url)[0]
            if (pwd == None):
                pwd_result = self.getSharePwd(surl)
                if (pwd_result['errno'] != 0):
                    return {"errno": 7, "err_msg": pwd_result['err_msg'], "extra": "", "info": ""}
                else:
                    pwd = pwd_result['pwd']
            referer = share_res.url
            verify_result = self.verifyShare(surl, bdstoken, pwd, referer)
            if (verify_result['errno'] != 0):
                return {"errno": 8, "err_msg": verify_result['err_msg'], "extra": "", "info": ""}
            else:
                # 加密分享验证通过后，使用全局session刷新页面（全局session中带有解密的Cookie）
                share_res = self.session.get(url, headers=self.headers)
                share_page = share_res.content.decode("utf-8")
        # 更新bdstoken，有时候会出现 AttributeError: 'NoneType' object has no attribute 'group'，重试几次就好了
        share_data = json.loads(re.search("yunData.setData\(({.*})\)", share_page).group(1))
        bdstoken = share_data['bdstoken']
        shareid = share_data['shareid']
        _from = share_data['uk']
        '''
        构造转存的URL，除了logid不知道有什么用，但是经过验证，固定值没问题，其他变化的值均可在验证通过的页面获取到
        '''
        save_url = 'https://pan.baidu.com/share/transfer?shareid=%s&from=%s&ondup=newcopy&async=1&channel=chunlei&web=1&app_id=250528&bdstoken=%s\
               &logid=MTU3MjM1NjQzMzgyMTAuMjUwNzU2MTY4MTc0NzQ0MQ==&clienttype=0' % (shareid, _from, bdstoken)
        file_list = share_data['file_list']['list']
        form_data = {
            # 这个参数一定要注意，不能使用['fs_id', 'fs_id']，谨记！
            'fsidlist': '[' + ','.join([str(item['fs_id']) for item in file_list]) + ']',
            'path': path,
        }
        headers = self.headers
        headers['Origin'] = 'https://pan.baidu.com'
        headers['referer'] = url
        '''
        用带登录Cookie的全局session请求转存
        如果有同名文件，保存的时候会自动重命名：类似xxx(1)
        暂时不支持超过文件数量的文件保存
        '''
        save_res = self.session.post(save_url, headers=headers, data=form_data)
        save_json = save_res.json()
        errno, err_msg, extra, info = (0, '转存成功', save_json['extra'], save_json['info']) if (
                    save_json['errno'] == 0) else (9, '转存失败：%d' % save_json['errno'], '', '')
        return {'errno': errno, 'err_msg': err_msg, "extra": extra, "info": info}
bbbb = BaiDuPan()
bbbb.saveShare('https://pan.baidu.com/s/1Mozs9rLxerrs7e5itBtSTQ', 'p6kk', path='/')