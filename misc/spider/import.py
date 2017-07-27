import json
import codecs
import glob
import os
from pprint import pprint
import pymongo
import time
import ssl

from selenium import webdriver

import urllib.request


client = pymongo.MongoClient("localhost", 27017)
# db
db = client.taobao

driver = None

SHOP_LIST = [["烽火体育SNEAKER之家", "beaconfire", "UvG8bvF8SMCcW"],
    ["四川正品小店", "yysport", "UMFQLMmg0vGcT"],
    ["Class-space", "cspace", "UOFIuMGkYvCx0"],
    ["库客运动", "cooke", "UMmcbvmQWOFvT"],
    ["雷恩体育", "solestage", "UvCx0vGcLvCxT"],
    ["蓝带体育", "blueribbon", "UvCcSOmNLvFN4"],
    ["gogo球鞋", "gogo", "UvFcbMGg4MFHSvNTT"],
    ["厚道体育运动正品店", "holdsports", "UvCH0MCQGvGx4"],
    ["厚道体育", "holdsports", "UvCH0MCQGvGx4"],
    ["球鞋家Sneakerfamily", "sneakerfamily", "UMGkYMmxYMCNG"],
    ["燎原装备Diffusion", "diffusion", "UvFguMFIbMFI0MQTT"],
    ["天津鞋门", "tjxm", "UvFNSMFH0vFHy"],
    ["NL23hood", "nl23hood", "UvCQ0vCvbvm8bOQTT"],
    ["小鸿体育", "hung", "UvFcuMmNuvCN0"],
    ["兄弟体育", "xiongdi", "UvFkGMFkYOmILOQTT"],
    ["抓地力潮流", "traction", "UMFc0MCv0vmNS"],
    ["OK球鞋", "oksneakers", "UMCxSvmxyOFHG"],
    ["姚家军", "sneakerlovers", "UvCQGOF8GMC8bvgTT"],
    ["巫师鞋柜", "wizard", "UOm84MFxYMFvT"],
    ["乔飞天下", "jordan365", "UMC8WMCNYvCxb"],
    ["牛哄哄运动店", "nhhyyd", "UvFIyvFc4vmIu"],
    ["Sneaker便利店", "sneakerconven", "UvCxYvGxuMFxGONTT"],
    ["快客体育freshshoes", "freshshoes", "UMGgbOmIYMCkb"],
    ["穿行体育cx club", "cx", "UMF80OmHYMmxT"],
    ["虎扑伙伴", "hupuhuoban", "UMCcbOmkyvCcS"],
    ["嘎嘎体育馆", "hlp00345", "UMGNGvmHYMmxb"],
    ["xx体育馆", "hlp00345", "UMGNGvmHYMmxb"],
    ["牛牛体育", "niuniu", "UvFNbvF8GvGv0MgTT"],
    ["凤凰体育", "phoenix", "UMCx4vmHWMF8L"],
    ["Chips运动", "chips", "UvFHGvCc0MGgbOQTT"],
    ["kikipipi", "kikipipi", "UOFguvmvGMCvT"]
]


def importJsonText(jsonTxt, shop):
    """
    Import multiple record with a JSON text, with the specific shop
    :jsonTxt - string JSON string of the rate list
        After json decode, the data['rateListDetail'] should be a list of taobao rates
    :shop - string the shopid (defined by ourselves)
    """
    data = json.loads(jsonTxt)
    skipped = False
    count = 0
    skipped = 0
    for rate in data['rateListDetail']:
        # Stop if there's an older record
        rate['myShopId'] = shop
        oldRate = db.shoes.find_one({'rateId' : rate['rateId']})
        if oldRate:
            if (rate['date'] != oldRate['date']):
                print("Rate ID seems not reliable. Exiting...")
                exit()
            skipped += 1
        else:
            db.shoes.insert_one(rate)
            count += 1
    print(str(count) + ' records imported. ' + str(skipped) + ' skipped.')
    return skipped == 0

def importFile(file, shop):
    """
    Import a json file downloaded from taobao
    :file - string the file path of the file to be imported
    :shop - string the shopid (defined by ourselves)
    """
    print("Importing file: `" + file + "`")
    _lines = codecs.open(file, 'r', encoding='gb18030').readlines()
    stripped = _lines[0].strip()
    suffixCutPos = 15 if stripped[0:14] == 'shop_rate_list' else 1;
    jsonTxt = stripped[suffixCutPos:-1]

    return importJsonText(jsonTxt, shop)

def importFolder(folder, shop):
    """
    Import a folder with json files downloaded from taobao, the files must end with ".htm"
    :folder - string the file path of the folder
    :shop - string the shopid (defined by ourselves)
    """
    print('Importing folder `' + folder + '` to collection `' + shop + '`...')
    for path, subdirs, files in os.walk(folder):
        for name in files:
            file = os.path.join(path, name)

            if not name.endswith("htm"):
                continue

            importFile(file, shop)


def crawlShop(urlSuffix, shopName):
    """
    Still experimenting
    """
    for i in range(1, 42):
        print('Importing page ' + str(i) + "...")
        url = urlSuffix + str(i)

        driver.get(url)
        pageSource = driver.page_source
        jsonTxt = pageSource.strip()[1:-1]
        importJsonText(jsonTxt, shopName)
        time.sleep(300)

def setupChromeDriver():
    """
    Setting up Selenium Chrome Driver
    Doesn't need this unless you crawl with selenium
    """
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    global driver
    driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)

def _getShopNameWithFolderName(name):
    for shop in SHOP_LIST:
        if name == shop[0]:
            return shop[1]

    return name

def importMultiShopsFolder(path):
    for name in os.listdir(path):
        folderPath = path + "/" + name
        if os.path.isdir(folderPath):
            shopName = _getShopNameWithFolderName(name)
            #print(name + ":" + shopName)
            #print("importFolder(" + folderPath + ", " + shopName + ")")
            importFolder(folderPath, shopName)


#setupChromeDriver()
#time.sleep(60)
#crawlShop('https://rate.taobao.com/member_rate.htm?user_id=UvG8bvF8SMCcW^&page=', 'beaconfire')

#importFolder('./data/html20160625/cooke/', 'cooke')
importMultiShopsFolder("./data")


# url = "https://rate.taobao.com/member_rate.htm?user_id=UvG8bvF8SMCcW&page=1"
# gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
# req = urllib.request.Request(
#     url,
#     data=None, 
#     headers={
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
#     }
# )
# f = urllib.request.urlopen(req, context=gcontext)
# print(f.read().decode('utf-8'))



## for each rateListDetail insert to database