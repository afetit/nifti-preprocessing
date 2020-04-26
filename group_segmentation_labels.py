import os
from os import listdir
from os.path import isfile, join
import matplotlib
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np

cerebstem_path = '/data/segmentations-data/template/cerebstem'
csf_path = '/data/segmentations-data/template/csf'
dgm_path = '/data/segmentations-data/template/dgm'
germinal_matrix_path = '/data/segmentations-data/template/germinal-matrix'
gm_path = '/data/segmentations-data/template/gm'
outlier_path = '/data/segmentations-data/template/outlier'
ventricles_path = '/data/segmentations-data/template/ventricles'
wm_path = '/data/segmentations-data/template/wm'

saving_path = '/data/initial-segmentation-masks-grouped-by-ahmed'

onlyfiles = [f for f in listdir(cerebstem_path) if isfile(join(cerebstem_path, f))]

for x in onlyfiles:
    cerebstem_filename = os.path.join(cerebstem_path, x)
    csf_filename = os.path.join(csf_path, x)
    dgm_filename = os.path.join(dgm_path, x)
    germinal_matrix_filename = os.path.join(germinal_matrix_path, x)
    gm_filename = os.path.join(gm_path, x)
    outlier_filename = os.path.join(outlier_path, x)
    ventricles_filename = os.path.join(ventricles_path, x)
    wm_filename = os.path.join(wm_path, x)

    cerebstem_img = nib.load(cerebstem_filename)
    cerebstem_img_data = cerebstem_img.get_fdata()
    new_header = cerebstem_img.header.copy()

    csf_img = nib.load(csf_filename)
    csf_img_data = csf_img.get_fdata()

    dgm_img = nib.load(dgm_filename)
    dgm_img_data = dgm_img.get_fdata()

    germinal_img = nib.load(germinal_matrix_filename)
    germinal_img_data = germinal_img.get_fdata()

    gm_img = nib.load(gm_filename)
    gm_img_data = gm_img.get_fdata()

    outlier_img = nib.load(outlier_filename)
    outlier_img_data = outlier_img.get_fdata()

    ventricles_img = nib.load(ventricles_filename)
    ventricles_img_data = ventricles_img.get_fdata()

    wm_img = nib.load(wm_filename)
    wm_img_data = wm_img.get_fdata()

    cerebstem_img_data[cerebstem_img_data < 30] = 0
    cerebstem_img_data[cerebstem_img_data > 30] = 1
    cerebstem_img_data[csf_img_data > 30] = 2
    cerebstem_img_data[dgm_img_data > 30] = 3
    cerebstem_img_data[germinal_img_data > 30] = 4
    cerebstem_img_data[gm_img_data > 30] = 5
    cerebstem_img_data[outlier_img_data > 30] = 6
    cerebstem_img_data[ventricles_img_data > 30] = 7
    cerebstem_img_data[wm_img_data > 30] = 8

    new_img = nib.nifti1.Nifti1Image(cerebstem_img_data, None, header=new_header)
    nib.save(new_img, join(saving_path, x))
