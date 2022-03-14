from PIL import Image
import os

# List of ascii characters used to build the image. "." is a lighter pixel, "@" is a darker pixel
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

# Convert an Image to ascii
def convert(path):

    # Open the image
    img = Image.open(os.path.abspath(path))

    # Resize the image
    new_width = 100
    width, height = img.size
    ratio = height / width
    new_height = int(new_width * ratio)
    img = img.resize((new_width, new_height))

    # Convert each pixel to grayscale
    img = img.convert("L")

    # Split the image into individual pixels
    pixels = img.getdata()

    # Grey scale values are 0 - 255, map each pixel to one of the 11 ASCII character from the ASCII_CHARS list
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])

    # Format the characters
    pixel_count = len(characters)
    ascii_image = "\n".join(
        characters[i : (i + new_width)] for i in range(0, pixel_count, new_width)
    )

    return ascii_image


def main():
    convert("website/uploads/mona.jpg")


if __name__ == "__main__":
    main()
