# -*- coding: utf-8 -*-
import pymysql
import re
from scrapy.exporters import JsonLinesItemExporter

class GetBossPipeline(object):
#     def __init__(self):
#         self.fp = open('jobs.json','wb')
#         self.exporter = JsonLinesItemExporter(self.fp,ensure_ascii=False)
#
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item
#
#     def close_spider(self,spider):
#         self.fp.close()


    def table_exists(self,con,table_name):
        sql = "show tables;"    #第一次使用需要将数据表删除
        con.execute(sql)
        tables = [con.fetchall()]
        table_list = re.findall('(\'.*?\')',str(tables))
        table_list = [re.sub("'",'',each) for each in table_list]
        if table_name in table_list:
            return 1
        else:
            return 0

    def process_item(self, item, spider):
        connect = pymysql.connect(
            user = 'root',
            password = 'root',
            db = 'MYSQL',
            host = '127.0.0.1',
            port = 3306,
            charset = 'utf8'
            )
        con = connect.cursor()
        con.execute("use w_lagouwang")
        table_name = 'zhipinwang'   #这张表是用来测试所有数据的  并非关键词表
        if(self.table_exists(con,table_name) != 1):
            # con.execute("drop table if exists zhipinwang")
            sql = '''create table zhipinwang(dp_name varchar(40),dp_type varchar(40),dp_founded varchar(20),
            job_name varchar(40),education varchar(40),experience varchar(20),salary varchar(20),state varchar(10),
            description varchar(800),welfare varchar(200),address varchar(100))'''
            con.execute(sql)
        data = {'dp_name':item['dp_name'],'dp_type':item['dp_type'],'dp_founded':item['dp_founded'],
                'job_name':item['job_name'],'education':item['education'],'experience':item['experience'],
                'salary':item['salary'],'state':item['state'],'description':item['description'],
                'welfare':item['welfare'],'address':item['address']}
        dp_name = data['dp_name']
        dp_type = data['dp_type']
        dp_founded = data['dp_founded']
        job_name = data['job_name']
        education = data['education']
        experience = data['experience']
        salary = data['salary']
        state = data['state']
        description = data['description']
        welfare = data['welfare']
        address = data['address']

        con.execute('insert into zhipinwang(dp_name,dp_type,dp_founded,job_name,education,experience,salary,state,description,welfare,address)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            [dp_name,dp_type,dp_founded,job_name,education,experience,salary,state,description,welfare,address])

        connect.commit()
        con.close()
        connect.close()
        return data