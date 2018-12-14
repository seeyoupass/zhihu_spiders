
import requests
import json,csv
import pandas as pd
from bs4 import BeautifulSoup
import time,pymongo,pymysql,random
from multiprocessing import Pool


headers={'X-Anit-Forge-Code':'0',
            'X-Anit-Forge-Token':None,
            'X-Requested-With':'XMLHttpRequest',
			'Cookie':'',#需自行添加
			'Host':'www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
}
#headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
def get_start_url(page,keyword,city): #定义关键词和城市获取url
    params = {'city': city,
              'needAddtionalResult': 'false'

              }
    formdata ={'first': 'true',
                 'pn': page,
                 'kd': keyword}
    #url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false'
    #urls = url+urlencode(formdata)
    try:
        html = requests.post('https://www.lagou.com/jobs/positionAjax.json',headers=headers,params=params,data=formdata)
        if html.status_code==200:
            #print(html.text)
            return html

    except requests.ConnectionError:
        return None

def parse_json(html):#解析获取的json并存为字典
    jd = json.loads(html.text)
    #print(jd['content']['positionResult']['result'])
    companyFullName=[]
    detial_url=[]
    workYear=[]
    edu=[]
    positionName=[]
    positionAdvantage=[]
    salary=[]
    industryField=[]
    companySize=[]
    companyLabelList=[]
    positionLables=[]
    district=[]
    skillLables=[]
    item={}
    for id in jd['content']['positionResult']['result']:
        url_id = id['positionId']
        # print(url_id)
        url = 'https://www.lagou.com/jobs/' + str(url_id) + '.html'
        detial_url.append(url)
        #print(detial_url)
        companyFullName_=id['companyFullName']
        companyFullName.append(companyFullName_)
        workYear_=id['workYear']
        workYear.append(workYear_)
        edu.append(id['education'])
        positionName.append(id['positionName'])
        positionAdvantage.append(id['positionAdvantage'])
        salary.append(id['salary'])
        industryField.append(id['industryField'])
        companySize.append(id['companySize'])
        companyLabelList.append(id['companyLabelList'])
        positionLables.append(id['positionLables'])
        district.append(id['district'])
        skillLables.append(id['skillLables'])
    #print(positionName,positionAdvantage,salary,industryField,companySize,companyLabelList, positionLables, district, skillLables,)
    item={'公司名称':companyFullName,'经验':workYear,'教育':edu,'职位':positionName,'诱惑':positionAdvantage,'工资':salary,'公司经验范围':industryField,'公司规模':companySize,'公司要求':companyLabelList,'职位要求':positionLables,'地址':district,'技能':skillLables,'详细网址':detial_url}
    print(item)
    #print(item.values())
    return item
def main(page,keyword,city):
    html=get_start_url(page,keyword,city)
    result=parse_json(html)
    save_file(result,page)


def save_file(result,page):#将数据存为csv格式
    df=pd.DataFrame(result)
    df.to_csv(str(page)+'lagou.csv',index=False,sep=',')
    # with open('lagous.csv', 'a',encoding='utf-8') as csv_file:
    #     writer = csv.writer(csv_file)
    #     for key, value in result.items():
    #         writer.writerow([key, value])


if __name__ =='__main__':
    #pass
    #main(2,'爬虫','上海')
    for i in range(1,6):
        time.sleep(90)
        main(i,'爬虫','上海')
    #
    #     print(get_start_url(i))
# import csv,json, pandas as pd
# p=my ={'name': '海知智能开发部招聘爬虫开发实习生', 'company': '海知智能开发部招聘', 'salary': '3k-6k /上海 /经验应届毕业生 /本科及以上 /实习', 'temptation': '人工智能', 'qualifications': '\n岗位描述：\n1、负责维护与改进现有爬虫框架；\\n2、负责爬取业务相关网站；\\n3、负责提取与处理数据。\n\n岗位要求：\n1、统计、计算机或相关学士学位，大四或研究生；\n2、熟悉编程语言Java/Python；\n3、熟悉关系型/非关系型数据库（Mysql, Postgresql, Mongo）；\n4、熟悉网络，熟悉Linux，较强技术文档阅读能力；\n5、熟悉基本数据结构和算法，逻辑思维强；\6、有一定沟通理解和表达能力，完成和其他人协作，认真负责。\n', 'url': 'https://www.lagou.com/jobs/3827697.html'}
# with open('dict.csv', 'a' ,encoding='utf-8') as csv_file:
#     writer = csv.writer(csv_file)
#     for key, value in my.items():
#        writer.writerow([key, value])
#
# with open('dict.txt', 'a' ,encoding='utf-8') as f:
#     f.write(json.dumps(my,ensure_ascii=False,)+'/n')
#     f.close()
#
# with open('lagou.csv','w',encoding='utf-8') as file:
#     title = 'name\tcompany\tsalary\ttemptation\tqualifications\turl'
#     file.write(title)
#     items=str(p['name']) + '\t' + str(p['company']) + '\t' + str(p['salary']) + '\t' + \
#                    str(p['temptation']) + '\t' + str(p['qualifications']) + '\t' + str(p['url']) + '\n'
#     file.write(items)
#     file.close()
#
# #pd.DataFrame(my.keys(),my.values())
# #print(my.keys(),my.values(),my.items())
# print()
