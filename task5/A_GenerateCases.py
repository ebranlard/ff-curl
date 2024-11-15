import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
# Local 
import weio
import welib.fast.case_gen as case_gen
import welib.fast.runner as runner
import welib.fast.postpro as postpro

MyDir=os.path.dirname(__file__)

# --- Parameters for this script
FSTF_EXE  = os.path.join(MyDir, './FAST.Farm_x64.exe') # Location of a FAST exe (and dll)
FSTF_EXE  = os.path.join(MyDir, './FAST.Farm_x64_2022_05_06.exe') # Location of a FAST exe (and dll)
ref_dir   = os.path.join(MyDir, './task5_template/')
main_fstf = 'input_curl.fstf'  # Main file in ref_dir, used as a template
main_fast = 'WT1.fst'           # Main file in ref_dir, used as a template
main_fast2= 'WT2.fst'           # Main file in ref_dir, used as a template

# work_dir  = 'task5_sims_noDfl/'     # Output folder (will be created)

work_dir  = 'task5_sims/'     # Output folder (will be created)

fast = weio.read(os.path.join(ref_dir, main_fast))
fstf= weio.read(os.path.join(ref_dir, main_fstf))
WT = fstf['WindTurbines']
# 
# print(fstf.keys())
try:
    os.mkdir(work_dir)
except:
    pass

# --- Defining the parametric study  (list of dictionnaries with keys as FAST parameters)
YAW = np.arange(-40,41,5)
BaseDict = {}
PARAMS_FSTF=[]
PARAMS_FAST=[]
PARAMS_FAST2=[]
for i,(yaw) in enumerate(YAW):
#     for ModWake in [1,2]:
    for ModWake in [2]:
        pfstf = dict()
        pfast = dict()
        pfast2= dict()
        basename = 'yaw_{:04d}_modwake{:d}'.format(yaw,ModWake)
        print(basename)
        pfstf['Mod_Wake'] = ModWake
        pfstf['__name__']= basename
        if ModWake==2:
            pfstf['k_VortexDecay'] = 0.0001
            # 
            if 'noDfl' in work_dir:
                pfstf['C_HWkDfl_O']  = 0
                pfstf['C_HWkDfl_OY'] = 0
                pfstf['C_HWkDfl_x']  = 0
                pfstf['C_HWkDfl_xY'] = 0
            elif 'Dfl_Tuned2' in work_dir:
                pfstf['C_HWkDfl_O']  = 0
                pfstf['C_HWkDfl_OY'] = 0.0
                pfstf['C_HWkDfl_x']  = 0
                pfstf['C_HWkDfl_xY'] = 0.001
            elif 'Dfl_Tuned3' in work_dir:
                pfstf['C_HWkDfl_O']  = 0
                pfstf['C_HWkDfl_OY'] = 0.3
                pfstf['C_HWkDfl_x']  = 0
                pfstf['C_HWkDfl_xY'] = 0.003
            elif 'Dfl_Tuned' in work_dir:
                pfstf['C_HWkDfl_O']  = 0
                pfstf['C_HWkDfl_OY'] = 0.3
                pfstf['C_HWkDfl_x']  = 0
                pfstf['C_HWkDfl_xY'] = 0.002
            if 'ModProj0' in work_dir:
                pfstf['Mod_Projection'] = 0
        else:
            pfstf['C_HWkDfl_O']  = "DEFAULT"
            pfstf['C_HWkDfl_OY'] = "DEFAULT"
            pfstf['C_HWkDfl_x']  = "DEFAULT"
            pfstf['C_HWkDfl_xY'] = "DEFAULT"

        WTloc = WT.copy()
        WTloc[0,3] = '"WT1_{}.fst"'.format(basename)
        WTloc[1,3] = '"WT2_{}.fst"'.format(basename)
        pfstf['WindTurbines']= WTloc

        pfast['EDFile|NacYaw'] = yaw 
        pfast ['ServoFile|DLL_FileName'] = '"'+basename+'_WT1.dll"'
        pfast['__name__']= 'WT1_'+basename

        pfast2['ServoFile|DLL_FileName'] = '"'+basename+'_WT2.dll"'
        pfast2['__name__']= 'WT2_'+basename

        case_gen.forceCopyFile('task5_template/ServoData/discon_x64_WT1.dll', os.path.join(work_dir,  basename+'_WT1.dll'))
        case_gen.forceCopyFile('task5_template/ServoData/discon_x64_WT2.dll', os.path.join(work_dir,  basename+'_WT2.dll'))


        PARAMS_FSTF.append(pfstf)
        PARAMS_FAST.append(pfast)
        PARAMS_FAST2.append(pfast2)

# # --- Generating all files in a workdir
fstffiles=case_gen.templateReplace(PARAMS_FSTF, ref_dir, outputDir=work_dir, removeRefSubFiles=True, main_file=main_fstf, oneSimPerDir=False)
fastfiles=case_gen.templateReplace(PARAMS_FAST, ref_dir, outputDir=work_dir, removeRefSubFiles=True, main_file=main_fast, oneSimPerDir=False)
fastfiles=case_gen.templateReplace(PARAMS_FAST2, ref_dir, outputDir=work_dir, removeRefSubFiles=True, main_file=main_fast2, oneSimPerDir=False)
print(fastfiles)
print(fstffiles)

# --- Creating a batch script just in case
runner.writeBatch(os.path.join(work_dir,'_RUN_ALL.bat'),fstffiles,fastExe=FSTF_EXE, nBatches=6)
# # --- Running the simulations
# runner.run_fastfiles(fastfiles, fastExe=FAST_EXE, parallel=True, showOutputs=False, nCores=4)
# 
# # --- Simple Postprocessing
# outFiles = [os.path.splitext(f)[0]+'.outb' for f in fastfiles]
# avg_results = postpro.averagePostPro(outFiles,avgMethod='periods',avgParam=1, ColMap = {'WS_[m/s]':'Wind1VelX_[m/s]'},ColSort='WS_[m/s]')
# print('>> Average results:')
# print(avg_results)
# return avg_results


if __name__ == '__main__':
    pass
