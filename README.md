## Ebay API

### findCompletedItems
这个调用搜索那些已经完成或不在用于销售的项目，使用categoryId按类搜索，使用keywords按关键词搜索, 或者可以两者结合。关键词查询标题和副标题，不搜索描述。

#### 使用详述
findCompletedItems响应包含匹配你搜索情况项目的详情。默认情况下，eBay在调用响应中返回特定的数据集合。控制findCompletedItems结果集可以使用下面的方法:

* 在特定eBay网站中搜索项目: 使用GLOBAL-ID参数(或者X-EBAY-SOA-GLOBAL-ID HTTP报头)指定用于搜索的eBay网站。
* 使用项目过滤器进行过滤: 可以通过itemFilter来控制结果，这里可以使用各种属性，包括项目condition, 投标数(number of bids), 价格范围，列表类型等等。
* 使用aspect过滤器精炼结果: aspectFilter可以使用标准的项目特性，例如样式或颜色，来精炼搜索结果。
* 在响应中包含额外的数据: 可以指定一个或多个outputSelector字段来检索比默认响应数据更多的数据。例如，可以检索每个销售者的信息, 或者aspect直方图(aspect histogram)。
* 结果排序: 使用sortOrder来指定返回项目的排序方式，例如价格排序或结束时间排序等等。

> 注意: findCompletedItems的默认sortOrder是最近的结束日期(End Date: recent first). 和其他查找API调用不同，对于findCompletedItems， BestMatch不被默认排序支持的。

* 结果分页: 使用paginationInput来将匹配搜索场景的项目分到不同的子集、页面中去。


#### itemFilter介绍
该选项是可选项，而且可重复。
详细介绍： http://developer.ebay.com/devzone/finding/callref/types/ItemFilterType.html

### 搜索API简介

* API地址: http://svcs.ebay.com/services/search/FindingService/v1
* 操作名称: OPERATION-NAME, 例如findCompletedItems, findItemsByCategory。
* 服务版本号: SERVICE-VERSION, 例如1.0.0
* 应用token(安全APPNAME): SERVICE-VERSION，申请后提供的一个token
* 搜索项目所在的特定Site: GLOBAL-ID, 例如EBAY-US
* 响应数据格式: RESPONSE-DATA-FORMAT, 例如JSON, XML等
* 关键词: keywords, 使用搜索关键词进行搜索时使用。
* REST-PAYLOAD:
* 分页输入参数对象: paginationInput, 设置请求分页的当前请求页(pageNumber)、每页数目(entriesPerPage)
* 分类ID: 使用分类进行搜索的时候使用，categoryId, 值为分类的id值。
* 过滤选项: itemFilter，可以提供多个不同的过滤选项，每个选项分别提供name和value来进行搜索过滤。 例如搜索仅免运费的项， 使用itemFilter(1).name=FreeShippingOnly&itemFilter(1).value=true; 再例如，仅搜索销售的项，使用itemFilter(2).name=SoldItemsOnly&itemFilter(2).value=true; 例如结束时间段过滤，分别使用itemFilter(n).name为EndTimeFrom和EndTimeTo， 而对应的值使用ISOString格式, javascript Date使用toISOString()获取值。




### 根据关键词搜索

http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findCompletedItems&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=davidkwa-bidtify-PRD-645f30466-13f9307d&GLOBAL-ID=EBAY-US&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords=Jordan%204%20pure%20money&paginationInput.pageNumber=1&paginationInput.entriesPerPage=100&itemFilter(0).name=MinPrice&itemFilter(0).value=160&itemFilter(0).paramName=Currency&itemFilter(0).paramValue=USD&itemFilter(1).name=FreeShippingOnly&itemFilter(1).value=false&itemFilter(2).name=SoldItemsOnly&itemFilter(2).value=true&itemFilter(3).name=EndTimeFrom&itemFilter(3).value=2017-05-19T16:00:00.000Z&itemFilter(4).name=EndTimeTo&itemFilter(4).value=2017-06-19T16:00:00.


### 根据分类ID搜索
http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByCategory&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=davidkwa-bidtify-PRD-645f30466-13f9307d&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&paginationInput.entriesPerPage=2&categoryId=307&outputSelector=AspectHistogram
