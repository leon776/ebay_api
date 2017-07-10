#!/usr/bin/env python

import requests
r = requests.get("http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findCompletedItems&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=davidkwa-bidtify-PRD-645f30466-13f9307d&GLOBAL-ID=EBAY-US&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords=Jordan%204%20pure%20money&paginationInput.pageNumber=1&paginationInput.entriesPerPage=100&itemFilter(0).name=MinPrice&itemFilter(0).value=160&itemFilter(0).paramName=Currency&itemFilter(0).paramValue=USD&itemFilter(1).name=FreeShippingOnly&itemFilter(1).value=false&itemFilter(2).name=SoldItemsOnly&itemFilter(2).value=true&itemFilter(3).name=EndTimeFrom&itemFilter(3).value=2017-05-19T16:00:00.000&itemFilter(4).name=EndTimeTo&itemFilter(4).value=2017-06-19T16:00:00.&outputSelector=AspectHistogram")


if r.status_code == requests.codes.ok:
    print r.json()
#    for k, v in r.json().items():
#        print k, v
