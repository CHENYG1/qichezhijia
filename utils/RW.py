from SUV_Spider.utils.db_tools import *
from SUV_Spider.utils.operater import writeLog
import pymysql, xlwt


def Put_Table(cartable,tablename,data,index):
    # 先检查字段是否都存在
    fields = getColumn(tablename)
    allShuxingName = []
    for i in range(len(set(data["shuxingTypeList"]))):
        for j in range(len(data["shuxingNameList"][i])):
            allShuxingName.append(data["shuxingNameList"][i][j])
    column_not_exist = list(set(allShuxingName).difference(set(fields)))  # 数据表中不存在的字段
    for item in data["data"]:
        for col in column_not_exist:
            del item[col]
    ids = []
    #for i in range(len(data["data"])):
    try:
        if not is_exist(kv={"carid":data["data"][index]["carid"]},tablename=tablename):
            insert(tablename, data["data"][index])
            ids.append(data["data"][index]["carid"])
            Update_carName(carid=data["data"][index]["carid"],cartable=cartable,parametertable=tablename)

    except Exception as e:
        writeLog("【存储车型错误】车型ID为-" + str(data["data"][index]["carid"])+ "错误信息为" + str(e))
        writeLog(str(data["data"][index]["carid"])+"【车型数据为】-" + str(data["data"][index]) )
    return ids


def Update_Table(cartable,tablename,data,index):

    fields = getColumn(tablename)
    allShuxingName = []
    for i in range(len(set(data["shuxingTypeList"]))):
        for j in range(len(data["shuxingNameList"][i])):
            allShuxingName.append(data["shuxingNameList"][i][j])
    column_not_exist = list(set(allShuxingName).difference(set(fields)))  # 数据表中不存在的字段
    for item in data["data"]:
        for col in column_not_exist:
            del item[col]
    ids = []
    try:
        if not is_exist(kv={"carid":data["data"][index]["carid"]},tablename=tablename):
            insert(tablename, data["data"][index])
            ids.append(data["data"][index]["carid"])
            Update_carName(carid=data["data"][index]["carid"],cartable=cartable,parametertable=tablename)
        else:
            update(tablename,tdict=data["data"][index],condition="carid = "+str(data["data"][index]["carid"]))
            Update_carName(carid=data["data"][index]["carid"], cartable=cartable, parametertable=tablename)
    except Exception as e:
        writeLog("【存储车型错误】车型ID为-" + str(data["data"][index]["carid"])+ "错误信息为" + str(e))
        writeLog(str(data["data"][index]["carid"])+"【车型数据为】-" + str(data["data"][index]) )
    return ids


def Put_One_Table(cartable,tablename,data):
    # 先检查字段是否都存在
    fields = getColumn(tablename)
    allShuxingName = []
    for i in range(len(set(data["shuxingTypeList"]))):
        for j in range(len(data["shuxingNameList"][i])):
            allShuxingName.append(data["shuxingNameList"][i][j])
    column_not_exist = list(set(allShuxingName).difference(set(fields)))  # 数据表中不存在的字段
    for item in data["data"]:
        for col in column_not_exist:
            del item[col]
    ids = []
    try:
        if not is_exist(kv={"carid": data["carid"]}, tablename=tablename):
            insert(tablename, data)
            ids.append(data["carid"])
            Update_carName(carid=data["carid"], cartable=cartable, parametertable=tablename)
    except Exception as e:
        writeLog("【存储车型错误】车型ID为-" + str(data["carid"]) + "错误信息为" + str(e))
        writeLog(str(data["carid"]) + "【车型数据为】-" + str(data))

    return ids


def Update_carName(carid,cartable,parametertable):
    """

    :param carid:
    :param cartable:
    :param parametertable:
    :return:
    """
    name = select(table=cartable,column='name',condition="carid="+carid)
    if len(name) != 0:
        update(table=parametertable,tdict={"name":name[0]["name"]},condition="carid="+carid)
    else:
        return


def Get_Need_to_Spide(carurltable,carparameterstable):
    # 把所有的车型ID都拿出来
    try:
        id_dict = select(carurltable, "carid")
        all_id_list = []
        for item in id_dict:
            all_id_list.append(item["carid"].replace("p", ""))
        # 把所有成功爬过的ID都拿着出来
        id_already_dict = select(carparameterstable, "distinct carid")
        id_already_list = []
        for item in id_already_dict:
            id_already_list.append(str(item["carid"]))
        # 本次需要爬取的ID LIST
        idNeed = list(set(all_id_list).difference(set(id_already_list)))  # 数据表中不存在的字段
        return idNeed
    except Exception as e:
        writeLog("【获取所需爬取车型ID列表错误】错误原因为："+str(e))
        return []

export_excel("C://Users//CHEN//PycharmProjects//CHEN//SUV_Spider","suv_car_url_list")