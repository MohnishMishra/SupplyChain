# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 09:44:46 2022

@author: amlanghosh
"""

import pandas as pd
from pulp import *
from data_preparation import *
from model import *

data = 'DummyProduct_SupplyChainData.xlsx'

df_supplier = pd.read_excel(data, sheet_name = 'Supplier')
supplier = list(df_supplier['Name'].unique())

dis_demand = []

with pd.ExcelWriter('Disrupted_Output.xlsx') as writer:

    for dis_sup in supplier:
        
        factory_product,material,product_factory = data_prep(data,dis_sup)
        df, d = model(material,factory_product,product_factory)
        
        print (str(dis_sup)+' '+str(1 - d))
        dis_demand.append((1-d)*100)
        
        df.to_excel(writer, sheet_name = str(dis_sup), index = False)
    
    df = pd.DataFrame({'Supplier': supplier, 'Disrupted Demand Percentage': dis_demand},
                      columns = ['Supplier','Disrupted Demand Percentage'])
    
    df.to_excel(writer, sheet_name = 'Results', index = False)
    