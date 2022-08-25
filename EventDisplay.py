import h5py
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm 
import numpy as np



##########################################################
#
#      Script to visualize larcv images in hdf5 format
#               Author: Luis Mora Lepin
#          luis.moralepin@postgrad.manchester.ac.uk
#
###########################################################


'''
Things to do: 
* Add option to select the class - file 
* What if we have more than one plane?
* Add text with run,subrun,event 
* Where the images will be stored? 
'''

def SearchID(run,subrun,event,id_list):
    id = 0 
    for element in id_list:
        if(element[1]==run and element[2]==subrun and element[3]==event):
            id = element[0]
        else:
            pass
    #print(id) # For debugging 
    return id 

def PlaneLabel(plane):
    plane_label = 'none'
    if(plane == 0):
        plane_label='U'
    elif(plane==1):
        plane_label='V'
    elif(plane==2):
        plane_label='Y'
    else:
        print("Error, plane number out of range")
    return plane_label 

def DatasetSelector(dataset):
    file='none'
    if(dataset == 'mc'):
        file='bnb_run3_nue_larcv_cropped.h5'
    elif(dataset == 'data'):
        file='bnb_run3_open_data_larcv.h5'
    elif(dataset == 'dirt'):
        file='bnb_run3_dirt_larcv.h5'
    elif(dataset == 'ext'):
        file='bnb_run3_ext_larcv.h5'
    else:
        print('Error, wrong dataset input')
    return file 







def EvDisp(run,subrun,event,plane,dataset,debug=False):
    base_dir = "./hepgpu4-data2/lmlepin/Ole_files/"
    input_file=base_dir+DatasetSelector(dataset)
    producer = 'wire'
    f = h5py.File(input_file,'r')
    event_id_list = f['eventid']
    entry = SearchID(run,subrun,event,event_id_list)
    if(debug):
    	entry = 10
    else: 
    	entry = SearchID(run,subrun,event,event_id_list)
    plane_label = PlaneLabel(plane)
    #print(list(f['image2d'].keys()))
    #print(list(f['image2d']['metadata']))
    #print(list(f['image2d']['wire'].keys()))
    wire_set = f['image2d'][producer]
    image=wire_set[list(wire_set.keys())[0]]
    #print(image)
    fontprops=fm.FontProperties(size=10)
    fig, ax1= plt.subplots(1,1)
    plt.title("Plane: " +  plane_label)
    plt.xlabel("Wire number")
    plt.ylabel("Time tick")
    ax1.imshow(image[entry,plane,:,:],cmap='turbo',origin="lower")
    scalebar1= AnchoredSizeBar(ax1.transData,
                                100,'30 cm','lower left',
                                color='white',
                                frameon=False,
                                size_vertical=1,
                                fontproperties=fontprops)
    ax1.add_artist(scalebar1)
    plt.show()
