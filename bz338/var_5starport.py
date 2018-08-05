"""
从各个入口进入北大法宝
"""
import redis
import requests
import re
import time
import datetime
from requests.exceptions import HTTPError, BaseHTTPError, ConnectionError, ConnectTimeout

base_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}


# 老代码
# def var_5star_step1():
#     cookies = get_cookie("xxtp", "metasota")
#     userid = re.findall("esybrmluserid=(.*?);", cookies)
#     if len(userid):
#         userid = userid[0]
#     zhuangchu_url = "http://www.bz338.com/e/rk/zhuangchu.php?zhongwenaddid=1576&zhongwenid=48&bclassid=64&userid=" + userid
#     headers = base_headers.copy()
#     headers["Host"] = "www.bz338.com"
#     headers["Referer"] = "http://www.bz338.com/e/action/ListInfo/?classid=73"
#     headers["Cookie"] = cookies
#     return requests.get(zhuangchu_url, headers=headers).status_code
#
#
# def var_5star_step2():
#     if var_5star_step1() == 200:
#         headers = base_headers.copy()
#         headers["Host"] = "202.121.166.131:9155"
#         headers[
#             "Referer"] = "http://www.bz338.com/e/rk/zhuangchu.php?zhongwenaddid=1576&zhongwenid=48&bclassid=64&userid=27187"
#         cookies = "CheckIPAuto=0;FWinCookie=1;Hm_lvt_58c470ff9657d300e66c7f33590e53a8="
#         cookies += str(int(time.time()))
#         cookies += ";" + "CheckIPDate=" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         headers["Cookie"] = cookies
#         rsp = requests.get("http://202.121.166.131:9155/vip_login/CheckLogin.ashx?t=1&n=1532330407331&menu_item=law",
#                            headers=headers, stream=True)
#         if rsp.status_code == 200:
#             return rsp.cookies.get_dict()
#     return None
#
#
# def var_5star_step22():
#     if var_5star_step2():
#         cookies = "SSLHTTPSESSIONID=" + var_5star_step2()["SSLHTTPSESSIONID"]
#         headers = base_headers.copy()
#         headers["Host"] = "202.121.166.131:9155"
#         headers[
#             "Referer"] = "http://202.121.166.131:9155/vip_login/CheckLogin.ashx?t=1&n=1532330407331&menu_item=law"
#         headers["Cookie"] = cookies
#         url = "http://202.121.166.131:9155/vip_login/CheckLogin.ashx?t=3&n=##n##&menu_item=law".replace("##n##", str(
#             int(time.time())))
#         rsp = requests.get(url, stream=True, headers=headers)
#         if rsp.status_code == 200:
#             # return rsp.cookies.get_dict()
#             return rsp
#     return None
class var_5star():
    @staticmethod
    def get_cookie(username, password):
        r = redis.StrictRedis(host="localhost", port=6379, db=0)
        cookie = (r.get({'username': username, 'password': password})).decode()
        return cookie

    def __init__(self, username, password):
        self.session = requests.Session()
        self.bz338_cookie = self.get_cookie(username, password)
        self.userid = re.findall("esybrmluserid=(.*?);", self.bz338_cookie)[0]

    def _zhuangchu_s1(self):
        # 判断是否成功跳入了zhuangchu.php页面
        headers1 = base_headers.copy()
        headers1["Cookie"] = self.bz338_cookie
        headers1["Host"] = "www.bz338.com"
        headers1["Referer"] = "http://www.bz338.com/e/action/ListInfo/?classid=73"
        try:
            rsp1 = self.session.get(
                "http://www.bz338.com/e/rk/zhuangchu.php",
                params={"zhongwenaddid": 1576, "zhongwenid": 48, "bclassid": 64, "userid": self.userid},
                headers=headers1)
            return rsp1.status_code
        except ConnectTimeout as ct:
            print(ct)
        except (HTTPError, BaseHTTPError) as he:
            print(he)
        except ConnectionError as ce:
            print(ce)
        return False

    def _fdslogin_s2(self):
        # 关键一步：模仿点击alert的操作，跳转华东政法的IP
        if self._zhuangchu_s1():
            headers2 = base_headers.copy()
            headers2["Host"] = "202.121.166.131:9000"
            headers2[
                "Referer"] = "http://www.bz338.com/e/rk/zhuangchu.php?zhongwenaddid=1576&zhongwenid=48&bclassid=64&userid=" + self.userid
            headers2["Cookie"] = "FWinCookie=1;click0=" + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            try:
                rsp2 = self.session.get("http://202.121.166.131:9000/login.fds",
                                        params={"user": "151040108", "pass": "151040108"},
                                        headers=headers2)
                if rsp2.status_code == 200:
                    return rsp2
            except ConnectTimeout as ct:
                print(ct)
            except (HTTPError, BaseHTTPError) as he:
                print(he)
            except ConnectionError as ce:
                print(ce)
        return False

    def _cluster_s3(self):
        # 获取ASP.NET_SessionId、SSLHTTPSESSIONID
        if self._fdslogin_s2():
            headers3 = base_headers.copy()
            headers3["Host"] = "202.121.166.131:9155"
            headers3[
                "Referer"] = "http://www.bz338.com/e/rk/zhuangchu.php?zhongwenaddid=1576&zhongwenid=48&bclassid=64&userid=" + self.userid
            try:
                rsp3 = self.session.get(
                    "http://202.121.166.131:9155/cluster_call_form.aspx?menu_item=law&EncodingName=&key_word=",
                    headers=headers3)
                if rsp3.status_code == 200:
                    return rsp3
            except ConnectTimeout as ct:
                print(ct)
            except (HTTPError, BaseHTTPError) as he:
                print(he)
            except ConnectionError as ce:
                print(ce)
        return False

    def _checklg_s4(self):
        # 获取cookies中的CookieId、CheckIPAuto、CheckIPDate、XXXXIPLogin、User_User
        if self._cluster_s3():
            headers4 = base_headers.copy()
            headers4["Host"] = "202.121.166.131:9155"
            headers4["Referer"] = "http://202.121.166.131:9155/vip_login/vip_login.aspx?menu_item=law&EncodingName="
            try:
                rsp4 = self.session.get("http://202.121.166.131:9155/vip_login/CheckLogin.ashx",
                                        params={"t": "3", "n": int(time.time() * 1000), "menu_item": "law"},
                                        headers=headers4)
                if rsp4.status_code == 200:
                    return rsp4
            except ConnectTimeout as ct:
                print(ct)
            except (HTTPError, BaseHTTPError) as he:
                print(he)
            except ConnectionError as ce:
                print(ce)
        return False

    def combin_cookie(self):
        if self._checklg_s4():
            Cookie = ""
            c1 = self._cluster_s3().cookies.get_dict()
            c2 = self._checklg_s4().cookies.get_dict()
            for k, v in c1.items():
                Cookie += k + "=" + v + ";"
            for k, v in c2.items():
                Cookie += k + "=" + v + ";"
            return [self._cluster_s3().url, Cookie[:-1]]
        return False

    def save_2redis(self):
        cu = self.combin_cookie()
        if cu:
            r = redis.StrictRedis(host="localhost", port=6379, db=1)
            r.set(cu[0], cu[-1])


# def var_5star():
#     session = requests.Session()
#     cookie = get_cookie("xxtp", "metasota")
#     # 判断是否跳入了zhuangchu.php页面
#     userid = re.findall("esybrmluserid=(.*?);", cookie)
#     if len(userid):
#         userid = userid[0]
#     headers1 = base_headers.copy()
#     headers1["Cookie"] = cookie
#     headers1["Host"] = "www.bz338.com"
#     headers1["Referer"] = "http://www.bz338.com/e/action/ListInfo/?classid=73"
#     rsp1 = session.get(
#         "http://www.bz338.com/e/rk/zhuangchu.php",
#         params={"zhongwenaddid": 1576, "zhongwenid": 48, "bclassid": 64, "userid": userid},
#         headers=headers1)
#     print(rsp1.status_code)
#     #
#     headers2 = base_headers.copy()
#     headers2["Host"] = "202.121.166.131:9000"
#     headers2[
#         "Referer"] = "http://www.bz338.com/e/rk/zhuangchu.php?zhongwenaddid=1576&zhongwenid=48&bclassid=64&userid=27187"
#     headers2["Cookie"] = "FWinCookie=1;click0=" + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
#     rsp2 = session.get("http://202.121.166.131:9000/login.fds", params={"user": "151040108", "pass": "151040108"},
#                        headers=headers2)
#     print(rsp2.status_code, rsp2.cookies.get_dict(), rsp2.text)
#     #
#     headers3 = base_headers.copy()
#     headers3["Host"] = "202.121.166.131:9155"
#     headers3[
#         "Referer"] = "http://www.bz338.com/e/rk/zhuangchu.php?zhongwenaddid=1576&zhongwenid=48&bclassid=64&userid=27187"
#     rsp3 = session.get("http://202.121.166.131:9155/cluster_call_form.aspx?menu_item=law&EncodingName=&key_word=",
#                        headers=headers3)
#     rsp3_cookies = rsp3.cookies.get_dict()
#     #
#     headers4 = base_headers.copy()
#     headers4["Host"] = "202.121.166.131:9155"
#     headers4["Referer"] = "http://202.121.166.131:9155/vip_login/vip_login.aspx?menu_item=law&EncodingName="
#     rsp4 = session.get("http://202.121.166.131:9155/vip_login/CheckLogin.ashx",
#                        params={"t": "3", "n": int(time.time() * 1000), "menu_item": "law"}, headers=headers4)
#     rsp4_cookies = rsp4.cookies.get_dict()


# def test_url():
#     headers_t = base_headers.copy()
#     headers_t["Host"] = "202.121.166.131:9155"
#     headers_t["Referer"] = "http://202.121.166.131:9155/cluster_call_form.aspx?menu_item=law&EncodingName=&key_word="


if __name__ == "__main__":
    while True:
        var5 = var_5star("xxtp", "metasota")
        var5.save_2redis()
        cu = var5.combin_cookie()
        if cu:
            print("current_url cookie:", cu)
            time.sleep(1800)
        continue
