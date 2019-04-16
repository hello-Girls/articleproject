# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql


class WeightPipeline(object):
    def open_spider(self, spider):
        print("开始")
        try:

            self.con = pymysql.connect(host="127.0.0.1",
                                       port=3306,
                                       user="root",
                                       passwd="jiangfuhua321",
                                       charset="utf8"
                                       )
            self.cursor = self.con.cursor(pymysql.cursors.DictCursor)
            print("已连接到mysql")
            try:
                self.cursor.execute("create database mydb")
                print("创建新的数据库")
            except:
                pass
            self.con.select_db("mydb")
            try:
                self.cursor.execute("drop table Sex")
                print("删除原来的表")
            except:
                pass
            try:
                sql = """
                create table Sex(
                       Id varchar(8) primary key,
                       Tag varchar(32),
                       Title varchar(512) ,
                       Subtitle varchar(256),
                       Profilephoto varchar(256),
                       Author varchar(64),
                       Date varchar(16),
                       Text text,
                       Pic varchar(256),
                       Video varchar(256)
                       )
"""

                self.cursor.execute(sql)
                print("创建新的表")
            except:
                self.cursor.execute("delete from Sex")
            self.opened = True
            self.count = 0
        except Exception as err:
            print(err)
            self.opened = False

    def close_spider(self, spider):
        if self.opened:
            self.con.commit()
            self.con.close()
            self.opened = False
        print("closed")
        print(self.count)  # 无法显示

    def process_item(self, item, spider):
        try:
            print("----------------------")
            print("标题："+item["title"])
            print("副标题："+item["subtitle"])
            print("作者："+item["author"])
            print("日期："+item["date"])
            print("头像链接："+item["profilephoto"])
            print("正文："+item["text"])
            print("图片链接："+item["pic"])
            print("---------------------")
            if self.opened:
                if item["title"]!='':
                    if item["author"]!='':
                        if item["text"]!='':
                            if item["subtitle"]!= '':


                               self.count += 1
                               print(self.count)
                               ID = str(self.count)
                               while len(ID) < 8:
                                 ID ="0"+ID
                               self.cursor.execute(
                                   "insert into Sex(Id,Tag,Title,Subtitle,Profilephoto,Author,Date,Text,Pic,Video) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    (ID, item["tag"],item["title"], item["subtitle"],item["profilephoto"], item["author"], item["date"], item["text"], item["pic"],item["video"]))



        except Exception as err:
            print(err)
        return item
