from pet import Pet, login, send, recive

ticket = "xQRFZoF0slMhC_ay4mBvxkxah96uuI4Vs5Q_c_c"
goods_num = 1  # 每件商品购买的数量
num = 3        # num件商品
while True:
    pet = Pet(goods_num, ticket)
    for i in range(num):
        pet.goods_detail()
        pet.add_cart()

    pet.get_goods_cart_list()
    pet.get_order()

    input("请确认是否已经付钱？？：")

    login()
    send()
    recive(ticket)
    # input("请确认是否收货成功！！")
