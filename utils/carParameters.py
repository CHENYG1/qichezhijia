# _*_ coding:utf-8 _*_
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from scrapy import Selector
from SUV_Spider.utils.db_tools import *
from SUV_Spider.utils.operater import *


class ConfigSpider(object):
    # 当前请求发生错误的链接
    curentLink=""
    # 车型id的set集合记录已经保存到数据中的车型id，用于判重，若该集合中已存在车型id则证明已经保存过了，无需再请求保存
    specIdSet=set()
    # 车型属性表中已经存在的车型ID，该集合代表已经爬取过的车型
    existChexingIdSet=set()
    # 车型表中所有的id集合,该集合代表所有的车型id
    chexingIdSet=set()

    # 模拟浏览器
    browser = webdriver.Chrome()

    # 请求车型配置页面 =>curentLink
    def requestConfigLink(self, configUrl):
        try:
            # https://car.autohome.com.cn/config/spec/28978.html#pvareaid=3454569
            self.browser.get(configUrl)
            wait = WebDriverWait(self.browser, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.tbcs')))
            time.sleep(0.1)  # 若不加一个会发生页面没有完全渲染
            self.curentLink = configUrl
            return True
        except Exception as e:
            return False

    # 解析伪元素class，获取className不重复的集合
    def parseSpanClassName(self):
        # 定义存放className的set集合
        classNameSet = set()
        try:
            # 取出page_source
            page_source = self.browser.page_source
            # 转selector取值
            page = Selector(text=page_source)
            # 定位table所在的div
            dataDiv = page.css("#config_data")
            # 定位div中所有的span
            spanList = dataDiv.xpath(".//span[@class]")
            for span in spanList:
                # print(span.xpath("@class").extract_first())
                className = span.xpath("@class").extract_first()
                if className and re.match(r'^\w*_\w*_\w*$', className):
                    classNameSet.add(className)
        except Exception as e:
            with open("errorLogs.txt","a+",encoding="utf-8") as f:
                f.write("页面"+self.curentLink+"获取伪元素class失败；失败原因是："+str(e)+"\n")
        return classNameSet

    # 翻译整个页面伪元素
    def translatePage(self, classNameSet):
        classNameRecorde = ""
        try:
            # 执行js，根据className取值，再显式赋值
            preGetImplicitContentJs = "return window.getComputedStyle(document.getElementsByClassName('%s')[0], 'before').getPropertyValue('content')"
            preSetViewableContenJs = """
                              var arr = document.getElementsByClassName('%s');
                              if (arr != undefined && arr.length > 0){
                                  for(i=0;i<arr.length;i++){
                                       arr[i].innerHTML=%s;
                                  }
                               }
                            """
            for className in classNameSet:
                classNameRecorde = className
                getImplicitContentJs = preGetImplicitContentJs % className
                content = self.browser.execute_script(getImplicitContentJs)
                # print(content)
                # 再次执行js，反向回显内容
                setViewableContenJs = preSetViewableContenJs % (className, content)
                self.browser.execute_script(setViewableContenJs)
            # 页面翻译完成
        except Exception as e:
            with open("errorLogs.txt","a+",encoding="utf-8") as f:
                f.write("页面"+self.curentLink+"翻译页面伪元素失败！失败原因是："+str(e)+"\n")

    # 解析导航栏中各车型id
    def parseChexingIdList(self, page):
        # 获取导航栏中车型id
        chexingIdList = list()
        try:
            tableNavTdList = page.css(".tbset").xpath(".//tr").xpath(".//td")
            for td in tableNavTdList:
                href = td.xpath("div/div/a/@href").extract_first()
                # print(href)
                if href:
                    id = href[href.find("spec/") + 5:href.find("/#")]
                    chexingIdList.append(id)
                    # 向已爬取车型集合中添加车型id，用于判重
                    self.specIdSet.add(id)
        except Exception as e:
            with open("errorLogs.txt", "a+", encoding="utf-8") as f:
                f.write("页面" + self.curentLink + "解析导航栏失败！失败原因是：" + str(e) + "\n")
        return chexingIdList


#爬取一个页面的所有车型的指定参数
# 一个页面就是一个车系
def Spide_Data(SPIDER,configUrl,valuetypes):
    #print(configUrl)

    #configUrl = "https://car.autohome.com.cn/config/spec/41097.html#pvareaid=3454569"
    try:
        if not SPIDER.requestConfigLink(configUrl):
            # 请求超时，证明没有数据，返回请求下一个
            print("\n请求超时")
        # 解析出页面所有的span
        classNameSet = SPIDER.parseSpanClassName()
        SPIDER.translatePage(classNameSet)
        # 取出最新的page_source
        page_source = SPIDER.browser.page_source
        # 将page_source装入到Selector中
        page = Selector(text=page_source)
        # 解析导航栏中车型id,加入爬取集合
        chexingIdList = SPIDER.parseChexingIdList(page)
        # 定位数据table所在的div
        dataDiv = page.css("#config_data")
        # 定位table
        tableList = dataDiv.xpath("table[@id]")
        print("/////{}".format(configUrl))
        allShuxingType = []
        allShuxingName = []
        allData = []
        for item in chexingIdList:
            allData.append({"carid":item})
        for table in tableList:
            # 每个table都是一个属性类型的所有集合
            trList = table.xpath(".//tr")
            shuxingNameList = []
            shuxingValueArray = []
            for index, tr in enumerate(trList):
                # 第一个是属性类别
                if index == 0:
                    shuxingTypeName = tr.xpath("string(.)").extract_first()
                    continue
                tdList = tr.xpath("*")
                shuxingValueList = []
                if shuxingTypeName in valuetypes:  # 只要
                    allShuxingType.append(shuxingTypeName)
                    for i, td in enumerate(tdList):  # 每一行是一个参数
                        # 第一个td就是属性名，后面的都是属性值
                        if i == 0:
                            shuxingName = td.xpath("string(.)").extract_first()
                            shuxingNameList.append(shuxingName)
                            continue
                        if i - 1 < len(chexingIdList):
                            shuxingValue = td.xpath("string(.)").extract_first()
                            # 检测\ax0
                            shuxingValue = "".join(shuxingValue.split())
                            shuxingValueList.append(shuxingValue)
                    shuxingValueArray.append(shuxingValueList)
                else:
                    continue
            allShuxingName.append(shuxingNameList)
            for j in range(len(chexingIdList)):
                # chexingIdList[j] = 3113 第j列
                for k in range(len(shuxingNameList)):
                    # 第k行 shuxingNameList = "厂商"
                    key = shuxingNameList[k]
                    value = shuxingValueArray[k][j]
                    allData[j][key] = value
        return({
            "chexingIdList":chexingIdList,
            "data":allData,
            "shuxingNameList":allShuxingName,
            "shuxingTypeList":allShuxingType
        })
    except Exception as e:
        writeLog("【抓取车型参数错误】页面链接-" + configUrl + "错误信息为" + str(e))
        print("400/////" + str(e))
        return ()


# data = Spide_Data(SPIDER=ConfigSpider(),configUrl = "https://car.autohome.com.cn/config/spec/41297.html#pvareaid=3454569")
#
# Put_Table("carpp",data)


