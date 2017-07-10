let fs = require('fs')
let request = require('request')
let md5 = require('js-md5')
let moment = require('moment')
const Sequelize = require('sequelize')

/*const sequelize = new Sequelize('shoes', 'root', 'qiao@1982', {
  host: 'localhost',
  dialect: 'mysql',

  pool: {
    max: 5,
    min: 0,
    idle: 10000
  },
  define: {
    timestamps: false
  },
})*/
const sequelize = new Sequelize('shoes', 'mysql', 'zj_tech@321678', {
  host: '5843080a34d43.gz.cdb.myqcloud.com',
  dialect: 'mysql',
  port: '5274',

  pool: {
    max: 5,
    min: 0,
    idle: 10000
  },
  define: {
    timestamps: false
  },
})

const SPU = sequelize.define('spus', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
  },
  product_no: {
    type: Sequelize.STRING,
  },
  keyword_ebay: {
    type: Sequelize.STRING,
  }
})

const SpiderLog = sequelize.define('ebay_spider_log', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
  },
  keyword: {
    type: Sequelize.STRING,
  },
  product_name: {
    type: Sequelize.STRING,
  },
  deal_date: {
    type: Sequelize.STRING,
  },
  deal_price: {
    type: Sequelize.DECIMAL,
  },
  size_id: {
    type: Sequelize.DOUBLE,
  },
  deal_no: {
    type: Sequelize.STRING,
  },
  spu_id: {
    type: Sequelize.INTEGER,
  },
  aspect: {
    type: Sequelize.TEXT,
  },
  content: {
    type: Sequelize.TEXT,
  }
})

/**
 * @desc 获取ebay api搜索结果，该版本写csv文件
 *
 * 搜索的关键词、开始时间、结束时间、价格暂时在变量中提供
 */

let outputfile = './output.csv'

/**
 * @desc 根据页面数、最低价、关键词、开始日期、结束日期产生请求API的URL
 * @return string url
 */
function makeURL(page_number, on_going, min_price, query_string, fromdate, todate, app_name) {
  var urlfilter = "";
  var filterarray = [{
      "name": "MinPrice",
      "value": min_price == null ? 0 : min_price,
      "paramName": "Currency",
      "paramValue": "USD"
    }, // CNY
    {
      "name": "FreeShippingOnly",
      "value": "false",
      "paramName": "",
      "paramValue": ""
    }, {
      "name": "SoldItemsOnly",
      "value": "true",
      "paramName": "",
      "paramValue": ""
    }, {
      "name": "EndTimeFrom",
      "value": fromdate,
      "paramName": "",
      "paramValue": ""
    }, {
      "name": "EndTimeTo",
      "value": todate,
      "paramName": "",
      "paramValue": ""
/*    }, { // 筛选人民币
      "name": "Currency",
      "value": "CNY",
      "paramName": "",
      "paramValue": "",*/
    }
  ];

  // Iterate through each filter in the array
  for (var i = 0; i < filterarray.length; i++) {
    //Index each item filter in filterarray
    var itemfilter = filterarray[i];
    // Iterate through each parameter in each item filter
    for (var index in itemfilter) {
      // Check to see if the paramter has a value (some don't)
      if (itemfilter[index] !== "") {
        if (itemfilter[index] instanceof Array) {
          for (var r = 0; r < itemfilter[index].length; r++) {
            var value = itemfilter[index][r];
            urlfilter += "&itemFilter\(" + i + "\)." + index + "\(" + r + "\)=" + value;
          }
        } else {
          urlfilter += "&itemFilter\(" + i + "\)." + index + "=" + itemfilter[index];
        }
      }
    }
  }
  //davidkwa-bidtify-PRD-645f30466-13f9307d
  // Construct the request
  // Replace MyAppID with your Production AppID
  var url = "http://svcs.ebay.com/services/search/FindingService/v1";
  if (!on_going)
    url += "?OPERATION-NAME=findCompletedItems";
  else
    url += "?OPERATION-NAME=findItemsByKeywords";
  url += "&SERVICE-VERSION=1.0.0";
  url += "&SECURITY-APPNAME=" + app_name;
  url += "&GLOBAL-ID=EBAY-US";
  url += "&RESPONSE-DATA-FORMAT=JSON";
  //url += "&callback=_cb_findItemsByKeywords";
  url += "&REST-PAYLOAD";
  url += "&keywords="; //Adidas%20yeezy%20v2%20core%20black%20white%20size%2010
  url += encodeURIComponent(query_string);
  url += "&paginationInput.pageNumber=" + page_number;
  url += "&paginationInput.entriesPerPage=100";
  url += urlfilter;
  url += "&outputSelector=AspectHistogram"  // 获取aspect histogram
  return url;
}

function writeHead(file) {
  let headString = `no,title,itemId,startTime,endTime,currentPrice['@currencyId'],currentPrice['__value__'],sellingState,listingType,md5`
  fs.appendFileSync(file, headString + "\n")
}

function writeRecord(file, record, no, aspectHistogramContainer, query_string) {
  let {
    itemId: [ itemId ],
    listingInfo: [
      {
        bestOfferEnabled: [ bestOfferEnabled ],
        buyItNowAvailable: [ buyItNowAvailable ],
        endTime: [ endTime ],
        gift: [ gift ],
        listingType: [ listingType ],
        startTime: [ startTime ],
      }
    ],
    returnsAccepted: [ returnsAccepted ],
    sellingStatus: [{
      convertedCurrentPrice: [ convertedCurrentPrice ],  // 这里价格是对象，里边有两个值 @currencyId和__value__
      currentPrice: [ currentPrice ], // 这里价格是对象，有两个值 @currencyId和__value__
      sellingState: [ sellingState ],
    }],
    title: [ title ],
    topRatedListing: [ topRatedListing ],
  } = record

  let md5string = md5(JSON.stringify(record))

  // 将文本中的,替换为中文逗号，csv格式
  title = title.replace(/,/g, "，")
  let rowString = `${no},${title},${itemId},${startTime},${endTime},${currentPrice['@currencyId']},${currentPrice['__value__']},${sellingState},${listingType},${md5string}`

  fs.appendFileSync(file, rowString + "\n")
/**
  `last_time` datetime DEFAULT NULL,
  `keyword` varchar(64) NOT NULL,
  `product_name` varchar(255) NOT NULL COMMENT '产品名称',
  `deal_date` varchar(64) NOT NULL COMMENT '成交时间',
  `deal_price` decimal(10,0) NOT NULL COMMENT '成交价',
  `size_id` double NOT NULL COMMENT '尺码',
  `spu_id` int(11) NOT NULL COMMENT '产品id',
  `content` longtext COMMENT '整行数据',
 */


  let logRecord = SpiderLog.build({
    keyword: query_string,
    product_name: title,
    deal_date: startTime,
    deal_price: currentPrice['__value__'],
    size_id: 0,
    spu_id: 0,
    deal_no: itemId,
    aspect: JSON.stringify(aspectHistogramContainer),
    content: JSON.stringify(record),
  })

  logRecord.save()
}
function makeRequest(page_number, on_going, min_price, query_string, fromdate, todate, app_name) {
  let url = makeURL(page_number, on_going, min_price, query_string, fromdate, todate, app_name)
  console.log('Begin request :', url)
  request({uri:url}, function(err, response, body) {
    let json = JSON.parse(body)
/**
{ findCompletedItemsResponse:
   [ { ack: [Object],
       version: [Object],
       timestamp: [Object],
       searchResult: [Object],
       paginationOutput: [Object] } ] }
 */
    // 首先从响应中拿出各个属性
    console.log(json)
    let {
      findCompletedItemsResponse: [
        {
          ack,
          aspectHistogramContainer,
          paginationOutput: [
            {
              pageNumber: [ pageNumber ],
              entriesPerPage: [ entriesPerPage ],
              totalPages: [ totalPages ],
              totalEntries: [ totalEntries ],
            }
          ],
          searchResult,
          timestamp,
          version,
        }
      ]
    } = json

    if(aspectHistogramContainer) {
      let [
         {
           aspect,
           domainDisplayName: [ domainDisplayName ],
         }
      ] = aspectHistogramContainer
    }
    let [resStatus] = ack

    if(resStatus === 'Success') { // 请求成功
      let count = searchResult[0]['@count'] // 含有特殊符号，直接取出
      let [
        { item },
      ] = searchResult

      item && item.map(function(record, index){
        let no = entriesPerPage * (page_number - 1) + index + 1
        console.log('write row ', no)
        if(record) {
          writeRecord(outputfile, record, no, aspectHistogramContainer, query_string)
        }
      })

      if(page_number < totalPages) { // 如果还有记录，继续请求
        page_number++
        makeRequest(page_number, on_going, min_price, query_string, fromdate, todate, app_name)
      }
    } else if (resStatus === 'Failure') { // 请求失败
    }
  })
}

function task(query_string, start, end, min_price) {
  // 开始页码
  let page_number = 1

  // unkwown
  let on_going = false


  let fromdate = (new Date(start)).toISOString()
  let todate = (new Date(end)).toISOString()

  // API token
  let app_name = 'davidkwa-bidtify-PRD-645f30466-13f9307d'

  // 先删除原来文件
  fs.unlinkSync(outputfile)
  // 写表头
  writeHead(outputfile)
  // 请求数据，写表体
  makeRequest(page_number, on_going, min_price, query_string, fromdate, todate, app_name)
}


/*SPU.findAll().then(items => {
  items.map(item => {
    let keyword_ebay = item.keyword_ebay
    console.log(item, keyword_ebay)
    let start = '01 20,2017'
    let end = '06 20,2017'
    let min_price = 200
    // 查询关键词
//    keyword_ebay = 'Jordan 4 pure money'
//    keyword_ebay = 'nike supreme uptempo black'
    task(keyword_ebay, start, end, min_price)
  })
}).then(() => {
  //sequelize.close()
})*/

let keyword_ebay = 'Adidas EQT 93/17 core black turbo'

keyword_ebay = 'supreme Nike Air More Uptempo sz10.5 black'
keyword_ebay = 'Air Jordan 4 IV Retro Pure Money Authentic With Receipt White Silver Size 10'
keyword_ebay = 'Air Jordan'
let start = '01 20,2017'
let end = '06 20,2017'
let min_price = 20
task(keyword_ebay, start, end, min_price)

