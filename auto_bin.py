# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 14:48:42 2018

@author: 56999
"""

import pandas as pd
import numpy as np

#mesure time of execution
import time
start = time.clock()

input_file_path = r'C:\Users\56999\Documents\Tencent Files\569994498\FileRecv\logit2.csv'
output_file_path = r'C:\Users\56999\Documents\Tencent Files\569994498\FileRecv\logit_output.csv'
df = pd.read_csv(input_file_path,encoding = "utf-8")
#df = pd.read_csv(input_file_path,encoding = "GBK")
x_columns = [x for x in df.columns if x not in 'gbflag']
X = df[x_columns]
y = df['gbflag']

#calculate the bin value with equal number of obs
def equal_num_bin(N, m):
    sep = (N.size/float(m))*np.arange(1,m+1)
    bins = sep.searchsorted(np.arange(N.size))
    N_sorted = np.sort(N)
    N_binned = N_sorted
    N_binned[0] = bins[0]
    #to deal with multiple repeated values, put them in the same bin
    for i in range(1,N_sorted.size): 
        if N_sorted[i] == N_sorted[i-1]:
            N_binned[i] = N_binned[i-1]
        else:
            N_binned[i] = bins[i]
    #argsort here is to reform the array by original index
    return N_binned[N.argsort().argsort()]

#for every numeric column, calculate the bin and woe value
def bin_woe_num(var,varname,y,n_good,n_bad,class_num = 50):
#    var_gbflag = pd.DataFrame([var,y]).transpose()
    binned = var.replace([-9999,0], [-2,-1])
#    var = var.replace(0, -1)
    to_bin = binned.loc[~binned[varname].isin([-2,-1])]
    #if the bin array is empty, skip this step
    if to_bin.size:
        idx_to_bin = binned.index[~binned[varname].isin([-2,-1])].tolist()
        bin_arr = equal_num_bin(np.array(to_bin[varname]),class_num)
        i = 0
        for idx in idx_to_bin:
            binned.loc[idx]=bin_arr[i]
            i += 1
    bin_list = set(binned[varname])
    # merge variable and y to get woe
#    var_gbflag = pd.concat([binned,y],1)
#    woe_list = []
#    str_to_print = ''
#    voi_list = []
#    for binn in bin_list:
#        #calculate woe
#        gb_list = var_gbflag.loc[var_gbflag[varname]==binn]['gbflag']
#        n_good_in_bin = len(gb_list.loc[gb_list == 1])
#        n_bad_in_bin = len(gb_list.loc[gb_list == 0])
#        p_good = n_good and n_good_in_bin / n_good or 0
#        p_bad = n_bad and n_bad_in_bin / n_bad or 0
#        woe = np.log((p_good and p_good or 0.000001)/(p_bad and p_bad or 0.000001))
#        woe_list.append(woe)
#        #calculate voi
#        voi = (p_good - p_bad) * woe
#        voi_list.append(voi)
#    voi_sum = sum(voi_list)
#    str_to_print = 'VOI of ' + varname + ' is: ' + str(round(voi_sum,6))
#    print(str_to_print)
#    woed = binned.replace(bin_list, woe_list)
#    return [binned, woed, voi_sum]
    return [binned]
    
#for string columns, calculate the bin and woe value
def bin_woe_str(var,varname,y,n_good,n_bad):
    var_list = set(var[varname])
    bin_list = np.arange(0,len(var_list))
    binned = var.replace(var_list, bin_list)
#    woe_list = []
#    var_gbflag = pd.concat([binned,y],1)
#    str_to_print = ''
#    voi_list = []
#    for binn in bin_list:
#        #calculate woe
#        gb_list = var_gbflag.loc[var_gbflag[varname]==binn]['gbflag']
#        n_good_in_bin = len(gb_list.loc[gb_list == 1])
#        n_bad_in_bin = len(gb_list.loc[gb_list == 0])
#        p_good = n_good and n_good_in_bin / n_good or 0
#        p_bad = n_bad and n_bad_in_bin / n_bad or 0
#        woe = np.log((p_good and p_good or 0.000001)/(p_bad and p_bad or 0.000001))
#        woe_list.append(woe)
#        #calculate voi
#        voi = (p_good - p_bad) * woe
#        voi_list.append(voi)
#    voi_sum = sum(voi_list)
#    str_to_print = 'VOI of ' + varname + ' is: ' + str(round(voi_sum,6))
#    print(str_to_print)
#    woed = binned.replace(bin_list, woe_list)
#    return [binned, woed, voi_sum]
    return [binned]
    
X_bin = pd.DataFrame()
X_woe = pd.DataFrame()
total_num = len(y)
n_good = len(y.loc[y == 1])
n_bad = total_num - n_good
X_voi = pd.DataFrame(columns = ['var','voi'])

#for every feature in the data set, do this to bin and woe
for varname in X.columns:
#   in case if there is only one value
    if len(set(X[varname])) > 1:
        if X[varname].dtypes in ['int64', 'float64']:
            result = bin_woe_num(pd.DataFrame(X[varname]),varname,y,n_good,n_bad,10)
            X_bin[varname] = result[0]
#            X_woe[varname] = result[1]
#            X_voi = X_voi.append(pd.DataFrame([[varname, result[2]]],columns = ['var','voi']))
        elif X[varname].dtypes in ['object', 'string']:
            result = bin_woe_str(pd.DataFrame(X[varname]),varname,y,n_good,n_bad)
            X_bin[varname] = result[0]
#            X_woe[varname] = result[1]
#            X_voi = X_voi.append(pd.DataFrame([[varname, result[2]]],columns = ['var','voi']))
        else:
            #print('N/A! N/A!')
            pass
#
#woe_gbflag = pd.concat([X_woe,y],1)
#woe_gbflag.to_csv(output_file_path)
X_bin.to_csv(r'C:\Users\56999\Documents\Tencent Files\569994498\FileRecv\logit_bin.csv')

#print time of execution
elapsed = (time.clock() - start)
print("Time used:",elapsed)

##sort the table of voi to get the first 65%
#X_voi_sorted = X_voi.sort_values('voi',ascending = 0).reset_index(drop = 1)
#X_voi_selected = X_voi_sorted[0:int(len(X_voi_sorted)*0.65)]
#X_woe_voi_selected = X_woe[X_voi_selected.iloc[:,0]].copy()
#print(str(len(X_woe_voi_selected.columns))+" features are selected by first 65% voi")
#woe_gbflag = pd.concat([X_woe_voi_selected,y],1)
#woe_gbflag.to_csv(output_file_path)
#
##select features by packages provided by sk learn
#from sklearn import feature_selection as fs
#
#chi_score = fs.chi2(X_woe+100,y)
## select function in sk learn doesn't check p values of chi square test
#X_woe_chi_selected = fs.SelectPercentile(fs.chi2, 65).fit_transform(X_woe+100,y)
#X_woe_chi_selected = X_woe_chi_selected - 100
#
#X_woe_variance_selected = fs.VarianceThreshold(threshold=(0.05)).fit_transform(X_woe)
#print(str(len(X_woe_variance_selected[0]))+" features are selected by variance >= 0.05")
#
##RFE should be set with the chosen estimator