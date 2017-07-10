#!/usr/bin/env python
# coding=utf-8
# Filename: search.py

import sys
import requests
import time
import datetime

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
        page_number = 1
    ):

    baseURL = '{url}&paginationInput.pageNumber={page_number}&paginationInput.entriesPerPage=100'.format(
        page_number = page_number,
        url = url
    )

    for k, size in enumerate(sizes):
        sizeURL = getSizeUrl(url, name, size['@valueName'])
        print(sizeURL)
        response = requests.get(sizeURL)
        if response.status_code == requests.codes.ok:
            result = response.json()['findCompletedItemsResponse'][0]
            ack = result['ack'][0]
            print(ack)


'''
@desc 发送请求
'''
def makeRequest(keyword, start, end, price, spuid, brand, page_number = 1):
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
                    page_number = page_number
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
                    page_number = page_number
                )

            # Not Specified ??

makeRequest(
    keyword = 'Jordan 4 pure money',
    start = '01/20,2017',
    end = '07/01,2017',
    price = 200,
    spuid = 11,
    brand = 'Nike'
)