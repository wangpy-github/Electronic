import random
import jsonpath
import requests

rec_id_str = str()


# 将商品加入购物车，并获取购物车id
def creat_cart(num, creat_cart_url, feed_token, number):
    goods_id = random.randint(1118, 1947)
    url = creat_cart_url
    json = {
        "goods_id": goods_id,
        "token": feed_token
    }
    try:
        response_data = requests.post(url, json=json).json()
    except Exception as e:
        print(e)
        print("无法加入购物车")
    if response_data:
        status = response_data["status"].get("succeed")
        error_desc = response_data["status"].get("error_desc")
        print("错误信息：", error_desc)
        rec_id_list = jsonpath.jsonpath(response_data, '$..cart_list[0]..rec_id')
        global rec_id_str
        rec_id_str = ",".join('%s' % id for id in rec_id_list)
        print("购物车ID：", rec_id_str)
    else:
        print("加入购物车失败")

    if status == 1:
        num += 1
    if num == number:
        return
    creat_cart(num, creat_cart_url, feed_token, number)


# 用户下单，并生成订单号
def down_order(down_order_url, feed_token):
    address_id_list = [127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138]  # TODO   地址随机
    address_id = random.choice(address_id_list)
    url = down_order_url
    if rec_id_str:
        json = {
            "address_id": address_id,
            "pay_id": 11,
            "rec_id": rec_id_str,
            "token": feed_token,
            "shipping_id": 3
        }
        try:
            response = requests.post(url, json=json)
            response_data = response.json()
        except Exception as e:
            print(e)
            print("订单接口获取数据失败")
    if response_data:
        order_sn = jsonpath.jsonpath(response_data, '$.data.order_info.order_sn')
        order_amount = jsonpath.jsonpath(response_data, '$.data.order_info.order_amount')
        order_id = jsonpath.jsonpath(response_data, '$.data.order_id')
        print("order_sn", order_sn)
        global order_id_str
        order_id_str = ",".join('%s' % id for id in order_id)
        print("订单ID:", order_id_str)
        print("订单金额：", order_amount)
    else:
        print("订单接口获取数据失败")


# 用户确认收货
def recived(feed_token, operation_url, Received_url):
    operation_url = operation_url
    Received_url = Received_url
    if order_id_str:
        operation_data = {
            "token": feed_token,
            "order_id": order_id_str,
            "order_status": "shipped"}

        Received_data = {
            "token": feed_token,
            "order_id": order_id_str,
            "refund_type": "affirm",
            "refund_sn": ""}
        try:
            requests.post(url=operation_url, data=operation_data).json()
        except Exception as e:
            print(e)
            print("==============？")
        try:
            requests.post(url=Received_url, data=Received_data).json()
        except Exception as e:
            print(e)
            print("用户确认收货失败")


# 小站订单操作
class login_order_exec():
    def login(self, mobile, password, login_url):
        json_login = {
            "mobile": mobile,
            "password": password
        }
        global session
        session = requests.session()
        try:
            global  r
            r = session.post(url=login_url, json=json_login)
        except:
            print("小站用户登录失败")

    def order_exec(self, operation, confirm_receipt_url):
        if r and order_id_str:
            json_order = {
                "operation": operation,
                "order_id": int(order_id_str)
            }
            try:
                data = session.post(url=confirm_receipt_url, json=json_order)
                response_data = data.json()
                status = jsonpath.jsonpath(response_data, '$.status.succeed')
                print("B端订单操作状态", status)
            except:
                print("B端订单操作失败")
        return

    def is_confirm(self, detail_url):
        if r and order_id_str:
            json_detail = {
                "id": order_id_str
            }
            try:
                data = session.post(url=detail_url, json=json_detail)
                response_data = data.json()
                status = jsonpath.jsonpath(response_data, '$.data.label_order_status')
                print("B端订单操作状态：", status)
            except:
                print("查看详情失败")
        return
