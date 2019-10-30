import jsonpath
import requests
import random


# C 端操作
class Pet(object):
    def __init__(self, goods_num, ticket):
        self.goods_num = goods_num  # 每件商品购买的数量
        self.ticket = ticket

    # 查看商品详情，获取specification_id  # 规格
    def goods_detail(self):
        global goods_id
        goods_id = random.randint(56, 1097)
        url1 = "https://app.majigo.net/goods/info?goodsId=" + str(goods_id)
        try:
            response_data = requests.get(url1, ).json()
            status = jsonpath.jsonpath(response_data, "$.status")
            if status == [200]:
                # 获取商品的sku
                specification_id_list = jsonpath.jsonpath(response_data, "$.data.skus..specification_id")
                global specification_id
                specification_id = random.choice(specification_id_list)
            elif status == [-1]:
                print("没有这个商品ID，将继续查询")
                self.goods_detail()
        except:
            print("查看商品详情失败")

    def add_cart(self):
        url2 = "https://app.majigo.net/user_cart/add"
        if specification_id:
            goodsData = "%d:%d:%d" % (goods_id, specification_id, self.goods_num)
            json = {
                "goodsData": goodsData,  # goodsId=414  specification_id=434  购买数量1
                "ticket": self.ticket
            }
            try:
                response_data = requests.post(url2, json=json, ).json()
                status = jsonpath.jsonpath(response_data, "$.status")
                if status == [200]:
                    print("添加到购物车成功")
                else:
                    self.add_cart()
            except:
                print("添加商品到购物车失败")
        else:
            print("没有specification_id")

    # 查看购物车商品列表，用于组合生成订单的参数
    def get_goods_cart_list(self):
        url5 = "https://app.majigo.net/user_cart/list?ticket=%s" % (self.ticket)
        try:
            response_data = requests.get(url=url5, ).json()
            # 组合数据，提交订单的goodsData
            store_list = jsonpath.jsonpath(response_data, "$.data.list[*]")
            goods = []
            for store in store_list:
                for goods_list in store.get("goodsList"):
                    goodsId = goods_list.get("goodsId")
                    specification_id = goods_list.get("specification_id")
                    num = goods_list.get("num")
                    goods_data = "%d:%d:%d" % (goodsId, specification_id, num)
                    goods.append(goods_data)
            global goodsData
            goodsData = ";".join(goods)

        except:
            print("查看购物车商品列表失败")

    # 生成订单
    def get_order(self):
        url4 = "https://app.majigo.net/order/goods"
        addressId = random.choice(
            [1024, 1025, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023])  # TODO   地址随机
        if goodsData:
            json4 = {
                "ticket": self.ticket,
                "goodsData": goodsData,
                "addressId": addressId,
                "payType": "miniwx"
            }
            try:
                response_data = requests.post(url=url4, json=json4, ).json()
                orderId = jsonpath.jsonpath(response_data, "$.data.orderId")
                global order_id
                order_id = ",".join('%s' % id for id in orderId)
                order_no = jsonpath.jsonpath(response_data, "$.data.order_no")
                price = jsonpath.jsonpath(response_data, "$.data.price")
                print("订单号：", order_no)
                print("订单金额：", price)
            except:
                print("订单生成失败")
        else:
            print("没有组合数据")


# 后台订单状态操作
def login():
    login_url = "http://app.majigo.net/admin_index/login"
    form_data_login = {
        "name": "admin",
        "password": "csh666888",
        "online": ""
    }
    try:
        global session
        session = requests.session()
        response_data = session.post(url=login_url, data=form_data_login).json()
        msg = jsonpath.jsonpath(response_data, "$.msg")
        print(msg)
    except:
        print("小站用户登录失败")
# 发货
def send():
    send_url = "http://app.majigo.net/admin_order/post"
    suiji = random.randint(10111, 33199)
    express_no = "710605084" + str(suiji)
    form_data_login = {
        "express_com": "yt",
        "express_no": express_no,
        "remark": "货物已发，请注意查收",
        "orderId":order_id
    }
    try:
        response_data = session.post(url=send_url, data=form_data_login).json()
        msg = jsonpath.jsonpath(response_data,"$.msg")
        print(msg)
    except:
        print("订单发货异常")

# 确认收货
def recive(ticket):
    recive_url = "https://app.majigo.net/order/getGoodsExpress"
    json = {
        "orderId" : order_id,
        "ticket" : ticket
    }
    try:
        response_data = requests.post(url=recive_url, json=json).json()
        msg = jsonpath.jsonpath(response_data,"$.msg")
        print(msg)
    except:
        print("确认收货异常")
