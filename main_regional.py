import numpy as np
import functions as rsr
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import sys
#from config import *
#pylab

path = '/disk/qnap-2/MARS/targ/xtra/rsr/bh_nh_bt/fret_sza100+_merged/low/'


#file_name = sys.argv[1]
#utils.inline_estim(file_name)

file_name = 'fret_sza100+_low_merged'


data_file = path + file_name + '.csv'

print('\nProcessing: ' + data_file + '!\n')

# Open data file - Surface echo is power is 13th column(values are powers in dB)
file = np.genfromtxt(data_file, delimiter = ',', dtype = str)

# convert signal into linear amplitude
amp = 10**(file[:,12].astype(np.float64)/20)

# Apply RSR to a given subset of amplitude

f = rsr.fit.lmfit(amp, fit_model='hk', bins='knuth')
f.report() # Display result
f.plot(method='analytic') # Plot results.
#np.savetxt('/disk/qnap-2/MARS/targ/xtra/rsr/bh_nh_bt/results4/med/rsr_results4_med_merged.csv', f, delimiter = ',')


# Apply RSR along a vector of successive amplitude
#utils.inline_estim(file_name)
#print('winsize = ' + str(winsize) + '\nsampling = ' + str(sampling))
#utils.plot_inline(b2) # Plot results
#plt.show()
