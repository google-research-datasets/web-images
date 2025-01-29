"""Generates the top-level LICENSE file based on the given CSV.

Author: Yannis Guyon (yguyon@google.com)
Licensed under Creative Commons Attribution-ShareAlike 4.0 International.
https://creativecommons.org/licenses/by-sa/4.0/
"""

import csv
import os
import sys


if __name__ == '__main__':
  if len(sys.argv) != 5:
    print('Usage: ' + os.path.basename(sys.argv[0]) + ' <CSV path> <image folder path> <licenses folder path> <LICENSE path>')
    sys.exit(1)

  assets = set()
  with open(sys.argv[1], 'r') as csv_file:
    csv_rows = list(csv.DictReader(csv_file))

  # Main license is written first.
  main_license_name = 'CC BY-SA 4.0'
  aggregated_licenses = ['''Files:
 all files not listed in this document''']
  for row in csv_rows:
    if main_license_name in row['License']:
      aggregated_licenses.append(' ' + os.path.join(sys.argv[2], row['Name']))
      assets.add(row['Name'])
  aggregated_licenses.append('')
  with open(os.path.join(sys.argv[3], main_license_name + '.txt'), 'r') as license:
    aggregated_licenses.append(license.read())

  # Various licenses.
  for license_file in os.scandir(sys.argv[3]):
    if not license_file.is_file():
      continue
    license_name = license_file.name.removesuffix('.txt')
    if license_name == main_license_name:
      continue  # Handled above.
    aggregated_licenses.append('''

------------------------------------------------------------------------------

Files:''')
    num_files = 0
    for row in csv_rows:
      if license_name in row['License']:
        aggregated_licenses.append(' ' + os.path.join(sys.argv[2], row['Name']))
        assets.add(row['Name'])
        num_files = num_files + 1
    if num_files == 0:
      print('Unused license file ' + license_file.name)
      sys.exit(1)
    aggregated_licenses.append('')
    with open(os.path.join(sys.argv[3], license_file.name), 'r') as license:
      aggregated_licenses.append(license.read())

  # Public domain.
  aggregated_licenses.append('''

------------------------------------------------------------------------------

Files in the public domain:''')
  for row in csv_rows:
    if 'Public domain' in row['License']:
      aggregated_licenses.append(' ' + os.path.join(sys.argv[2], row['Name']))
      assets.add(row['Name'])

  if len(assets) != len(csv_rows):
    print('Missing licenses:')
    for row in csv_rows:
      if row['Name'] not in assets:
        print('  ' + row['Name'])
    sys.exit(1)

  with open(sys.argv[4], 'w') as top_level_license:
    top_level_license.write('\n'.join(aggregated_licenses))

  print('Done')
  sys.exit(0)
