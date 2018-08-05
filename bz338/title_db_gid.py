"""
获取每种类别的page_count
查询doSearch.ashx，获得
"""
from urllib.parse import quote, urlparse
import redis
import requests
from lxml import etree
import time
import random
from bs4 import BeautifulSoup
import re
import math
from requests.exceptions import ConnectTimeout, HTTPError, BaseHTTPError, ConnectionError

base_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}


def get_page_count(Db=None, menu_item=None, clusterwhere=None, others=None):
    # 根据 Db menu_item clust_param others 的字段信息，构造URL，获取特定数据库中的小类别的page_count
    r = redis.StrictRedis(host="localhost", port=6379, db=1)
    referer = r.keys()[-1].decode()
    cookie = r.get(r.keys()[-1]).decode()
    uo = urlparse(referer)
    url = uo.scheme + "://" + uo.netloc + "/doSearch.ashx"
    headers = base_headers.copy()
    headers["Host"] = uo.hostname
    headers["Referer"] = referer
    headers["Cookie"] = cookie
    param = {"Db": Db, "clusterwhere": quote(clusterwhere), "clust_db": Db, "range": "name",
             "menu_item": menu_item}
    try:
        rsp = requests.post(url, data=param, headers=headers, timeout=240)
        if rsp.status_code == 200:
            html = rsp.text
            bs = BeautifulSoup(html, "lxml")
            pcs = bs.find_all(string=re.compile("共找到"))
            if len(pcs):
                page_count = re.findall("\d+", pcs[0].replace("\xa0", " "))[0]
                rsp.close()
                return page_count
    except ConnectTimeout as ct:
        print(ct)
    except (HTTPError, BaseHTTPError) as he:
        print(he)
    except (ConnectionRefusedError, ConnectionError, ConnectionAbortedError) as ce:
        print(ce)
    return None


def get_title_gid(name=None, Db=None, menu_item=None, clusterwhere=None, page_count=None):
    # 根据参数获得各个法律条文的title gid
    r = redis.StrictRedis(host="localhost", port=6379, db=1)
    referer = r.keys()[-1].decode()
    cookie = r.get(r.keys()[-1]).decode()
    uo = urlparse(referer)
    url = uo.scheme + "://" + uo.netloc + "/doSearch.ashx"
    #
    param = {
        "range": "name",
        "check_hide_xljb": "1",
        "check_gaojijs": "1",
        "orderby": quote("发布日期"),
    }
    param["Db"] = Db
    param["clust_db"] = Db
    param["clusterwhere"] = quote(clusterwhere)
    param["page_count"] = page_count
    param["menu_item"] = menu_item
    #
    headers = base_headers.copy()
    headers["Cookie"] = cookie
    headers["Referer"] = referer
    headers["Host"] = uo.hostname
    #
    total_page_nums = int(math.ceil(int(page_count) / 40))
    db3 = redis.StrictRedis(host="localhost", port=6379, db=3)
    downloaded_page_nums = total_page_nums - 1
    if db3.exists({"name": name, "Db": Db, "menu_item": menu_item, "clusterwhere": clusterwhere}):
        downloaded_page_nums = db3.get(
            {"name": name, "Db": Db, "menu_item": menu_item, "clusterwhere": clusterwhere}).decode()
    #
    r_db2 = redis.StrictRedis(host="localhost", port=6379, db=2, encoding="utf-8")
    for i in range(int(downloaded_page_nums), -1, -1):
        param["aim_page"] = i
        try:
            rsp = requests.post(url, data=param, headers=headers)
            if rsp.status_code == 200:
                html = rsp.text
                et = etree.HTML(html)
                t_gids = et.xpath('//div[@id="dir_sub_div"]//a[@class="main-ljwenzi"]')
                for _ in t_gids:
                    r_db2.rpush({"name": name, "Db": Db, "menu_item": menu_item, "clusterwhere": clusterwhere},
                                {"title": _.text, "href": _.get("href")})
                    print(name, _.text, _.get("href"))
                time.sleep(random.random())
                continue
            else:
                print(rsp.status_code, rsp.text)
            rsp.close()
        except ConnectTimeout as ct:
            print(ct)
        except (HTTPError, BaseHTTPError) as he:
            print(he)
        except ConnectionError as ce:
            print(ce)
        finally:
            # 保留已下载记录
            db3 = redis.StrictRedis(host="localhost", port=6379, db=3)
            db3.set({"name": name, "Db": Db, "menu_item": menu_item, "clusterwhere": clusterwhere},
                    i)


if __name__ == "__main__":
    clust = [
        {"name": "法律", "clust_param": "0/XA01", "Db": "chl", "menu_item": "law", "clusterwhere": "效力级别=XA01"},
        {"name": "行政法规 ", "clust_param": "0/XC02", "Db": "chl", "menu_item": "law", "clusterwhere": "效力级别=XC02"},
        {"name": "司法解释", "clust_param": "0/XG04", "Db": "chl", "menu_item": "law", "clusterwhere": "效力级别=XG04"},
        {"name": "部门规章", "clust_param": "0/XE03", "Db": "chl", "menu_item": "law", "clusterwhere": "效力级别=XE03"},
        {"name": "团体规定", "clust_param": "0/XI05", "Db": "chl", "menu_item": "law", "clusterwhere": "效力级别=XI05"},
        {"name": "行业规定", "clust_param": "0/XK06", "Db": "chl", "menu_item": "law", "clusterwhere": "效力级别=XK06"},
        {"name": "军事法规规章", "clust_param": "0/XQ09 ", "Db": "chl", "menu_item": "law", "clusterwhere": "XA01"},
        {"name": "地方性法规", "clust_param": "0/XM07", "Db": "lar", "menu_item": "law", "clusterwhere": "效力级别=XM07"},
        {"name": "地方政府规章", "clust_param": "0/XO08", "Db": "lar", "menu_item": "law", "clusterwhere": "效力级别=XO08"},
        {"name": "地方规范性文件", "clust_param": " 0/XP08", "Db": "lar", "menu_item": "law", "clusterwhere": "效力级别=XP08"},
        {"name": "地方司法文件", "clust_param": "0/XP09", "Db": "lar", "menu_item": "law", "clusterwhere": "效力级别=XP09"},
        {"name": "地方工作文件", "clust_param": "0/XP10", "Db": "lar", "menu_item": "law", "clusterwhere": "效力级别=XP10"},
        {"name": "行政许可复批", "clust_param": "0/XP11", "Db": "lar", "menu_item": "law", "clusterwhere": "效力级别=XP11"},
        {"name": "征求意见", "clust_param": "3/091001", "Db": "protocol", "menu_item": "lfbj_all",
         "clusterwhere": "类别=091001"},
        {"name": "草案及其说明", "clust_param": "3/091002", "Db": "protocol", "menu_item": "lfbj_all",
         "clusterwhere": "类别=091002"},
        {"name": "审议意见", "clust_param": "3/091003", "Db": "protocol", "menu_item": "lfbj_all",
         "clusterwhere": "类别=091003"},
        {"name": "立法草案_其他", "clust_param": "3/091001", "Db": "protocol", "menu_item": "lfbj_all",
         "clusterwhere": "类别=091001"},
        {"name": "问答", "clust_param": "3/093001", "Db": "lawexplanation", "menu_item": "lfbj_all",
         "clusterwhere": "类别=093001"},
        {"name": "解读", "clust_param": "3/093002", "Db": "lawexplanation", "menu_item": "lfbj_all",
         "clusterwhere": "类别=093002"},
        {"name": "理解与适用", "clust_param": "3/093003", "Db": "lawexplanation", "menu_item": "lfbj_all",
         "clusterwhere": "类别=093003"},
        {"name": "法规解读_其他", "clust_param": "3/093004", "Db": "lawexplanation", "menu_item": "lfbj_all",
         "clusterwhere": "类别=093004"},
        {"name": "全国人大常委会工作报告", "clust_param": "1/090001", "Db": "workreport", "menu_item": "lfbj_all",
         "clusterwhere": "类别=090001"},
        {"name": "全国人大常委会执法检查", "clust_param": "1/090002", "Db": "workreport", "menu_item": "lfbj_all",
         "clusterwhere": "类别=090002"},
        {"name": "国务院政府工作报告", "clust_param": "1/090003", "Db": "workreport", "menu_item": "lfbj_all",
         "clusterwhere": "类别=090003"},
        {"name": "最高人民法院工作报告", "clust_param": "1/090004", "Db": "workreport", "menu_item": "lfbj_all",
         "clusterwhere": "类别=090004"},
        {"name": "最高人民检察院工作报告", "clust_param": "1/090005", "Db": "workreport", "menu_item": "lfbj_all",
         "clusterwhere": "类别=090005"},
        {"name": "地方政府工作报告", "clust_param": "1/090006", "Db": "workreport", "menu_item": "lfbj_all",
         "clusterwhere": "类别=090006"}
    ]
    while True:
        _ = clust[random.randint(0, len(clust) - 1)]
        pc = get_page_count(Db=_["Db"], menu_item=_["menu_item"],
                            clusterwhere=_["clusterwhere"])
        time.sleep(random.random() * 10)
        if pc:
            get_title_gid(name=_["name"], Db=_["Db"], menu_item=_["menu_item"],
                          clusterwhere=_["clusterwhere"], page_count=pc)
            time.sleep(random.random() * 10)
        time.sleep(random.randint(10, 30))
        continue
