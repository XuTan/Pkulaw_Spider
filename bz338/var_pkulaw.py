"""

通过正规北大法宝官方网站的账号
获取登录状态

"""

import requests
import re
import time
import datetime
import random
import redis
from requests.exceptions import HTTPError, BaseHTTPError, ConnectionError, ConnectTimeout

base_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}

HEADERS_Host = "www.pkulaw.cn"


class var_pkulaw:

    def __init__(self, username, password):
        self.session = requests.Session()
        self.username = username
        self.password = password

    def _pkulaw_s1(self):
        headers1 = base_headers.copy()
        headers1["Host"] = HEADERS_Host
        try:
            rsp1 = self.session.get(
                "http://www.pkulaw.cn/",
                headers=headers1)
            if rsp1.status_code == 200:
                return rsp1
        except ConnectTimeout as ct:
            print("except in var_pkulaw,_pkulaw_s1", ct)
        except (HTTPError, BaseHTTPError) as he:
            print("except in var_pkulaw,_pkulaw_s1", he)
        except ConnectionError as ce:
            print("except in var_pkulaw,_pkulaw_s1", ce)

        return False

    def _clust_s2(self):
        if self._pkulaw_s1():
            headers2 = base_headers.copy()
            headers2["Host"] = HEADERS_Host
            headers2["Referer"] = "http://www.pkulaw.cn/"
            try:
                rsp2 = self.session.get("http://www.pkulaw.cn/cluster_call_form.aspx",
                                        params={"menu_item": "law", "EncodingName": "", "key_word": ""},
                                        headers=headers2)
                if rsp2.status_code == 200:
                    return rsp2
            except ConnectTimeout as ct:
                print("except in var_pkulaw,_clust_s2", ct)
            except (HTTPError, BaseHTTPError) as he:
                print("except in var_pkulaw,_clust_s2", he)
            except ConnectionError as ce:
                print("except in var_pkulaw,_clust_s2", ce)
        return False

    def _viplogin_s3(self):
        # 获取ASP.NET_SessionId、SSLHTTPSESSIONID
        if self._clust_s2():
            headers3 = base_headers.copy()
            headers3["Host"] = HEADERS_Host
            headers3[
                "Referer"] = "http://www.pkulaw.cn/cluster_call_form.aspx?menu_item=law&EncodingName=&key_word="
            try:
                rsp3 = self.session.get(
                    "http://www.pkulaw.cn/vip_login/vip_login.aspx", params={"menu_item": "law", "EncodingName": ""},
                    headers=headers3)
                if rsp3.status_code == 200:
                    return rsp3
            except ConnectTimeout as ct:
                print("except in var_pkulaw,_viplogin_s3", ct)
            except (HTTPError, BaseHTTPError) as he:
                print("except in var_pkulaw,_viplogin_s3", he)
            except ConnectionError as ce:
                print("except in var_pkulaw,_viplogin_s3", ce)
        return False

    def _checklg_s4(self):
        # 获取cookies中的CookieId、CheckIPAuto、CheckIPDate、XXXXIPLogin、User_User
        if self._viplogin_s3():
            headers4 = base_headers.copy()
            headers4["Host"] = HEADERS_Host
            headers4["Referer"] = "http://www.pkulaw.cn/vip_login/vip_login.aspx?menu_item=law&EncodingName="
            try:
                rsp4 = self.session.get("http://www.pkulaw.cn/vip_login/CheckLogin.ashx",
                                        params={"t": "1", "u": self.username, "p": self.password,
                                                "n": int(time.time() * 1000), "menu_item": "law"},
                                        headers=headers4)
                if "对不起" in rsp4.text:
                    return False
                elif rsp4.status_code == 200 and self.username in rsp4.text:
                    return rsp4
            except ConnectTimeout as ct:
                print("except in var_pkulaw,_checklg_s4", ct)
            except (HTTPError, BaseHTTPError) as he:
                print("except in var_pkulaw,_checklg_s4", he)
            except ConnectionError as ce:
                print("except in var_pkulaw,_checklg_s4", ce)
        return False

    def _combin_cookie(self):
        if self._checklg_s4():
            Cookie = ""
            c = self._checklg_s4().cookies.get_dict()
            for k, v in c.items():
                Cookie += k + "=" + v + ";"
            return [self._clust_s2().url, Cookie[:-1]]
        return False

    def _save_2redis(self):
        if self._checklg_s4():
            cookie = self._combin_cookie()
            if cookie:
                r9 = redis.StrictRedis(host="localhost", port=6379, db=9)
                r9.set("PKULAW_STATUS", {"current_url": self._clust_s2().url, "Cookie": cookie})
                return cookie
        return False

    def run_var_pkulaw(self):
        while True:
            var_pku = var_pkulaw(self.username, self.password)
            cookies_get = var_pku._save_2redis()
            if cookies_get:
                print(cookies_get)
                time.sleep(1800)
            else:
                print("fail ", cookies_get, time.time())
                time.sleep(random.random() * 10)


if __name__ == "__main__":
    v = var_pkulaw("caishiyue", "19941115csy")
    v.run_var_pkulaw()
