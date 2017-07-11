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
    db = pymysql.connect(
        host = "127.0.0.1",
        port = 3306,
        user = "dev",
        password = "dev@2017",
        db = "shoes",
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
        min_price = None                 # 过滤的最低价
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

    #print(urlfilter)

    url = 'http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME={API}&SERVICE-VERSION=1.0.0&SECURITY-APPNAME={app_name}&GLOBAL-ID=EBAY-US&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords={keywords}{urlfilter}'.format(
        API = 'findCompletedItems' if on_going is False else 'findItemsByKeywords',
        app_name = app_name,
        keywords = query_string,
        urlfilter = urlfilter
    )

    return url

def getAspectUrl(url, page_number):
    return '{url}&outputSelector(0)=AspectHistogram&paginationInput.pageNumber={page_number}&paginationInput.entriesPerPage=100'.format(url = url, page_number = page_number)

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

    records = []
    for k, size in enumerate(sizes):
        sizeValue = size['@valueName']
        sizeURL = getSizeUrl(url, name, sizeValue)
        print(sizeURL)
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

                print(paginationOutput, entriesPerPage, totalPages, totalEntries, item)
                if(len(item) > 0):
                    with open(file, 'a+') as csvfile:
                        spamwriter = csv.writer(csvfile)
                        for index, record in enumerate(item):
                            itemId = record['itemId'][0]
                            listingInfo = record['listingInfo'][0]
                            sellingStatus = record['sellingStatus'][0]
                            title = record['title'][0]

                            currentPrice = sellingStatus['currentPrice'][0]['__value__']
                            currencyId = sellingStatus['currentPrice'][0]['@currencyId']
                            startTime = listingInfo['startTime'][0]
                            endTime = listingInfo['endTime'][0]

                            rowDict = {
                                "keyword": keyword,
                                "product_name": title,
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
                                "content": json.dumps(record, sort_keys = True)
                            }
                            records.append(rowDict)
                            insertSQL = 'INSERT INTO %s (keyword, product_name, deal_date, currency, deal_price, size_name, brand, size, size_id, deal_no, spu_id, aspect, content) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (table_name, pymysql.escape_string(keyword), pymysql.escape_string(title), startTime, currencyId, currentPrice, name, brand, sizeValue, sizeValue, itemId, spuid, pymysql.escape_string(json.dumps(sizes, sort_keys = True)), pymysql.escape_string(json.dumps(record, sort_keys = True)))
                            print(insertSQL)
                            try:
                                cursor.execute(insertSQL)
                            except Exception as e:
                                print('ignore the row')

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
                    print(sizeURL, len(records), page_number, totalPages)
                    if(page_number < totalPages):
                        page_number = page_number + 1
                        searchWithSizes(
                            url = sizeURL,
                            sizes = sizes,
                            name = name,
                            keyword = keyword,
                            spuid = spuid,
                            brand = brand,
                            page_number = page_number
                        )

'''
@desc 发送请求
'''
def makeRequest(keyword, start, end, price, spuid, brand, file, table_name = '', page_number = 1):
    url = makeURL(
        query_string = keyword,
        min_price = price,
        fromdate = start,
        todate = end
    )

    aspectURL = getAspectUrl(url, page_number)

    print(aspectURL)
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
            # 美码、欧码属性名
            textUSA = "US Shoe Size (Men's)"
            textEURO = "Euro Size"

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

def runTask(options):
    keyword = options['keyword']
    start = options['start']
    end = options['end']
    price = options['price']
    spuid = options['spuid']
    brand = options['brand']

    table_name = getTableName('ebay_spider_logs', int(spuid))
    cwd = os.getcwd()
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
    main(sys.argv[1:])
    conn.close()
