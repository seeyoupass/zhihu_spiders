# -*- coding: utf-8 -*-
import scrapy
import json
from zhihu.items import ZhihuTopicItem
class ZhihutopicSpider(scrapy.Spider):
    name = 'zhihutopic'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    def __init__(self):
        self.headers = {
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            # 'Cache-Control': 'max-age=0',
            # 'Connection': 'keep-alive',
            'Host': 'www.zhihu.com',
            'Referer': 'https://www.zhihu.com/signup?next=%2F',
            # 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        self.request_url='https://www.zhihu.com/api/v4/topics/19776749/feeds/essence?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count%3B&limit=10&offset={}'

    def start_requests(self):
        for i in range(0,50,10):
            url=self.request_url.format(i)
            yield scrapy.Request(url=url,headers=self.headers,callback=self.parse,dont_filter=True)

    def parse(self, response):
        jd = json.loads(response.text)
        for url in jd['data']:
            id=str(url['target']['question']['id'])
            url=url['target']['url'].replace('api','question').replace('v4',id).replace('answers','answer')
            yield scrapy.Request(url,headers=self.headers,callback=self.parse_detail,dont_filter=True)


    def parse_detail(self,response):
        item = ZhihuTopicItem()
        item['question_title'] = response.css('.QuestionHeader-title ::text').extract_first()
        item['tags'] = ','.join(response.css('.Tag-content .Popover div ::text').extract())
        item['question_detial'] = response.xpath('//span[@class="RichText ztext"]/text()').extract_first()
        item['answer'] = response.css('.List-headerText span::text').extract_first()
        item['answer_user'] = response.css('.UserLink-link::text').extract_first()
        # item['text']=','.join( response.css('.RichText p  ::text').extract())
        item['text'] = ','.join(
            response.xpath('//span[@class="RichText ztext CopyrightRichText-richText"]/p/text()').extract())
        item['time'] = response.css('.ContentItem-time ::text').extract_first()
        item['awesome'] = response.css('.Voters button ::text').extract_first()
        item['comment_total'] = response.xpath('//div[@class="ContentItem-actions RichContent-actions"]/button/text()').extract_first()
        item['url'] = response.url
        yield item
