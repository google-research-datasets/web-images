"""Generates index.html, presenting a grid of the thumbnails of the images referenced in the CSV.

Author: Yannis Guyon (yguyon@google.com)
Licensed under Creative Commons Attribution-ShareAlike 4.0 International.
https://creativecommons.org/licenses/by-sa/4.0/
"""

import csv
import os
import sys
import PIL.Image
import subprocess


image_categories = ['Translucent', 'Animated', 'Camera-captured', 'Scan', 'Synthetic', 'Up-to-128x128px', 'Screen-captured', 'Medical', 'Gaming', 'Emoji']

if __name__ == '__main__':
  if len(sys.argv) != 4:
    print('Usage: ' + os.path.basename(sys.argv[0]) + ' <CSV path> <image folder path> <index.html path>')
    sys.exit(1)

  with open(sys.argv[1], 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    html = ['''<!DOCTYPE html>
<html lang="en">
  <head>
    <title>Filtered image grid view</title>
    <style>
      button {
        margin: 10px;
      }
      #grid {
        display: flex;
        flex-flow: row wrap;
        align-items: center;
        align-content: flex-start;
        gap: 5px;
      }
      img {
        max-width: 256px;
        max-height: 256px;
        background-image: url(transparency_checkerboard.webp);
      }
      img:hover {
        box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
      }''']

    for image_category in image_categories:
      html.append('      .' + image_category + ' {  }')

    html.append('    </style>')
    html.append('''    <script>
      function toggle(className, displayValue) {
        var elements = document.getElementsByClassName(className);
        for (var e in elements) {
          if (elements.hasOwnProperty(e)) {
            elements[e].style.display = displayValue;
          }
        }
      }
    </script''')
    html.append('  </head>')
    html.append('  <body>')

    html.append('    <div style="display: flex;">')
    html.append('      <div style="display: flex; flex-direction: column;">')
    html.append('        <button onClick="toggle(\'Any\', \'\')">Show all</button>')
    html.append('        <button onClick="toggle(\'Any\', \'none\')">Hide all</button>')
    html.append('      </div>')
    for image_category in image_categories:
      html.append('      <div style="display: flex; flex-direction: column;">')
      html.append('        <button onClick="toggle(\'' + image_category + '\', \'\')">Show all ' + image_category + '</button>')
      html.append('        <button onClick="toggle(\'' + image_category + '\', \'none\')">Hide all ' + image_category + '</button>')
      html.append('      </div>')
    html.append('    </div>')

    html.append('    <div id="grid">')

    for row in csv_reader:
      image_path = os.path.join(sys.argv[2], row['Name'])
      preview_path = image_path
      if image_path.endswith('png'):
        preview_path = image_path.split('.png')[0] + '.thumb.webp'
        im = PIL.Image.open(image_path)
        im.thumbnail((256, 256))
        im.save(preview_path)
      if image_path.endswith('gif'):
        preview_path = image_path.split('.gif')[0] + '.thumb.webp'
        args = ("ffmpeg",
                "-i", image_path,
                "-vf", "scale=w=256:h=256:force_original_aspect_ratio=decrease",
                "-vcodec", "webp",
                "-loop", "0",
                "-pix_fmt", "yuva420p",
                preview_path, "-y")
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)

      # Map categories to css classes.
      css_classes = ['Any']
      for image_category in image_categories:
        if row[image_category] == '1':
          css_classes.append(image_category)
      html.append('      <a href="https://github.com/google-research-datasets/web-images/blob/main/2023/' + image_path + '" target="_blank" class="' + ' '.join(css_classes) + '">')
      html.append('        <img src="' + preview_path + '" title="' + row['Name'] + ' (' + row['Direct link or conversion command line'] + ' - ' + row['Source'] + ')">')
      html.append('      </a>')

    html.append('''    </div>
    <p>This page is licensed under the <a href="https://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International license</a> (Yannis Guyon - 2023). The images have their own licenses and credits as described in <a href="https://github.com/google-research-datasets/web-images/blob/main/2023/images.csv">images.csv</a>.</p>
  </body>
</html>
''')
    with open(sys.argv[3], 'w') as html_file:
      html_file.write('\n'.join(html))

  print('Done')
  sys.exit(0)
