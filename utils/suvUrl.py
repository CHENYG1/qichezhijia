import requests
from SUV_Spider.utils.db_tools import *
from SUV_Spider.utils.operater import *
from lxml import etree
import time
import random

"""
获取SUV车系存入series_url_list
车型的URL 存入car_url_list
"""
headers1 = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/64.0.3282.186 Safari/537.36"}


# https://car.autohome.com.cn/price/list-0-101-0-0-0-0-0-0-0-0-0-0-0-0-0-1.html 轿车 23页
# https://car.autohome.com.cn/price/list-0-9-0-0-0-0-0-0-0-0-0-0-0-0-0-{}.html suv 32页
# https://car.autohome.com.cn/price/list-0-7-0-0-0-0-0-0-0-0-0-0-0-0-0-1.html 跑车 4页

# 请求系列
def get_series_url(tablename,carlevel):
    urlconfig={
        "suv":{
            "url":"https://car.autohome.com.cn/price/list-0-9-0-0-0-0-0-0-0-0-0-0-0-0-0-{}.html",
            "pagecount":32
        },
        "car":{
            "url":"https://car.autohome.com.cn/price/list-0-101-0-0-0-0-0-0-0-0-0-0-0-0-0-{}.html",
            "pagecount":23
        },
        "roadster": {
            "url": "https://car.autohome.com.cn/price/list-0-7-0-0-0-0-0-0-0-0-0-0-0-0-0-{}.html",
            "pagecount":4
        }
    }
    pagecount = urlconfig[carlevel]["pagecount"]
    baseUrl = urlconfig[carlevel]["url"]
    series_count = 0 #计算本次爬取记录总数
    insert_count = 0 #计算本次新增总数
    pass_count = 0 #计算本次跳过记录数即已经存在的记录数
    for i in range(1, pagecount):  # 总共有xx页
        url = baseUrl.format(i)
        try:
            fileorigin = requests.get(url, headers=headers1)
            fileorigin.encoding = 'UTF-8'
            req1 = fileorigin.text
            soup = etree.HTML(req1)
            urlxptext = '//*[@id="brandtab-1"]/div/div/div[2]/div[1]/a/@href'
            urlconfig = soup.xpath(urlxptext)
            fileorigin.encoding = 'gb2312'
            req2 = fileorigin.text
            soup = etree.HTML(req2)
            namexptext = '//*[@id="brandtab-1"]/div/div/div[2]/div[1]/a/text()'
            nameconfig = soup.xpath(namexptext)
            series_count += len(urlconfig)
            for j in range(len(urlconfig)):
                record = {
                    "seriesname":nameconfig[j],
                    "seriesurl":"https://car.autohome.com.cn"+urlconfig[j]
                }
                if is_exist(record,tablename):
                    pass_count += 1
                    continue
                else:
                    insert_count += 1
                    insert(tablename,record)
            process_bar((i+1) / pagecount, start_str='', end_str="100%", total_length=pagecount)  # 进度条
            time.sleep(random.randint(1, 3))
        except Exception as e:
            writeLog("【抓取车系错误】页数-"+str(i)+"错误信息为"+str(e))

    return {
        "insert_count": insert_count,
        "pass_count": pass_count,
        "series_count": series_count
    }


def update_series_url(tablename,carlevel,page):
    urlconfig={
        "suv":{
            "url":"https://car.autohome.com.cn/price/list-0-9-0-0-0-0-0-0-0-0-0-0-0-0-0-{}.html",
            "pagecount":32
        },
        "car":{
            "url":"https://car.autohome.com.cn/price/list-0-101-0-0-0-0-0-0-0-0-0-0-0-0-0-{}.html",
            "pagecount":23
        },
        "roadster": {
            "url": "https://car.autohome.com.cn/price/list-0-7-0-0-0-0-0-0-0-0-0-0-0-0-0-{}.html",
            "pagecount":4
        }
    }
    if page=='':
        page = 1
    baseUrl = urlconfig[carlevel]["url"]
    series_count = 0 #计算本次爬取记录总数
    insert_count = 0 #计算本次新增总数
    pass_count = 0 #计算本次跳过记录数即已经存在的记录数
    for i in range(page,page+1):  # 某一页
        url = baseUrl.format(i)
        try:
            fileorigin = requests.get(url, headers=headers1)
            fileorigin.encoding = 'UTF-8'
            req1 = fileorigin.text
            soup = etree.HTML(req1)
            urlxptext = '//*[@id="brandtab-1"]/div/div/div[2]/div[1]/a/@href'
            urlconfig = soup.xpath(urlxptext)
            fileorigin.encoding = 'gb2312'
            req2 = fileorigin.text
            soup = etree.HTML(req2)
            namexptext = '//*[@id="brandtab-1"]/div/div/div[2]/div[1]/a/text()'
            nameconfig = soup.xpath(namexptext)
            series_count += len(urlconfig)
            for j in range(len(urlconfig)):
                record = {
                    "seriesname":nameconfig[j],
                    "seriesurl":"https://car.autohome.com.cn"+urlconfig[j]
                }
                if is_exist(record,tablename):
                    continue
                else:
                    insert_count += 1
                    insert(tablename,record)
        except Exception as e:
            writeLog("【抓取车系错误】页数-"+str(i)+"错误信息为"+str(e))
    return {
        "insert_count": insert_count,
        "pass_count": pass_count,
        "series_count": series_count
    }


# 请求车型
def get_certain_car_url(series_table_name,tablename):
    series_count = 0  # 计算本次爬取记录总数
    insert_count = 0  # 计算本次新增总数
    pass_count = 0  # 计算本次跳过记录数即已经存在的记录数
    sereisURLs = select(series_table_name,"seriesname,seriesurl") #获取车系链接
    if len(sereisURLs) == 0:
        return 404
    for i in range(len(sereisURLs)):
        seriesurl = sereisURLs[i]["seriesurl"]
        seriesname = sereisURLs[i]["seriesname"]
        try:
            fileorigin = requests.get(seriesurl, headers=headers1)
            fileorigin.encoding = 'UTF-8'
            req1 = fileorigin.text
            soup = etree.HTML(req1)
            urlxptext = '//*[@id="divSeries"]/div/ul/li/div[1]/div/p[1]/a/@href'
            urlconfig = soup.xpath(urlxptext)
            idxptext = '//*[@id="divSeries"]/div/ul/li/div[1]/div/p[1]/@id'
            idconfig = soup.xpath(idxptext)
            fileorigin.encoding = 'gb2312'
            req2 = fileorigin.text
            soup = etree.HTML(req2)
            namexptext = '//*[@id="divSeries"]/div/ul/li/div[1]/div/p[1]/a/text()'
            nameconfig = soup.xpath(namexptext)
            series_count += len(urlconfig)
            for j in range(len(urlconfig)):
                if is_exist({"carid":idconfig[j]},tablename):
                    pass_count += 1
                    continue
                else:
                    record = {
                        "carid": str(idconfig[j]).replace("p", ""),
                        "name": nameconfig[j],
                        "url": "https:" + urlconfig[j],
                        "seriesname": seriesname,
                        "seriesurl": seriesurl
                    }
                    insert(tablename, record)
                    insert_count += 1
            process_bar((i+1) / len(sereisURLs), start_str='', end_str="100%", total_length=len(sereisURLs))  # 进度条
            time.sleep(random.randint(1,3))
        except Exception as e:
            writeLog("【抓取车型错误】车系链接-" + seriesurl + "错误信息为" + str(e))
    return {
        "insert_count": insert_count,
        "pass_count": pass_count,
        "series_count": series_count
    }

#
# if __name__ == '__main__':
    # get_series_url(createtable=False,tablename="series_url_list",carlevel="roadster")

    #get_certain_car_url(series_table_name="series_url_list",createtable=False,tablename="car_url_list")

