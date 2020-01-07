import json
a = {'ecjia_admin_api_token': '044e026481e87cc9d7a7487cea6fac93f61bef04'}
a = str(a)

A = json.dumps(a)
c = json.loads(A)

# print("json类型：", type(A))
# A  = A + "s"
# print(A)
# print("dict类型：", type(c))
# print(c)


s = "s"
if s in [str]:
    print("ss")