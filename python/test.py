#!/usr/bin/env python
import math

def batch(iterable, n=1):
    print(iterable)
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


for x in batch(range(0, 10), 3):
    print(x)



    insertSQL = '''REPLACE INTO {table_name} (keyword, product_name, deal_date, currency, deal_price, size_name, brand, size, size_id, deal_no, spu_id, aspect, content) VALUES '''.format(table_name = table_name)

    values = []
    valueSQL = '''("{keyword}", "{product_name}", "{deal_date}", "{currency}", {deal_price}, "{size_name}", "{brand}", "{size}", "{size_id}", "{deal_no}", "{spu_id}", "{aspect}", "{content}")'''                                                                                                                                                                     
    for (deal_no, record) in records.items():
        values.append(valueSQL.format(
            keyword = pymysql.escape_string(record['keyword']), 
            product_name = pymysql.escape_string(record['product_name']),
            deal_date = record['deal_date'],
            currency = record['currency'],
            deal_price = record['deal_price'],
            size_name = record['size_name'],
            brand = record['brand'],
            size = record['size'],
            size_id = record['size_id'],
            deal_no = record['deal_no'],
            spu_id = record['spu_id'],
            aspect = pymysql.escape_string(json.dumps(record['aspect'], sort_keys = True)),
            content = pymysql.escape_string(json.dumps(record, sort_keys = True))
        ))

    for blocks in batch(values, bulkSize):
        sql = insertSQL + ', '.join(blocks)
        sql_logger.info('bulk insert sql: ' + sql)
        try:
            cursor.execute(sql)
            # 必需commit才能到数据库中
            conn.commit()

        except Exception as e:
            sql_logger.error('Exception sql: ' + sql)   
            print('ignore the row', sql)

