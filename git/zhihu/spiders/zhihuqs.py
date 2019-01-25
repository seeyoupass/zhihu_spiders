# -*- coding: utf-8 -*-
import scrapy
import json
from zhihu.items import ZhihuqsItem

class ZhihuqsSpider(scrapy.Spider):
    name = 'zhihuqs'
    allowed_domains = ['https://www.zhihu.com']
    start_urls = ['http://https://www.zhihu.com/']

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
        self.request_url = 'https://www.zhihu.com/api/v4/questions/28626263/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics&offset=&limit=3&sort_by=default&platform=desktop'

    def start_requests(self):
        yield scrapy.Request(url=self.request_url,headers=self.headers,callback=self.parse)

    def parse(self, response):
        item=ZhihuqsItem()
        jd = json.loads(response.text)
        for it in jd['data']:
            item['answer_user']= it['author']['name']
            item['comment_total'] = it['comment_count']
            item['text'] = it['content']
            item['awesome'] = it['voteup_count']
            yield item

        next_url = jd['paging']['next']
        if next_url is not None:
            yield scrapy.Request(url=next_url,headers=self.headers,callback=self.parse,dont_filter=True)


