#Function finds first return from radargram per method in Grima et al., 2012
#Author: Brandon S. Tober
#Created 30January2018

import os
from PIL import Image
import math
import numpy as np
import scipy.misc
from config import *
                
#convert binary .img PDS RGRAM to numpy array. Reshape array with 3600 lines
dtype = np.dtype('float32')     
rgram = open(path + file_name + '_rgram.img', 'rb') 
imarray = np.fromfile(rgram, dtype)     
l = len(imarray)
c = 3600
imarray = imarray.reshape(c,l/c)

#declare trace to plot power of as half point
trace = l/(2*c)

trace_db = np.empty((c,1))  #create empty criteria array to record trace power 

for i in range(c):
    trace_db[i,:] = np.log10(imarray[i,trace])*10

#
np.savetxt(file_name + '_trace_db.txt', trace_db, delimiter=',', newline = '\n', comments = '', header = 'PDB', fmt='%.8f')

#convert RGRAM array and fret array to images and save
#fret_array = Image.fromarray(fret_index)
#scipy.misc.imsave(root + '/' + file_name + '_fret_array.jpg', fret_array)


print('Processing of power for trace #' + str(trace) + ' done!')
