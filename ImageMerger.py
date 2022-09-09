import csv
import getopt
import os
import sys

from PIL import Image, ImageColor


def merge_images(image1_path: str, image2_path: str, horizontal: bool, mode: str, fill_color: tuple):
    try:
        image1 = Image.open(image1_path)
        image2 = Image.open(image2_path)

        if horizontal:
            finalWidth = image1.width + image2.width
            finalHeight = max(image1.height, image2.height)
        else:
            finalWidth = max(image1.width, image2.width)
            finalHeight = image1.height + image2.height

        mergedImage = Image.new(mode=mode, size=(
            finalWidth, finalHeight), color=fill_color)

        if horizontal:
            mergedImage.paste(image1, (0, 0))
            mergedImage.paste(image2, (image1.width, 0))
        else:
            mergedImage.paste(image1, (0, 0))
            mergedImage.paste(image2, (0, image1.height))

        return mergedImage, True
    except:
        return None, False


def merge_and_save(image1_path: str, image2_path: str, horizontal: bool, mode: str, fill_color: tuple, final_path: str, optimize: bool):
    try:
        finalImage, success = merge_images(image1_path=image1_path, image2_path=image2_path,
                                           horizontal=horizontal, mode=mode, fill_color=fill_color)
        if success:
            dirname = os.path.dirname(final_path)
            if len(dirname) > 0:
                os.makedirs(dirname, exist_ok=True)
            finalImage.save(fp=final_path, optimize=optimize)
            return finalImage, True
        else:
            return None, False
    except:
        return None, False


def print_merge_message(image1_path: str, image2_path: str, final_path: str, success: bool):
    print("Merge", image1_path, "with", image2_path, "into",
          final_path, "SUCCESS" if success else "FAILURE")


def main(argv):
    image_list_path = ""

    image1_path = ""
    image2_path = ""
    final_path = ""

    horizontal = True
    mode = "RGBA"
    fill_color = (255, 255, 255, 255)
    optimize = False

    verbose = False

    option_values, _ = getopt.getopt(args=argv, shortopts="", longopts=[
                                     "image-list-path=", "image1-path=", "image2-path=", "final-path=", "vertical", "mode=", "fill-color=", "optimize", "verbose"])

    for option_name, option_value in option_values:
        if option_name == "--image-list-path":
            image_list_path = option_value
        elif option_name == "--image1-path":
            image1_path = option_value
        elif option_name == "--image2-path":
            image2_path = option_value
        elif option_name == "--final-path":
            final_path = option_value
        elif option_name == "--vertical":
            horizontal = False
        elif option_name == "--mode":
            mode = option_value
        elif option_name == "--fill-color":
            fill_color = ImageColor.getrgb(option_value)
        elif option_name == "--optimize":
            optimize = True
        elif option_name == "--verbose":
            verbose = True

    if verbose:
        print("--- Merge Arguments ---")
        if len(image_list_path) > 0:
            print("image_list_path:", image_list_path)
        else:
            print("    image1_path:", image1_path)
            print("    image2_path:", image2_path)
            print("     final_path:", final_path)
        print("     horizontal:", horizontal)
        print("           mode:", mode)
        print("     fill_color:", fill_color)
        print("       optimize:", optimize)
        print("-----------------------")

    if len(image_list_path) > 0:
        try:
            with open(image_list_path, newline='') as csv_file:
                csv_reader = csv.reader(
                    csv_file, delimiter=',', escapechar="\\")
                for row in csv_reader:
                    _, success = merge_and_save(image1_path=row[0], image2_path=row[1], horizontal=horizontal,
                                                mode=mode, fill_color=fill_color, final_path=row[2], optimize=optimize)

                    print_merge_message(
                        image1_path=row[0], image2_path=row[1], final_path=row[2], success=success)

        except FileNotFoundError:
            print("Could not process", image_list_path, ": File Not Found")

    else:
        _, success = merge_and_save(image1_path=image1_path, image2_path=image2_path, horizontal=horizontal,
                                    mode=mode, fill_color=fill_color, final_path=final_path, optimize=optimize)

        print_merge_message(image1_path=image1_path, image2_path=image2_path,
                            final_path=final_path, success=success)


if __name__ == "__main__":
    main(sys.argv[1:])
