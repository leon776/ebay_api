#!/usr/bin/env python
# coding=utf-8
# Filename: search.py

import sys
import requests
import time
import datetime
import csv
import json
import pymysql
import os
import getopt
import math
import logging
import re

cateIds = [
    93427,      # Men's shoes 
    3034,       # Women's shoes
    57929,      # Boys' Shoes
    57974,      # Unisex Shoes
    155202,     # Girls' Shoes
]
# 美码、欧码属性名
textUSA = "US Shoe Size (Men's)"
textEURO = "Euro Size"
newWithBox = 'New with box'
cwd = os.path.split(os.path.realpath(__file__))[0]

DB_HOST = '127.0.0.1'
DB_USER = 'dev'
DB_PASS = 'dev@2017'
DB_NAME = 'shoes'
DB_PORT = 3306
DB_CHARSET = 'utf8mb4'

# 暂时废弃
records = {}
bulkSize = 10


def getLogger(name):
    logger = logging.getLogger(name)
    hdlr = logging.FileHandler('{}/ebay_spider_{}.log'.format(cwd, name))
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.INFO)

    return logger

sql_logger = getLogger('sql')
url_logger = getLogger('url')
misc_logger = getLogger('misc')

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

def printUsage():
    cmdText = 'Usage: command.py --k <keyword> -s <start> -e <end> -p <price> -i <spuid> -b <brand>'

    print('-' * 100)
    print('')
    print(cmdText)
    print('')
    print('-' * 100)
    print()
    print()
    print('-h, --help', '显示帮助')
    print('-k, --keyword <keyword>', '搜索关键词, 关键词含空格，用引号引起来')
    print('-s, --start <mm dd,yyyy>', '搜索的开始日期，格式为: mm dd,yyyy')
    print('-e, --end <mm dd,yyyy>', '搜索的结束日期，格式为: mm dd,yyyy')
    print('-p, --price <price>', '过滤的最低价，单位USD')
    print('-i, --spuid <spuid>', 'spuid')
    print('-b, --brand <brand>', 'brand name')
    print()
    print()

def getOpts(opts):
    keyword = None
    start = None
    end = None
    price = None
    spuid = None
    brand = None

    for opt, arg in opts:
        if opt == '-h':
            printUsage()
            sys.exit()
        elif opt in ("-k", "--keyword"):
            keyword = arg
        elif opt in ("-s", "--start"):
            start = arg
        elif opt in ("-e", "--end"):
            end = arg
        elif opt in ("-p", "--price"):
            price = arg
        elif opt in ("-i", "--spuid"):
            spuid = arg
        elif opt in ("-b", "--brand"):
            brand = arg
    if(
        keyword is None or
        start is None or
        end is None or
        price is None or
        spuid is None or
        brand is None
    ):
        return None
    else:
        return {
            "keyword": keyword,
            "start": start,
            "end": end,
            "price": price,
            "spuid": spuid,
            "brand": brand,
        }

def connection():
    # need modify database charset to utf8mb4
    # ALTER DATABASE shoes CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;
    # https://stackoverflow.com/questions/20411440/incorrect-string-value-xf0-x9f-x8e-xb6-xf0-x9f-mysql
    db = pymysql.connect(
        host = DB_HOST,
        port = DB_PORT,
        user = DB_USER,
        password = DB_PASS,
        db = DB_NAME,
        charset = DB_CHARSET, # Exception when insert, not sure why
        cursorclass = pymysql.cursors.DictCursor,
    )

    return db

def close_db(db):
    db.close()

'''
@desc 根据关键词、开始时间、结束时间、最低价等产生搜索URL
@param query_sting String: 请求关键词
@param fromdate String: 开始时间，格式mm/dd,yyyy, 例如01/20,2017
@param todate String: 结束时间，格式mm/dd,yyyy, 例如01/20,2017
@param page_number Number: 请求页码数
@param min_price Number: 过滤的最低价

@return url String: 返回请求url
'''
def makeURL(
        query_string,                    # 请求关键词
        fromdate = None,                 # 开始日期 格式 mm/dd,yyyy
        todate = None,                   # 结束日期 格式 mm/dd,yyyy
        app_name = 'davidkwa-bidtify-PRD-645f30466-13f9307d',  # token string
        page_number = 1,                 # 请求分页页码
        on_going = False,                # 暂时无用
        min_price = None,                 # 过滤的最低价
    ):

    if fromdate is not None:
        _tfrom = time.strptime(fromdate,'%m/%d,%Y')
        fromdate = datetime.datetime(*_tfrom[:3]).isoformat()

    if todate is not None:
        _tto = time.strptime(todate,'%m/%d,%Y')
        todate = datetime.datetime(*_tto[:3]).isoformat()

    filters = [
        {      # 最低价
            "name"       : "MinPrice",
            "value"      : 0 if min_price is None else min_price,
            "paramName"  : "Currency",
            "paramValue" : "USD",
        }, {   # 免运费
            "name"       : "FreeShippingOnly",
            "value"      : False,
            "paramName"  : None,
            "paramValue" : None,
        }, {   # 仅销售项
            "name"       : "SoldItemsOnly",
            "value"      : True,
            "paramName"  : None,
            "paramValue" : None,
        }, {   # 结束时间的开始日期
            "name"       : "EndTimeFrom",
            "value"      : fromdate,
            "paramName"  : None,
            "paramValue" : None,
        }, {   # 结束时间的结束日期
            "name"       : "EndTimeTo",
            "value"      : todate,
            "paramName"  : None,
            "paramValue" : None,
        }
    ]

    urlfilter = ''
    for index, filter in enumerate(filters):
        for key in filter:
            if filter[key] is not None:
                if isinstance(filter[key], list):
                    print('is array')
                else:
                    urlfilter += "&itemFilter({index}).{key}={value}".format(
                        index=index,
                        key=key,
                        value=filter[key]
                    )

    url = 'http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME={API}&SERVICE-VERSION=1.0.0&SECURITY-APPNAME={app_name}&GLOBAL-ID=EBAY-US&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords={keywords}{urlfilter}'.format(
        API = 'findCompletedItems' if on_going is False else 'findItemsByKeywords',
        app_name = app_name,
        keywords = query_string,
        urlfilter = urlfilter
    )

    return url

def getAspectUrl(url, page_number, cid = None):
    url = '{url}&outputSelector(0)=AspectHistogram&paginationInput.pageNumber={page_number}&paginationInput.entriesPerPage=100'.format(url = url, page_number = page_number)
    if cid is not None:
        url += '&categoryId=' + str(cid)

    return url

def getSizeUrl(url, name, value):
    return '{url}&aspectFilter(0).aspectName={sizeName}&aspectFilter(0).aspectValueName={sizeValue}'.format(
        url = url,
        sizeName = name,
        sizeValue = value,
    )

def searchWithSizes(
        url,
        sizes,
        name,
        keyword,
        spuid,
        brand,
        table_name,
        file,
        page_number = 1
    ):


    baseURL = '{url}&paginationInput.pageNumber={page_number}&paginationInput.entriesPerPage=100'.format(
        page_number = page_number,
        url = url
    )

    for k, size in enumerate(sizes):
        sizeValue = size['@valueName']
        sizeURL = getSizeUrl(url, name, sizeValue)
        url_logger.info('URL with Size: ' + sizeURL)
        print('URL with size: ', sizeURL)
        response = requests.get(sizeURL)
        if response.status_code == requests.codes.ok:
            result = response.json()['findCompletedItemsResponse'][0]
            ack = result['ack'][0]

            if(ack == 'Success'):
                searchResult = result['searchResult'][0]
                paginationOutput = result['paginationOutput'][0]
                entriesPerPage = int(paginationOutput['entriesPerPage'][0])
                totalPages = int(paginationOutput['totalPages'][0])
                totalEntries = int(paginationOutput['totalEntries'][0])
              
                item = []
                if('item' in searchResult):
                    item = searchResult['item']

                #print(paginationOutput, entriesPerPage, totalPages, totalEntries, item)
                if(len(item) > 0):
                    with open(file, 'a+') as csvfile:
                        spamwriter = csv.writer(csvfile)
                        for index, rec in enumerate(item):
                            itemId = rec['itemId'][0]
                            listingInfo = rec['listingInfo'][0]
                            sellingStatus = rec['sellingStatus'][0]
                            title = rec['title'][0]
                            currentPrice = sellingStatus['currentPrice'][0]['__value__']
                            currencyId = sellingStatus['currentPrice'][0]['@currencyId']
                            startTime = listingInfo['startTime'][0]
                            endTime = listingInfo['endTime'][0]
                            try:
                                conditionDisplayName = rec['condition'][0]['conditionDisplayName'][0]
                            except:
                                conditionDisplayName = ''

                            if(conditionDisplayName != newWithBox):
                                record = {
                                    "keyword": keyword,
                                    "product_name": emoji_filter(title),
                                    "deal_date": startTime,
                                    "currency": currencyId,
                                    "deal_price": currentPrice,
                                    "size_name": name,
                                    "brand": brand,
                                    "size": sizeValue,
                                    "size_id": sizeValue,
                                    "deal_no": itemId,
                                    "spu_id": spuid,
                                    "aspect": json.dumps(sizes, sort_keys = True),
                                    "content": json.dumps(rec, sort_keys = True)
                                }
                                records[itemId] = record

                                insertSQL = '''REPLACE INTO {table_name} (keyword, product_name, deal_date, currency, deal_price, size_name, brand, size, size_id, deal_no, spu_id, aspect, content) VALUES '''.format(table_name = table_name)

                                values = []
                                valueSQL = '''("{keyword}", "{product_name}", "{deal_date}", "{currency}", {deal_price}, "{size_name}", "{brand}", "{size}", "{size_id}", "{deal_no}", "{spu_id}", "{aspect}", "{content}")'''                                                                                                                                                                     
                                sql = insertSQL + valueSQL.format(
                                    keyword = pymysql.escape_string(record['keyword']), 
                                    product_name = pymysql.escape_string(record['product_name']),
                                    deal_date = record['deal_date'],
                                    currency = record['currency'],
                                    deal_price = record['deal_price'],
                                    size_name = record['size_name'],
                                    brand = record['brand'],
                                    size = record['size'],
                                    size_id = record['size_id'],
                                    deal_no = record['deal_no'],
                                    spu_id = record['spu_id'],
                                    aspect = pymysql.escape_string(json.dumps(record['aspect'], sort_keys = True)),
                                    content = pymysql.escape_string(json.dumps(record, sort_keys = True))
                                )

                                sql_logger.info('bulk insert sql: ' + sql)
                                try:

                                    cursor.execute(sql)

                                except Exception as e:
                                    sql_logger.error('Exception sql: ' + sql)   
                                    print('ignore the row', sql)



                                spamwriter.writerow([
                                    keyword,
                                    title,
                                    startTime,
                                    currencyId,
                                    currentPrice,
                                    name,
                                    brand,
                                    sizeValue,
                                    sizeValue,
                                    spuid,
                                    itemId,
                                    json.dumps(sizes, sort_keys = True),
                                    json.dumps(record, sort_keys = True)
                                ])

                                            
                            # 必需commit才能到数据库中
                            conn.commit()

                    #print(sizeURL, len(records), page_number, totalPages)
                    if(page_number < totalPages):
                        page_number = page_number + 1
                        searchWithSizes(
                            url = url,
                            sizes = sizes,
                            name = name,
                            keyword = keyword,
                            spuid = spuid,
                            brand = brand,
                            page_number = page_number,
                            table_name = table_name,
                            file = file
                        )

'''
@desc 发送请求
'''
def makeRequest(keyword, start, end, price, spuid, brand, file, table_name = '', page_number = 1, useCate = False):
    url = makeURL(
        query_string = keyword,
        min_price = price,
        fromdate = start,
        todate = end,
    )

    aspectURLs = []
    if not useCate: # 首先不用分类id查询, 提高效率
        aspectURLs.append(getAspectUrl(url, page_number))
    else: # 直接查询没有拿到aspect, 使用分类ID查询
        for cid in cateIds:
            aspectURLs.append(getAspectUrl(url, page_number, cid = cid))

    print(aspectURLs)
    for aspectURL in aspectURLs:
        url_logger.info('URL with aspect: ' + aspectURL)
        print('URL with aspect: ', aspectURL)
        response = requests.get(aspectURL)
        if response.status_code == requests.codes.ok:
            result = response.json()['findCompletedItemsResponse'][0]
            ack = result['ack'][0]

            # 首先查询结果为成功状态，同时需要包含aspectHistogramContainer键
            if (ack == 'Success' and
                'aspectHistogramContainer' in result.keys()
            ):
                aspectHistogramContainer = result['aspectHistogramContainer'][0]
                aspect = aspectHistogramContainer['aspect']

                # 美码、欧码属性列表
                sizesUSA = []
                sizesEURO = []
                for k, prop in enumerate(aspect):
                    if (prop['@name'] == textUSA):
                        sizesUSA = prop['valueHistogram']

                    if (prop['@name'] == textEURO):
                        sizesEURO = prop['valueHistogram']

                lenUSA = len(sizesUSA)
                lenEURO = len(sizesEURO)

                if(lenUSA == 0 and lenEURO == 0 and useCate is False): # 使用关键词查询有aspect, 但没有尺寸的，同样使用分类进行重查
                    makeRequest(
                        keyword = keyword,
                        start = start,
                        end = end,
                        price = price,
                        spuid = spuid,
                        brand = brand,
                        table_name = table_name,
                        file = file,
                        useCate = True
                    )
                
                # 遍历美码
                if(lenUSA > 0):
                    searchWithSizes(
                        url = url,
                        sizes = sizesUSA,
                        name = textUSA,
                        keyword = keyword,
                        spuid = spuid,
                        brand = brand,
                        page_number = page_number,
                        table_name = table_name,
                        file = file
                    )

                # 遍历欧码
                if(lenEURO > 0):
                    searchWithSizes(
                        url = url,
                        sizes = sizesEURO,
                        name = textEURO,
                        keyword = keyword,
                        spuid = spuid,
                        brand = brand,
                        page_number = page_number,
                        table_name = table_name,
                        file = file
                    )

                # Not Specified ??
            else:
                if(useCate is False) : # 如果还未用分类查询，那么用分类进行查询
                    makeRequest(
                        keyword = keyword,
                        start = start,
                        end = end,
                        price = price,
                        spuid = spuid,
                        brand = brand,
                        table_name = table_name,
                        file = file,
                        useCate = True
                    )


def runTask(options):
    keyword = options['keyword']
    start = options['start']
    end = options['end']
    price = options['price']
    spuid = options['spuid']
    brand = options['brand']

    table_name = getTableName('ebay_spider_logs', int(spuid))
    #print(table_name)
    #cwd = os.getcwd()
    outfile = 'output_{spuid}_{start}_{end}_{price}.data'.format(
        spuid = spuid,
        start = start,
        end = end,
        price = price,
    ).replace(',', '').replace('/', '')

    outfile = cwd + '/datas/' + outfile

    makeRequest(
        keyword = keyword,
        start = start,
        end = end,
        price = price,
        spuid = spuid,
        brand = brand,
        table_name = table_name,
        file = outfile,
    )


def getTableName(table_name, spuid):
   table_name = '%s_%02d' % (table_name, int(spuid % 10))
   return table_name
def emoji_filter(text):
    # https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python
    emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text) # no emoji

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hk:s:e:p:i:b:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        printUsage()
        sys.exit(2)

    if(len(opts) == 0):
        printUsage()
        sys.exit(2)

    options = getOpts(opts)
    if(options is None):
        printUsage()
        sys.exit(2)

    runTask(options)

if __name__ == "__main__":
    conn = connection()

    cursor = conn.cursor()

    # insert exception fixed
    cursor.execute('SET NAMES utf8mb4;')
    cursor.execute('SET CHARACTER SET utf8mb4;')
    cursor.execute('SET character_set_connection=utf8mb4;')

    main(sys.argv[1:])
    conn.close()
