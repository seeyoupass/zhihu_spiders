# -*- coding: utf-8 -*-
import scrapy
import json
from zhihu.items import ZhihuItem


class ZhihuwSpider(scrapy.Spider):
    name = 'zhihuw'
    allowed_domains = ['https://www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']


    def __init__(self):

        self.headers={#'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        #'Accept-Encoding': 'gzip, deflate, br',
                        #'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                        #'Cache-Control': 'max-age=0',
                        #'Connection': 'keep-alive',
                        'Host': 'www.zhihu.com',
                        'Referer': 'https://www.zhihu.com/signup?next=%2F',
                        #'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
                    }
        self.request_url='https://www.zhihu.com/api/v3/feed/topstory/hot-list-web?limit=50&desktop=true'


    def start_requests(self):
        yield scrapy.Request(url=self.request_url,headers=self.headers,callback=self.parse)

    def parse(self, response):
        jd=json.loads(response.text)
        for url in jd['data']:
            #print(url['target']['link']['url'])
            url_page=url['target']['link']['url']
            yield scrapy.Request(url=url_page,headers=self.headers,callback=self.parse_detail,dont_filter=True)

    def parse_detail(self,response):
        item=ZhihuItem()
        item['question_title']=response.css('.QuestionHeader-title ::text').extract_first()
        item['tags']=','.join(response.css('.Tag-content .Popover div ::text').extract())
        item['question_detial']=response.xpath('//span[@class="RichText ztext"]/text()').extract_first()
        item['answer']= response.css('.List-headerText span::text').extract_first()
        item['answer_user']= response.css('.UserLink-link::text').extract_first()
        #item['text']=','.join( response.css('.RichText p  ::text').extract())
        item['text'] = ','.join( response.xpath('//span[@class="RichText ztext CopyrightRichText-richText"]/p/text()').extract())
        item['time']= response.css('.ContentItem-time ::text').extract_first()
        item['awesome']=response.css('.Voters button ::text').extract_first()
        item['comment_total']= response.xpath('//div[@class="ContentItem-actions RichContent-actions"]/button/text()').extract_first()
        item['url']=response.url
        print(response.url)
        comment_detail=eval(response.xpath('//div[@class="ContentItem AnswerItem"]/@data-zop').extract_first())['itemId']
        comment_url='https://www.zhihu.com/api/v4/answers/{}/root_comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&order=normal&limit=20&offset=0&status=open'.format(comment_detail)
        yield scrapy.Request(url=comment_url,headers=self.headers,callback=self.parse_comment,dont_filter=True)
        yield item

    def parse_comment(self,response):
        item = ZhihuItem()
        jd = json.loads(response.text)
        name=[]
        content=[]
        for comment in jd['data']:
            name.append(comment['author']['member']['name'])
            content.append(comment['content'])
        item['comment_content']=dict(zip(name,content))
        yield item
