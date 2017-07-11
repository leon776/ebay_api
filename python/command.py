#!/usr/bin/env python
# coding=utf-8

import sys
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

def main(argv):
    keyword = None
    start = None
    end = None
    price = None
    spuid = None
    brand = None

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

    print(options)
if __name__ == "__main__":
    main(sys.argv[1:])
