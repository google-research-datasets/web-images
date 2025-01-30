"""List each file name from the given CSV file and prints its md5 hash.

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


if __name__ == '__main__':
  if len(sys.argv) != 3:
    print('Usage: ' + os.path.basename(sys.argv[0]) + ' <CSV path> <image folder path>')
    sys.exit(1)

  image_folder_path = sys.argv[2]
  files_in_csv = []
  with open(sys.argv[1], 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
      image_path = os.path.join(image_folder_path, row['Name'])
      md5 = hashlib.md5(open(image_path, 'rb').read()).hexdigest()
      print(row['Name'] + ' ' + md5)
  sys.exit(0)
