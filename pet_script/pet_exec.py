from pet_script.pet import Pet, login, send, recive
import time
ticket = "xQRFZoF0slMhC_ay4mBvxkxah96uuI4Vs5Q_c_c"
goods_num = 1  # 每件商品购买的数量
num = 2      # num件商品
while True:
    pet = Pet(goods_num, ticket)
    for i in range(num):
        pet.goods_detail()
        time.sleep(1)
        pet.add_cart()

    pet.get_goods_cart_list()
    time.sleep(1.5)
    pet.get_order()

    input("请确认是否已经付钱？？：")

    login()
    time.sleep(2)
    send()
    recive(ticket)
    # input("请确认是否收货成功！！")
