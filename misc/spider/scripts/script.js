// Author: Jeanno Cheung
// Date: 22/06/2017

var interval = null;
var intervalSec = 300000;

var SHOP_LIST = [["烽火体育SNEAKER之家", "beaconfire", "UvG8bvF8SMCcW"],
	["四川正品小店", "yysport", "UMFQLMmg0vGcT"],
	["Class-space", "cspace", "UOFIuMGkYvCx0"],
	["库客运动", "cooke", "UMmcbvmQWOFvT"],
	["雷恩体育solestage", "lane", "UvCx0vGcLvCxT"],
	["蓝带体育", "blueribbon", "UvCcSOmNLvFN4"],
	["gogo球鞋", "gogo", "UvFcbMGg4MFHSvNTT"],
	["厚道体育运动正品店", "holdsports", "UvCH0MCQGvGx4"],
	["球鞋家sneakerfamily", "sneakerfamily", "UMGkYMmxYMCNG"],
	["燎原装备Diffusion", "diffusion", "UvFguMFIbMFI0MQTT"],
	["天津鞋门usa", "tjxm", "UvFNSMFH0vFHy"],
	["NL23hood", "nl23hood", "UvCQ0vCvbvm8bOQTT"],
	["小鸿体育", "hung", "UvFcuMmNuvCN0"],
	["兄弟体育", "xiongdi", "UvFkGMFkYOmILOQTT"],
	["抓地力潮流", "traction", "UMFc0MCv0vmNS"],
	["ok球鞋", "oksneakers", "UMCxSvmxyOFHG"],
	["姚家军", "sneakerlovers", "UvCQGOF8GMC8bvgTT"],
	["巫师鞋柜", "wizard", "UOm84MFxYMFvT"],
	["乔飞天下", "jordan365", "UMC8WMCNYvCxb"],
	["牛哄哄运动店", "nhhyyd", "UvFIyvFc4vmIu"],
	["sneaker便利店", "sneakerconven", "UvCxYvGxuMFxGONTT"],
	["快客体育freshshoes", "freshshoes", "UMGgbOmIYMCkb"],
	["穿行体育cxclub", "cx", "UMF80OmHYMmxT"],
	["虎扑伙伴", "hupuhuoban", "UMCcbOmkyvCcS"],
	["嘎嘎体育馆", "hlp00345", "UMGNGvmHYMmxb"],
	["牛牛体育", "niuniu", "UvFNbvF8GvGv0MgTT"],
	["凤凰体育", "phoenix", "UMCx4vmHWMF8L"],
	["Chips运动", "chips", "UvFHGvCc0MGgbOQTT"],
	["kikipipi", "kikipipi", "UOFguvmvGMCvT"]];


var MEMBER_RATE_URL = "https://rate.taobao.com/member_rate.htm?user_id=";

function _fetch(taobaoId, page) {
	var url = MEMBER_RATE_URL + taobaoId + "&page=" + page;
	console.log("Fetching: " + url);
	document.getElementById('downloadIframe').src = url;
}

function loopFetch(ids, maxPage) {
	var storeI = 0;
	var page = 1;
	var myFetch = function() {
		_fetch(ids[storeI], page);
		page++;
		if (page > maxPage) {
			page = 1;
			storeI = (storeI + 1) % ids.length;
		}
	};
	myFetch();
	interval = setInterval(myFetch, intervalSec);
}


function fetch() {
	var page = parseInt($("#nextPageInput").val());
	if (page > 42) {
		return;
	}
	var taobaoId = $("#shopSelect").val();
	_fetch(taobaoId, page);
	page++;
	$("#nextPageInput").val(page)
}

function start() {
	$('#fetchBtn').addClass("disabled");
	$('#startBtn').addClass("disabled");
	$('#stopBtn').removeClass("disabled");
	$('#shopSelect').attr("disabled", "");
	$('#nextPageInput').attr("disabled", "");
	fetch();
	interval = setInterval(function() {
		var page = parseInt($("#nextPageInput").val());
		if (page > 42) {
			alert("Cannot fetch over 42 pages. Aborting...")
			stop();
		}
		fetch();
	}, intervalSec);
}

function stop() {
	$('#fetchBtn').removeClass("disabled");
	$('#startBtn').removeClass("disabled");
	$('#stopBtn').addClass("disabled");
	$('#shopSelect').removeAttr("disabled");
	$('#nextPageInput').removeAttr("disabled");
	clearInterval(interval);
}

// TODO: setup Select list
function buildShopSelect() {
	var shopSelect = $("#shopSelect");
	for (var i = 0; i < SHOP_LIST.length; i++) {
		var shop = SHOP_LIST[i];
		var shopOption = $('<option value="' + shop[2] + '">' + shop[0] + '</option>');
		shopSelect.append(shopOption);
	}
}

// For Jeanno only
function myLoop() {
	loopFetch(["UvG8bvF8SMCcW", "UMFQLMmg0vGcT", "UOFIuMGkYvCx0"], 40);
}

buildShopSelect();
