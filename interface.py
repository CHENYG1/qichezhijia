from SUV_Spider.utils.RW import *
from SUV_Spider.utils.suvUrl import *
from SUV_Spider.utils.carParameters import *
import json
import os


while True:
    print("==============================================================================================================")
    print("====================================== 汽车之家数据爬取：功能界面 ============================================")
    print("==============================================================================================================")
    print("=====================================1.爬取指定级别所有车系数据           ====================================")
    print("=====================================2.更新指定级别车系数据               ====================================")
    print("=====================================3.爬取指定级别所有车系下的所有车型链接===================================")
    print("=====================================4.更新指定级别车系下的车型链接        ===================================")
    print("=====================================5.爬取指定级别所有车系下所有车型参数  ===================================")
    print("=====================================6.更新指定级别车系指定车型参数        ===================================")
    print("=====================================7.导出爬取的数据为Excel文件           ===================================")
    print("==============================================================================================================")
    print("==============================================================================================================")
    cmdline = eval(input("请输入参数选择执行相应命令:"))

    if cmdline == 1:
        print("//////////////////////////////////////////爬取指定级别所有车系数据//////////////////////////////////////////")
        carlevel = ""
        while carlevel not in ["roadster","suv","car"]:
            carlevel = input("请输入指定级别（suv / car / roadster）：")
            if carlevel not in ["roadster","suv","car"]:
                print("级别输入错误！请重新输入！")
        args = {
            "seriesTablename":carlevel+"_series_url_list",
            "carLevel":carlevel,
        }
        countdata = get_series_url(tablename=args["seriesTablename"],carlevel=args["carLevel"])
        print("//////////////////////////////////////////\n本次共计插入数据"+str(countdata["insert_count"])+"条//////////////////////////////////////////")
    elif cmdline == 2:
        print("//////////////////////////////////////////更新指定级别车系数据////////////////////////////////////////////")
        carlevel = ""
        while carlevel not in ["roadster", "suv", "car"]:
            carlevel = input("请输入指定级别（suv / car / roadster）：")
            if carlevel not in ["roadster", "suv", "car"]:
                print("级别输入错误！请重新输入！")
        args = {
            "seriesTablename": carlevel + "_series_url_list",
            "carLevel": carlevel,
        }
        page = eval(input("请输入要指定爬取的页数(默认第一页)："))
        countdata = update_series_url(tablename=args["seriesTablename"], carlevel=args["carLevel"],page=page)
        print("本次共计新增数据" + str(countdata["insert_count"]) + "条")
    elif cmdline == 3:
        print("//////////////////////////////////////////爬取指定级别所有车系所有车型数据///////////////////////////////////")
        carlevel = ""
        while carlevel not in ["roadster", "suv", "car"]:
            carlevel = input("请输入指定级别（suv / car / roadster）：")
            if carlevel not in ["roadster", "suv", "car"]:
                print("级别输入错误！请重新输入！")
        args = {
            "seriesTablename": carlevel + "_series_url_list",
            "carTablename": carlevel +"_car_url_list",  # 存储车型的表
            "carLevel": carlevel,
        }
        # 获取所有车的 名字和ID 链接
        countdata = get_certain_car_url(series_table_name=args["seriesTablename"], tablename=args["carTablename"])
        if countdata == 404:
            print("请先爬取对应级别的车系数据！")
        else:
            print("\n//////////////////////////////////////////"+"本次共计插入数据" + str(countdata["insert_count"]) + "条//////////////////////////////////////////")
    elif cmdline == 5:
        print("//////////////////////////////////////////爬取指定级别所有车系下所有车型参数///////////////////////////////////")
        carlevel = ""
        while carlevel not in ["roadster", "suv", "car"]:
            carlevel = input("请输入指定级别（suv / car / roadster）：")
            if carlevel not in ["roadster", "suv", "car"]:
                print("级别输入错误！请重新输入！")
        args = {
            "carParameterTablename": carlevel +"_carparameters",  # 存储所有参数的表
            "carTablename": carlevel + "_car_url_list",  # 存储车型的表
            "carLevel": carlevel,
            "shuxingTypes": ["基本参数", "车身", "发动机", "变速箱", "底盘转向", "车轮制动"]
        }
        NeedToSpide = Get_Need_to_Spide(args["carTablename"], args["carParameterTablename"])
        print(NeedToSpide)
        if len(NeedToSpide) == 0:
            print("请先爬取相应级别的车型数据！或者已经爬取完了所有车型！")
        else:
            IDSpided = []
            # 从备份文件中先存数据
            print("数据抓取中……")
            for i in range(len(NeedToSpide)):
                process_bar(i+1 / len(NeedToSpide), start_str='', end_str="100%",
                            total_length=len(NeedToSpide))  # 进度条
                data = Spide_Data(SPIDER=ConfigSpider(),
                                  configUrl="https://car.autohome.com.cn/config/spec/{}.html".format(NeedToSpide[i]),
                                  valuetypes=args["shuxingTypes"])
                if data:
                    for item in data["chexingIdList"]:
                        IDSpided.append(item)
                    current_index = data["chexingIdList"].index(NeedToSpide[i])
                    with open("backend.json", "w",encoding="gb2312") as f:
                        json.dump(data, f)
                    ids = Put_Table(args["carTablename"],args["carParameterTablename"], data,current_index)
                    IDSpided.append(ids)
                else:
                    continue
            print("\n")
    elif cmdline == 6:
        print("//////////////////////////////////////////更新指定车型的所有参数///////////////////////////////////")
        carlevel = ""
        while carlevel not in ["roadster", "suv", "car"]:
            carlevel = input("请输入指定级别（suv / car / roadster）：")
            if carlevel not in ["roadster", "suv", "car"]:
                print("级别输入错误！请重新输入！")
        args = {
            "carParameterTablename": carlevel + "_carparameters",  # 存储所有参数的表
            "carTablename": carlevel + "_car_url_list",  # 存储车型的表
            "carLevel": carlevel,
            "shuxingTypes": ["基本参数", "车身", "发动机", "变速箱", "底盘转向", "车轮制动"]
        }
        carid = eval(input("请输入指定的车型ID："))

        data = Spide_Data(SPIDER=ConfigSpider(),
                          configUrl="https://car.autohome.com.cn/config/spec/{}.html".format(carid),
                          valuetypes=args["shuxingTypes"])
        if data["status"] == 200:
            try:
                current_index = data["chexingIdList"].index(str(carid))
                with open("backend.json", "w", encoding="gb2312") as f:
                    json.dump(data, f)
                ids = Update_Table(args["carTablename"], args["carParameterTablename"], data, current_index)
            except Exception as e:
                print(e)
            print("车型ID " + str(carid) + " 更新完成！")
            print("\n")
        else:
            print("更新失败！")
            print("\n")
    elif cmdline == 7:
        carlevel = ""
        while carlevel not in ["roadster", "suv", "car"]:
            carlevel = input("请输入指定级别（suv / car / roadster）：")
            if carlevel not in ["roadster", "suv", "car"]:
                print("级别输入错误！请重新输入！")
        args = {
            "carParameterTablename": carlevel + "_carparameters",  # 存储所有参数的表
            "carTablename": carlevel + "_car_url_list",  # 存储车型的表
            "carLevel": carlevel,
            "shuxingTypes": ["基本参数", "车身", "发动机", "变速箱", "底盘转向", "车轮制动"]
        }
        pc = select(carlevel + "_carparameters","count(*)")[0]["count(*)"]
        cc = select(carlevel + "_car_url_list","count(*)")[0]["count(*)"]
        sc = select(carlevel + "_series_url_list","count(*)")[0]["count(*)"]
        print(carlevel + "_carparameters     |   车型参数表   |  "+str(pc))
        print(carlevel + "_car_url_list      |   车型链接表   |  "+ str(cc))
        print(carlevel + "_series_url_list   |   车系连接表   |  " + str(sc))

        tablename = ""
        while tablename not in [carlevel + "_carparameters", carlevel + "_car_url_list", carlevel + "_series_url_list"]:
            tablename = input("请输入要导出的数据表名称：")
            if tablename not in [carlevel + "_carparameters", carlevel + "_car_url_list", carlevel + "_series_url_list"]:
                print("数据表名称错误！请重新输入！")
        path = input("请输入文件存储路径（当前路径"+ str(os.getcwd())+"):" )
        try:
            result = eval(repr(path).replace('\\', '/'))
            print(result)
            export_excel(result,tablename)
            print("文件导出成功！")
        except Exception as e:
            print(e)
            print("\n")
