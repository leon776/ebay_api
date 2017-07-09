#!/usr/bin/env node

let program = require('commander')
let colors = require('colors')
let runSearch = require('./spider')

function make_red(txt) {
  return colors.red(txt); //display the help text in red on the console
}

/**
 * @usage eg: ./command.js -k "Jordan 11 low georgetown" -s "01 20,2017" -e "07 01,2017" -p 100 -i 11 -b Nike
 */
program
  .version('0.1.0')
  .usage('./command -k <keyword> -s <start> -e <end> -p <price> -i <spuid> -b <brand>')
  .option('-k, --keyword <keyword>', '搜索关键词, 关键词含空格，用引号引起来')
  .option('-s, --start <mm dd,yyyy>', '搜索的开始日期，格式为: mm dd,yyyy')
  .option('-e, --end <mm dd,yyyy>', '搜索的结束日期，格式为: mm dd,yyyy')
  .option('-p, --price <price>', '过滤的最低价，单位USD')
  .option('-i, --spuid <spuid>', 'spuid')
  .option('-b, --brand <brand>', 'brand name')
  .parse(process.argv)

let {
  keyword,
  start,
  end,
  price,
  spuid,
  brand,
} = program
if(
  !keyword || !start || !end || !price ||
  !spuid || !brand
) { // 参数未正确提供
  program.outputHelp(make_red)
} else { // 提供正确， 运行爬虫
  console.log(`keyword: ${keyword} start: ${start} end: ${end} price: ${price} spuid: ${spuid} brand: ${brand}`)
  runSearch(keyword, start, end, price, spuid, brand)
}
