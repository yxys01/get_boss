# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from scrapy.http import Request
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import os
path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
import sys
sys.path.append(path)
from get_boss.items import GetBossItem


headers = {
        'x-devtools-emulate-network-conditions-client-id': "5f2fc4da-c727-43c0-aad4-37fce8e3ff39",
        'upgrade-insecure-requests': "1",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'dnt': "1",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.8,en;q=0.6",
        'cookie': "__c=1527989289; __g=-; lastCity=100010000; toUrl=https%3A%2F%2Fwww.zhipin.com%2Fjob_detail%2Fc77944563dd5cc1a1XV70tW0ElM%7E.html%3Fka%3Dsearch_list_1_blank%26lid%3DTvnYVWp16I.search; JSESSIONID=""; __l=l=%2Fwww.zhipin.com%2F&r=; __a=33024288.1527773672.1527940079.1527989289.90.5.22.74; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1527774077,1527835258,1527940079,1527989289; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1527991981",
        'cache-control': "no-cache",
        'postman-token': "76554687-c4df-0c17-7cc0-5bf3845c9831",
        'x-requested-with':'XMLHttpRequest',
        'referer':"https://www.zhipin.com/job_detail/?query=&scity=100010000&industry=&position=",
        # 'user-agent':ua               #需要替换的
        #'user-agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52'

    }

class BossSpider(CrawlSpider):
    name = 'boss'
    start_urls = ['https://www.zhipin.com/gongsir/5d627415a46b4a750nJ9.html?page=1']
    url1 = 'https://www.zhipin.com'     #用来做拼接


     # 匹配职位列表页的规则(定义抽取连接规则)
    rules = (
        Rule(LinkExtractor(allow=r'.+\?page=\d+'), callback="parse_url",follow=True),
    )
    # 匹配详情页的规则
    # rules = (
    #     Rule(LinkExtractor(allow=r'.+job_detail/\w+~.html'), callback="detail_parse", follow=False),
    # )

    def parse_url(self, response):
        item = GetBossItem()

        for i in range(1,15):
            url = response.xpath('//*[@id="main"]/div[2]/div[2]/div[2]/ul/li[{}]/a/@href'.format(str(i))).extract()
            url = self.url1+str(url[0])
            print(url)
            # if item['url']:
            yield Request(url,
                          callback=self.detail_parse,#回调详情页函数
                          meta={'item':item}, #将参数传递给meta#
                          priority=10,
                          dont_filter=True, #强制不过滤
                          #headers=headers
                          # headers=self.headers
                          )


    def detail_parse(self,response):
        item = response.meta['item']   #接收item
         # 企业名称
        dp_name = response.xpath('//div[@class="job-sec"]/div[@class="name"]/text()').get().strip()
         # 企业类型
        dp_type = response.xpath('//div[@class="level-list"]/li[@class="company-type"]/text()').getall()[0]
         # 企业成立时间
        dp_founded = response.xpath('//div[@class="level-list"]/li[@class="res-time"]/text()').getall()[0]
         # 职位名称
        job_name = response.xpath('//div[@class="company-info"]/div[@class="name"]/h1/text()').get().strip()
         # 学历要求
        education = response.xpath('//*[@id="main"]/div[1]/div/div/div[2]/p/text()').getall()[2]
         # 工作经验要求
        experience = response.xpath('//*[@id="main"]/div[1]/div/div/div[2]/p/text()').getall()[1]
         # 薪资
        salary = response.xpath('//*[@id="main"]/div[1]/div/div/div[2]/div[2]/span/text()').get().strip()
         # 招聘状态
        state = response.xpath('//*[@id="main"]/div[3]/div/div[1]/div[2]/p[6]/text()').get().strip()
         # 职位描述
        description = response.xpath('//*[@id="main"]/div[3]/div/div[2]/div[2]/div[1]/div/text()').getall()
        description = str(description).strip('[\']\\n ')
         # 员工福利
        welfare = response.xpath('//*[@id="main"]/div[1]/div/div/div[2]/div[3]/div[2]/span/text()').getall()
        welfare = str(welfare)
        # 工作地址
        address = response.xpath('//div[@class="job-location"]/div[@class="location-address"]/text()').get().strip()


        item['dp_name']=dp_name
        item['dp_type']=dp_type
        item['dp_founded']=dp_founded
        item['job_name']=job_name
        item['education']=education
        item['experience']=experience
        item['salary']=salary
        item['state']=state
        item['description']=description
        item['welfare']=welfare
        item['address']=address

        yield item
