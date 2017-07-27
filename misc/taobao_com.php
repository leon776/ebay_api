<?php
/**
 * Created by PhpStorm.
 * User: taylor yue
 * Date: 2017/6/16
 * Time: 20:25
 */



set_time_limit(0);
//error_reporting(0);

$DBNAME = 'demo';
$TBNAME = 'taobao';
$DB_IP = 'localhost';
$CNAME = '淘宝店铺评论信息';
$dsn="mysql:dbname=".$DBNAME.";host=".$DB_IP;
try{
    $pdo=new PDO($dsn,'root','root');
}catch(PDOException $e){
    echo '数据库连接失败'.$e->getMessage();
}
$pdo->query('set names utf8');
$sql_c = "CREATE TABLE IF NOT EXISTS `" . $TBNAME . "` (
`id` int(20) NOT NULL AUTO_INCREMENT COMMENT '自增id',
`search_list_title` text,
`title` text COMMENT '标题',
`auctionPrice` text  ,
`date` text  ,
`sku` text ,
`size` text ,
`type` text ,
`aucNumId` varchar(50),
`create_time` text,
`search_key` text,
`rateId` text,
`page` text,
`shop_id` text,
`shop_user_id` text,
`url_d` text,
`shop_url` text,
PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='" . $CNAME . "';";
//echo $sql_c;die;
$pdo->exec($sql_c);

function getMillisecond() {
    list($t1, $t2) = explode(' ', microtime());
    return (float)sprintf('%.0f',(floatval($t1)+floatval($t2))*1000);
}

function vcurl($url, $post = '', $cookie = '', $cookiejar = '', $referer = '',$stime='20',$localhost='0',$header='')
{
    $tmpInfo = '';
    $cookiepath = getcwd().'./'.$cookiejar;
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $url);
    switch($localhost)
    {
        case "3":
            echo 'ffffffffffffff';
            curl_setopt($curl, CURLOPT_PROXY, 's3.proxy.mayidaili.com:8123');
            break;
    }
    if(!empty($_SERVER['HTTP_USER_AGENT'])){
        $HTTP_USER_AGENT = $_SERVER['HTTP_USER_AGENT'];
    }else{
        $HTTP_USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36";
    }
    curl_setopt($curl, CURLOPT_USERAGENT, $HTTP_USER_AGENT);
    if($referer) {
        curl_setopt($curl, CURLOPT_REFERER, $referer);
    } else {
        curl_setopt($curl, CURLOPT_AUTOREFERER, 1);
    }
    if($post) {
        curl_setopt($curl, CURLOPT_POST, 1);
        curl_setopt($curl, CURLOPT_POSTFIELDS, $post);
    }
    if($cookie) {
        curl_setopt($curl, CURLOPT_COOKIE, $cookie);
    }
    if($cookiejar) {
        curl_setopt($curl, CURLOPT_COOKIEJAR, $cookiepath);
        curl_setopt($curl, CURLOPT_COOKIEFILE, $cookiepath);
        //curl_setopt($curl, CURLOPT_COOKIE, $cookie);
    }
    curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, 0);
    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($curl, CURLOPT_FOLLOWLOCATION, 1);
    curl_setopt($curl, CURLOPT_TIMEOUT, $stime);

    curl_setopt($curl, CURLOPT_HEADER, 0);          //是否打印出http请求header信息
    curl_setopt($curl, CURLOPT_NOBODY, 0);          //是否显示获取的内容

    curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($curl, CURLOPT_HTTPHEADER, array('Proxy-Authorization: '));
    $tmpInfo = curl_exec($curl);
    $errno = curl_errno($curl);
    curl_close($curl);
    /*
    if($errno==28) { self::$timeout_infos='2';}
    elseif($errno==7){self::$timeout_infos='3';}
    elseif($errno==52){self::$timeout_infos='4';}
    */
    return $tmpInfo;
}
function vcurl2($url, $post = '', $cookie = '', $cookiejar = '', $referer = '',$stime='20',$localhost='0',$header='')
{
    date_default_timezone_set("Asia/Shanghai");
    $appKey = '106803123';
    $secret = '8615a8df62d69fc2d9fdd2bec784d749';
    $paramMap = array(
        'app_key'   => $appKey,
        'timestamp' => date('Y-m-d H:i:s')
    );
    ksort($paramMap);
    $codes = $secret;
    $auth = 'MYH-AUTH-MD5 ';
    foreach ($paramMap as $key => $val) {
        $codes .= $key . $val;
        $auth  .= $key . '=' . $val . '&';
    }
    $codes .= $secret;
    $auth .= 'sign=' . strtoupper(md5($codes));

    $cookiepath = getcwd().'./'.$cookiejar;
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $url);
    switch($localhost)
    {
        case "3":
            echo 'using prox...';
            curl_setopt($curl, CURLOPT_PROXY, 's3.proxy.mayidaili.com:8123');
            break;
    }
    if(!empty($_SERVER['HTTP_USER_AGENT'])){
        $HTTP_USER_AGENT = $_SERVER['HTTP_USER_AGENT'];
    }else{
        $HTTP_USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36";
    }
    curl_setopt($curl, CURLOPT_USERAGENT, $HTTP_USER_AGENT);
    if($referer) {
        curl_setopt($curl, CURLOPT_REFERER, $referer);
    } else {
        curl_setopt($curl, CURLOPT_AUTOREFERER, 1);
    }
    if($post) {
        curl_setopt($curl, CURLOPT_POST, 1);
        curl_setopt($curl, CURLOPT_POSTFIELDS, $post);
    }
    if($cookie) {
        curl_setopt($curl, CURLOPT_COOKIE, $cookie);
    }
    if($cookiejar) {
        curl_setopt($curl, CURLOPT_COOKIEJAR, $cookiepath);
        curl_setopt($curl, CURLOPT_COOKIEFILE, $cookiepath);
        //curl_setopt($curl, CURLOPT_COOKIE, $cookie);
    }
    curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, 0);
    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($curl, CURLOPT_FOLLOWLOCATION, 1);
    curl_setopt($curl, CURLOPT_TIMEOUT, $stime);

    curl_setopt($curl, CURLOPT_HEADER, 0);          //是否打印出http请求header信息
    curl_setopt($curl, CURLOPT_NOBODY, 0);          //是否显示获取的内容

    curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($curl, CURLOPT_HTTPHEADER, array("Proxy-Authorization: {$auth}"));
    $tmpInfo = curl_exec($curl);
    $errno = curl_errno($curl);
    curl_close($curl);
    /*
    if($errno==28) { self::$timeout_infos='2';}
    elseif($errno==7){self::$timeout_infos='3';}
    elseif($errno==52){self::$timeout_infos='4';}
    */
    return $tmpInfo;
}


//// 判断是淘宝还是天猫
//if(strpos($url,'tmall') !== false) {
//    $is_tmall = 1;
//    preg_match("|\?id=([\d]{1,})|",$url,$out);
//}else{
//    preg_match("|id=([\d]{1,})|",$url,$out);
//}
$search_key_arr = array( '裤子', 'NIKE Magista OPUS FG', '阿甘鞋');

$cookiefile = 'cookie.txt';

//echo urldecode($url);die;
//echo $tmp;die;
//  搜索
//$url = 'https://s.taobao.com/search?q=%E9%98%BF%E7%94%98%E9%9E%8B&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20170616&ie=utf8';
//$list_html = requests::get($url);
//
//  jsonp  资源 搜索结果列表资源

foreach($search_key_arr AS $search_key) {
    $tmp_url = "https://s.taobao.com/search?q=".urlencode($search_key)."&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_".date('Ymd')."&ie=utf8";
    $tmp = vcurl($tmp_url, '', '', $cookiefile);

//    $tmp_url_2 = "https://log.mmstat.com/v.gif?logtype=1&title=jordan%2011%20%u5927%u9B54%u738B_%u6DD8%u5B9D%u641C%u7D22&pre=https%3A%2F%2Fs.taobao.com%2Fsearch%3Fq%3Djordan%2B11%2B%25E5%25A4%25A7%25E9%25AD%2594%25E7%258E%258B%26imgfile%3D%26js%3D1%26stats_click%3Dsearch_radio_all%253A1%26initiative_id%3Dstaobaoz_20170618%26ie%3Dutf8&cache=e82e7c8&scr=1366x768&cna=GDC4EVaFTjwCAbRmOmS8IBFt&spm-cnt=a230r.1.0.0.kim7dE&category=&uidaplus=&aplus&yunid=&f5bde75e1ae31&trid=0a67b87714977781491602724e8ab5&asid=AQAAAADlR0ZZ4nm9PgAAAADmOVqddsKWaA==&thw=cn&p=1&o=win8&b=chrome58&s=1366x768&w=webkit&mx=360ee&ism=pc&lver=7.4.4&jsver=aplus_std&isAplusInternal=Y&tag=1&stag=-1";
//    echo urldecode(urldecode($tmp_url_2));die;
//    vcurl($tmp_url_2, '', '', $cookiefile);

//    print_r($search_key);die;
    //  jsonp  资源 搜索结果列表资源
    $list_url = "https://s.taobao.com/api?_ksTS=" . getMillisecond() . "_".rand(1,1000)."&callback=jsonp" . rand(1, 1000) . "&ajax=true&m=customized&stats_click=search_radio_all:1&q=" . urlencode($search_key) . "&s=36&imgfile=&initiative_id=staobaoz_".date('Ymd')."&bcoffset=0&js=1&ie=utf8&rn=f33150613c6579ea523be3399a660995";

    $list_html = vcurl2($list_url, '','', $cookiefile, '', '', 3);          // jsonp 搜索结果列表资源
//    $list_html = vcurl($list_url, '','', $cookiefile);          // jsonp 搜索结果列表资源

//    echo $list_html;die;
    usleep(rand(10,100));
    preg_match_all('/\((.*)\);$/siU', $list_html, $ll_vv);
    $response = json_decode($ll_vv[1][0], true);//die;
//    print_r($response);die;
    //搜索结果列表页  一页有48 个商品
    for($search_list_ll =0; $search_list_ll < 48; $search_list_ll++ )
    {
        //"https://rate.taobao.com/user-rate-UvCkuvmg4MCvbvgTT.htm?spm=a1z10.1-c.0.0.5d5XbG"    // new balance
        //print_r($result['API.CustomizedApi']['itemlist']['auctions']['3']);die;
        $data['encryptedUserId'] = "UvCkuvmg4MCvbvgTT";
        $data['encryptedUserId'] = $response['API.CustomizedApi']['itemlist']['auctions'][$search_list_ll]['shopcard']['encryptedUserId'];
//         店铺链接 //store.taobao.com/shop/view_shop.htm?user_number_id=353571709
        $data['shop_url'] = $result['API.CustomizedApi']['itemlist']['auctions']['0']['shopLink'];
        $data['shop_url'] = 'https://rate.taobao.com/user-rate-' . $data['encryptedUserId'] . '.htm';
//         搜索关键字搜索出来的标题
        $data['title'] = $response['API.CustomizedApi']['itemlist']['auctions'][$search_list_ll]['title'];
        $data['user_id'] = $response['API.CustomizedApi']['itemlist']['auctions'][$search_list_ll]['user_id'];
//        print_r($data);die;
        /*[encryptedUserId] => UvCvLOFvYOFIT
[shop_url] => https://rate.taobao.com/user-rate-UvCvLOFvYOFIT.htm
[title] => 杭州鞋帮Air <span class=H>Jordan</span> <span class=H>11</span> &ldqu
-10&rdquo; AJ<span class=H>11</span><span class=H>大</span><span class=H>魔王</
>378038-378037-002*/
        $page = 50;
        ////列表页翻页
        for ($list_pp = 1; $list_pp <= $page; $list_pp++) {
//            print_r($data);die;
            // 店铺列表页评论   翻页容易触发登陆验证
            //    $url_d = 'https://rate.taobao.com/member_rate.htm?_ksTS=1497630012623_156&callback=shop_rate_list&content=1&result=&from=rate&user_id=UvFcbOmkuvGQGOQTT&identity=2&rater=0&direction=0&page='.$list_pp;

            if($list_pp==1){
                $url_d = 'https://rate.taobao.com/member_rate.htm?_ksTS=' . getMillisecond() . '_' . rand(1, 1000) . '&callback=shop_rate_list&content=1&result=&from=rate&user_id=' . $data['encryptedUserId'] . '&identity=1&rater=0&direction=0';
                $referer = $url_d;
            }else{
                $url_d = 'https://rate.taobao.com/member_rate.htm?_ksTS=' . getMillisecond() . '_' . rand(1, 1000) . '&callback=shop_rate_list&content=1&result=&from=rate&user_id=' . $data['encryptedUserId'] . '&identity=1&rater=0&direction=0&page='.$list_pp;
                $referer = $url_d;
            }
//            $html = vcurl($url_d, '', '', $cookiefile, $referer);
            $html = vcurl2($url_d, '', '', $cookiefile, $referer, '', 3);
            sleep(rand(5,15));
//            echo $html;die;
            preg_match_all('/auction(.*)buyAmount/siU', $html, $list_vv);
            $list_div = $list_vv[1];                // 列表页  评论数量
            for ($ii = 0; $ii < count($list_div); $ii++) {
//                print_r($data);die;
                $list_div[$ii] = iconv("GB2312", "UTF-8", $list_div[$ii]);
                preg_match_all('/auctionPrice":(.*)\,/siU', $list_div[$ii], $a_vv);
                $result['auctionPrice'] = $a_vv[1][0];     //价格
                preg_match_all('/title":"(.*)"\,/siU', $list_div[$ii], $a_vv);
                $result['title'] = $a_vv[1][0];     //商品名

                preg_match_all('/date":"(.*)"\,/siU', $list_div[$ii], $a_vv);
                $result['date'] = $a_vv[1][0];     //时间
                // "sku": "颜色分类:白色（偏瘦，建议拍大一码）;尺码:43"
                preg_match_all('/sku":"(.*)"/siU', $list_div[$ii], $a_vv);
                $result['sku'] = addslashes($a_vv[1][0]);     //颜色，尺码

                preg_match_all('/尺码:(.*)$/siU', $result['sku'], $a_vv);
                $result['size'] = $a_vv[1][0];              // 尺码

                preg_match_all('/颜色分类:(.*)\&nbsp/siU', $result['sku'], $a_vv);
                $result['type'] = addslashes($a_vv[1][0]);              // 颜色分类

                preg_match_all('/aucNumId":"(.*)"\,/siU', $list_div[$ii], $a_vv);
                $result['aucNumId'] = $a_vv[1][0];     //aucNumId
                preg_match_all('/rateId":"(.*)"\,/siU', $list_div[$ii], $a_vv);
                $result['rateId'] = $a_vv[1][0];     //rate id


                $result['search_key'] = $search_key;                        // 输入的搜索关键字
                $result['create_time'] = date('Y-m-d H:i:s');               // 数据抓取时间
                $result['page'] = $search_list_ll.'--'.$list_pp.'--'.$ii;        // 第几页的第几条
                $result['shop_id'] = $data['encryptedUserId'];                  // 店铺id
                $result['shop_user_id'] = $data['user_id'];                     // 店铺
                $result['url_d'] = $url_d;                                   // 店铺商品评论详情
                $result['shop_url'] = $data['shop_url'];
                $result['search_list_title'] = trim(strip_tags($data['title']));

//                print_r($result);die;
                // 判断 搜索列表页 中的关键字  === 店铺商品评论
//                if($result['title'] == $data['title']){
                $kkey = implode('`,`', array_keys($result));
                $vvalue = implode('","', array_values($result));

                $sql_i = sprintf('INSERT INTO %s (`%s`) VALUES ("%s")', $TBNAME, $kkey, $vvalue);
                print_r($sql_i);
                $pdo->query($sql_i);
                file_put_contents('errolog.txt', $pdo->errorInfo(), FILE_APPEND);

//                }
//                        print_r($result);die;

                //        die;
            }
        }
    }
}
//   "auctionPrice": 175,  价格
//    "title": "夏季男鞋潮鞋2017新款小白鞋休闲白色平板鞋夏天白鞋韩版潮流百搭", 商品名
//    "date": "2017.06.17",   时间
//     "sku": "颜色分类:黑色;尺码:41"
//    "aucNumId": "543646479239",
//echo $html;die;