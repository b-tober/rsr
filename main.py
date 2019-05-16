import numpy as np
import rsr.functions as rsr
import matplotlib.pyplot as plt
import sys,os
'''
script to run rsr for input file with radar surface return amplitude

example call:

python -m rsr.main /home/btober/Documents/5050702_001_fret_geom.csv

note: run from directory containing both subradar and rsr packages. use -m flag for relative import paths to work
'''
def main(file_name, winsize=1000, sampling=250, nbcores=2, verbose=True):
    # Load data from geom file with surface reflectivity amplitude in last column
    data = np.genfromtxt(in_path + file_name, delimiter = ',', dtype = str)
    amp = data[:,-1].astype(float)

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
    # slice original geom file and only keep necessary data - create new data header
    header = str('column,longitude,latitude,sza,sref,')  + ','.join(str(x)for x in list(a))
    # append results of lmfit at xo coordinates to data file - using int(x), note: for 1000 winsize, xo would be 499.5 - forcing rsr results to be appended to physical trace location using int(xo) indices
    data = data[w['xo'].astype(int)[:],:]      
    data = data[:,[1,6,7,11]]            
    out = np.append(data, a, 1)                         

    try:
        np.savetxt(out_path + file_name.split('_')[0] + '_' + file_name.split('_')[1] + '_rsr.csv', 
        out, delimiter = ',', newline = '\n', comments = '',header = header,  fmt = '%s') 
    except Exception as err:
        print(err)

    print(file_name.split('_')[0] + '_' + file_name.split('_')[1] + ' processing done!')

    return

if __name__ == '__main__':
    # get correct data paths if depending on current OS
    # ---------------
    # INPUTS - set to desired parameters
    # ---------------
    study_area = 'bh_nh_bt/'  
    winsize = 1000              # window size for fit
    sampling = 250              # step size for fit along track
    nbcores = 2
    verbose = False             # report results of fit if true
    # ---------------
    mars_path = '/MARS'
    in_path = mars_path + '/targ/xtra/SHARAD/EDR/surfPow/' + study_area
    out_path = mars_path + '/targ/xtra/SHARAD/rsr/' + study_area

    if os.getcwd().split('/')[1] == 'media':
        mars_path = '/media/anomalocaris/Swaps' + mars_path
        in_path = '/media/anomalocaris/Swaps' + in_path
        out_path = '/media/anomalocaris/Swaps' + out_path
    elif os.getcwd().split('/')[1] == 'mnt':
        mars_path = '/mnt/d' + mars_path
        in_path = '/mnt/d' + in_path
        out_path = '/mnt/d' + out_path
    elif os.getcwd().split('/')[1] == 'disk':
        mars_path = '/disk/qnap-2' + mars_path
        in_path = '/disk/qnap-2' + in_path
        out_path = '/disk/qnap-2' + out_path
    else:
        print('Data path not found')
        sys.exit()

    # create necessary output directories if nonexistent
    try:
        os.makedirs(out_path)
    except FileExistsError:
        pass

    file_name = sys.argv[1]     # input geom file with surface reflectivity for each trace
    main(file_name, winsize=winsize, sampling=sampling, nbcores=nbcores, verbose=verbose)
