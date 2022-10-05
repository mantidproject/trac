# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 09:47:13 2012

@author: gesner
"""

import sys
sys.path.insert(0,'/home/gesner/workspace/mantid_debug/bin/')
from mantid.simpleapi import *
from matplotlib import pyplot as plt
import numpy

#The detector is 192 x 192
LoadNexus(Filename=r'SANS2D00002500.nxs',OutputWorkspace='2500_sans_nxs',EntryNumber='1')
wrong_cropping = CropWorkspace(InputWorkspace='2500_sans_nxs',StartWorkspaceIndex='37064',EndWorkspaceIndex='73735')
correct_cropping = CropWorkspace(InputWorkspace='2500_sans_nxs',StartWorkspaceIndex='36872',EndWorkspaceIndex='73735')
#the wrong cropping happens because there was the assumption that for the minimum DetectorID 2 000 000 you would have the minimum SpectrumID number. 

bins = wrong_cropping.getDimension(0).getNBins() # should be 152
wrong_data = numpy.concatenate([wrong_cropping.readY(i) for i in range(wrong_cropping.getNumberHistograms())])
correct_data = numpy.concatenate([correct_cropping.readY(i) for i in range(correct_cropping.getNumberHistograms())])


# Now, there is another problem, if you organize the dataset as 191x192xbins you will have the correct image
wrong_dataset = wrong_data.reshape((191,192,bins))
wrong_image = numpy.sum(wrong_dataset,axis=2)
plt.imshow(wrong_image, label="Correct 191x192")
plt.show()
plt.plot(numpy.sum(wrong_image, axis=0))
plt.show()

#But if you organize the dataset differently: 192x191xbins you will end up with a wrong dataset

wrong_dataset = wrong_data[:191*191*bins].reshape((191,191,bins))
wrong_image = numpy.sum(wrong_dataset,axis=2)
plt.imshow(wrong_image, label="Wrong 191x191")
plt.show()
plt.plot(numpy.sum(wrong_image, axis=0))
plt.show()


correct_dataset = correct_data.reshape((192,192,bins))
correct_image = numpy.sum(correct_dataset, axis=2)
plt.imshow(correct_image, label="With all the entries 192x192")
plt.show()
plt.plot(numpy.sum(correct_image, axis=0))
plt.show()
