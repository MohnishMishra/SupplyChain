# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 14:11:55 2022

@author: amlanghosh
"""

from pulp import *
import pandas as pd

def model(material, factory_product, product_factory):
    
    scr = LpProblem('SupplyChainResiliency', sense = LpMinimize)
        
    var_RawMaterialQuantity = {}
    for i in material:
        for j in material[i]:
            for k in material[i][j]:
                var_RawMaterialQuantity[i,j,k] = LpVariable('RM_{0}_{1}_{2}'.format(i,j,k), 
                                                            lowBound = 0, 
                                                            upBound = material[i][j][k],
                                                            cat = LpContinuous)
                
    var_FinishedGoodQuantity = {}
    for i in factory_product:
        for j in factory_product[i]['product']:
            var_FinishedGoodQuantity[i,j] = LpVariable('FG_{0}_{1}_{2}'.format(i,j,k),
                                                  lowBound = 0,
                                                  upBound = factory_product[i]['prod_capacity'],
                                                  cat = LpContinuous)
    
    # var_FinishedGoodQuantity = LpVariable.dicts('FG',((i,j) for i in factory_product
    #                                                   for j in factory_product[i]['product']),
    #                                             lowBound = 0, cat = LpContinuous)
    
    var_LostProduction = LpVariable.dicts('LP', ((i) for i in product_factory), 
                                          lowBound = 0, cat = LpContinuous)
    
    for prod in product_factory:
        scr += (var_LostProduction[prod] + lpSum([var_FinishedGoodQuantity[fac,prod]
                                        for fac in product_factory[prod]['factory']]) 
          >= product_factory[prod]['demand'], 'prod_{0}'.format(prod))

        # scr += (lpSum([var_FinishedGoodQuantity[fac,prod]
        #                                 for fac in product_factory[prod]['factory']]) 
        #  >= product_factory[prod]['demand'], 'prod_{0}'.format(prod))
    
    for fac in factory_product:
        scr += (lpSum([var_FinishedGoodQuantity[fac,prod] for prod in factory_product[fac]['product']])
         <= factory_product[fac]['prod_capacity'], 'Fac_{0}'.format(fac))
    
    for fac in factory_product:
        for prod in factory_product[fac]['product']:
            for mat in factory_product[fac]['product'][prod]:
                scr += (var_FinishedGoodQuantity[fac,prod]*factory_product[fac]['product'][prod][mat]
                 <= lpSum([var_RawMaterialQuantity[mat,fac,sup] for sup in material[mat][fac]]), 
                 'mat_{0}_{1}_{2}'.format(mat,prod,fac))
    
    scr += lpSum([var_LostProduction[prod] for prod in product_factory])
    # scr += (lpSum([var_FinishedGoodQuantity[fac,prod] 
    #              for fac in factory_product for prod in factory_product[fac]['product']])
    #         - lpSum([var_RawMaterialQuantity[mat,fac,sup]
    #                  for mat in material
    #                  for fac in material[mat]
    #                  for sup in material[mat][fac]]))
    
    scr.solve()
    
    if LpStatus[scr.status] == 'Optimal':
        output_dict = {
                        '': [],
                        'Product/Material': [],
                        'Supplier':[],
                        'Factory':[],
                        'Quantity': [],
                        'Max Quantity': []
                        }
        for prod in product_factory:
            output_dict[''].append('Lost Production')
            output_dict['Product/Material'].append(prod)
            output_dict['Supplier'].append('')
            output_dict['Factory'].append('')
            output_dict['Quantity'].append(var_LostProduction[prod].varValue)
            output_dict['Max Quantity'].append('')

        output_dict[''].append('')
        output_dict['Product/Material'].append('')
        output_dict['Supplier'].append('')
        output_dict['Factory'].append('')
        output_dict['Quantity'].append('')
        output_dict['Max Quantity'].append('')

        for prod in product_factory:
            for fac in product_factory[prod]['factory']:
                output_dict[''].append('Finished Good')
                output_dict['Product/Material'].append(prod)
                output_dict['Supplier'].append('')
                output_dict['Factory'].append(fac)
                output_dict['Quantity'].append(var_FinishedGoodQuantity[fac,prod].varValue)
                output_dict['Max Quantity'].append('')
        
        demand_met = 0
        total_demand = 0
        for prod in product_factory:
            output_dict[''].append('Total')
            output_dict['Product/Material'].append(prod)
            output_dict['Supplier'].append('')
            output_dict['Factory'].append('')
            output_dict['Quantity'].append(
                sum([var_FinishedGoodQuantity[fac,prod].varValue for fac in product_factory[prod]['factory']]))
            demand_met += sum([var_FinishedGoodQuantity[fac,prod].varValue for fac in product_factory[prod]['factory']])
            output_dict['Max Quantity'].append(product_factory[prod]['demand'])
            total_demand += product_factory[prod]['demand']

        output_dict[''].append('')
        output_dict['Product/Material'].append('')
        output_dict['Supplier'].append('')
        output_dict['Factory'].append('')
        output_dict['Quantity'].append('')
        output_dict['Max Quantity'].append('')
        
        for mat in material:
            for fac in material[mat]:
                for sup in material[mat][fac]:
                    output_dict[''].append('Raw Material')
                    output_dict['Product/Material'].append(mat)
                    output_dict['Supplier'].append(sup)
                    output_dict['Factory'].append(fac)
                    output_dict['Quantity'].append(var_RawMaterialQuantity[mat,fac,sup].varValue)
                    output_dict['Max Quantity'].append(material[mat][fac][sup])
        df = pd.DataFrame(output_dict, columns = ['','Product/Material','Supplier','Factory','Quantity','Max Quantity'])
    else:
        print ('Infeasible')
    
    return df, demand_met/total_demand
    
    # for i in scr.variables():
    #     print (str(i.name) + '=' + str(i.varValue))
        
    #print (scr)