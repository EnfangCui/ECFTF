# minimum and maximum battery thresholds
#bmin = 16200    # half-way threshold
#bmax = 32400    # energy stored in 2AA batteries (3Ah, 3V), in Joules
import matplotlib.pyplot as plt

class buchli():
    def __init__(self, epsilon, slots_per_cycle, b0, bmin, bmax):
        self.Bcap = bmax
        self.slots = slots_per_cycle
        self.alloc = [0 for i in range(self.slots)]
        self.epsilon = epsilon
        self.eh_pred = None
        self.B0 = b0
        self.bmin = bmin

    def allocate(self, eh_pred):
        self.eh_pred = eh_pred
        # compute envelope
        env_r = [sum(eh_pred[:i]) for i in range(self.slots+1)]
        env_l = [i+ self.B0 - self.Bcap for i in env_r]
        env_u = [i+ self.B0 - self.bmin for i in env_r]
        # initialise f as avg between lower and upper
        f = [(env_l[i]+env_u[i])/2 for i in range(self.slots+1)]
        f[0] = 0
        f[-1] = max(env_r[-1],env_l[-1])  # for energy-neutral operation
        for i in range(len(f)):
            if f[i]<0:
                f[i]=0
        # plt.plot(env_l)
        # plt.plot(env_u)
        # plt.plot(f)
        # adjust f until reaches optimum
        while True:
            diff_max = 0
            temp = max(min(f[0], self.Bcap), 0)
            if abs(f[0] - temp) > diff_max: diff_max = abs(f[0] - temp)
            f[0] = temp
            for t in range(1, len(eh_pred)):
                temp = (f[t-1] + f[t+1])/2
                temp = max(min(temp, env_u[t]), env_l[t])
                if abs(f[t]-temp) > diff_max: diff_max = abs(f[t]-temp)
                f[t] = temp
            temp = f[0] + env_l[-1]
            if diff_max < self.epsilon: break
        # plt.plot(f)
        # plt.show()
        self.alloc = [f[t+1]-f[t] for t in range(len(f)-1)]
        self.batt_pred = [env_u[t] - f[t] for t in range(self.slots+1)]
        return (self.alloc,f,env_l,env_u)

