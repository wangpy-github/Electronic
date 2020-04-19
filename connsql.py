import random
import jsonpath
import pymysql
import requests
import time
import xlwt


class Mysql():
    def __init__(self, host, user, password, database, charset, port=3306):
        self.conn = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database,
            charset=charset
        )
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()

    def fetchone(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def fetchall(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()


# 后台订单状态操作
session = requests.session()


def login():
    login_url = "http://app.majigo.net/admin_index/login"
    form_data_login = {
        "name": "admin",
        "password": "csh666888",
        "online": ""
    }
    try:
        response_data = session.post(url=login_url, data=form_data_login).json()
        msg = jsonpath.jsonpath(response_data, "$.msg")
        print(msg)
    except:
        print("小站用户登录失败")


# 发货
def send(order_id):
    send_url = "http://app.majigo.net/admin_order/post"
    suiji = random.randint(10111, 33199)
    express_no = "710605084" + str(suiji)
    form_data_login = {
        "express_com": "yt",
        "express_no": express_no,
        "remark": "货物已发，请注意查收",
        "orderId": order_id
    }
    try:
        response_data = session.post(url=send_url, data=form_data_login).json()
        msg = jsonpath.jsonpath(response_data, "$.msg")
        print(msg)
    except:
        print("订单发货异常")


def order_num_sum(start_time, end_time, sql):
    start = time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
    end = time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))
    return mysql.fetchone(sql.format(start, end))


def order_excel(start_time, end_time, sql):
    start = time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
    end = time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))
    orders = mysql.fetchall(sql.format(start, end))
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('My Worksheet')
    for row in range(len(orders)):
        order = orders[row]  # type:dict
        order["pay_time"] = time.strftime("%Y-%m-%d %H:%M", time.localtime(order["pay_time"]))
        col = 0
        for val in order.values():
            # 参数对应 行, 列, 值
            worksheet.write(row, col, label=val)
            col += 1
    workbook.save('./Excel_test.xls')


if __name__ == '__main__':
    # 刷单人员的已支付且未发货订单
    sql1 = "select id " \
           "from wf_order " \
           "WHERE uid in (21,16018,17092,17079,16975,15874,16951,17090,16967,17091,891,105,15589) " \
           "AND pay_status=1 AND order_status=1 " \
           "order by id DESC ;"
    # 真实用户下单查看
    sql2 = "select uid, order_no, pay_time " \
           "from wf_order " \
           "WHERE uid not in (21,16018,17092,17079,16975,15874,16951,17090,17091,16967,891,105,15589) " \
           "AND pay_status=1 and order_status=1 " \
           "order by id DESC ;"
    # 查看时间段内订单数量及总金额
    sql3 = "select count(*) '总数量', sum(price) '总金额', avg(price) '平均价' " \
           "from wf_order " \
           "WHERE uid=15874 AND pay_status=1 and order_status !=9 and pay_time >{} and pay_time<{};"
    # 订单表
    sql4 = "select id, uid, order_no, num, price, total_price, " \
           "case wf_order.pay_status " \
           "WHEN 1 THEN '已付款'  " \
           "WHEN 0 THEN '待支付' " \
           "when 2 THEN '已发货' " \
           "when 4 THEN '待评价' " \
           "ELSE '其他' " \
           "END 支付状态," \
           "pay_time " \
           "from wf_order " \
           "WHERE uid=15874 AND pay_status=1 and order_status !=9 and pay_time >{} and pay_time<{} " \
           "ORDER BY id DESC;"
    mysql = Mysql(host="47.100.225.33", user="root", password="iS04_a-kjA!s*", database="chongshe_test", charset="utf8")

    # 批量发货
    print("-" * 100, "批量发货")
    r = mysql.fetchall(sql1)
    login()
    for order in r:
        send(order["id"])

    # 查看真实用户
    print("-" * 100, "查看真实用户")
    real_orders = mysql.fetchall(sql2)
    for real_order in real_orders:
        real_order["pay_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(real_order["pay_time"]))
        print(real_order)

    # 查看订单数量及总金额
    print("-" * 100, "订单数量及总金额")
    start_time = '2020-4-12 00:00:00'
    end_time = '2020-4-12 23:59:59'
    order_num_sum = order_num_sum(start_time, end_time, sql3)
    print(order_num_sum)

    # 生成订单表
    # if order_num_sum["总金额"] is not None and order_num_sum["总金额"] >= 69900:
    #     order_excel(start_time, end_time, sql4)
    #     print("-" * 100, "生成订单表")

    order_excel(start_time, end_time, sql4)
    print("-" * 100, "生成订单表")
