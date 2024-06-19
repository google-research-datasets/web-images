# Web Images

Collection of still PNG and animated GIF images gathered on the Internet in 2023.

## Tags

Each image belongs to at least one of these categories as described in the [images.csv](2023/images.csv) table:

- Translucent
- Animated
- Camera-captured
- Scan
- Synthetic
- Up-to-128x128px
- Screen-captured
- Medical
- Gaming
- Emoji

### Visualizer

The images can be listed by category using the [grid viewer](2023/index.html) (`git clone` first).

## File integrity check

Medical imaging resources were converted to PNG using Python and the `nibabel` and `cv2` dependencies:

```py
image = cv2.resize(nibabel.load().get_fdata()[shape0,shape1,shape2], (dimension0, dimension1))
cv2.imwrite(png_path, image / (image.max() / 255))
```

To obtain the same MD5 hashes as listed in the [images.csv](2023/images.csv) table, PNG metadata was stripped from the files using the following Python command:

```py
cv2.imwrite(path, cv2.imread(path, cv2.IMREAD_UNCHANGED), [cv2.IMWRITE_PNG_COMPRESSION, 9])
```

## License

Each image has its own license, copyright and credits as described in the [images.csv](2023/images.csv) table. See the [licenses](2023/licenses) folder.

The image list itself is licensed under the Creative Commons license [Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/). See the [LICENSE](LICENSE) file.
