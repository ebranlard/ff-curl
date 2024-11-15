import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# Local 
import weio

from C_Plot import plot

work_dir1  = 'task5_sims_old/'
work_dir2 = 'task5_sims/'   

YAW = np.arange(-40,41,5)

PP = np.zeros((2,len(YAW)))
PC = np.zeros((2,len(YAW)))

for ModWake in [2,1]:
    for i,(yaw) in enumerate(YAW):
        basename = 'yaw_{:04d}_modwake{:d}'.format(yaw,ModWake)
        print(basename, end='')
        if ModWake==1:
            filebase = os.path.join(work_dir1, basename)
        else:
            filebase = os.path.join(work_dir2, basename)
        try:
            t1 = weio.read(filebase+'.T1.out') .toDataFrame()
            t2 = weio.read(filebase+'.T2.out') .toDataFrame()
        except:
            print('[WARN] >>> Missing')
            t1=None
            t2=None
            continue
    
        tmax = t1['Time_[s]'].values[-1]
        if tmax<150:
            print('[WARN] >>> unfin. ', tmax)
            continue
        elif tmax<3698:
            print('[WARN] >>> unfin. ', tmax)
        else:
            print('[ OK ]')
        t1=t1[ t1['Time_[s]']>150].mean()
        t2=t2[ t2['Time_[s]']>150].mean()
        if ModWake==1:
            PP[0,i] = t1['GenPwr_[kW]']/1000
            PP[1,i] = t2['GenPwr_[kW]']/1000
        else:
            PC[0,i] = t1['GenPwr_[kW]']/1000
            PC[1,i] = t2['GenPwr_[kW]']/1000

print(PC)
print(PP)

plot(YAW, PP, 'Polar_({:})'.format(work_dir1))
plot(YAW, PC, 'Curl_({:})'.format(work_dir2))

plt.show()

np.savez('Powers_{}.npz'.format(work_dir2.replace('/','')), YAW=YAW, PC=PC, PP=PP)

