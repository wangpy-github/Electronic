import random
import time
from pet import Pet, login, send, recive

ticket = "xQRFZoF0slMhC_ay4mBvxkxah96uuI4Vs5Q_c_c"
goods_num = 1  # 每件商品购买的数量
while True:
    num = random.randint(1, 3)
    print("--本-次-商-品-数-量--:", num)

    # tim = random.randint(1, 3)
    # print("等待{}分钟...".format(tim))
    # time.sleep(tim*60)

    pet = Pet(goods_num, ticket)
    for i in range(num):
        pet.goods_detail()
        pet.add_cart()

    pet.get_goods_cart_list()
    pet.get_order()

    input("请确认是否已经付钱？？：")

    login()
    time.sleep(1.5)
    send()
    recive(ticket)
