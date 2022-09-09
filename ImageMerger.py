import csv
import getopt
import os
import sys

from PIL import Image, ImageColor


def merge_images(orientation: str, size: int, mode: str, fill_color: tuple, image_paths: list[str]) -> tuple[Image.Image, bool]:
    try:
        images = []

        final_width = 0
        final_height = 0

        current_width = 0
        current_height = 0

        current_size = 0

        for image_path in image_paths:
            image = Image.open(image_path)
            images.append(image)

            if size == 0 or current_size < size:
                current_size += 1
            else:
                final_width = max(final_width, current_width)
                final_height = max(final_height, current_height)

                current_width = 0
                current_height = 0

                current_size = 1

            if orientation == "v":
                current_width = max(current_width, final_width + image.width)
                current_height += image.height
            else:
                current_width += image.width
                current_height = max(
                    current_height, final_height + image.height)

        final_width = max(final_width, current_width)
        final_height = max(final_height, current_height)

        mergedImage = Image.new(mode=mode, size=(
            final_width, final_height), color=fill_color)

        current_size = 0

        current_primary_pixel = 0
        current_secondary_pixel = 0
        next_secondary_pixel = 0

        for image in images:
            if size == 0 or current_size < size:
                current_size += 1
            else:
                current_size = 1

                current_primary_pixel = 0
                current_secondary_pixel = next_secondary_pixel
                next_secondary_pixel = 0

            if orientation == "v":
                mergedImage.paste(
                    image, (current_secondary_pixel, current_primary_pixel))

                current_primary_pixel += image.height
                next_secondary_pixel = max(
                    next_secondary_pixel, current_secondary_pixel + image.width)
            else:
                mergedImage.paste(
                    image, (current_primary_pixel, current_secondary_pixel))

                current_primary_pixel += image.width
                next_secondary_pixel = max(
                    next_secondary_pixel, current_secondary_pixel + image.height)

        return mergedImage, True
    except:
        return None, False


def merge_and_save(orientation: str, size: int, mode: str, fill_color: tuple, optimize: bool, quality: int, merge_path: str, image_paths: list[str]) -> tuple[Image.Image, bool]:
    try:
        finalImage, success = merge_images(
            orientation=orientation, size=size, mode=mode, fill_color=fill_color, image_paths=image_paths)
        if success:
            dirname = os.path.dirname(merge_path)
            if len(dirname) > 0:
                os.makedirs(dirname, exist_ok=True)
            finalImage.save(optimize=optimize, quality=quality, fp=merge_path)
            return finalImage, True
        else:
            return None, False
    except:
        return None, False


def main(argv):
    orientation = "h"
    size = 0
    mode = "RGBA"
    fill_color = "#00000000"
    optimize = True
    quality = 75

    verbose = False

    merge_path = "merge.png"

    option_values, image_paths = getopt.getopt(args=argv, shortopts="", longopts=[
                                               "orientation=", "size=", "mode=", "fill-color=", "optimize=", "quality=", "verbose", "merge-path="])

    for option_name, option_value in option_values:
        if option_name == "--orientation":
            try:
                if option_value[0].lower() == "v":
                    orientation = "v"
            except:
                pass

        elif option_name == "--size":
            try:
                size = int(option_value)
            except:
                pass

        elif option_name == "--mode":
            mode = option_value

        elif option_name == "--fill-color":
            fill_color = ImageColor.getrgb(option_value)

        elif option_name == "--optimize":
            try:
                if option_value[0].lower() in ["f", "n"]:
                    optimize = False
            except:
                pass

        elif option_name == "--quality":
            try:
                quality = int(option_value)
            except:
                pass

        elif option_name == "--verbose":
            verbose = True

        elif option_name == "--merge-path":
            merge_path = option_value

    if verbose:
        print("--- Merge Arguments ---")
        print("orientation:", orientation)
        print("       size:", size)
        print("       mode:", mode)
        print(" fill_color:", fill_color)
        print("   optimize:", optimize)
        print("    quality:", quality)
        print(" merge_path:", merge_path)
        print("image_paths:", image_paths)
        print("-----------------------")

    _, success = merge_and_save(orientation=orientation, size=size, mode=mode, fill_color=fill_color,
                                optimize=optimize, quality=quality, merge_path=merge_path, image_paths=image_paths)

    print("Merge", image_paths, "into", merge_path,
          "SUCCESS ✓" if success else "FAILURE ✗")


if __name__ == "__main__":
    main(sys.argv[1:])
