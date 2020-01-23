import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from algorithms import ftf
import datetime


#Load Dataset
dataframe = pd.read_csv("../../data/eh_2min.csv")
data = dataframe['value']
print(len(data))

bmin = 196    # half-way threshold
bmax = 756    # energy stored in 2AA batteries (3Ah, 3V), in Joules
b0 = 378

cycle_num = 0
range_start = 0
range_end = 3000

for slots_per_cycle in range(50,99,50):
    print("current cycle:", slots_per_cycle)
    allocated=[]
    b0=378
    all_time = datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
    print("init all_time:",all_time)
    for i in range(range_start,range_end-slots_per_cycle):
        nav_cycle = data[i: i + slots_per_cycle].reset_index(drop=True)
        # cycle=data[0:slots_per_cycle].reset_index(drop=True)
        # cycle=data[i*slots_per_cycle:(i+1)*slots_per_cycle].reset_index(drop=True)
        #buchli算法 eplison = 0.01
        starttime = datetime.datetime.now()
        # alg_buchli= buchli.buchli(0.01, slots_per_cycle, b0, bmin, bmax)
        # (allocated1 ,f,l,u)= alg_buchli.allocate(nav_cycle)

        alg_ftf = ftf.ftf(slots_per_cycle, bmin, bmax, b0)
        allocated1 = alg_ftf.allocate(nav_cycle)

        endtime = datetime.datetime.now()
        temp_time = endtime - starttime
        all_time = all_time+temp_time
        b0 = b0 + nav_cycle[0] - allocated1[0]
        allocated.append(allocated1[0])

    nav_cycle = data[range_end-slots_per_cycle:range_end].reset_index(drop=True)
    # print("nav cycle:",nav_cycle)
    starttime = datetime.datetime.now()
    # alg_buchli= buchli.buchli(0.01, slots_per_cycle, b0, bmin, bmax)
    # (allocated1 ,f,l,u)= alg_buchli.allocate(nav_cycle)
    print(len(nav_cycle))
    alg_ftf = ftf.ftf(slots_per_cycle, bmin, bmax, b0)
    allocated1 = alg_ftf.allocate(nav_cycle)

    endtime = datetime.datetime.now()
    temp_time = endtime - starttime
    all_time = all_time + temp_time
    b0 = b0 + sum(nav_cycle) - sum(allocated1)
    allocated.extend(allocated1)
    #plt.plot(allocated1)
    #plt.plot(cycle)

    avg_time = (all_time.microseconds/1000000+all_time.seconds)/(range_end-slots_per_cycle+1)
    print("average time:",avg_time)
    fair_utility = 0
    for item in allocated:
        fair_utility = fair_utility + math.log(1+item)
    print("Fail utility:",fair_utility)
    print("Final B0:",b0)
    # plt.figure()
    # plt.plot(data[range_start:range_end])
    # plt.plot(allocated)
    # plt.show()
    result_ftf = "zhendong_multi/"+"result_fast_multi" + "_" + str(slots_per_cycle) + "" + ".txt"
    #TODO 求平均时间
    f = open(result_ftf, 'w')
    f.write("fair_utility:" + str(fair_utility))
    f.write("\n")
    f.write("final_b0:" + str(b0))
    f.write("\n")
    f.write("time:" + str(avg_time))
    f.write("\n")
    f.write("alloc:"+str(allocated))
    f.flush()
    f.close()
print("...ftf finish.")


