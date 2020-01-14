import numpy as np
import rsr.functions as rsr
import matplotlib.pyplot as plt
import sys,os,glob
import pandas as pd
'''
script to run rsr for input file with radar surface return amplitude

example call:

python -m rsr.main [study_area] [number_cores] [surface_power_geom_file]

argv[1] is the verbose setting, bool
argv[2] is the study region
argv[3] is the number of threads to use
argv[4] is the window size
argv[5] is the window step size

note: run from directory containing both subradar and rsr packages. use -m flag for relative import paths to work
'''

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def main(file_name, winsize=1000, sampling=250, nbcores=2, verbose=True):
    fname = file_name.split('/')[-1]
    fname = fname.split('_')[0] + '_' + fname.split('_')[1]
    # Load data from geom file with surface reflectivity amplitude in last column
    data = pd.read_csv(file_name)
    amp = data['SREF'].to_numpy()

    # Apply RSR to a given subset of amplitude.
    # sample = amp[80000:85000]
    # f = rsr.run.processor(amp, fit_model='hk')
    # f.plot() # Plot results
    # plt.show()

    # Apply RSR along a vector of successive amplitude.
    # The RSR is applied on windows made of (winsize) values. Each window is separated by
    # (sampling) samples (can be time consuming).
    w,a = rsr.run.along(amp, winsize=winsize, sampling=sampling, nbcores=nbcores,verbose=verbose)

    # rsr.utils.plot_along(a) # Plot results
    # plt.show()
    #----------------------------------------------------------

    # append rsr results to geom table at each window midpoint
    # slice original geom file and only keep necessary data for window centers
    # append results of lmfit at xo coordinates to data file - using int(x), note: for 1000 winsize, xo would be 499.5 - forcing rsr results to be appended to physical trace location using int(xo) indices
    data = data.iloc[w['xo'].astype(int)[:],:]

    out = pd.concat([data.reset_index(drop=True), a.reset_index(drop=True)], axis=1)

    # remove sref trace field to avoid confusion with rsr window stats
    out = out.drop(columns = 'SREF')

    out.columns = [x.upper() for x in out.columns]

    # add window size and step size field to output data
    out['WINSIZE'] = np.repeat(np.array(winsize),out.shape[0])
    out['SAMPLING'] = np.repeat(np.array(sampling),out.shape[0])

    try:
        # if data_set == 'stack':
        #     out.to_csv(out_path + file_name.split('_')[0] + '_' + file_name.split('_')[1] + '_stack_rsr.csv', index = False)
        # else:
        out.to_csv(out_path + fname + '_rsr.csv', index = False) 
    except Exception as err:
        print(err)

    print(fname + ' processing done!')

    return

if __name__ == '__main__':
    # get correct data paths if depending on current OS
    # ---------------
    # INPUTS - set to desired parameters
    # ---------------
    verbose = int(sys.argv[1])             # report results of fit if true
    if verbose == 0:
        verbose = False
        blockPrint()
    else: 
        verbose = True
    study_area = str(sys.argv[2]) + '/'  
    nbcores = int(sys.argv[3])  # number of cores to run in parallel
    winsize = int(sys.argv[4])              # window size for fit
    sampling = int(sys.argv[5])              # step size for fit along track
    # ---------------
    in_path = '/zippy/MARS/targ/xtra/SHARAD/EDR/surfPow/' + study_area
    out_path = '/zippy/MARS/targ/xtra/SHARAD/EDR/rsr/' + study_area

    # create necessary output directories if nonexistent
    try:
        os.makedirs(out_path)
    except FileExistsError:
        pass

    for file in glob.glob(in_path + "*.csv"):
        main(file, winsize=winsize, sampling=sampling, nbcores=nbcores, verbose=verbose)
