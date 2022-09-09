# Python Image Merger

A Python image merging script.

## Dependencies

This scrip uses [Pillow](https://pillow.readthedocs.io/en/stable/index.html#) for image manipulation. Please [install Pillow](https://pillow.readthedocs.io/en/stable/installation.html) before using this script.

## Usage

There are two main ways to use this script. You can either merge 2 images or use a .csv file to batch image merging.

### Merging 2 Images

```console
python ImageMerger.py --image1-path 'test_files/orange.png' --image2-path 'test_files/scarlet_red.png' --final-path 'test_files/output/test_vertical.png' --vertical --mode 'RGB' --fill-color 'rgb(255,255,255)' --optimize --verbose
```

- `--image1-path [str]`: The path to the first image, relative to the current running directory.
- `--image2-path [str]`: The path to the second image, relative to the current running directory.
- `--final-path [str]`: The path where to store the merged image, relative to the current running directory.
- `--vertical`: Include if you want the merge to happen vertically. Optional. Default is horizontal.
- `--mode [str]`: A string defining the type and depth of the pixels in the final image. Refer to [Pillow modes](https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes) for all possible options. Optional. Default is `RGBA`.
- `fill-color [str]`: A string defining the final image's background color (only visible when images have mismatched sizes). Refer to [Pillow color names](https://pillow.readthedocs.io/en/stable/reference/ImageColor.html#color-names) for all possible options. Optional. Default is `#ffffffff` or `(255, 255, 255, 255)`.
- `--optimize`: Include if you want the final image to be optimized. Optional.
- `--verbose`: Include if you want the program to output to the console the value of all setup variables. Optional.

### Using a CSV file

```console
python ImageMerger.py --image-list-path 'test_files/test_image_list.csv' --vertical --mode 'RGB' --fill-color 'rgb(255,255,255)' --optimize --verbose
```

- `--image-list-path [str]`: The path to the [.csv file](#csv-file-structure), relative to the current running directory.
- `--vertical`: Include if you want the merges to happen vertically. Optional. Default is horizontal.
- `--mode [str]`: A string defining the type and depth of the pixels in the final images. Refer to [Pillow modes](https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes) for all possible options. Optional. Default is `RGBA`.
- `fill-color [str]`: A string defining the final images' background color (only visible when images have mismatched sizes). Refer to [Pillow color names](https://pillow.readthedocs.io/en/stable/reference/ImageColor.html#color-names) for all possible options. Optional. Default is `#ffffffff` or `(255, 255, 255, 255)`.
- `--optimize`: Include if you want the final images to be optimized. Optional.
- `--verbose`: Include if you want the program to output to the console the value of all setup variables. Optional.

#### CSV File Structure

```csv
image1_path,image2_path,final_path1
image3_path,image4_path,final_path2
image5_path,image6_path,final_path3
[...]
```

Note that these paths should not have any quotes around them. Here's an example:

```csv
test_files/chameleon.png,test_files/chameleon.png,test_files/output/test_csv1.png
test_files/sky_blue.png,test_files/plum.png,test_files/output/test_csv2.png
test_files/aluminium_light.png,test_files/aluminium_dark.png,test_files/output/test_csv3.png
```
