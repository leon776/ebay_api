# -*- coding: utf-8 -*-
import re
import json
import pymysql
import random
import hashlib
import time
import requests
from multiprocessing import Pool
import os
import logging

"""   mysql 建表语句
CREATE TABLE `taobao` (
  `id` int(20) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `search_list_title` text,
  `auction_title` text COMMENT '标题',
  `auction_auctionPrice` text,
  `auction_sku` text,
  `auction_aucNumId` text,
  `date` text,
  `rateId` text,
  `content` text,
  `user_rank` text,
  `user_nick` text,
  `aucNumId` varchar(50) DEFAULT NULL,
  `create_time` text,
  `page` text,
  `list` text,
  `shop_id` text,
  `shop_user_id` text,
  `url_d` text,
  `shop_url` text,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3633 DEFAULT CHARSET=utf8 COMMENT='淘宝店铺评论信息';
"""
def prox(url, headers):
    my_app_key = "106803123"
    app_secret = "8615a8df62d69fc2d9fdd2bec784d749"
    mayi_url = 's3.proxy.mayidaili.com'
    mayi_port = '8123'

    # 蚂蚁代理服务器地址
    mayi_proxy = {'http': 'http://{}:{}'.format(mayi_url, mayi_port)}

    # 计算签名
    timesp = '{}'.format(time.strftime("%Y-%m-%d %H:%M:%S"))
    codes = app_secret + 'app_key' + my_app_key + 'timestamp' + timesp + app_secret
    sign = hashlib.md5(codes.encode('utf-8')).hexdigest().upper()

    # 拼接一个用来获得蚂蚁代理服务器的「准入」的 header (Python 的 concatenate '+' 比 join 效率高)
    authHeader = 'MYH-AUTH-MD5 sign=' + sign + '&app_key=' + my_app_key + '&timestamp=' + timesp

    # 用 Python 的 Requests 模块。先订立 Session()，再更新 headers 和 proxies
    s = requests.Session()
    s.headers.update({'Proxy-Authorization': authHeader})
    s.proxies.update(mayi_proxy)
    if headers:
        cc = s.get(url, headers=headers)
    else:
        cc = s.get(url, headers=headers)
    return cc
def get_data(shop_url):
    TBNAME = "taobao"
    db = pymysql.connect(host='5843080a34d43.gz.cdb.myqcloud.com', port=5274, user='shoes', passwd='shoes@2016#$%^', db='shoes', charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
    # db = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='demo', charset='utf8',
    #                      cursorclass=pymysql.cursors.DictCursor)

    cursor = db.cursor()
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=TBNAME+'.log',
                        filemode='w')

    shop_id = re.findall('rate-(.*).htm', shop_url)[0]
    sql_s = "SELECT `date` FROM " + TBNAME + " WHERE shop_id = '" + shop_id + "' LIMIT 1"
    cursor.execute(sql_s)
    res = cursor.fetchall()
    if res:
        tt = res[0].get("date")
        last_time_unix = time.mktime(time.strptime(tt, '%Y年%m月%d日 %H:%M'))
    else:
        tt = "2010年1月1日 00:01"
        last_time_unix = time.mktime(time.strptime(tt, '%Y年%m月%d日 %H:%M'))

    for page in range(1, 50):
        shop_id = re.findall('rate-(.*).htm', shop_url)[0]
        current_milli_time = lambda: int(round(time.time() * 1000))
        headers = {
            'cookie':'_med=dw:1366&dh:768&pw:1366&ph:768&ist:0; thw=cn; _ga=GA1.2.1877918441.1497885726; miid=1583496525463143946; linezing_session=jQgJB9AWDBeDsIq4VGGvTpNd_14995167317209O1r_1; x=e%3D1%26p%3D*%26s%3D0%26c%3D3%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; v=0; uc3=sg2=BYbypVgrUkbJJpIZg%2Fc7g1DGc99zcwtJybqH3ZQmel4%3D&nk2=EUL80e6zs1B4XQ%3D%3D&id2=UNN4BKX0cAH%2BPQ%3D%3D&vt3=F8dBzWIOylFvLq0agA8%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D; existShop=MTQ5OTUyNjg2MA%3D%3D; uss=VymYWskzJMZ826rBfGfWURvFIZqeEEgOj%2B7bgKC0mL%2BPMa4FyB%2BkzBmj5A%3D%3D; lgc=rexqiutest; tracknick=rexqiutest; cookie2=2c6d4a0293dbc9e3037ed32265e3bc63; sg=t04; cookie1=B0T61i5lYHOAwo8ykOi%2FzL6ilU5Zn9POsb3uMLsp04I%3D; unb=3352470510; skt=83a7d5eb7e4971ae; t=e48d663acdaeb1de57f2dadabce3c884; _cc_=WqG3DMC9EA%3D%3D; tg=5; _l_g_=Ug%3D%3D; _nk_=rexqiutest; cookie17=UNN4BKX0cAH%2BPQ%3D%3D; l=Avv7i1UbYSyPqbV9Fjceyve2C9RlZg9S; _tb_token_=699e33e8ef81; mt=ci=0_1&cyk=-1_-1; uc1=cookie14=UoW%2BsW4HS2Kf5g%3D%3D&lng=zh_CN&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&existShop=false&cookie21=VT5L2FSpdiBh&tag=8&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&pas=0; isg=AkJCOcuSr33TkbMGVA61_obnk0hkuyIqDtzxjoxbHbVg3-NZdKHjPfVf-e1Y; cna=wtbOETd+CAkCAW/QcFWvRxa5',
        'upgrade-insecure-requests':'1',
        'user-agent':'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        if page == 1:
            url_c = "https://rate.taobao.com/member_rate.htm?_ksTS="+str(current_milli_time)+"_"+str(random.randint(1,1000))+"&callback=shop_rate_list&content=1&result=&from=rate&user_id="+shop_id+"&identity=1&rater=0&direction=0"
        elif page > 1:
            url_c = "https://rate.taobao.com/member_rate.htm?_ksTS="+str(current_milli_time)+"_"+str(random.randint(1,8000))+"&callback=shop_rate_list&content=1&result=&from=rate&user_id="+shop_id+"&identity=1&rater=0&direction=0&page="+str(page)
        # req = requests.get(url_c, headers=headers)
        req = prox(url_c, headers)                     #  使用代理 则取消注释

        if req.status_code == 200:
            logging.info("request OK !!!")
            jj = req.text.replace('shop_rate_list(', '').replace(')', '')
            s = json.loads(jj)
            list = 0
            if s["rateListDetail"]:
                for row  in s["rateListDetail"]:
                    list +=1
                    result = {}
                    # 标题
                    result['auction_title'] = row["auction"]["title"]
                    # 价格
                    result["auction_auctionPrice"] = row["auction"]["auctionPrice"]
                    # 颜色分类
                    result["auction_sku"] = row["auction"]["sku"]
                    # aucNumId
                    result["auction_aucNumId"] = row["auction"]["aucNumId"]
                    # date
                    result["date"] = row["date"]
                    # rateId
                    result["rateId"] = row["rateId"]
                    # content
                    result["content"] = row["content"]
                    # user_rank
                    result["user_rank"] = row["user"]["rank"]
                    # nick
                    result["user_nick"] = row["user"]["nick"]

                    result["shop_url"] = shop_url
                    result["shop_id"] = shop_id
                    result["page"] = str(list)+"---"+str(page)
                    result['create_time'] = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

                    date_unix = time.mktime(time.strptime(result["date"], '%Y年%m月%d日 %H:%M'))
                    if date_unix < last_time_unix:
                        logging.info("当前时间" + date_unix + "超过了表中的时间" + last_time_unix)
                        break
                    if result:  # 如果不为空
                        kkey = "`,`".join(map(str, result.keys()))
                        vvalue = '","'.join(map(str, result.values()))
                        sql = 'INSERT INTO  ' + TBNAME + ' (`' + kkey + '`) VALUES ("' + vvalue + '")'
                        # logging.info(sql)
                        try:
                            a = cursor.execute(sql)
                            db.commit()
                        except Exception as e:
                            logging.error(e)
                    else:
                        continue
            else:
                logging.warning(s)
        else:
            logging.error('false!!!!')
        logging.info("page "+str(page)+" is success")
        time.sleep(random.randint(400, 500))
if __name__=='__main__':
    p = Pool(2)
    shop_url_arr = ["https://rate.taobao.com/user-rate-UvG8bvF8SMCcW.htm?spm=a1z10.1-c-s.0.0.kiAzBm",
                    "https://rate.taobao.com/user-rate-UMFQLMmg0vGcT.htm?spm=a230r.7195193.1997079397.3.IHVTmd"]
    for i in shop_url_arr:
        p.apply_async(get_data, args=(i,))
        logging.info("Waiting for all subprocesses done...")
    p.close()
    p.join()
