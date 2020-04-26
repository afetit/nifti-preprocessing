import os
from os import listdir, mkdir
from os.path import isfile, join
import nibabel as nib

mask_path = '/data/segmentations-deepmedic-all-subjects' #where segmentation masks live
t2_path = '/data/Ro1.00'#where t2 images live
saving_path = '/data/grouped-by-subject'#save-to directory

onlyfiles = [f for f in listdir(mask_path) if isfile(join(mask_path,f))]

for x in onlyfiles:

    #----- Routine for extracting slices from segmentations files------
    full_filename = os.path.join(mask_path, x)
    print('reading', full_filename)
    img = nib.load(full_filename)

    n_i, n_j, n_k = img.shape #image dimensions, then get mid points for coronal, sagittal and axial
    n_i_mid = n_i // 2
    n_j_mid = n_j // 2
    n_k_mid = n_k // 2

    img_data = img.get_fdata()#get data matrix, then define slices from each of the 3 orientations
    data_i = img_data[n_i_mid:n_i_mid+1, :, :]
    data_j = img_data[:, n_j_mid:n_j_mid+1, :]
    data_k = img_data[:, :, n_k_mid:n_k_mid+1]

    new_header = img.header.copy()#header data

    xsplit = x.split("_", 5)  # split file name so that i can get rid of extra text of segmentation file names

    saving_path_subdir = join(saving_path, xsplit[0] + '_' + xsplit[1])#point to saving directory, and create subdirectory for the image
    mkdir(saving_path_subdir)

    new_img_i = nib.nifti1.Nifti1Image(data_i, img.get_affine(), header=new_header) #save nifti files
    nib.save(new_img_i, join(saving_path_subdir, "mask_sag_" + x))
    new_img_j = nib.nifti1.Nifti1Image(data_j, img.get_affine(), header=new_header)
    nib.save(new_img_j, join(saving_path_subdir, "mask_cor_" + x))
    new_img_k = nib.nifti1.Nifti1Image(data_k, img.get_affine(), header=new_header)
    nib.save(new_img_k, join(saving_path_subdir, "mask_ax_" + x))

    #----- Routine for extracting slices from T2 files------
    full_filename_t2 = os.path.join(t2_path, xsplit[0] + '_' + xsplit[1] + '_' + xsplit[2] + '_'+ xsplit[3] + '_' + xsplit[4])

    print('reading', full_filename_t2) #below is same as above, but for T2 files

    imgt2 = nib.load(full_filename_t2)
    imgt2_data = imgt2.get_fdata()

    t2data_i = imgt2_data[n_i_mid:n_i_mid+1, :, :, 1]
    t2data_j = imgt2_data[:, n_j_mid:n_j_mid+1, :, 1]
    t2data_k = imgt2_data[:, :, n_k_mid:n_k_mid+1, 1]

    new_headert2 = imgt2.header.copy()
    new_imgt2_i = nib.nifti1.Nifti1Image(t2data_i, imgt2.get_affine(), header=new_headert2)
    nib.save(new_imgt2_i, join(saving_path_subdir, "t2_sag_" + xsplit[0] + '_' + xsplit[1] + '_' + xsplit[2] + '_'+ xsplit[3] + '_' + xsplit[4]))
    new_imgt2_j = nib.nifti1.Nifti1Image(t2data_j, imgt2.get_affine(), header=new_headert2)
    nib.save(new_imgt2_j, join(saving_path_subdir, "t2_cor_" + xsplit[0] + '_' + xsplit[1] + '_' + xsplit[2] + '_'+ xsplit[3] + '_' + xsplit[4]))
    new_imgt2_k = nib.nifti1.Nifti1Image(t2data_k, imgt2.get_affine(), header=new_headert2)
    nib.save(new_imgt2_k, join(saving_path_subdir, "t2_ax_" + xsplit[0] + '_' + xsplit[1] + '_' + xsplit[2] + '_'+ xsplit[3] + '_' + xsplit[4]))






















