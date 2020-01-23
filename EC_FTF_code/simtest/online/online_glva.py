import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import datetime
import os
from keras.models import Sequential, load_model
from algorithms import eh_constants
from algorithms import gorlatova
#Load Dataset
#Load Dataset
source_list = ["eh_guiyi"]
divstring = "results/"

for file_raw_name in source_list:
    filename = '../../data/'+file_raw_name+'.csv'
    split = 0.50
    seq_len = 308
    dataframe = pd.read_csv(filename)
    i_split = int(len(dataframe) * split)
    data_train = dataframe['value'].values[:i_split]
    data_test = dataframe['value'].values[i_split:]
    len_train = len(data_train)
    len_test = len(data_test)
    print(len_train)
    print(len_test)

    #model_path = os.path.join('../../saved_models', '03042019-085938-e10.h5')
    model_path = os.path.join('../../saved_models', file_raw_name+'.h5')
    mymodel = load_model(model_path)
    result_all = []
    real_all = []
    bmin = 196  # half-way threshold
    bmax = 756  # energy stored in 2AA batteries (3Ah, 3V), in Joules
    b0 = 378
    allocated = []
    all_cycle = []
    last = 0
    count = 0
    last_allocate = []
    last_cycle = []
    last_b0 = 0
    overuse_errors = 0
    waste_errors = 0

    waste_energy = []

    range_start = 0
    range_end = 3000
    #TODO做成三个大list，一个原始数据，一个预测数据，一个分配的数据，
    # 然后在循环过程中右移指针，达成我们的错误回溯目的
    #目前来看错误回溯有一定效果
    all_pred_cycle = [0]*len_test
    all_nav_cycle = [0]*len_test
    all_alloc_cycle = [0]*len_test
    all_b0 = [0]*len_test

    for i in range(range_start,range_end):
        windows = data_test[i: i + seq_len]
        x = []
        y = []
        data_x = []
        data_y = []
        for j in range(6):
            x.append(windows[j * 44:(j + 1) * 44])
        data_x.append(x)
        data_y = windows[6 * 44:7 * 44]
        predicted = mymodel.predict(np.array(data_x))
        result = np.array(predicted)
        result = result.reshape(-1, 1)

        pred_cycle = [(item + 0.6) * 7.58 for item in result]
        nav_cycle = [(item + 0.6) * 7.58 for item in data_y]

        pred_cycle_2 = []
        all_b0[i] = b0
        for item in pred_cycle:
            if item >= 0:
                pred_cycle_2.append(float(item))
            else:
                pred_cycle_2.append(0)

        slots_per_cycle = 44
        #start buchli
        starttime = datetime.datetime.now()
        print("B0 of this cycle:",b0)
        alg_glva = gorlatova.Gorlatova(slots_per_cycle, bmin)
        allocated1 = alg_glva.allocate(nav_cycle, b0)

        # 统计浪费和不足
        if allocated1[0] >eh_constants.emax:
            allocated1[0] = eh_constants.emax
        elif allocated1[0] < eh_constants.emin:
            allocated1[0] = eh_constants.emin
        else:
            pass
        b0_temp = b0 + nav_cycle[0] - allocated1[0]

        if (b0_temp<bmin):
            overuse_errors=overuse_errors+1
            allocated1[0] = allocated1[0]-(bmin-b0_temp)
            b0 = bmin

        elif (b0_temp>bmax):
            waste_errors = waste_errors+1
            waste_energy.append(b0_temp-bmax) #浪费的能量
            b0 = bmax

        else:
            b0 = b0 + nav_cycle[0] - allocated1[0]

        allocated.append(allocated1[0])
        all_cycle.append(nav_cycle[0])


        endtime = datetime.datetime.now()
        print("energy harvseted of this slot:",nav_cycle[0])
        print("energy consumed of this slot:", allocated1[0])
        print ("fast process time:",endtime - starttime)

    fair_utility = 0
    for item in allocated:
        fair_utility = fair_utility + math.log(1+item)
    print("fair_utility:",fair_utility)
    print("overuse errors:",overuse_errors)
    print("waste errors:",waste_errors)
    print("waste energy:",sum(waste_energy))
    print("Final B0:",b0)
    result_filepath = divstring+"glva_"+file_raw_name+"_"+str(range_start)+"_"+str(range_end)+".txt"
    f = open(result_filepath,'w')
    f.write("fair_utility:"+str(fair_utility))
    f.write("\n")
    f.write("final_b0:"+str(b0))
    f.write("\n")
    f.write("overuse_errors:"+str(overuse_errors))
    f.write("\n")
    f.write("waste_errors:"+str(waste_errors))
    f.write("\n")
    f.write("waste_energy:"+str(sum(waste_energy)))
    f.write("\n")
    f.write("allocated:"+str(allocated))
    f.write("\n")
    f.write("all_cycle:"+str(all_cycle))
    f.write("\n")
    f.flush()
    f.close()
    plt.figure(1)
    plt.figure(1, figsize=(15, 10))
    plt.plot(all_cycle,color='b',label='Energy harvested')
    plt.plot(allocated,color='r',label='Energy consumed')
    font1={
        'family':'Times New Roman',
        'weight':'normal',
        'size':23
    }
    plt.xlabel("Time slot t",font1)
    plt.ylabel("Energy Amount /J",font1)
    plt.legend(prop=font1)
    plt.figure(2)
    plt.plot(all_b0)
    plt.show()