from PIL import Image
import os

def resize_image(input_path, output_path, scale=None, width=None, height=None, quality=85):
    """
    Resizes an image by a given scale or to specified dimensions (width and height),
    and decreases the file size by setting a lower JPEG quality if needed.
    
    Parameters:
    - input_path (str): Path to the input image file.
    - output_path (str): Path to save the resized image.
    - scale (float, optional): Scale factor to resize the image (e.g., 0.5 for 50%).
    - width (int, optional): New width in pixels. Ignored if scale is provided.
    - height (int, optional): New height in pixels. Ignored if scale is provided.
    - quality (int, optional): JPEG quality for output image (1-100, where 100 is best quality).
    
    Note: Either scale or both width and height should be provided.
    """
    # Open the original image
    img = Image.open(input_path)
    # Calculate new size based on scale or provided width/height
    if scale:
        new_width = int(img.width )
        new_height = int(img.height )
    elif width and height:
        new_width = width
        new_height = height
    else:
        raise ValueError("Provide either a scale or both width and height for resizing.")

    # Resize the image
    resized_img = img.resize((new_width, new_height), Image.LANCZOS)

    # Check if the image is in RGBA mode and convert to RGB if necessary
    if resized_img.mode == "RGBA":
        resized_img = resized_img.convert("RGB")

    # Save the resized image with the specified quality (for JPEG format)
    resized_img.save(output_path, quality=quality)
    print(output_path)
    print(f"Image saved at {output_path} with size {new_width}x{new_height} pixels at quality {quality}.")

    file_size_kb = os.path.getsize(output_path) / 1024  # Convert bytes to KB
    file_size_kb1 = os.path.getsize(input_path) / 1024  # Convert bytes to KB
    print(f"Image saved at {output_path} with size {new_width}x{new_height} pixels at quality {quality}.")
    print(f"Final file size: {file_size_kb1:.2f} KB")
    print(f"Final file size: {file_size_kb:.2f} KB")

    return file_size_kb1,file_size_kb,new_width,new_height

# Example Usage
# Resize to 50% of original size, save as JPEG with reduced quality of 70
# resize_image('./projectimg.jpg', 'output_scaled5.jpg', scale=0.5, quality=70)
