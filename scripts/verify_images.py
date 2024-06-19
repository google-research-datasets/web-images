"""Check that the image files match the metadata in the CSV.

Author: Yannis Guyon (yguyon@google.com)
Licensed under Creative Commons Attribution-ShareAlike 4.0 International.
https://creativecommons.org/licenses/by-sa/4.0/
"""

import csv
import cv2
import hashlib
import imageio
import numpy
import os
import PIL.Image
import sys


def imread(path):
  if (path.endswith('png')):
    # OpenCV correctly reads 16-bit PNGs.
    return cv2.imread(path, cv2.IMREAD_UNCHANGED)
  elif (path.endswith('gif')):
    # PIL.Image supports alpha.
    image = PIL.Image.open(path)
    if image.has_transparency_data:
      return numpy.array(image.convert('RGBA'))
    return numpy.array(image.convert('RGB'))
  else:
    # Generic fallback.
    return imageio.imread(path)


image_categories = ['Translucent', 'Animated', 'Camera-captured', 'Scan', 'Synthetic', 'Up-to-128x128px', 'Screen-captured', 'Medical', 'Gaming', 'Emoji']

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print('Usage: ' + os.path.basename(sys.argv[0]) + ' <CSV path> <image folder path>')
    sys.exit(1)

  ok = True
  image_folder_path = sys.argv[2]
  files_in_csv = []
  with open(sys.argv[1], 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
      files_in_csv.append(row['Name'])
      image_path = os.path.join(image_folder_path, row['Name'])
      image = imread(image_path)

      # Compare the image with the CSV data.
      md5 = hashlib.md5(open(image_path, 'rb').read()).hexdigest()
      if row['md5'] != md5:
        ok = False
        print('md5 ' + md5 + ' of ' + row['Name'] + ' does not match ' + row['md5'])
      
      if row['Width'] == '' or row['Height'] == '':
        ok = False
        print('Dimensions of ' + row['Name'] + ' are ' + str(image.shape[1]) + ' ' + str(image.shape[0]))
      elif image.shape[1] != int(row['Width']) or image.shape[0] != int(row['Height']):
        ok = False
        print('Dimensions ', image.shape, ' of ' + row['Name'] + ' do not match ' + row['Width'] + ', ' + row['Height'])
      if (len(image.shape) <= 2 or image.shape[2] == 1 or image.shape[2] == 3) and row['Translucent'] == '1':
        ok = False
        print('Plane count ', image.shape, ' of ' + row['Name'] + ' does not match translucency')

      if row['Bit depth'] == '':
        ok = False
        print('Bit depth of ' + row['Name'] + ' is ' + str(image.dtype))
      elif str(image.dtype) != 'uint' + row['Bit depth']:
        ok = False
        print('Bit depth ', str(image.dtype), ' of ' + row['Name'] + ' does not match ' + row['Bit depth'])

      # Each image should be tagged with at least one category.
      num_tags = 0
      for image_category in image_categories:
        if row[image_category] == '1':
          num_tags = num_tags + 1
      if num_tags == 0:
        ok = False
        print('Image ' + row['Name'] + ' has no tag')

  # Check that all files in the folder are referenced in the CSV table.
  for filename in os.scandir(image_folder_path):
    if filename.is_file() and not filename.name in files_in_csv:
      ok = False
      print('Missing ' + filename.name + ' in ' + os.path.basename(sys.argv[1]))
  
  if ok:
    print('All good')
  sys.exit(0)
