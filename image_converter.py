from PIL import Image
import math
import numpy as np


# ASCII character combinations, they are sorted from darkest to lightest
#ASCII_CHARS = ['@', '#', '%', '&', '*', '=', '+', '-', ':', '.']
#ASCII_CHARS = ['@', '#', '8', '&', 'o', ':', '*', '.', ' ']
#ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
ASCII_CHARS = ['@', '%', '#', '*', '+', '=', '-', ':', '.', ' ']

# Resize image according to a new width (to maintain aspect ratio)
def resize_image(image, new_width=None):
    # Find new width and height so that number of characters won't exceed 2000
    width, height = image.size
    aspect_ratio = height / width
    if new_width == None:
        discord_msg_limit = 2000
        used_chars = 20
        size = discord_msg_limit - used_chars
        new_width = int(math.sqrt(size/(aspect_ratio * 2)))

    new_height = int(new_width * aspect_ratio)

    # Multiplying width by two because a character's height takes close to twice its width's space so it doesn't look squished
    resized_image = image.resize((new_width * 2, new_height))
    return resized_image

def handle_transparency(image):
    # To replace transparent areas with a white background
    background_color = (255, 255, 255, 255)  # white background
    new_image = Image.new("RGBA", image.size, background_color)
    new_image.paste(image, (0, 0), image)  # Paste using transparency mask
    return new_image

# Convert the image to grayscale
def grayscale_image(image):
    return image.convert('L')

# Map pixels to ASCII characters based on intensity
def map_pixels_to_ascii(image):
    # Convert image data to numpy array
    pixels = np.array(image)

    # Normalize the pixel values to fall between 0 and len(ASCII_CHARS) - 1
    ascii_indices = pixels // ((256 // len(ASCII_CHARS)) + 1)

    # Use the normalized indices to map to ASCII characters
    ascii_str = ''.join(ASCII_CHARS[pixel] for pixel in ascii_indices.flatten())

    return ascii_str

# Split the ASCII string into lines to match the image dimensions
def generate_ascii_art(image, width=None):
    image = resize_image(image, width)
    width, _ = image.size

    grayscale_img = grayscale_image(image)
    
    ascii_str = map_pixels_to_ascii(grayscale_img)
    pixel_count = len(ascii_str)
    
    ascii_art = "\n".join([ascii_str[index:(index + width)] for index in range(0, pixel_count, width)])
    return ascii_art

# Load image and generate ASCII art
def image_to_ascii(image_path, width=None):
    try:
        if image_path:
            # Check if the image might have transparency ("png" or "gif" format has it and we dont work with gifs)
            if image_path[-3:] == "png":
                image = Image.open(image_path).convert("RGBA")
                image = handle_transparency(image)
            else:
                image = Image.open(image_path)
    except Exception as e:
        print(f"Unable to open image: {e}")
        return e

    ascii_art = generate_ascii_art(image, width)
    if width == None:
        ascii_art = f"```\n{ascii_art}\n```"

    # Save the ASCII art to a text file
    with open('ascii_art.txt', 'w') as f:
        f.write(ascii_art)
    
    # Print the ASCII art to the console if it's for message format (just for some testing)
    if width == None:
        print(ascii_art)

    return ascii_art