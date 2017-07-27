/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50714
 Source Host           : localhost
 Source Database       : shoes

 Target Server Type    : MySQL
 Target Server Version : 50714
 File Encoding         : utf-8

 Date: 06/05/2017 23:50:35 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `banner`
-- ----------------------------
DROP TABLE IF EXISTS `banner`;
CREATE TABLE `banner` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(128) DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL COMMENT '0停用，1启用',
  `deleted` tinyint(1) DEFAULT NULL COMMENT '0正常1删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `categories`
-- ----------------------------
DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `pid` int(11) NOT NULL COMMENT '父类ID',
  `name` int(11) NOT NULL COMMENT '分类名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='分类表';

-- ----------------------------
--  Table structure for `deal_records_0`
-- ----------------------------
DROP TABLE IF EXISTS `deal_records_0`;
CREATE TABLE `deal_records_0` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `spu_id` int(11) NOT NULL COMMENT '产品ID',
  `size_id` int(11) NOT NULL COMMENT '尺码id',
  `price` double NOT NULL COMMENT '产品售价',
  `deal_date` varchar(32) NOT NULL COMMENT '成交时间，时间戳',
  `create_time` varchar(32) NOT NULL COMMENT '创建时间',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0正常，1停用',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='成交记录表';

-- ----------------------------
--  Table structure for `deal_records_1`
-- ----------------------------
DROP TABLE IF EXISTS `deal_records_1`;
CREATE TABLE `deal_records_1` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `spu_id` int(11) NOT NULL COMMENT '产品ID',
  `size_id` int(11) NOT NULL COMMENT '尺码id',
  `price` double NOT NULL COMMENT '产品售价',
  `deal_date` varchar(32) NOT NULL COMMENT '成交时间，时间戳',
  `create_time` varchar(32) NOT NULL COMMENT '创建时间',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0正常，1停用',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='成交记录表';

-- ----------------------------
--  Table structure for `deal_records_2`
-- ----------------------------
DROP TABLE IF EXISTS `deal_records_2`;
CREATE TABLE `deal_records_2` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `spu_id` int(11) NOT NULL COMMENT '产品ID',
  `size_id` int(11) NOT NULL COMMENT '尺码id',
  `price` double NOT NULL COMMENT '产品售价',
  `deal_date` varchar(32) NOT NULL COMMENT '成交时间，时间戳',
  `create_time` varchar(32) NOT NULL COMMENT '创建时间',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0正常，1停用',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='成交记录表';

-- ----------------------------
--  Table structure for `deal_records_3`
-- ----------------------------
DROP TABLE IF EXISTS `deal_records_3`;
CREATE TABLE `deal_records_3` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `spu_id` int(11) NOT NULL COMMENT '产品ID',
  `size_id` int(11) NOT NULL COMMENT '尺码id',
  `price` double NOT NULL COMMENT '产品售价',
  `deal_date` varchar(32) NOT NULL COMMENT '成交时间，时间戳',
  `create_time` varchar(32) NOT NULL COMMENT '创建时间',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0正常，1停用',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='成交记录表';

-- ----------------------------
--  Table structure for `deal_records_4`
-- ----------------------------
DROP TABLE IF EXISTS `deal_records_4`;
CREATE TABLE `deal_records_4` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `spu_id` int(11) NOT NULL COMMENT '产品ID',
  `size_id` int(11) NOT NULL COMMENT '尺码id',
  `price` double NOT NULL COMMENT '产品售价',
  `deal_date` varchar(32) NOT NULL COMMENT '成交时间，时间戳',
  `create_time` varchar(32) NOT NULL COMMENT '创建时间',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0正常，1停用',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='成交记录表';

-- ----------------------------
--  Table structure for `deal_records_5`
-- ----------------------------
DROP TABLE IF EXISTS `deal_records_5`;
CREATE TABLE `deal_records_5` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `spu_id` int(11) NOT NULL COMMENT '产品ID',
  `size_id` int(11) NOT NULL COMMENT '尺码id',
  `price` double NOT NULL COMMENT '产品售价',
  `deal_date` varchar(32) NOT NULL COMMENT '成交时间，时间戳',
  `create_time` varchar(32) NOT NULL COMMENT '创建时间',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0正常，1停用',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='成交记录表';

-- ----------------------------
--  Table structure for `deal_records_6`
-- ----------------------------
DROP TABLE IF EXISTS `deal_records_6`;
CREATE TABLE `deal_records_6` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `spu_id` int(11) NOT NULL COMMENT '产品ID',
  `size_id` int(11) NOT NULL COMMENT '尺码id',
  `price` double NOT NULL COMMENT '产品售价',
  `deal_date` varchar(32) NOT NULL COMMENT '成交时间，时间戳',
  `create_time` varchar(32) NOT NULL COMMENT '创建时间',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0正常，1停用',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='成交记录表';

-- ----------------------------
--  Table structure for `deal_records_7`
-- ----------------------------
DROP TABLE IF EXISTS `deal_records_7`;
CREATE TABLE `deal_records_7` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `spu_id` int(11) NOT NULL COMMENT '产品ID',
  `size_id` int(11) NOT NULL COMMENT '尺码id',
  `price` double NOT NULL COMMENT '产品售价',
  `deal_date` varchar(32) NOT NULL COMMENT '成交时间，时间戳',
  `create_time` varchar(32) NOT NULL COMMENT '创建时间',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0正常，1停用',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='成交记录表';

-- ----------------------------
--  Table structure for `deal_records_8`
-- ----------------------------
DROP TABLE IF EXISTS `deal_records_8`;
CREATE TABLE `deal_records_8` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `spu_id` int(11) NOT NULL COMMENT '产品ID',
  `size_id` int(11) NOT NULL COMMENT '尺码id',
  `price` double NOT NULL COMMENT '产品售价',
  `deal_date` varchar(32) NOT NULL COMMENT '成交时间，时间戳',
  `create_time` varchar(32) NOT NULL COMMENT '创建时间',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0正常，1停用',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='成交记录表';

-- ----------------------------
--  Table structure for `deal_records_9`
-- ----------------------------
DROP TABLE IF EXISTS `deal_records_9`;
CREATE TABLE `deal_records_9` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `spu_id` int(11) NOT NULL COMMENT '产品ID',
  `size_id` int(11) NOT NULL COMMENT '尺码id',
  `price` double NOT NULL COMMENT '产品售价',
  `deal_date` varchar(32) NOT NULL COMMENT '成交时间，时间戳',
  `create_time` varchar(32) NOT NULL COMMENT '创建时间',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0正常，1停用',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='成交记录表';

-- ----------------------------
--  Table structure for `faq`
-- ----------------------------
DROP TABLE IF EXISTS `faq`;
CREATE TABLE `faq` (
  `id` int(11) NOT NULL,
  `question` text NOT NULL COMMENT '问题',
  `answer` text NOT NULL COMMENT '答案',
  `sort` int(11) DEFAULT NULL COMMENT '排序，越大越靠前',
  `deleted` tinyint(1) DEFAULT NULL COMMENT '0正常，1删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `key_words`
-- ----------------------------
DROP TABLE IF EXISTS `key_words`;
CREATE TABLE `key_words` (
  `id` int(11) NOT NULL COMMENT '关键词id',
  `name` varchar(100) NOT NULL COMMENT '用户搜索关键词',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0正常，1删除',
  `create_time` varchar(32) NOT NULL COMMENT '提交时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `labels`
-- ----------------------------
DROP TABLE IF EXISTS `labels`;
CREATE TABLE `labels` (
  `id` int(11) NOT NULL,
  `name` varchar(128) NOT NULL COMMENT '标签名',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0正常，1删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `rankings`
-- ----------------------------
DROP TABLE IF EXISTS `rankings`;
CREATE TABLE `rankings` (
  `id` int(11) NOT NULL COMMENT '榜单id',
  `type` tinyint(1) NOT NULL COMMENT 'type: 0-销售榜，1-增福榜，2-跌幅榜',
  `spuid` int(11) NOT NULL COMMENT '产品id',
  `num` double NOT NULL COMMENT '涨跌幅/销售量',
  `position` int(11) NOT NULL COMMENT '排名',
  `date` varchar(32) NOT NULL COMMENT '日期，精确到日',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `researches`
-- ----------------------------
DROP TABLE IF EXISTS `researches`;
CREATE TABLE `researches` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `title` varchar(100) NOT NULL COMMENT '报告标题',
  `cover` varchar(200) NOT NULL COMMENT '图片',
  `content` text NOT NULL COMMENT '报告内容',
  `views` int(11) NOT NULL COMMENT '查看次数',
  `ctime` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `utime` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  `deleted` tinyint(3) NOT NULL DEFAULT '0' COMMENT '0正常，1删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='研究报告';

-- ----------------------------
--  Table structure for `sizes`
-- ----------------------------
DROP TABLE IF EXISTS `sizes`;
CREATE TABLE `sizes` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `eu_size` int(11) NOT NULL COMMENT '尺寸名称',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0正常，1删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='产品尺寸表';

-- ----------------------------
--  Table structure for `spu_label`
-- ----------------------------
DROP TABLE IF EXISTS `spu_label`;
CREATE TABLE `spu_label` (
  `id` int(11) NOT NULL,
  `label_id` int(11) NOT NULL COMMENT '标签id',
  `spu_id` int(11) NOT NULL COMMENT '产品id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `spus`
-- ----------------------------
DROP TABLE IF EXISTS `spus`;
CREATE TABLE `spus` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'spuid',
  `product_no` varchar(20) NOT NULL DEFAULT '0' COMMENT '货号',
  `en_name` varchar(200) NOT NULL COMMENT '产品名称',
  `zh_name` varchar(200) NOT NULL,
  `code` varchar(16) DEFAULT NULL COMMENT '交易代码',
  `cover` varchar(200) NOT NULL COMMENT '产品封面',
  `price` double NOT NULL DEFAULT '0' COMMENT '产品价格',
  `cate_id` int(11) NOT NULL COMMENT '分类ID',
  `ttm` varchar(20) NOT NULL COMMENT '上市时间time to market',
  `ctime` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `utime` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  `deleted` tinyint(3) NOT NULL DEFAULT '0' COMMENT '0正常，1删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='产品表';

-- ----------------------------
--  Table structure for `tmp_data_0`
-- ----------------------------
DROP TABLE IF EXISTS `tmp_data_0`;
CREATE TABLE `tmp_data_0` (
  `id` int(11) NOT NULL,
  `product_name` varchar(64) NOT NULL COMMENT '产品名称',
  `deal_date` varchar(32) NOT NULL COMMENT '成交时间',
  `deal_price` decimal(10,0) NOT NULL COMMENT '成交价',
  `size_id` double NOT NULL COMMENT '尺码',
  `spu_id` int(11) NOT NULL COMMENT '产品id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `tmp_data_1`
-- ----------------------------
DROP TABLE IF EXISTS `tmp_data_1`;
CREATE TABLE `tmp_data_1` (
  `id` int(11) NOT NULL,
  `product_name` varchar(64) NOT NULL COMMENT '产品名称',
  `deal_date` varchar(32) NOT NULL COMMENT '成交时间',
  `deal_price` decimal(10,0) NOT NULL COMMENT '成交价',
  `size_id` double NOT NULL COMMENT '尺码',
  `spu_id` int(11) NOT NULL COMMENT '产品id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `tmp_data_2`
-- ----------------------------
DROP TABLE IF EXISTS `tmp_data_2`;
CREATE TABLE `tmp_data_2` (
  `id` int(11) NOT NULL,
  `product_name` varchar(64) NOT NULL COMMENT '产品名称',
  `deal_date` varchar(32) NOT NULL COMMENT '成交时间',
  `deal_price` decimal(10,0) NOT NULL COMMENT '成交价',
  `size_id` double NOT NULL COMMENT '尺码',
  `spu_id` int(11) NOT NULL COMMENT '产品id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `tmp_data_3`
-- ----------------------------
DROP TABLE IF EXISTS `tmp_data_3`;
CREATE TABLE `tmp_data_3` (
  `id` int(11) NOT NULL,
  `product_name` varchar(64) NOT NULL COMMENT '产品名称',
  `deal_date` varchar(32) NOT NULL COMMENT '成交时间',
  `deal_price` decimal(10,0) NOT NULL COMMENT '成交价',
  `size_id` double NOT NULL COMMENT '尺码',
  `spu_id` int(11) NOT NULL COMMENT '产品id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `tmp_data_4`
-- ----------------------------
DROP TABLE IF EXISTS `tmp_data_4`;
CREATE TABLE `tmp_data_4` (
  `id` int(11) NOT NULL,
  `product_name` varchar(64) NOT NULL COMMENT '产品名称',
  `deal_date` varchar(32) NOT NULL COMMENT '成交时间',
  `deal_price` decimal(10,0) NOT NULL COMMENT '成交价',
  `size_id` double NOT NULL COMMENT '尺码',
  `spu_id` int(11) NOT NULL COMMENT '产品id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `tmp_data_5`
-- ----------------------------
DROP TABLE IF EXISTS `tmp_data_5`;
CREATE TABLE `tmp_data_5` (
  `id` int(11) NOT NULL,
  `product_name` varchar(64) NOT NULL COMMENT '产品名称',
  `deal_date` varchar(32) NOT NULL COMMENT '成交时间',
  `deal_price` decimal(10,0) NOT NULL COMMENT '成交价',
  `size_id` double NOT NULL COMMENT '尺码',
  `spu_id` int(11) NOT NULL COMMENT '产品id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `tmp_data_6`
-- ----------------------------
DROP TABLE IF EXISTS `tmp_data_6`;
CREATE TABLE `tmp_data_6` (
  `id` int(11) NOT NULL,
  `product_name` varchar(64) NOT NULL COMMENT '产品名称',
  `deal_date` varchar(32) NOT NULL COMMENT '成交时间',
  `deal_price` decimal(10,0) NOT NULL COMMENT '成交价',
  `size_id` double NOT NULL COMMENT '尺码',
  `spu_id` int(11) NOT NULL COMMENT '产品id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `tmp_data_7`
-- ----------------------------
DROP TABLE IF EXISTS `tmp_data_7`;
CREATE TABLE `tmp_data_7` (
  `id` int(11) NOT NULL,
  `product_name` varchar(64) NOT NULL COMMENT '产品名称',
  `deal_date` varchar(32) NOT NULL COMMENT '成交时间',
  `deal_price` decimal(10,0) NOT NULL COMMENT '成交价',
  `size_id` double NOT NULL COMMENT '尺码',
  `spu_id` int(11) NOT NULL COMMENT '产品id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `tmp_data_8`
-- ----------------------------
DROP TABLE IF EXISTS `tmp_data_8`;
CREATE TABLE `tmp_data_8` (
  `id` int(11) NOT NULL,
  `product_name` varchar(64) NOT NULL COMMENT '产品名称',
  `deal_date` varchar(32) NOT NULL COMMENT '成交时间',
  `deal_price` decimal(10,0) NOT NULL COMMENT '成交价',
  `size_id` double NOT NULL COMMENT '尺码',
  `spu_id` int(11) NOT NULL COMMENT '产品id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `tmp_data_9`
-- ----------------------------
DROP TABLE IF EXISTS `tmp_data_9`;
CREATE TABLE `tmp_data_9` (
  `id` int(11) NOT NULL,
  `product_name` varchar(64) NOT NULL COMMENT '产品名称',
  `deal_date` varchar(32) NOT NULL COMMENT '成交时间',
  `deal_price` decimal(10,0) NOT NULL COMMENT '成交价',
  `size_id` double NOT NULL COMMENT '尺码',
  `spu_id` int(11) NOT NULL COMMENT '产品id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `user_product_lists`
-- ----------------------------
DROP TABLE IF EXISTS `user_product_lists`;
CREATE TABLE `user_product_lists` (
  `id` int(11) NOT NULL,
  `uid` int(11) NOT NULL COMMENT '用户id',
  `spu_id` int(11) NOT NULL COMMENT 'spuid',
  `size_id` int(11) NOT NULL COMMENT 'skuid',
  `price` decimal(10,0) NOT NULL COMMENT '成交价格',
  `date` varchar(32) NOT NULL COMMENT '购买日期',
  `deleted` tinyint(1) NOT NULL COMMENT '0正常，1删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `user_wish_lists`
-- ----------------------------
DROP TABLE IF EXISTS `user_wish_lists`;
CREATE TABLE `user_wish_lists` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `uid` int(11) NOT NULL COMMENT '用户ID',
  `skuid` int(11) NOT NULL COMMENT '产品ID',
  `spuid` int(11) NOT NULL,
  `size` double DEFAULT NULL COMMENT '尺码',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='心愿列表';

-- ----------------------------
--  Table structure for `users`
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `firstname` varchar(30) DEFAULT NULL COMMENT '姓',
  `lastname` varchar(30) DEFAULT NULL COMMENT '名',
  `nickname` varchar(30) NOT NULL COMMENT '微信昵称',
  `cover` varchar(64) DEFAULT NULL COMMENT '微信头像',
  `gender` tinyint(1) DEFAULT NULL COMMENT '性别0男1女',
  `email` varchar(50) DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(11) DEFAULT NULL COMMENT '手机号',
  `size` varchar(200) DEFAULT '0' COMMENT '常选尺寸',
  `province` varchar(30) DEFAULT NULL COMMENT '省名',
  `city` varchar(30) DEFAULT NULL COMMENT '市',
  `area` varchar(30) DEFAULT NULL COMMENT '区',
  `address` varchar(30) DEFAULT NULL COMMENT '地址',
  `zip_code` varchar(30) DEFAULT NULL COMMENT '邮编',
  `ctime` int(10) unsigned DEFAULT '0' COMMENT '创建时间',
  `utime` int(10) unsigned DEFAULT '0' COMMENT '更新时间',
  `status` tinyint(3) DEFAULT '1' COMMENT '用户状态，1正常，0禁用',
  `openid` varchar(32) NOT NULL COMMENT '微信openid',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='用户表';

SET FOREIGN_KEY_CHECKS = 1;
