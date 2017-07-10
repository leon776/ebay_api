require('es6-promise').polyfill()
require('isomorphic-fetch')
let fs = require('fs')
let request = require('request')

let outputfile = './output.csv'
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
    url += "&paginationInput.pageNumber=" + page_number;
    url += "&paginationInput.entriesPerPage=100";
    url += urlfilter;

    return url;
}

function writeHead(file) {
  //let headString = `no,autoPay,conditionDisplayName,conditionId`
  //headString += `,country,galleryURL,globalId,isMultiVariationListing,itemId,bestOfferEnabled,buyItNowAvailable,endTime,gift,listingType,startTime`

  //headString += `,loc,paymentMethod,categoryId,categoryName,returnsAccepted`

  //headString += `,convertedCurrentPrice['@currencyId'],convertedCurrentPrice['__value__']`
  //headString += `,currentPrice['@currencyId'],currentPrice['__value__']`
  //headString += `,sellingState,expeditedShipping,handlingTime,oneDayShippingAvailable,shipToLocations`

  //rowString += `,shippingServiceCost[0]['@currencyId'],shippingServiceCost[0]['__value__']`
  //headString += `,shippingType,title,topRatedListing,viewItemURL`

  let headString = `no,title,itemId,startTime,endTime,currentPrice['@currencyId'],currentPrice['__value__'],sellingState,listingType`
  fs.appendFileSync(file, headString + "\n")
}

function writeRecord(file, record, no) {
  let {
    autoPay: [ autoPay ],
    condition: [
      {
        conditionDisplayName: [ conditionDisplayName ],
        conditionId: [ conditionId ],
      }
    ],
    country: [ country ],
    galleryURL: [ galleryURL ],
    globalId: [ globalId ],
    isMultiVariationListing: [ isMultiVariationListing ],
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
    location: [ loc ],
    paymentMethod: [ paymentMethod ],
    primaryCategory: [
      {
        categoryId: [ categoryId ],
        categoryName: [ categoryName ],
      }
    ],
    returnsAccepted: [ returnsAccepted ],
    sellingStatus: [{
      convertedCurrentPrice: [ convertedCurrentPrice ],  // 这里价格是对象，里边有两个值 @currencyId和__value__
      currentPrice: [ currentPrice ], // 这里价格是对象，有两个值 @currencyId和__value__
      sellingState: [ sellingState ],
    }],
    shippingInfo: [{
      expeditedShipping: [ expeditedShipping ],
      handlingTime: [ handlingTime ],
      oneDayShippingAvailable: [ oneDayShippingAvailable ],
      shipToLocations: [ shipToLocations ],
      shippingServiceCost,
//              shippingServiceCost: [ shippingServiceCost ],
      shippingType: [ shippingType ],
    }],
    title: [ title ],
    topRatedListing: [ topRatedListing ],
    viewItemURL: [ viewItemURL ],
  } = record

  /*let rowString = `${no},${autoPay},${conditionDisplayName},${conditionId}`
  rowString += `,${country},${galleryURL},${globalId},${isMultiVariationListing},${itemId},${bestOfferEnabled},${buyItNowAvailable},${endTime},${gift},${listingType},${startTime}`

  rowString += `,${loc},${paymentMethod},${categoryId},${categoryName},${returnsAccepted}`

  rowString += `,${convertedCurrentPrice['@currencyId']},${convertedCurrentPrice['__value__']}`
  rowString += `,${currentPrice['@currencyId']},${currentPrice['__value__']}`
  rowString += `,${sellingState},${expeditedShipping},${handlingTime},${oneDayShippingAvailable},${shipToLocations}`

  //rowString += `,${shippingServiceCost[0]['@currencyId']},${shippingServiceCost[0]['__value__']}`
  rowString += `,${shippingType},${title},${topRatedListing},${viewItemURL}`*/

  title = title.replace(/,/, "，")
  let rowString = `${no},${title},${itemId},${startTime},${endTime},${currentPrice['@currencyId']},${currentPrice['__value__']},${sellingState},${listingType}`

  fs.appendFileSync(file, rowString + "\n")
}
let start = '05 20,2017'
let end = '06 20,2017'

let page_number = 1
let on_going = false
let min_price = 160
let query_string = 'Jordan 4 pure money'
let fromdate = (new Date(start)).toISOString()
let todate = (new Date(end)).toISOString()
let app_name = 'davidkwa-bidtify-PRD-645f30466-13f9307d'

// 先删除原来文件
fs.unlinkSync(outputfile)
writeHead(outputfile)
function makeRequest(page_number, on_going, min_price, query_string, fromdate, todate, app_name) {
  let url = makeURL(page_number, on_going, min_price, query_string, fromdate, todate, app_name)
  console.log('Begin request :', url)
  request({uri:url}, function(err, response, body) {
    let json = JSON.parse(body)
    // 首先从响应中拿出各个属性
    let {
      findCompletedItemsResponse: [
        {
          ack,
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

    let [resStatus] = ack

    if(resStatus === 'Success') { // 请求成功
      let count = searchResult[0]['@count'] // 含有特殊符号，直接取出
      let [
        { item },
      ] = searchResult

      item.map(function(record, index){
        let no = entriesPerPage * (page_number - 1) + index + 1
        console.log('write row ', no)
        writeRecord(outputfile, record, no)
      })

      if(page_number <= totalPages) { // 如果还有记录，继续请求
        page_number++
        makeRequest(page_number, on_going, min_price, query_string, fromdate, todate, app_name)
      }
    } else if (resStatus === 'Failure') { // 请求失败
    }
  })
}
function makeFetch(page_number, on_going, min_price, query_string, fromdate, todate, app_name) {
  let url = makeURL(page_number, on_going, min_price, query_string, fromdate, todate, app_name)
  console.log(url)
  fetch(url).then(
    response => {
      return response.json()
    }
  ).then(
    json => {
      // 首先从响应中拿出各个属性
      let {
        findCompletedItemsResponse: [
          {
            ack,
            paginationOutput,
            searchResult,
            timestamp,
            version,
          }
        ]
      } = json

      let [resStatus] = ack

      if(resStatus === 'Success') { // 请求成功
        let count = searchResult[0]['@count'] // 含有特殊符号，直接取出
        let [
          { item },
        ] = searchResult

        item.map(function(record, index){
          let no = 100 * (page_number - 1) + index + 1
          writeRecord(outputfile, record, no)
        })

      } else if (resStatus === 'Failure') { // 请求失败
      }
    }
  )
}

makeRequest(page_number, on_going, min_price, query_string, fromdate, todate, app_name)

/*while(page_number <= 100) {
  makeRequest(page_number, on_going, min_price, query_string, fromdate, todate, app_name)
  page_number++
}*/

