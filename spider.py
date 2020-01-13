import requests
import re
from lxml import etree
import os
import random
import time


src_url = "https://s.weibo.com"
url = "https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6"
header = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'Cookie': 'SINAGLOBAL=4368590787044.595.1567714621870; _s_tentry=login.sina.com.cn; Apache=1382960326091.4114.1578472347182; ULV=1578472347190:5:2:2:1382960326091.4114.1578472347182:1578304638518; YF-V5-G0=2583080cfb7221db1341f7a137b6762e; Ugrow-G0=5c7144e56a57a456abed1d1511ad79e8; login_sid_t=54bb6b006010adc8a40b9538d29f0eaf; cross_origin_proto=SSL; WBtopGlobal_register_version=307744aa77dd5677; SCF=ApQoukW37S3vNQW-HTyvWyR3MRjJywyJ0KjPC_lsTmzAXQ7jcRJyA3z4xWYkHLZA3SiM5JUMViPHHmVNsp8qflA.; SUHB=0QS5VG0ij83Hrt; webim_unReadCount=%7B%22time%22%3A1578583756972%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A25%2C%22msgbox%22%3A0%7D; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WWcADJ1H2M2r1699D9YlbWZ5JpVF02feKMRSKzpSK-E; SUB=_2AkMpS8nWdcPxrAVSmvkWyW3haYVH-jyanqAgAn7uJhMyAxhu7kkRqSdutBF-XBrVSUi_BMJp-Aisc27svuCZ-AQ1; UOR=m.ali213.net,widget.weibo.com,login.sina.com.cn; YF-Page-G0=afcf131cd4181c1cbdb744cd27663d8d|1578648725|1578648552'
}
comment_request_url1 = "https://weibo.com/aj/v6/comment/big?ajwvr=6&id="
comment_request_url2 = "&from=singleWeiBo"
'''
comment_request_url = "https://weibo.com/aj/v6/comment/big?ajwvr=6&id=?&from=singleWeiBo(&__rnd=?)"
comment_request_url = "https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4459109472170327&root_comment_max_id=?&root_comment_max_id_type=0&root_comment_ext_param=&page=?&filter=hot&sum_comment_number=?&filter_tips_before=0&from=singleWeiBo(&__rnd=1578648738073)"
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'U_TRS1=0000005c.65794161.5ce3b8d9.94f2401b; UOR=www.baidu.com,blog.sina.com.cn,; SINAGLOBAL=221.4.34.12_1558427868.83793; lxlrttp=1560672234; gr_user_id=fcd4c413-fbec-4d15-a215-87b3adedf633; grwng_uid=8d35b6fd-6796-4288-9d4a-f5e95d57d2db; UM_distinctid=16ea7c83041709-0a1cf269535917-6313363-1fa400-16ea7c830421c5; SCF=ArmsTo98FJCCnKNy6v1uN4bn0IM1N4D4gX-CJw9xIqozmrvRS8iu6xYuxOsa6nZYM9nParbTvg8XQy6DQjhHrS4.; Apache=14.146.95.217_1578472347.172523; U_TRS2=0000008c.1e6c18bb7.5e15d1d8.b709914d; bdshare_firstime=1578488281473; ULV=1578488282165:7:1:1:14.146.95.217_1578472347.172523:1571134532884; ULOGIN_IMG=gz-0479e1ace5eb43194647d512ffdeab689e19; SUB=_2A25zEae3DeRhGeBN6VMS9SjPzjSIHXVQZp5_rDV_PUJbm9AfLU3ykW9NRJ2-9jg6QdYeY2Se2rGac9ywtg8maLr6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWcADJ1H2M2r1699D9YlbWZ5NHD95Qce0zpe0-ce0-RWs4DqcjG-fxDdJvEwBtt; sso_info=v02m6alo5qztZOVhqWum7eJuYmnlamZg7S2jLOIsYyzlLaMs5S4',
    'Host': 'my.sina.com.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}
'''
rank = []
affair = []
view = []


def main():

    #热搜榜
    html_source = requests.get(url, headers=header)
    html = etree.HTML(html_source.text)

    #排名 事件 热度
    print("排名  热搜事件  热度")
    rank = html.xpath('//td[@class="td-01 ranktop"]/text()')
    affair = html.xpath('//td[@class="td-02"]/a/text()')
    view = html.xpath('//td[@class="td-02"]/span/text()')

    #置顶
    top_url = re.findall(r'<a href="(.*?)" target="_blank">('+ affair[0] +')</a>', html_source.text)
    top_url = src_url + str(top_url[0][0])
    print("top", affair[0], view[0])
    html_top = requests.get(top_url, headers=header)

    #置顶话题
    top_topic_url = re.findall(r'<p class="from" >([\s\S]*?)</p>', html_top.text)
    top_topic_url = re.findall(r'<a href="(.*?)\?refer_flag=', top_topic_url[0])[0]
    top_topic_url = 'https:' + top_topic_url + '?type=comment'

    #置顶微博
    top_html = requests.get(top_topic_url, headers=header)
    top_html.encoding = "utf-8"
    comment_id = re.findall(r'action-type=\\"search_type\\" action-data=\\"id=(.*?)&filter=hot&from=singleWeiBo', top_html.text)[0]

    #评论ajax——url1
    comment_piece_url = comment_request_url1 + comment_id + comment_request_url2
    comment_piece = requests.get(comment_piece_url, headers=header)
    comment_piece.encoding = 'utf-8'
    comment = re.findall(r'<div class=\\"WB_text\\">\\n(.*?)<\\/div>', comment_piece.text)

    comment_content = []
    comment_number = 0
    for i in range(len(comment)):
        comment[i] = comment[i] + "<\/div>"
        nowcomment = re.findall(r'\\uff1a(.*?)<\\/div>', comment[i])
        if len(nowcomment) == 0:
            continue

        #评论文字部分处理
        nowcomment_text = re.sub(r'<.*?>', '', nowcomment[0])
        nowcomment_text = re.sub(r'&nbsp;', '', nowcomment_text)
        nowcomment_text = re.sub(r'\\n', '', nowcomment_text)
        nowcomment_text = re.sub(r'\\/', '/', nowcomment_text)
        nowcomment_text = nowcomment_text.encode('utf-8', errors='ignore').decode('unicode_escape')
        if len(nowcomment_text) == 0:
            continue
        comment_content.append(nowcomment_text)
        comment_number = comment_number + 1

    #获取ajax——url2~n
    while(comment_number <= 100):
        comment_piece_url = re.findall(r'action-data=\\"id=('+ comment_id +')(.*?)\\\\"', comment_piece.text)
        if len(comment_piece_url) == 0:
            break
        comment_piece_url = comment_request_url1 + comment_id + comment_piece_url[0][1] + comment_request_url2
        #print(comment_piece_url)
        comment_piece = requests.get(comment_piece_url, headers=header)
        comment_piece.encoding = 'utf-8'
        comment = re.findall(r'<div class=\\"WB_text\\">\\n(.*?)<\\/div>', comment_piece.text)
        for i in range(len(comment)):
            comment[i] = comment[i] + "<\/div>"
            nowcomment = re.findall(r'\\uff1a(.*?)<\\/div>', comment[i])
            if len(nowcomment) == 0:
                continue
            nowcomment_text = re.sub(r'<.*?>', '', nowcomment[0])
            nowcomment_text = re.sub(r'&nbsp;', '', nowcomment_text)
            nowcomment_text = re.sub(r'\\n', '', nowcomment_text)
            nowcomment_text = re.sub(r'\\/', '/', nowcomment_text)
            nowcomment_text = nowcomment_text.encode('utf-8', errors='ignore').decode('unicode_escape')
            if len(nowcomment_text) == 0:
                continue
            comment_content.append(nowcomment_text)
            comment_number = comment_number + 1
    print("共爬取"+str(comment_number)+"条评论")

    with open(affair[0] + '.txt', 'w', encoding='utf-8') as file:
        for i in range(comment_number):
            file.write(comment_content[i].encode('utf-8', errors='ignore').decode('utf-8'))
            file.write("\n")

    #热搜 len(affair)
    for i in range(1, 50):
        hot_url = re.findall(r'<a href="(.*?)" target="_blank">('+ affair[i] +')</a>', html_source.text)
        if len(hot_url) != 0:
            hot_url = src_url + str(hot_url[0][0])
        else:
            continue
        print(i, affair[i], view[i])
        try:
            html_hot = requests.get(hot_url, headers=header)
            time.sleep(random.random())
        except requests.exceptions.InvalidURL:
            continue
        html_hot.encoding = "utf-8"
        top_topic_url = re.findall(r'<p class="from" >([\s\S]*?)</p>', html_hot.text)
        if len(top_topic_url) == 0:
            continue
        top_topic_url = re.findall(r'<a href="(.*?)\?refer_flag=', top_topic_url[0])
        if len(top_topic_url) == 0:
            continue
        else:
            top_topic_url = top_topic_url[0]
        top_topic_url = 'https:' + top_topic_url + '?type=comment'
        hot_html = requests.get(top_topic_url, headers=header)
        time.sleep(random.random())
        hot_html.encoding = "utf-8"
        comment_id = re.findall(r'action-type=\\"search_type\\" action-data=\\"id=(.*?)&filter=hot&from=singleWeiBo', hot_html.text)
        if len(comment_id) != 0:
            comment_id = comment_id[0]
        else:
            continue
        comment_piece_url = comment_request_url1 + comment_id + comment_request_url2
        comment_piece = requests.get(comment_piece_url, headers=header)
        time.sleep(random.random())
        comment_piece.encoding = 'utf-8'
        comment = re.findall(r'<div class=\\"WB_text\\">\\n(.*?)<\\/div>', comment_piece.text)
        comment_content = []
        comment_number = 0
        for j in range(len(comment)):
            comment[j] = comment[j] + "<\/div>"
            nowcomment = re.findall(r'\\uff1a(.*?)<\\/div>', comment[j])
            if len(nowcomment) == 0:
                continue
            nowcomment_text = re.sub(r'<.*?>', '', nowcomment[0])
            nowcomment_text = re.sub(r'&nbsp;', '', nowcomment_text)
            nowcomment_text = re.sub(r'\\n', '', nowcomment_text)
            nowcomment_text = re.sub(r'\\/', '/', nowcomment_text)
            nowcomment_text = nowcomment_text.encode('utf-8', errors='ignore').decode('unicode_escape')
            if len(nowcomment_text) == 0:
                continue
            comment_content.append(nowcomment_text)
            comment_number = comment_number + 1
        while (comment_number <= 100):
            comment_piece_url = re.findall(r'action-data=\\"id=(' + comment_id + ')(.*?)\\\\"', comment_piece.text)
            if len(comment_piece_url) == 0:
                break
            comment_piece_url = comment_request_url1 + comment_id + comment_piece_url[0][1] + comment_request_url2
            #print(comment_piece_url)
            comment_piece = requests.get(comment_piece_url, headers=header)
            time.sleep(random.random())
            comment_piece.encoding = 'utf-8'
            comment = re.findall(r'<div class=\\"WB_text\\">\\n(.*?)<\\/div>', comment_piece.text)
            for j in range(len(comment)):
                comment[j] = comment[j] + "<\/div>"
                nowcomment = re.findall(r'\\uff1a(.*?)<\\/div>', comment[j])
                if len(nowcomment) == 0:
                    continue
                nowcomment_text = re.sub(r'<.*?>', '', nowcomment[0])
                nowcomment_text = re.sub(r'&nbsp;', '', nowcomment_text)
                nowcomment_text = re.sub(r'\\n', '', nowcomment_text)
                nowcomment_text = re.sub(r'\\/', '/', nowcomment_text)
                nowcomment_text = nowcomment_text.encode('utf-8', errors='ignore').decode('unicode_escape')
                if len(nowcomment_text) == 0:
                    continue
                comment_content.append(nowcomment_text)
                comment_number = comment_number + 1
        print("共爬取" + str(comment_number) + "条评论")
        with open(affair[i] + '.txt', 'w', encoding='utf-8') as file:
            for j in range(comment_number):
                file.write(comment_content[j].encode('utf-8', errors='ignore').decode('utf-8'))
                file.write("\n")
        time.sleep(5)
    os.system("pause")


file_dir = r"E:\Grade 15  2019\Python课\2019.12.22\test2"


def find(voca):
    num = 0
    for filename in os.listdir(file_dir):
        if filename.endswith('.txt'):
            with open(filename, 'r', encoding='utf-8') as file:
                comment_piece = file.readlines()
                for j in range(len(comment_piece)):
                    flag = re.findall(r'('+ voca +')', comment_piece[j])
                    if len(flag) != 0:
                        print(comment_piece[j])
                        num = num + 1
    print(num)


main()
#find("哈哈哈哈")
