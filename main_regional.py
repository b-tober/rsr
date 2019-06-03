import numpy as np
import rsr.functions as rsr
import matplotlib.pyplot as plt
import sys,os,time
'''
script to run regional rsr for input file with radar surface return amplitude

example call:

python -m rsr.main_regional [study_area] [surface_power_file]

[argv1] is study region
[argv2] is the surface amplitude data, along with navigation csv file

note: run from directory containing both subradar and rsr packages. use -m flag for relative import paths to work
'''
def main(file_name):

    t0 = time.time()                                                                            # begin time

    data_file = in_path + file_name

    print('\nProcessing regional RSR: ' + file_name + '\n')

    data = np.genfromtxt(data_file, delimiter = ',', dtype = float, names=True)                 # import amplitude data

    amp = data['sref']

    amp = amp[~np.isnan(amp)]

    [f,out] = rsr.run.processor(amp, fit_model='hk')                                            # apply RSR to regional amplitude data

    f.plot(method='analytic')                                                                   # plot results
    plt.show()

    plt.savefig(out_path + file_name.split('_')[2] + '_rsr.png')                                # save plot

    with open(out_path + file_name.split('_')[2] + '_rsr.txt','w') as fOut:                     # save rsr output
        fOut.write(out)
    
    
    t1 = time.time()                                                                            # end time
    
    print('--------------------------------')
    print('Total Runtime: ' + str(round((t1 - t0),4)) + ' seconds')
    print('--------------------------------')
    return

if __name__ == '__main__':
    # get correct data paths if depending on current OS
    # ---------------
    # INPUTS - set to desired parameters
    # ---------------
    study_area = str(sys.argv[1]) + '/'  
    # ---------------
    mars_path = '/MARS'
    in_path = mars_path + '/targ/xtra/SHARAD/EDR/surfPow/' + study_area + 'regional/'
    out_path = mars_path + '/targ/xtra/SHARAD/rsr/' + study_area + 'regional/'

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
    elif os.getcwd().split('/')[1] == 'home':
        mars_path = '/home/btober/Documents' + mars_path
        in_path = '/home/btober/Documents' + in_path
        out_path = '/home/btober/Documents' + out_path
    else:
        print('Data path not found')
        sys.exit()


    file_name = sys.argv[2]                                                                     # input file with surface reflectivity for each trace

    if ('stack' in file_name):                                                                  # check if using stacked data, and modify out path
        data_set = 'stack'
        out_path = out_path + data_set + '/'
    else:
        data_set = 'amp'
    
    try:
        os.makedirs(out_path)                                                                   # create necessary output directories if nonexistent
    except FileExistsError:
        pass

    main(file_name)