import numpy as np
import pandas as pd

country_list={'before':{'USA':[8,1.5],'Saudi':[6,0.5],'Russia':[5,0.5]},'after':{'USA':[8,2],'Saudi':[6,1.5],'Russia':[7,4]}}
#참가자들이 직접 입력하시면 됩니다. 
oil_price_list = {'before':{'USA':[60.55,64.58,68.24,71.53,74.45],'Saudi':[66.54,71.46,75.78,79.51,82.63],'Russia':[66.58,69.29,71.11,72.38,73.31]},'after':{'USA':[44,44,44,44,44],'Saudi':[44,44,44,44,44],'Russia':[44,44,44,44,44]}}

reorder_arr=np.arange(5,100,20) # Reorder Point 범위 설정 가능
order_arr=np.arange(5,100,20)   # Order Quantity 범위 설정 가능

def multi_simulation(period,inventory_cost_input,lead_mean,lead_std,reorder,order_quantity):
    total_cost=[]
    
    for _ in range(100) :                                 
        inventory_cost = inventory_cost_input
        cost = 0
        demand = [7] * period
        inventory = [100]
        order = []
        arrival=[0]
        user = "N"
        for i in range(period):
            for sample_period, order_amount in order:
                if sample_period <= i:
                    inventory[i] += order_amount
                    order.pop(0)

            if inventory[i] <= reorder and i>=arrival[0]:
                user = "O"
            else : 
                user = "N"
        
            if user == "O":
                cost += order_quantity * oil_price
                arrival= i + np.random.normal(lead_mean,lead_std,1)
                order.append((arrival[0], order_quantity))

            if inventory[i]>0 :
                cost += (inventory[i]) * inventory_cost
            else : 
                cost -= (inventory[i]) * (3 * oil_price)
            
            inventory.append(inventory[i] - demand[i])
            
        total_cost.append(cost)
        
    mean_cost=np.mean(total_cost)
    std_cost=np.std(total_cost)   
    return [mean_cost,std_cost]
war_status=['before','after']
country_status=['USA','Saudi','Russia']
for war in range(2):
  if war==0 :
      print('<전쟁 전>')
      inventory_cost=8
  else : 
      print('<전쟁 후>')
      inventory_cost=10
  for country in range(3):
    print("  {} : ".format(country_status[country])) 
    reorder_print=[]
    order_print=[]
    cost_mean=[]
    cost_std=[]
    oil_price=np.mean(oil_price_list[war_status[war]][country_status[country]])
    for i in range(len(reorder_arr)):
        for j in range(len(order_arr)):
            #period 500까지 100번 실행 후 나온 Total Cost 의 평균, 표준편차 출력 
            result_print=multi_simulation(500,inventory_cost,country_list[war_status[war]][country_status[country]][0],country_list[war_status[war]][country_status[country]][1],reorder_arr[i],order_arr[j])
            cost_mean.append(result_print[0])
            cost_std.append(result_print[1])
            reorder_print.append(reorder_arr[i])
            order_print.append(order_arr[j])
    result=pd.DataFrame([reorder_print,order_print,cost_mean,cost_std],index=["Reorder","Order","Cost Mean","Cost Std"])
    sorted_cost_indexes = sorted(range(len(cost_mean)), key=lambda k: cost_mean[k])[:3] 
    for i in range(3) :
        print("  {}번째로 낮은 cost를 가졌던 (R,Q)는 ({},{})입니다".format(i+1,reorder_print[sorted_cost_indexes[i]],order_print[sorted_cost_indexes[i]]))
        print("  Cost 의 평균 : {}, 표준편차는 : {}".format(cost_mean[sorted_cost_indexes[i]],cost_std[sorted_cost_indexes[i]]))
    result.to_csv("Optimization Result2.csv")


