import random as r

if __name__ == '__main__':
    first_name = ["朗逸汽车保养", "轩逸汽车保养", "长安汽车保养", "名爵汽车保养", "哈佛汽车保养",'雅阁汽车保养','思域汽车保养']
    secod_name = ['1', '2', '3', '4', '5','6','7']

    goodsname = r.choice(first_name) + ''.join(r.choice(secod_name))
    print(goodsname)
