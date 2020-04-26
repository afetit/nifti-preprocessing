import os
from os import listdir
from os.path import isfile, join
import matplotlib
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np

loading_path_imgs = '/data/images/fetal_brains_new_recons_aligned/not-normalised/Ro1.00-not-normalised-dyn-extracted'
loading_path_masks = '/data/images/fetal_brains_new_recons_aligned/not-normalised/Mo1.00'
saving_path = '/data/images/fetal_brains_new_recons_aligned/normalised/Ro1.00-dyn-and-brain-extracted-then-normalised'

onlyfiles = [f for f in listdir(loading_path_imgs) if isfile(join(loading_path_imgs,f))]

for x in onlyfiles:
    x_mask = x.replace("Ro1.00", "Mo1.00")
    full_filename = os.path.join(loading_path_imgs, x)
    full_maskname = os.path.join(loading_path_masks, x_mask)

    print('reading:', full_filename)
    print('mask name:', full_maskname)

    img = nib.load(full_filename)
    img_shape = img.shape
    img_data = img.get_fdata()
    new_header = img.header.copy()

    mask = nib.load(full_maskname)
    mask_shape = mask.shape
    mask_data = mask.get_fdata()
    new_header_mask = mask.header.copy()

    img_data[mask_data < 1] = 0

    mean_pixel = np.mean(img_data[mask_data >1])
    std_pixel = np.std(img_data[mask_data >1])

    img_data[mask_data > 1] = img_data[mask_data > 1] - mean_pixel
    img_data[mask_data > 1] = img_data[mask_data > 1] / std_pixel


    new_img = nib.nifti1.Nifti1Image(img_data, None, header=new_header)
    nib.save(new_img, join(saving_path,x))