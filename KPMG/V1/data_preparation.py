# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 10:19:59 2022

@author: amlanghosh
"""

import pandas as pd

#data = 'DummyProduct_SupplyChainData.xlsx'

def data_prep(data, supplier):
    df_factory = pd.read_excel(data, sheet_name = 'Factory')
    df_network = pd.read_excel(data, sheet_name = 'Supplier-Factory Network')
    df_demand = pd.read_excel(data, sheet_name = 'Demand')
    df_product = pd.read_excel(data, sheet_name = 'Product')
    
#   supplier = list(df_supplier['Name'].unique())
    factory_product = {}
    material = {}
    product_factory = {}
    
    for row in df_factory.itertuples():
        if row[1] not in factory_product:
            factory_product[row[1]] = {'prod_capacity': int(row[3]), 'product':{row[2]:{}}}
        else:
            factory_product[row[1]]['product'][row[2]] = {}
            
        if row[2] not in product_factory:
            product_factory[row[2]] = {'factory': [row[1]]}
        else:
            product_factory[row[2]]['factory'].append(row[1])
    
    for row in df_network.itertuples():
        if row[3] not in material:
            if row[1] != supplier:
                material[row[3]] = {row[2]:{row[1]:int(row[4])}}
            else:
                material[row[3]] = {row[2]:{row[1]:0}}
        else:
            if row[2] not in material[row[3]]:
                if row[1] == supplier:
                    material[row[3]][row[2]] = {row[1]:0}
                else:
                    material[row[3]][row[2]] = {row[1]:int(row[4])}
            else:
                if row[1] == supplier:
                    material[row[3]][row[2]][row[1]] = 0
                else:
                    material[row[3]][row[2]][row[1]] = int(row[4])
    
    for row in df_demand.itertuples():
        product_factory[row[1]]['demand'] = float(row[2])
    
    for row in df_product.itertuples():
        factory_product[row[2]]['product'][row[1]][row[3]] = int(row[4])
    
    return factory_product, material, product_factory