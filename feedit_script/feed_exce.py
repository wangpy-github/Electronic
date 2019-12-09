import feedit_script

# token
feed_token = "1f398757fdae92f5b4c3fa39971e9c7b0c5bc2ab"
# 加入购物车的商品数量
number = 1
# B端登陆账号密码
mobile = "17739792833"
password = "123456"
# 地址
host = "hs.wangxuekeji.com"
creat_cart_url = "https://" + host + "/sites/api/?url=cart/create"
down_order_url = "https://" + host + "/sites/api/?url=flow/done"
login_url = "https://" + host + "/sites/api/?url=h5_merchant/login"
ship_url = "https://" + host + "/sites/api/?url=admin/orders/status"
detail_url = "https://" + host + "/sites/api/?url=admin/orders/detail"
operation_url = "https://" + host + "/sites/api/?url=orders/operation"
Received_url = "https://" + host + "/sites/api/?url=order/affirmReceived"

while True:
    num = 0
    # 用户加入购物车，并生成订单
    feedit_script.creat_cart(num, creat_cart_url, feed_token, number)
    feedit_script.down_order(down_order_url, feed_token)
    input("请确认支付：")

    # B端订单状态操作
    obj = feedit_script.login_order_exec()
    obj.login(mobile, password, login_url)
    # 开始接单
    obj.order_exec("confirm", ship_url)
    # 开始配送
    obj.order_exec("ship", ship_url)
    # 配送完成
    obj.order_exec("goods_service_to_user", ship_url)

    # 判断是否待用户确认收货
    obj.is_confirm(detail_url)

    # C端确认收货
    feedit_script.recived(feed_token, operation_url, Received_url)
    obj.is_confirm(detail_url)

