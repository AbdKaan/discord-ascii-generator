from PIL import Image
from urllib.request import urlopen
import numpy as np

# ASCII characters set from darkest to lightest
ASCII_CHARS = ['@', '#', '%', '&', '*', '=', '+', '-', ':', '.']
#ASCII_CHARS = ['@', '#', '8', '&', 'o', ':', '*', '.', ' ']
#ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
#ASCII_CHARS = ['@', '%', '#', '*', '+', '=', '-', ':', '.', ' ']

# Resize image according to a new width (to maintain aspect ratio)
def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width)
    # Multiplying width by two because 
    resized_image = image.resize((new_width * 2, new_height))
    return resized_image

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
def generate_ascii_art(image, width=100):
    image = resize_image(image, new_width=width)
    grayscale_img = grayscale_image(image)
    
    ascii_str = map_pixels_to_ascii(grayscale_img)
    pixel_count = len(ascii_str)
    
    ascii_art = "\n".join([ascii_str[index:(index + width*2)] for index in range(0, pixel_count, width*2)])
    return ascii_art

# Load image and generate ASCII art
def image_to_ascii(image_path, width=15):
    try:
        if image_path:
            image = Image.open(image_path)
    except Exception as e:
        print(f"Unable to open image: {e}")
        return e

    ascii_art = generate_ascii_art(image, width)
    ascii_art = f"```\n{ascii_art}\n```"
    print(len(ascii_art))
    # Save the ASCII art to a text file
    with open('ascii_art.txt', 'w') as f:
        f.write(ascii_art)
    
    # Print the ASCII art to the console
    print(ascii_art)

    return ascii_art