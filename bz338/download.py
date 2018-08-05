"""
根据redis数据库db=2中的内容，下载保存数据到db3
"""
import os
import redis
import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString
import re
import random
from urllib.parse import urlparse
import time
import json
from requests.exceptions import ConnectTimeout, HTTPError, BaseHTTPError, ConnectionError

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive=false",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}

DETAIL_KEYWORD = {
    "类别": "Category",
    "法规类别": "Category",
    "发文字号": "DocumentNO",
    "效力级别": "Effectiveness",
    "实施日期": "ImplementDate",
    "发布日期": "IssueDate",
    "发布部门": "IssueDepartment",
    "批准日期": "RatifyDate",
    "批准部门": "RatifyDepartment",
    "时效性": "Timeliness"
}


def extract_detial(trs):
    data = dict()
    titles = trs[0].find_all("span")
    data["Title"] = titles[0].get_text().strip()
    if len(titles) == 2:
        data["TitleEN"] = titles[-1].get_text().strip()
    # 处理除标题、正文外的信息到data字典中
    for tr in trs[1:]:
        tds = tr.find_all("td")
        for td in tds:
            chinese_keywords = re.findall("【(.*?)】", td.decode())
            for ck in chinese_keywords:
                if ck in DETAIL_KEYWORD.keys():
                    text = td.text.strip()
                    txt = text[2 + len(ck):].strip()
                    data.__setitem__(DETAIL_KEYWORD[ck], txt)
    # 剔除法宝联想标签
    if len(trs[-1].find_all("div", {"class", "TiaoYinV2"})):
        for _ in trs[-1].find_all("div", {"class", "TiaoYinV2"}):
            _.decompose()
    # 保存法宝引证码 再剔除
    if len(trs[-1].find_all("table")):
        clis = trs[-1].find_all("table")[0].find_all("a")
        if len(clis):
            data["CLI"] = clis[-1].get_text().strip()
        trs[-1].find_all("table")[0].decompose()
    # 保存法律变迁史
    if len(trs[-1].find_all("font", {"class", "TiaoYin"})):
        law_change = []
        base_cli_list = data["CLI"].split(".")
        remove_br_a = trs[-1].find_all("font", {"class", "TiaoYin"})[0].find_next_siblings()
        trs[-1].find_all("font", {"class", "TiaoYin"})[0].decompose()
        for _ in remove_br_a:
            if _.name == "br":
                _.decompose()
            elif _.name == "a":  # 本法变迁的a标签
                js_href = _.get("href")
                cli_num = re.findall("\d+", js_href)
                if len(cli_num):
                    law_change_cli = "".join(_ + "." for _ in base_cli_list[:-1])  # 通过本法CLI拼凑完整变迁法CLI
                    law_change.append((_.text.strip(), law_change_cli + cli_num[0]))
                _.decompose()
            elif _.name == "p" or _.name == "div":
                break
        data["law_change"] = law_change
    # 记录法宝联想的text后剔除
    remove_fblxs = []
    if len(trs[-1].find_all("font", {"class", "FBLXTITLE"})):
        for fblx in trs[-1].find_all("font", {"class", "FBLXTITLE"}):
            lx = ""
            if isinstance(fblx.previous_sibling, NavigableString):
                if "（" in fblx.previous_sibling.string.strip("\n"):
                    lx += fblx.previous_sibling
            for fblx_next in fblx.next_elements:
                if isinstance(fblx_next, NavigableString):
                    if "）" in fblx_next.strip():
                        # 法宝联想结束
                        lx += fblx_next
                        break
                    else:
                        lx += fblx_next
            remove_fblxs.append(lx)
    text = trs[-1].text
    if remove_fblxs:
        for fblx in remove_fblxs:
            if text.find(fblx) >= 0:
                index = text.find(fblx)
                text = text[:index] + text[index + len(fblx):]
    data["FullText"] = text.strip("\n")
    # 正文中嵌入图片、有附件情况 记录在日志中
    if len(trs[-1].find_all("img")):
        print("{0}:{1}".format(str(data), trs[-1].find_all("img")))
    elif trs[-1].find_all("a", {"class": "fjLink"}):
        print("{0}:{1}".format(str(data), trs[-1].find_all("a", {"class": "fjLink"})))
    return data


if __name__ == "__main__":
    cnt = 0
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive=false",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    while True:
        db2 = redis.StrictRedis(host="localhost", port=6379, db=2)
        db2_keys2 = db2.keys()
        k = eval(db2_keys2[random.randint(0, len(db2_keys2) - 1)])
        if os.path.exists(os.path.join("F:\\data", k["name"])) is not True:
            os.mkdir(os.path.join("F:\\data\\", k["name"]))
        k_length = db2.llen(k)
        for times in range(k_length):
            db1 = redis.StrictRedis(host="localhost", port=6379, db=1)
            u = db1.keys()[-1].decode()  # url
            c = db1.get(u).decode()  # cookies
            # db9 = redis.StrictRedis(host="localhost", port=6379, db=9)
            # k = db9.keys()
            # u, c = None, None
            # if k:
            #     uc = eval(db9.get(k[0]).decode())
            #     u = uc["current_url"]
            #     c = uc["Cookie"][-1]
            url_parse = urlparse(u)
            host = url_parse.netloc
            headers["Host"] = host
            headers["Referer"] = u
            headers["Cookie"] = c
            value = eval(db2.lpop(k))
            url = "http://" + host + "/" + value["href"]
            try:
                rsp = requests.get(url, headers=headers)
                if rsp.status_code == 200:
                    title = re.sub('[\\\/:*?"<>|]', '', value["title"])
                    # et = etree.HTML(rsp.text)
                    # txt = et.xpath('//table[@id="tbl_content_main"]//tr//text()')
                    soup = BeautifulSoup(rsp.text, "lxml")
                    table = soup.find_all(id="tbl_content_main")
                    if table is None or len(table) == 0:
                        continue
                    trs = [_ for _ in table[0].children if _.name == "tr"]
                    if len(trs):
                        for i in range(len(trs) - 1, -1, -1):
                            if trs[i].text.strip() == "":
                                trs = trs[:i]
                                break
                        data = extract_detial(trs)
                        with open(os.path.join("F:\\data", k["name"],
                                               title + ".json"),
                                  "w",
                                  encoding="utf-8") as ff:
                            ff.write(json.dumps(data, ensure_ascii=False))
                            cnt += 1
                        print(cnt, k["name"], value["title"])
                    else:
                        print(rsp.status_code, rsp.text)
                else:
                    print(rsp.status_code)
                    continue
                time.sleep(random.random())
                rsp.close()
            except ConnectTimeout as ct:
                print(ct)
                continue
            except (HTTPError, BaseHTTPError) as he:
                print(he)
                continue
            except ConnectionError as ce:
                print(ce)
                continue
