class ftf():
    def __init__(self, slots_per_cycle, bmin, bmax, b0):
        self.Bcap = bmax
        self.bmin = bmin
        self.B0 = b0

    def allocate(self, eh_pred):
        env_r = [sum(eh_pred[:i]) for i in range(len(eh_pred) + 1)]
        env_l = [i + self.B0 - self.Bcap for i in env_r]
        env_u = [i + self.B0 - self.bmin for i in env_r]
        result_i = []
        result_e = []

        i_start = 0
        i_end = len(env_l) - 1
        en_start = 0
        en_end = max(env_r[-1], env_l[-1])
        i = 0
        while i < len(env_l) - 1:
            (a, b) = ipsearch(i_start, i_end, en_start, en_end, env_l, env_u)
            result_i.append(a)
            result_e.append(b)
            i_start = a
            en_start = b
            i = i_start
            i = i + 1

        result = []
        start_value = 0
        k = (result_e[0]) / (result_i[0])
        for i in range(0, result_i[0]):
            value = start_value + k * (i - 0)
            result.append(value)
        result.append(result_e[0])
        start_value = result_e[0]
        if len(result_i) > 1:
            for i in range(1, len(result_i)):
                for j in range(result_i[i - 1] + 1, result_i[i]):
                    k = (result_e[i] - result_e[i - 1]) / (result_i[i] - result_i[i - 1]);
                    value = start_value + k * (j - result_i[i - 1])
                    result.append(value)
                result.append(result_e[i])
                start_value = result_e[i]
        allocated = []
        for i in range(1, len(result)):
            allocated.append(result[i] - result[i - 1])
        return allocated
        
def ipsearch(i_start, i_end, en_start, en_end, env_l, env_u):
    first_flag = 0  # 0是没有交点；1是首先与下界有交点；2是首先与上界有交点
    temp = [] # 存储相交的那一段的横坐标值
    for i in range(i_start, i_end + 1):
        k0 = (en_end - en_start) / (i_end - i_start)
        temp_f = k0 * (i - i_start) + en_start
        if (temp_f < env_l[i]) and first_flag == 0:
            temp.append(i)
            print("1 Find rgp x-axis:",temp)
            first_flag = 1
            if i == i_end:
                return (i_end, en_end)
            if i == i_start+1:
                return (i,env_l[i])
        elif (temp_f > env_u[i]) and first_flag == 0:
            temp.append(i)
            print("2 Find rgp x-axis:", temp)
            if i == i_end:
                return (i_end, en_end)
            if i == i_start+1:
                return (i,env_u[i])
            first_flag = 2
        elif (temp_f > env_u[i]) and first_flag == 1:
            temp.append(i)
            print("3 Find rgp x-axis:", temp)
            # 开始找切点
            temp_tgp_x = []  # 存储相交这一段内的所有切点的横坐标值，用于寻找最优切点
            temp_tgp_y = []  # 存储相交这一段内的所有切点的纵坐标值，用于寻找最优切点
            for item in range(temp[0], temp[1]):
                k = (env_l[item] - en_start) / (item - i_start)
                if env_l[item] - k > env_l[item - 1] and env_l[item] + k > env_l[item + 1]:
                    temp_tgp_x.append(item)
                    temp_tgp_y.append(env_l[item])
            if len(temp_tgp_x) > 0:
                # 寻找最优切点的程序
                k_tgp = 0
                i_tgp = 0
                en_tgp = 0
                for j in range(len(temp_tgp_x)):
                    k_temp_tgp = (temp_tgp_y[j] - en_start) / (temp_tgp_x[j] - i_start)
                    if k_temp_tgp > k_tgp:  # 与下届相交找斜率最大的切点
                        k_tgp = k_temp_tgp
                        i_tgp = temp_tgp_x[j]
                        en_tgp = temp_tgp_y[j]
                (i_tgp, en_tgp) = ipsearch(i_start, i_tgp, en_start, en_tgp, env_l, env_u)
                return (i_tgp, en_tgp)
            first_flag = 0
            temp = []
        elif (temp_f < env_l[i]) and first_flag == 2:
            temp.append(i)
            print("4 Find rgp x-axis:", temp)
            # TODO开始找切点
            temp_tgp_x = []  # 存储相交这一段内的所有切点的横坐标值，用于寻找最优切点
            temp_tgp_y = []  # 存储相交这一段内的所有切点的纵坐标值，用于寻找最优切点
            for item in range(temp[0], temp[1]):
                k = (env_u[item] - en_start) / (item - i_start);
                if env_u[item] - k < env_u[item - 1] and env_u[item] + k < env_u[item + 1]:
                    temp_tgp_x.append(item)
                    temp_tgp_y.append(env_u[item])
            if len(temp_tgp_x) > 0:
                k_tgp = (temp_tgp_y[0] - en_start) / (temp_tgp_x[0] - i_start)
                i_tgp = temp_tgp_x[0]
                en_tgp = temp_tgp_y[0]
                for j in range(1, len(temp_tgp_x)):
                    k_temp_tgp = (temp_tgp_y[j] - en_start) / (temp_tgp_x[j] - i_start)
                    if k_temp_tgp < k_tgp:  # 与下届相交找斜率最大的切点
                        k_tgp = k_temp_tgp
                        i_tgp = temp_tgp_x[j]
                        en_tgp = temp_tgp_y[j]
                (i_tgp, en_tgp) = ipsearch(i_start, i_tgp, en_start, en_tgp, env_l, env_u);
                return (i_tgp, en_tgp)
            first_flag = 0
            temp = []
        elif (i == i_end) and (first_flag == 0):  # TODO需要增加数据到尽头的处理
            return (i_end, en_end)
        elif i == i_end and first_flag == 1:  # TODO需要增加数据到尽头的处理
            temp.append(i)
            print("5 Find rgp x-axis:", temp)
            temp_tgp_x = []  # 存储相交这一段内的所有切点的横坐标值，用于寻找最优切点
            temp_tgp_y = []  # 存储相交这一段内的所有切点的纵坐标值，用于寻找最优切点
            #k_base = (env_l[i_end] - en_start) / (i_end - i_start)
            for item in range(temp[0], temp[1]):
                k = (env_l[item] - en_start) / (item - i_start)
                if env_l[item] - k > env_l[item - 1] and env_l[item] + k > env_l[item + 1]:
                    #if k <k_base:
                    temp_tgp_x.append(item)
                    temp_tgp_y.append(env_l[item])
            if len(temp_tgp_x) > 0:
                # 寻找最优切点的程序
                k_tgp = 0
                i_tgp = 0
                en_tgp = 0
                for j in range(len(temp_tgp_x)):
                    k_temp_tgp = (temp_tgp_y[j] - en_start) / (temp_tgp_x[j] - i_start)
                    if k_temp_tgp > k_tgp:  # 与下届相交找斜率最大的切点
                        k_tgp = k_temp_tgp
                        i_tgp = temp_tgp_x[j]
                        en_tgp = temp_tgp_y[j]
                print("asdf:",i_start,i_tgp,en_start,en_tgp)
                #(i_tgp, en_tgp) = ipsearch(i_start, i_tgp, en_start, en_tgp, env_l, env_u)
                (i_tgp, en_tgp) = ipsearch(i_start, i_tgp, en_start, en_tgp, env_l, env_u)
                return (i_tgp, en_tgp)
            if len(temp_tgp_x) ==0:
                return (temp[1], env_l[temp[1]])
            first_flag = 0
            temp = []
        elif i == i_end and first_flag == 2:  # TODO需要增加数据到尽头的处理
            temp.append(i)
            print("6 Find rgp x-axis:", temp)
            temp_tgp_x = []  # 存储相交这一段内的所有切点的横坐标值，用于寻找最优切点
            temp_tgp_y = []  # 存储相交这一段内的所有切点的纵坐标值，用于寻找最优切点
            for item in range(temp[0], temp[1]):
                k = (env_u[item] - en_start) / (item - i_start);
                if env_u[item] - k < env_u[item - 1] and env_u[item] + k < env_u[item + 1]:
                    temp_tgp_x.append(item)
                    temp_tgp_y.append(env_u[item])
            if len(temp_tgp_x) > 0:
                k_tgp = (temp_tgp_y[0] - en_start) / (temp_tgp_x[0] - i_start)
                i_tgp = temp_tgp_x[0]
                en_tgp = temp_tgp_y[0]
                for j in range(1, len(temp_tgp_x)):
                    k_temp_tgp = (temp_tgp_y[j] - en_start) / (temp_tgp_x[j] - i_start)
                    if k_temp_tgp < k_tgp:  # 与下届相交找斜率最大的切点
                        k_tgp = k_temp_tgp
                        i_tgp = temp_tgp_x[j]
                        en_tgp = temp_tgp_y[j]
                print("x-start:",i_start,"x-end:",i_end,"y-start:",en_start,"y-end:",en_tgp)
                (i_tgp, en_tgp) = ipsearch(i_start, i_tgp, en_start, en_tgp, env_l, env_u)
                return (i_tgp, en_tgp)
            if len(temp_tgp_x) ==0:
                return (temp[1], env_u[temp[1]])
            first_flag = 0
            temp = []
        else:
            pass
