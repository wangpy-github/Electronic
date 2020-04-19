import pymysql
# 查看某一个时间段内，真实用户的下单情况
# 我的用户信息
start_add_time = '2019-8-22-23-59'
end_add_time = '2019-10-25-23-59'

conn = pymysql.connect(host="212.64.57.50", port=3306, user="dev", password="Scp3908!op", database="house_dev",
                       charset="utf8")
cursor = conn.cursor()
sql = """
SELECT
   o.order_sn '订单号',
   s.merchants_name '商家名称',
   FROM_UNIXTIME(o.add_time, '%%Y-%%c-%%d %%h:%%i:%%s') '下单时间',
   o.consignee '购买者信息',
   o.goods_amount '总金额',
   o.order_amount '应付金额',
   (
   case o.order_status 
        when 0 THEN '待支付' 
        when 1 THEN '已支付/待收货' 
        when 2 THEN '已完成' 
        when 3 THEN '已取消' 
        ELSE '其他' 
        END
   ) '订单状态'
FROM hs_order_info as o 
LEFT JOIN hs_store_franchisee as s ON o.store_id=s.store_id
WHERE user_id <> 8 and o.add_time > UNIX_TIMESTAMP("%s") AND o.add_time < UNIX_TIMESTAMP("%s")
""" % (start_add_time, end_add_time)
row_count = cursor.execute(sql)
for line in cursor.fetchall():
    print(line)
cursor.close()
conn.close()
print("共%s条数据" % (row_count))
