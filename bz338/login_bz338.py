"""
登陆到bz338网站
"""
import requests
import redis
import time
import random
from requests.exceptions import HTTPError, BaseHTTPError, ConnectionError, ConnectTimeout

base_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Host": "www.bz338.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}


# Cookies  Origin Referer
class bz338():

    def __init__(self, un, pwd):
        self.username = un
        self.password = pwd

    def doaction_login(self):
        form_data = {
            "enews": "login",
            "lifetime": "315360000",
            "username": self.username,
            "password": self.password
        }
        headers = base_headers
        headers["Origin"] = "http://www.bz338.com"
        headers["Referer"] = "http://www.bz338.com/e/member/login/"
        try:
            rsp = requests.post("http://www.bz338.com/e/member/doaction.php", data=form_data, headers=headers)
            if rsp.status_code == 200:
                Cookies = ""
                for k, v in rsp.cookies.items():
                    Cookies += k + "=" + v + ";"
                return {"status_code": rsp.status_code,
                        "cookies": Cookies[:-1]
                        }
        except ConnectTimeout as ct:
            print(ct)
        except (HTTPError, BaseHTTPError) as he:
            print(he)
        except ConnectionError as ce:
            print(ce)
        return False

    def bdfb_login(self):
        if self.doaction_login():
            doaction_login_return = self.doaction_login()
            if doaction_login_return["status_code"] == 200 and len(doaction_login_return["cookies"]) > 0:
                url = "http://www.bz338.com/e/action/ListInfo/?classid=73"
                headers = base_headers
                headers["Referer"] = "http://www.bz338.com/e/action/ListInfo/?classid=64"
                headers["Cookie"] = doaction_login_return["cookies"]
                try:
                    rsp = requests.get(url, headers=headers)
                    if rsp.status_code == 200:
                        return True
                except ConnectTimeout as ct:
                    print(ct)
                except (HTTPError, BaseHTTPError) as he:
                    print(he)
                except ConnectionError as ce:
                    print(ce)
        return False

    def save_2redis(self):
        r = redis.StrictRedis(host="localhost", port=6379, db=0)
        unpwd = {"username": self.username, "password": self.password}
        if self.bdfb_login():
            Cookie = self.doaction_login()["cookies"]
            r.set(unpwd, Cookie)
            return True
        return False


if __name__ == "__main__":
    while True:
        un = "xxtp"
        pwd = "metasota"
        b38 = bz338(un, pwd)
        rts = b38.doaction_login()
        if rts:
            print(rts)
            lg = b38.bdfb_login()
            if lg:
                print("bdfb_login:", lg)
                s2r = b38.save_2redis()
                if s2r:
                    print("save_2redis:", s2r)
                    time.sleep(3600)
        time.sleep(random.random() * 40)
        continue
