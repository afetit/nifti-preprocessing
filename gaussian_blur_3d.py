import os
from os import listdir
from os.path import isfile, join
import nibabel as nib
from skimage import filters

loading_path_imgs = '/Data/t2w'
saving_path = '/images/gaussian_blur'

onlyfiles = [f for f in listdir(loading_path_imgs) if isfile(join(loading_path_imgs,f))]

for x in onlyfiles:
    full_filename = os.path.join(loading_path_imgs, x)
    print('reading:', full_filename)

    img = nib.load(full_filename)
    i, j, k = img.shape
    img_data = img.get_fdata()
    img_data_gauss = img_data

    for kk in range(i):
        img_data_gauss[kk] = filters.gaussian(img_data[kk], sigma=1)

    new_header = img.header.copy()
    new_img = nib.nifti1.Nifti1Image(img_data_gauss, None, header=new_header)
    nib.save(new_img, join(saving_path, x))

