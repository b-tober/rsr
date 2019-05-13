import numpy as np
import functions as rsr
#from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import sys

#----------------------------------------------------------


file_name = sys.argv[1]
rsr.utils.inline_estim(file_name)


#----------------------------------------------------------

#data_file = file_name + '.csv'


# Open data file - Surface echo is power is 13th column(values are powers in dB)
#file = np.genfromtxt(data_file, delimiter = ',', dtype = str)

# convert signal into linear amplitude
#amp = 10**(file[:,12].astype(np.float64)/20)

# Apply RSR to a given subset of amplitude
#sample = amp   #[80000:85000]
#f = fit.lmfit(sample, fit_model='hk', bins='knuth')
#f.report() # Display result
#f.plot(method='analytic') # Plot results.

# Apply RSR along a vector of successive amplitude
#utils.inline_estim(file_name)
#print('winsize = ' + str(winsize) + '\nsampling = ' + str(sampling))
#utils.plot_inline(b2) # Plot results
#plt.show()
