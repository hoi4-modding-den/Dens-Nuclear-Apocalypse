from PIL import Image
import random

def get_unique_rgb_values(image_path):
    # Open the image
    img = Image.open(image_path)
    
    # Convert image to RGB mode (just in case it's not already in RGB)
    img = img.convert('RGB')
    
    # Get the width and height of the image
    width, height = img.size
    
    # Create a set to store unique RGB values
    unique_rgb_values = set()

    # Loop through each pixel in the image and add the RGB value to the set
    for x in range(width):
        for y in range(height):
            rgb_value = img.getpixel((x, y))
            unique_rgb_values.add(rgb_value)
    
    return unique_rgb_values

def generate_random_rgb(excluded_rgb_values):
    while True:
        # Generate a random RGB value (each component between 0 and 255)
        random_rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        # Check if the generated value is not already in the excluded set
        if random_rgb not in excluded_rgb_values:
            return random_rgb

def main():
    # Example image file path (you can change this to your image file path)
    image_path = "map/provinces.bmp"
    
    # Get unique RGB values from the image
    unique_rgb_values = get_unique_rgb_values(image_path)
    
    # Generate a random RGB value that is not in the set of unique RGB values
    random_rgb = generate_random_rgb(unique_rgb_values)
    
    # Print the result
    print(f"Random RGB value not in the image: {random_rgb}")
    
    # Pause the console to let the user see the result before it closes
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
