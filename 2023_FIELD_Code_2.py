
import numpy as np
import pandas as pd
from IPython.display import clear_output

clear_output
def simulation(period):
    cost = 0
    country_list={'before':{'USA':[8,1.5],'Saudi':[6,0.5],'Russia':[5,0.5]},'after':{'USA':[8,2],'Saudi':[6,1.5],'Russia':[7,4]}}
    cost_list = [0]
    #참가자들이 직접 입력하시면 됩니다. / 1 period = 5일, 6 period = 한 달 로 진행됩니다. 
    oil_price_list = {'before':{'USA':[0,0,0,0,0],'Saudi':[0,0,0,0,0],'Russia':[0,0,0,0,0]},'after':{'USA':[0,0,0,0,0],'Saudi':[0,0,0,0,0],'Russia':[0,0,0,0,0]}}
    oil_price_print=[]
    demand = [7] * period
    inventory = [100]
    order = []
    user_order=0
    order_time=[0] * period
    arrival_time=['-'] * period
    lead_time=['-'] * period

    print("시뮬레이션에 오신 걸 환영합니다!")
    print("전쟁 전인가요 후인가요?")
    print("before / after 중에 선택해주세요")
    war=input()
    while (war != "before" and war != "after"):
        war = input()
    if war=='before' :
        inventory_cost = 8
    else : 
        inventory_cost = 10
    print("나라를 선택해주세요")
    print("USA / Saudi / Russia 중에 선택해주세요")
    coun = input()
    while (coun != "USA" and coun != "Saudi" and coun !="Russia"):
        coun = input()
    lead_mean, lead_std=country_list[war][coun]
    for i in range(period):
        oil_price=oil_price_list[war][coun][int(i/6)]
        print("<Period %i>" %i)
        oil_price_print.append(oil_price)
        for sample_period, order_amount in order:
            if sample_period <= i:
                print("주문이 도착했습니다!!")
                inventory[i] += order_amount
                order.pop(0)
        print("현재 석유 가격: {}".format(oil_price))
        print("현재 수요: %i" %demand[i])
        print("현재 보관량: %i" %inventory[i])
        print("현재 비용: {}" .format(cost))

        while True:
            print("행동을 선택하세요!")
            print("[O] 주문")
            print("[N] 다음 Period로")
            user = input()
            while (user != "O" and user != "N"):
                user = input()
            if user == "O":
                print("얼마나 주문하실 건가요?")
                while True:
                    user_order = input()
                    try:
                        user_order = int(user_order)
                        print("%i를 주문했습니다!" %user_order)
                        cost += user_order * oil_price
                        order_time[i] = 1
                        arrival= i + np.random.normal(lead_mean,lead_std,1)
                        lead_time[i]=int(arrival[0])+1-i
                        arrival_time[i] = int(arrival[0])+1
                        order.append((arrival_time[i], user_order))
                        break
                    except:
                        continue

            print("================================")
            break
        if inventory[i]>0 :
            cost += (inventory[i]) * inventory_cost
        else :
            cost -= (inventory[i]) * (3 * oil_price)

        inventory.append(inventory[i] - demand[i])
        cost_list.append(cost)
    result = pd.DataFrame([oil_price_print, demand, inventory, cost_list,order_time,lead_time,arrival_time], index = ["Oil Price","Demand", "Inventory", "Cost","Order","Lead Time", "Arrival"])

    result.to_csv("결과.csv")
simulation(25)
