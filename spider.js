let fs = require('fs')
let request = require('request')
let moment = require('moment')
const Sequelize = require('sequelize')

const sequelize = new Sequelize('shoes', 'mysql', 'zj_tech@321678', {
  host: '5843080a34d43.gz.cdb.myqcloud.com',
  dialect: 'mysql',
  port: '5274',

  pool: {
    max: 5,
    min: 0,
//    idle: 1000
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
  size_name: {
    type: Sequelize.STRING,
  },
  size: {
    type: Sequelize.STRING,
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
  url += urlfilter;
  return url;
}

function searchAspect(baseUrl, query_string) {
  let page_number = 1
  // step 1: 获取aspect histogram
  url = baseUrl + "&outputSelector(0)=AspectHistogram"
  url += "&paginationInput.pageNumber=" + page_number;
  url += "&paginationInput.entriesPerPage=100";

  console.log('Begin request search: ', url)
  request({uri: url}, function(err, response, body) {
    let json = JSON.parse(body)
    let {
      findCompletedItemsResponse: [
        {
          ack: [
            retStatus,
          ],
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

    if(retStatus === 'Success') { // 搜索成功
      console.log(`Total Results is ${totalEntries}`)
      if(aspectHistogramContainer) { // 有属性返回的
        let [
          {
            aspect
          }
        ] = aspectHistogramContainer

        let usSizes = null
        let euroSizes = null
        let brands = null

        let usSizeName = "US Shoe Size (Men's)"
        let euroSizeName = 'Euro Size'
        let brandName = 'Brand'
        aspect.map(item => {
          if(item['@name'] === usSizeName) {
            usSizes = item
          }

          if(item['@name'] === euroSizeName) {
            euroSizes = item
          }

          if(item['@name'] === brandName) {
            brands = item
          }
        })

        if(usSizes) {
          let name = usSizes['@name']
          let valueHistogram = usSizes['valueHistogram']

          let count = valueHistogram.reduce((count, item) => {
            return count + parseInt(item['count'][0], 10)
          }, 0)
          // 使用美码进行二次搜索
          searchWithSizes(baseUrl, valueHistogram, name, 1, query_string)
        }

        if(euroSizes) {
          let euroname = euroSizes['@name']
          let eurovalueHistogram = euroSizes['valueHistogram']

          let eurocount = eurovalueHistogram.reduce((count, item) => {
            return count + parseInt(item['count'][0], 10)
          }, 0)

          // 使用欧码进行二次搜索
          searchWithSizes(baseUrl, eurovalueHistogram, euroname, 1, query_string)
        }
      } else {
      }
    }
  })
}

function searchWithSizes(baseUrl, sizes, name, page_number, query_string) {
  let url = baseUrl + "&paginationInput.pageNumber=" + page_number;
  url += "&paginationInput.entriesPerPage=100";

  sizes.map(item => {
    let sizeValue = item['@valueName']
    if(sizeValue !== 'Not Specified') {
      url = `${url}&aspectFilter(0).aspectName=${name}&aspectFilter(0).aspectValueName=${sizeValue}`
      console.log(`Begin search with ${name}: ${url}`)
      request({uri: url}, function(err, response, body) {
        let json = JSON.parse(body)
        let {
          findCompletedItemsResponse: [
            {
              ack: [
                retStatus,
              ],
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

        console.log(`Search with size ${name} - ${sizeValue}'s total items is ${totalEntries}`)

        if(retStatus === 'Success') {
          let count = searchResult[0]['@count'] // 含有特殊符号，直接取出
          let [
            { item },
          ] = searchResult

          item && item.map(function(record, index){
            let no = entriesPerPage * (page_number - 1) + index + 1
            if(record) {
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
              let logRecord = SpiderLog.build({
                keyword: query_string,
                product_name: title,
                deal_date: startTime,
                deal_price: currentPrice['__value__'],
                size_name: name,
                size: sizeValue,
                size_id: sizeValue,
                spu_id: 0,
                deal_no: itemId,
                aspect: JSON.stringify(sizes),
                content: JSON.stringify(record),
              })

              logRecord.save()
            }
          })

          if(page_number < totalPages) { // 如果还有记录，继续请求
            page_number++
            searchWithSizes(baseUrl, sizes, name, page_number, query_string)
          }
        }
      })
    }
  })
}
function makeRequest(page_number, on_going, min_price, query_string, fromdate, todate, app_name) {
  let url = makeURL(page_number, on_going, min_price, query_string, fromdate, todate, app_name)

  searchAspect(url, query_string)
}

function runSearch(query_string, start, end, min_price) {
  // 开始页码
  let page_number = 1

  // unkwown
  let on_going = false


  let fromdate = (new Date(start)).toISOString()
  let todate = (new Date(end)).toISOString()

  // API token
  let app_name = 'davidkwa-bidtify-PRD-645f30466-13f9307d'

  // 请求数据，写表体
  makeRequest(page_number, on_going, min_price, query_string, fromdate, todate, app_name)
}


let keyword_ebay = 'Jordan 4 pure money'
let start = '01 20,2017'
let end = '06 20,2017'
let min_price = 100
runSearch(keyword_ebay, start, end, min_price)


