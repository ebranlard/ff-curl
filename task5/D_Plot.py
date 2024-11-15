
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os
# Local 
import weio
cases=[
# 'task5_sims_old/yaw_0040_modwake1.dat',
'task5_sims/yaw_0020_modwake1.fstf',
'task5_sims/yaw_0020_modwake2.fstf'
        ]

cases2=[ 'Polar', 'Curl' ]


D=126
pad=0.12
size="4%"
U0=7.9

matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['axes.labelsize']  = 14 
matplotlib.rcParams['axes.titlesize']  = 14
matplotlib.rcParams['legend.fontsize'] = 14




fig,axes = plt.subplots(2,2, sharex=True, figsize=(12.8,3.5)) # (6.4,4.8)
fig.subplots_adjust(left=0.043, right=0.96, top=0.921, bottom=0.13, hspace=0.30, wspace=0.20)

def plot(snap=30, avg=False):


    for ic,(c,cs) in enumerate(zip(cases,cases2)):
        basedir = os.path.dirname(c)
        basename = os.path.basename(c)
        base = os.path.splitext(basename)[0]
        print(basedir, base)

        if avg:
            n=0
            for i in np.arange(snap):
                vtk = weio.read(os.path.join(basedir,'vtk_ff/{}.Low.DisXY1.{:04d}.vtk'.format(base,i)))
                print('>>>', os.path.join(basedir,'vtk_ff/{}.Low.DisXY1.{:04d}.vtk'.format(base,i)))
                if i==0:
                    U = vtk.point_data_grid['Velocity']
                else:
                    U += vtk.point_data_grid['Velocity']
                n+=1
            U /= snap
            print('>>> snap, ', snap,n)
        else:
            vtk = weio.read(os.path.join(basedir,'vtk_ff/{}.Low.DisXY1.{:04d}.vtk'.format(base,snap)))
            U = vtk.point_data_grid['Velocity']

        U2 = U[:, :, 0, 0].T
        print(U.shape, np.min(U2), np.max(U2) )
        
        x  = vtk.xp_grid
        y  = vtk.yp_grid
        z  = vtk.zp_grid

        if avg:
            ax =axes[1,ic] 
        else:
            ax =axes[0,ic] 
        #levels=np.linspace(3,11,30)/U0
        levels=np.linspace(0.35,1.2,30)
        im = ax.contourf((x-100)/D,y/D, U2/U0, levels=levels,  vmin=np.min(levels), vmax=np.max(levels)) 
        #ax.set_aspect('equal', adjustable='box')
        ax.tick_params(direction='in', top=True, right=True, which='both')
        ax.set_aspect('equal')
        if avg:
            ax.set_title(cs + ' - time averaged')
        else:
            ax.set_title(cs + r' - $t={:}$s'.format(snap*9)
    #     ax.set_xlim([0,1500])
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size=size, pad=pad)   
        cb = fig.colorbar(im, cax=cax)
        cb.set_ticks([0.35,0.6,0.8,1.0,1.2])
#         cb.set_clim([4,10])


plot(snap=211, avg=False)
plot(snap=411, avg=True)
axes[0,0].set_ylabel('y/D [-]')
axes[1,0].set_ylabel('y/D [-]')
axes[1,0].set_xlabel('x/D [-]')
axes[1,1].set_xlabel('x/D [-]')


# ax.set_xlabel('')
# ax.set_ylabel('')
# ax.legend()
# fig.savefig('ConvectionModels.png')
fig.savefig('figs/task5_contours.pdf')
fig.savefig('figs/task5_contours.png')
plt.show()


if __name__ == '__main__':
    pass
