#!/usr/bin/env python
import os
import numpy as np
import pylab
import mahotas as mh
import glob
import watershed # label image by calling watershed.py
import utils # crop cell by calling utils.py
import plot
from PIL import Image
import skimage
import skimage.io
import scipy
import pandas as pd
import click
import matplotlib.patches as mpatches
from IPython import embed
if os.name != 'nt':
  from tsne import bh_sne
from time import time
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from sklearn import manifold, datasets
import sys
from IPython import embed

def tsne_images(res,perplexity,dpi):
  filenames=list(glob.glob('static/uploads/*g'))
  total_res = res**2
  x_value = np.zeros((len(filenames),total_res)) # Dimension of the image: 70*70=4900; x_value will store images in 2d array
  count = 0
  images = []
  colour = np.zeros(len(filenames))
  for imageName in filenames: 
    image = scipy.misc.imresize(skimage.io.imread(imageName), (res,res)) #reshape size to (70,70) for every image; 70 being the res
    image3d=image[:,:,:3]
    image2d=mh.colors.rgb2grey(image3d)
    image1d = image2d.flatten() #image1d stores a 1d array for each image
    images.append(image3d)
    x_value[count,:] = image1d # add a row of values
    count += 1

  # vis_data = bh_sne(x_value,perplexity=perplexity)# tsne embedding
  tsne = manifold.TSNE( init='pca', random_state=0, perplexity=perplexity)
  vis_data = tsne.fit_transform(x_value)

  canvas = plot.image_scatter(vis_data[:, 0], vis_data[:, 1], images, colour, min_canvas_size=4000)
  plt.imshow(canvas,origin='lower')
  # plt.title('%s vs %s' % (x,y))
  # plt.xlabel('%s' % x)
  # plt.ylabel('%s' % y)
  # patches=[]
  #plt.legend(handles=patches,bbox_to_anchor=(1.04,0.5), loc="center left", borderaxespad=0, frameon=False)
  save_location = 'static/output/output.png' 
  plt.savefig(save_location,dpi=dpi,pad_inches=1,bbox_inches='tight')
  # plt.show()
  print('Saved image scatter to %s' % save_location)
  return vis_data