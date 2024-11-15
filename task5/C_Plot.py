import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
# Local 
import weio


matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['axes.labelsize']  = 15 
matplotlib.rcParams['axes.titlesize']  = 16
matplotlib.rcParams['legend.fontsize'] = 14


def plot(yaw, PP, title):
    i0 = np.argmin(np.abs(yaw))
    c0 = np.array([104,170,207])/255.
    c1 = np.array([241,137,97])/255.
    print(yaw[i0])
    fig,ax = plt.subplots(1, 1, sharey=False, figsize=(6.4,4.0)) # (6.4,4.8)
    fig.subplots_adjust(left=0.093, right=0.985, top=0.936, bottom=0.143, hspace=0.20, wspace=0.20)
    # ax.plot(yaw, PP[0,:], label='T1 polar')
    # # ax.plot(yaw, PP[0,:] +PP[1,:], label='T2 polar')
    # ax.plot(yaw, PC[0,:], label='T1 curl')
    # ax.plot(yaw, PC[0,:]+PC[1,:], label='T2 curl')
    PP[np.isnan(PP)]=0
    print(PP)

    width=4
    ax.bar(yaw, PP[0,:], width, label='Turbine 1', color=c0 )
    ax.bar(yaw, PP[1,:], width, label='Turbine 2', color=c1, bottom=PP[0,:])

    ax.plot([-43,43], np.array([0,0])+PP[0,i0]          ,'--', c=c0,  lw=1.5)
    ax.plot([-43,43], np.array([0,0])+PP[0,i0]+PP[1,i0],'k--',        lw=1.5)

    Ptot  = PP[0,:]+PP[1,:]
    Pincr = (Ptot[:]-Ptot[i0])/Ptot[i0]*100
    for i,(p,y) in enumerate(zip(Pincr,yaw)):
        ax.text(y,0.25,'{:+.1f}%'.format(p), rotation=90, ha='center', va='bottom')

    ax.set_xlabel('Yaw [deg]')

    ax.tick_params(direction='in', top=True, right=True, which='both')
    ax.set_xlim([-43,43])
    ax.set_ylim([0,3.2])
    ax.set_xticks(yaw)
    ax.set_xticklabels(ax.get_xticks(), rotation = 90)
    ax.set_ylabel('Power [MW]')
    ax.legend(ncol=2, frameon=False, loc='upper right')
    #ax.legend(fontsize=12, ncol=2, handletextpad=0.2, borderpad=0.5, labelspacing=0.6, columnspacing=0.9, handlelength=1.3,  frameon=False, bbox_to_anchor=(-0.0,0.4722/scale), bbox_transform=ax.transData, loc='lower center')
    ax.set_title(title)
    return fig




if __name__ == '__main__':

    work_dir2 = 'task5_sims/'   


    d = np.load('Powers_{}.npz'.format(work_dir2.replace('/','')))
    yaw = d['YAW']
    PP = d['PP']
    PC = d['PC']

    figp = plot(yaw, PP, 'Polar')
    figc = plot(yaw, PC, 'Curl')

    figc.savefig('./figs/task5_power_curl.pdf')
    figp.savefig('./figs/task5_power_polar.pdf')
    plt.show()
