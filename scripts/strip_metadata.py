"""Copy all images from one folder to another, stripping any metadata.

Author: Yannis Guyon (yguyon@google.com)
Licensed under Creative Commons Attribution-ShareAlike 4.0 International.
https://creativecommons.org/licenses/by-sa/4.0/
"""

import cv2
import imageio
import os
# import PIL.Image
import sys


if __name__ == '__main__':
  if len(sys.argv) != 3:
    print('Usage: ' + os.path.basename(sys.argv[0]) + ' <source image folder path> <destination image folder path>')
    sys.exit(1)

  for filename in os.listdir(sys.argv[1]):
    original_image_path = os.path.join(sys.argv[1], filename)
    image_path = os.path.join(sys.argv[2], filename)
    if os.path.isfile(original_image_path):
      if (filename.endswith('png')):
        # OpenCV correctly reads 16-bit PNGs and outputs smaller PNGs.
        image = cv2.imread(original_image_path, cv2.IMREAD_UNCHANGED)
        cv2.imwrite(image_path, image, [cv2.IMWRITE_PNG_COMPRESSION, 9])
      elif (filename.endswith('gif')):
        # I could not make any of the following work losslessly:
        #   imageio.mimwrite(path, image)                                                    # Does not work for alpha.
        #   frames[0].save(path, save_all=True, append_images=frames[1:], disposal=2)        # Loss when saving to GIF.
        #   PIL.Image.open(original_image_path).save(image_path, save_all=True, disposal=2)  # Loss when saving to GIF.
        # So just copy the file instead and too bad if there is metadata:
        os.popen('cp "' + original_image_path + '" "' + image_path + '"').read()
      else:
        # Generic fallback.
        imageio.imwrite(image_path, imageio.imread(original_image_path))

  print('Done')
  sys.exit(0)
