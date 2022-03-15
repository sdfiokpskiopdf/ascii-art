from PIL import Image
import os

# List of ascii characters used to build the image. "." is a lighter pixel, "@" is a darker pixel
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

# Remove transparency
def remove_transparency(im, bg_colour=(255, 255, 255)):

    # Only process if image has transparency
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):

        # Need to convert to RGBA if LA format due to a bug in PIL
        alpha = im.convert("RGBA").split()[-1]

        # Create a new background image of our matt color.
        # Must be RGBA because paste requires both images have the same format
        bg = Image.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg

    else:
        return im


# Convert an Image to ascii
def convert(path, chars=1000000, max_width=200):

    # Open the image
    img = Image.open(os.path.abspath(path))

    # Remove transparency (if any)
    img = remove_transparency(img)

    # Resize the image
    width = img.size[0]
    if width > max_width:
        new_width = max_width
    else:
        new_width = width
    while True:
        width, height = img.size
        ratio = height / width / 1.45
        new_height = int(new_width * ratio)
        area = new_height * new_width
        if area > chars:
            new_width -= 1
        else:
            break

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

    # Delete the image
    os.remove(os.path.abspath(path))

    return ascii_image


def main():
    convert("website/uploads/mona.jpg")


if __name__ == "__main__":
    main()
