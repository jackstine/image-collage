from PIL import Image, ImageOps

def rescale_and_center(image_paths, output_path, output_size, background_color=(255, 255, 255)):
    """
    Rescale an image, maintain aspect ratio, center it, and add padding to fit the desired output size.

    :param image_path: Path to the input image.
    :param output_path: Path to save the output image.
    :param output_size: Tuple specifying the final dimensions (width, height).
    :param background_color: Background color as an (R, G, B) tuple.
    """
    width = output_size[0]
    # height = output_size[1]
    left = -1
    border = 20
    done = False
    
    count = 0
    output_image = Image.new("RGB", output_size, background_color)
    for image_path in image_paths:
        count += 1
        with Image.open(image_path) as img:
            # Preserve aspect ratio while resizing to fit within output size
            img.thumbnail(output_size, Image.LANCZOS)

            # Create a new image with the desired output size and background color

            # Calculate position to center the resized image on the background
            width_of_image = img.size[0]
            x_offset = 0
            y_offset = 0
            if left == - 1:
                pass
            else:
                y_offset = left + border
                y_end_offset = y_offset + width_of_image
                if y_end_offset > width:
                    # exit program
                    y_offset = -1

            if y_offset != - 1:
                print(x_offset, y_offset)
                output_image.paste(img, (y_offset, x_offset))
                output_image.save(output_path + str(count) + ".jpg")
            else:
                output_image.save(output_path)
                done = True
                break
            left = img.size[0] + y_offset
        if done:
            break
    if not done:
        print("saved Image")
        output_image.save(output_path)

# Example usage
if __name__ == "__main__":
    input_image = ["peakpx (3).jpg", "peakpx (4).jpg", "peakpx (5).jpg",  "peakpx (6).jpg", "peakpx (7).jpg" ]  # Path to the input image
    output_image = "output.jpg"  # Path to save the output image
    laptop_demensions = (3456, 2234)
    desktop_demensions = (3840,1080)  # Desired output size (width, height)
    bg_color = (0, 0, 0)  # Background color (R, G, B)

    rescale_and_center(input_image, output_image, desktop_demensions, bg_color)