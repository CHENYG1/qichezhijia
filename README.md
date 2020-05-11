数据库准备

- MYSQL 数据库 ```vcar_vcyber_com```

- 数据表：存储车系的表；存储车型的表；存储车型所有参数的表|每个车系都要创建三张名字不同的表，且都为car level + tablename的形式。

  1. 存储车系的表car level+_```series_url_list```：

     ```sql
     DROP TABLE IF EXISTS `suv_series_url_list`;
     CREATE TABLE `suv_series_url_list`  (
       `id` int(11) NOT NULL AUTO_INCREMENT,
       `seriesname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
       `seriesurl` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
       PRIMARY KEY (`id`) USING BTREE
     ) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
     
     SET FOREIGN_KEY_CHECKS = 1;
     
     ```

  2. 存储车型的表car level+_```car_url_list```:

     ```sql
     DROP TABLE IF EXISTS `suv_car_url_list`;
     CREATE TABLE `suv_car_url_list`  (
       `id` int(11) NOT NULL AUTO_INCREMENT,
       `carid` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '车型ID',
       `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '车型名称',
       `url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '车型链接',
       `seriesname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '车系名称',
       `seriesurl` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '车系链接'，
        PRIMARY KEY (`id`) USING BTREE，
     ) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
     
     SET FOREIGN_KEY_CHECKS = 1;
     ```

     

  3. 存储车型参数的表```car_parameters```:

     说明：预选规定需要爬取的车型参数

     ```sql
     DROP TABLE IF EXISTS `suv_carparamaters`;
     CREATE TABLE jsuv_carparamaters (`carid` varchar(225),`name` varchar(225),`厂商` varchar(225),`级别` varchar(225),`能源类型` varchar(225),
     `环保标准` varchar(225),`最大功率(kW)` varchar(225),`最大扭矩(N·m)` varchar(225),`发动机` varchar(225),`变速箱` varchar(225),
     `长*宽*高(mm)` varchar(225),`最高车速(km/h)` varchar(225),`官方0-100km/h加速(s)` varchar(225),`实测0-100km/h加速(s)` varchar(225),
     `实测100-0km/h制动(m)` varchar(225),`工信部综合油耗(L/100km)` varchar(225),`实测油耗` varchar(225),
     `整车质保` varchar(225),`长度(mm)` varchar(225),`宽度(mm)` varchar(225),`高度(mm)` varchar(225),
     `轴距(mm)` varchar(225),`前轮距(mm)` varchar(225),`后轮距(mm)` varchar(225),`最小离地间隙(mm)` varchar(225),
     `车身结构` varchar(225),`车门数(个)` varchar(225),`座位数(个)` varchar(225),`油箱容积(L)` varchar(225),`行李厢容积(L)` varchar(225),
     `整备质量(kg)` varchar(225),`发动机型号` varchar(225),`排量(mL)` varchar(225),`排量(L)` varchar(225),`进气形式` varchar(225),
     `气缸排列形式` varchar(225),`气缸数(个)` varchar(225),`每缸气门数(个)` varchar(225),`压缩比` varchar(225),`配气机构` varchar(225),
     `缸径(mm)` varchar(225),`行程(mm)` varchar(225),`最大马力(Ps)` varchar(225),`最大功率转速(rpm)` varchar(225),
     `最大扭矩转速(rpm)` varchar(225),`发动机特有技术` varchar(225),`燃料形式` varchar(225),`燃油标号` varchar(225),
     `供油方式` varchar(225),`缸盖材料` varchar(225),`缸体材料` varchar(225),`挡位个数` varchar(225),`变速箱类型` varchar(225),
     `简称` varchar(225),`驱动方式` varchar(225),`前悬架类型` varchar(225),`后悬架类型` varchar(225),`助力类型` varchar(225),
     `车体结构` varchar(225),`前制动器类型` varchar(225),`后制动器类型` varchar(225),`驻车制动类型` varchar(225),`前轮胎规格` varchar(225),
     `后轮胎规格` varchar(225),`备胎规格` varchar(225),`rowid` int(11) NOT NULL AUTO_INCREMENT,
      PRIMARY KEY (`rowid`) USING BTREE)
     ```

     

     准备好相关数据库和数据表后，配置数据库连接参数：
      utils.db_tool.py
     ```python
     DBCONFIG = {
             'host': 'localhost',
             'port': 3306,
             'user': 'root',
             'passwd': '*******',
             'dbname': 'vcar_vcyber_com',
             'charset': 'utf8mb4'
         }
     ```

     
