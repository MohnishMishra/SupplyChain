import pulp 
problem = pulp.LpProblem("My_Problem", pulp.LpMinimize)

# Upper bound has to be added and that depends on the invertory cost and budget

penalty_cost = pulp.LpVariable ('penalty_cost', lowBound=0, cat = 'Continuous') #f
lost_sales = pulp.LpVariable ('lost_sales', lowBound=0, cat = 'Continuous') #l
material_flow = pulp.LpVariable ('material_flow', lowBound=0, cat = 'Continuous') #x
demand_rate = pulp.LpVariable ('demand_rate', lowBound=0, cat = 'Continuous') #d
ttr_chain = pulp.LpVariable ('ttr', lowBound=0, cat = 'Continuous') #t
ttr_node = pulp.LpVariable ('ttr_node', lowBound= 0, cat = 'Continuous') #t 
goods_produced =pulp.LpVariable ('goods_produced', lowBound= 0, cat = 'Continuous') #u
goods_in_inventory = pulp.LpVariable ('inventory', lowBound= 0, cat = 'Continuous') #r
unit_inventory_holding_cost = pulp.LpVariable ('unit_inventory_holding_cost', lowBound = 0, cat= 'Continuous') #h
indicator_matrix = pulp.LpVariable ('indicator', lowBound= 0, cat = 'Continuous') #I
bom_matrix = pulp.LpVariable ('bom_matrix', lowBound= 0, cat = 'Continuous') #B
survival_indicator = pulp.LpVariable ('survival_indicator', lowBound= 0, cat = 'Continuous') #v
production_capacity = pulp.LpVariable ('production', lowBound= 0, cat = 'Continuous') #c

problem += sum(penalty_cost*lost_sales) + sum(unit_inventory_holding_cost * goods_in_inventory) #objective

problem += sum(material_flow) + lost_sales >= (demand_rate * ttr_chain)
problem += sum(material_flow) - goods_produced <= goods_in_inventory
problem += sum((material_flow * indicator_matrix)/(bom_matrix)) - goods_produced >= 0
problem += sum(goods_produced) <= (ttr_chain - ttr_node (1 - survival_indicator)) * production_capacity
            

