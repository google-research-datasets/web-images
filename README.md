# Web Images

Collection of still PNG and animated GIF images gathered on the Internet and from other sources.

## Tags

Each image belongs to at least one of these categories as described in the [images.csv](images.csv) table:

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
- High-bit-depth (more than 8 bits per pixel per channel when uncompressed)

### Visualizer

The images can be listed by category using the [grid viewer](https://google-research-datasets.github.io/web-images/).

## Preprocessing

Medical imaging resources were converted to PNG using Python and the `nibabel` and `cv2` dependencies:

```py
image = cv2.resize(nibabel.load().get_fdata()[shape0,shape1,shape2], (dimension0, dimension1))
cv2.imwrite(png_path, image / (image.max() / 255))
```

All PNG files were stripped of any metadata using the `optipng` command line tool:

```sh
optipng -clobber -strip all
```

## License

Each image has its own license, copyright and credits as described in the [images.csv](images.csv) table.

The image list itself is licensed under the Creative Commons license [Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/).

See the [LICENSE](LICENSE) file.
