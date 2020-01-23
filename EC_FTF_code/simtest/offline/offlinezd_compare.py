import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from EHWSN.algorithms import buchli
from EHWSN.algorithms import gorlatova
from EHWSN.algorithms import mallec
from EHWSN.algorithms import fastest
import datetime


#Load Dataset
dataframe = pd.read_csv("../../data/eh_3min.csv")
divstring = "zhendong/"
data = dataframe['value']


bmin = 196    # half-way threshold
bmax = 756    # energy stored in 2AA batteries (3Ah, 3V), in Joules
b0 = 378
#slots_per_cycle = 50


for slots_per_cycle in range(50,250,50):
    print("current cycle:",slots_per_cycle)
    cycle=data[100:100+slots_per_cycle].reset_index(drop=True)
    #buchli算法 eplison = 0.01
    starttime = datetime.datetime.now()
    alg_buchli= buchli.buchli(0.01, slots_per_cycle, b0, bmin, bmax)
    (allocated1 ,f,l,u)= alg_buchli.allocate(cycle)
    endtime = datetime.datetime.now()
    temp_time = endtime - starttime
    final_b0 = b0+sum(cycle)-sum(allocated1)
    #plt.plot(allocated1)
    #plt.plot(cycle)
    fair_utility = 0
    for item in allocated1:
        fair_utility = fair_utility + math.log(1+item)
    result_buchli_0_01 = divstring+"result_buchli_0_01"+"_"+str(slots_per_cycle)+""+".txt"
    f = open(result_buchli_0_01, 'w')
    f.write("fair_utility:" + str(fair_utility))
    f.write("\n")
    f.write("final_b0:" + str(final_b0))
    f.write("\n")
    f.write("alloc:"+str(allocated1))
    f.write("\n")
    f.write("time:"+str(temp_time))
    f.flush()
    f.close()
    print("...buchli eplison = 0.01 finish.")

    #buchli算法 eplison = 0.1
    starttime = datetime.datetime.now()
    alg_buchli= buchli.buchli(0.1, slots_per_cycle, b0, bmin, bmax)
    (allocated2 ,f,l,u)= alg_buchli.allocate(cycle)
    endtime = datetime.datetime.now()
    temp_time = endtime - starttime
    final_b0 = b0 + sum(cycle) - sum(allocated2)
    fair_utility = 0
    for item in allocated2:
        fair_utility = fair_utility + math.log(1+item)
    result_buchli_0_1 = divstring+"result_buchli_0_1"+"_"+str(slots_per_cycle)+""+".txt"
    f = open(result_buchli_0_1, 'w')
    f.write("fair_utility:" + str(fair_utility))
    f.write("\n")
    f.write("final_b0:" + str(final_b0))
    f.write("\n")
    f.write("alloc:"+str(allocated2))
    f.write("\n")
    f.write("time:"+str(temp_time))
    f.flush()
    f.close()

    print("...buchli eplison = 0.1 finish.")

    #buchli算法 eplison = 1
    starttime = datetime.datetime.now()
    alg_buchli= buchli.buchli(1, slots_per_cycle, b0, bmin, bmax)
    (allocated3 ,f,l,u)= alg_buchli.allocate(cycle)
    endtime = datetime.datetime.now()
    temp_time = endtime - starttime
    fair_utility = 0
    # print(allocated3)
    for item in allocated3:
        fair_utility = fair_utility + math.log(1+item)
    result_buchli_1 = divstring+"result_buchli_1"+"_"+str(slots_per_cycle)+""+".txt"
    f = open(result_buchli_1, 'w')
    f.write("fair_utility:" + str(fair_utility))
    f.write("\n")
    f.write("alloc:"+str(allocated3))
    f.write("\n")
    f.write("time:"+str(temp_time))
    f.flush()
    f.close()
    print("...buchli eplison = 1 finish.")

    #gorlatova算法
    starttime = datetime.datetime.now()
    alg_glva = gorlatova.Gorlatova(slots_per_cycle, bmin)
    allocated4 = alg_glva.allocate(cycle,b0)
    endtime = datetime.datetime.now()
    temp_time = endtime - starttime
    final_b0 = b0 + sum(cycle) - sum(allocated4)
    fair_utility = 0
    for item in allocated4:
        fair_utility = fair_utility + math.log(1+item)
    result_glva = divstring+"result_glva" + "_" + str(slots_per_cycle) + "" + ".txt"
    f = open(result_glva, 'w')
    f.write("fair_utility:" + str(fair_utility))
    f.write("\n")
    f.write("final_b0:" + str(final_b0))
    f.write("\n")
    f.write("alloc:" + str(allocated4))
    f.write("\n")
    f.write("time:"+str(temp_time))
    f.flush()
    f.close()
    print("...glva finish.")

    #fastest算法
    starttime = datetime.datetime.now()
    alg_fast = fastest.fastest(slots_per_cycle, bmin, bmax, b0)
    allocated5 = alg_fast.allocate(cycle)
    endtime = datetime.datetime.now()
    temp_time = endtime - starttime
    final_b0 = b0 + sum(cycle) - sum(allocated5)
    fair_utility = 0
    for item in allocated5:
        fair_utility = fair_utility + math.log(1+item)
    result_fast = divstring+"result_fast" + "_" + str(slots_per_cycle) + "" + ".txt"
    f = open(result_fast, 'w')
    f.write("fair_utility:" + str(fair_utility))
    f.write("\n")
    f.write("final_b0:" + str(final_b0))
    f.write("\n")
    f.write("alloc:" + str(allocated5))
    f.write("\n")
    f.write("time:"+str(temp_time))
    f.flush()
    f.close()
    print("...fast finish.")

plt.show()
print("All cycle has been finished.")
