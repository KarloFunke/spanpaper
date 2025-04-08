"""
create_wallpaper.py

This script takes a high-resolution wallpaper image and slices it to fit across multiple monitors,
each with its own physical size, resolution, scaling factor, and vertical offset.

Ideal for Linux (e.g., Ubuntu) setups with multiple displays that have different sizes, resolutions, DPI or alignment.

USAGE:
    python create_wallpaper.py <input_image> <output_image>

DEPENDENCIES:
    pip install pillow

HOW IT WORKS:
- You define your monitor layout (left to right) in the script.
- The script calculates the physical layout, crops and scales your image accordingly,
  and generates a combined wallpaper image that fits perfectly across all screens.

FINAL STEP:
To use the generated wallpaper, apply it using GNOME Tweaks:
    ➤ sudo apt install gnome-tweaks
    ➤ Open GNOME Tweaks → Appearance → Background
    ➤ Select the generated wallpaper as Image
    ➤ Set 'Adjustment' to 'Spanned'

Author: https://github.com/KarloFunke
"""


import sys
from math import sqrt
from PIL import Image


# - - - - - - - Configure your Monitor Layout here - - - - - - - 

# Each monitor is defined with:
#   width         - pixel width of the monitor
#   height        - pixel height of the monitor
#   scaling       - the UI scaling factor set in your Ubuntu display settings
#   size_in       - physical diagonal size in inches
#   aspect_w/h    - the aspect ratio (e.g., 16:9 → aspect_w = 16, aspect_h = 9)
#   offset_bottom - vertical offset in inches from the lowest monitor (e.g., if it's raised)

# ⚠️⚠️⚠️ IMPORTANT: In Ubuntu's "Displays" settings, all monitor bottoms should be aligned!
# Even if a monitor is physically higher, leave them aligned in the OS.
# Why? Because where the mouse lands is cursed anyway lol — may as well go full cursed
# and the wallpaper wont work anymore if you change it.


# from LEFT monitor to RIGHT monitor
monitors = [
    {
        "width": 1920,
        "height": 1080,
        "scaling": 1.25,
        "size_in": 15.6,
        "aspect_w": 16,
        "aspect_h": 9,
        "offset_bottom": 0.1
    },
    {
        "width": 3840,
        "height": 2160,
        "scaling": 1.5,
        "size_in": 32.0,
        "aspect_w": 16,
        "aspect_h": 9,
        "offset_bottom": 0.0
    },
    {
        "width": 2560,
        "height": 1440,
        "scaling": 1.25,
        "size_in": 27.0,
        "aspect_w": 16,
        "aspect_h": 9,
        "offset_bottom": 0.75
    }
]

# Define the gap size between the monitors in inches
# The first value is the gap between the first two monitors, and so on.
gaps_in = [0.4, 0.5]



# - - - - - - - The Script (don't change anything here unless you want to alter functionality) - - - - - - - 



def main():
    if len(sys.argv) < 3:
        print("Usage: python create_wallpaper.py <input_image> <output_image>")
        sys.exit(1)

    if len(gaps_in) != len(monitors) - 1:
        print("Error: gaps_in must have one less element than monitors.")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # Calculate physical sizes of each monitor in inches
    for m in monitors:
        aspect_diagonal = sqrt(m["aspect_w"]**2 + m["aspect_h"]**2)
        m["width_in"] = m["size_in"] * m["aspect_w"] / aspect_diagonal
        m["height_in"] = m["size_in"] * m["aspect_h"] / aspect_diagonal

    # Calculate the physical width
    total_width_in = sum(m["width_in"] for m in monitors) + sum(gaps_in)

    # Calculate the physical height
    max_height_in = max(m["height_in"] + m["offset_bottom"] for m in monitors)

    print(f"Setup dimensions in inches:\n  width:  {total_width_in}\n  height: {max_height_in}\n")

    # Determine the actual pixel sizes the monitors will display in the final output
    # This depends on the scaling used
    for m in monitors:
        m["width_scaled"] = int(round(m["width"] / m["scaling"]))
        m["height_scaled"] = int(round(m["height"] / m["scaling"]))

    # Calculate the dimensions of the generated output
    total_output_width = sum(m["width_scaled"] for m in monitors)
    output_height = max(m["height_scaled"] for m in monitors)

    print("Output image dimensions (your input image should be at least this size to avoid blur):")
    print(f"  width:  {total_output_width}\n  height: {output_height}\n")

    # Open the original image and load its dimensions (in pixels, of course)
    original_img = Image.open(input_path)
    input_w, input_h = original_img.size

    print(f"Input image dimensions:\n  width:  {input_w}\n  height: {input_h}\n")

    # Calculate the aspect ratios of the input image and the overall monitor layout
    input_aspect = input_w / input_h
    layout_aspect = total_width_in / max_height_in

    # Check whether the input image aspect ratio matches the layout's.
    # If not, crop the image to match the layout aspect ratio.
    if input_aspect > layout_aspect:
        # Input too wide → crop horizontally (pillarbox)
        new_input_w = int(round(input_h * layout_aspect))
        left = (input_w - new_input_w) // 2
        crop_box = (left, 0, left + new_input_w, input_h)
        print("Cropping horizontally to match overall layout aspect.")

    elif input_aspect < layout_aspect:
        # Input too tall → crop vertically (letterbox)
        new_input_h = int(round(input_w / layout_aspect))
        top = (input_h - new_input_h) // 2
        crop_box = (0, top, input_w, top + new_input_h)
        print("Cropping vertically to match overall layout aspect.")

    else:
        crop_box = (0, 0, input_w, input_h)
        print("Aspect ratio matches — no cropping needed. Hope you didn’t waste time cropping manually, because this script does it anyway lol.")

    # Crop the image
    original_img = original_img.crop(crop_box)

    # Update dimensions after cropping
    input_w, input_h = original_img.size

    # Create the final output (Red background so unused areas are clearly visible if anything goes wrong)
    output_img = Image.new("RGB", (total_output_width, output_height), color=(255, 0, 0))

    # Main loop:
    # For each monitor, take the corresponding slice of the input image
    # based on physical size, and scale it to fit in the output image
    current_x = 0            # pixel offset in the final stitched image
    running_inch_x = 0.0     # physical inch offset from the left in the overall layout

    for i, m in enumerate(monitors):
        # If the original image is 100% width, this calculates the fractional position
        # where this monitor's slice starts and ends (values between 0 and 1)
        left_frac = running_inch_x / total_width_in
        right_frac = (running_inch_x + m["width_in"]) / total_width_in

        # Calculate the pixel range corresponding to those fractions
        crop_left = int(round(left_frac * input_w))
        crop_right = int(round(right_frac * input_w))

        # Vertical offset fraction: how many inches from the bottom baseline
        offset_frac = m["offset_bottom"] / max_height_in

        # Height fraction of this monitor relative to the entire layout height
        height_frac = m["height_in"] / max_height_in

        # In normalized top-to-bottom space: 0.0 is top, 1.0 is bottom
        bottom_frac = 1.0 - offset_frac
        top_frac = bottom_frac - height_frac

        # Convert these fractions to actual pixel coordinates
        crop_top = int(round(top_frac * input_h))
        crop_bottom = int(round(bottom_frac * input_h))

        # Crop the corresponding region from the input image
        region = original_img.crop((crop_left, crop_top, crop_right, crop_bottom))

        # Resize the region to the monitor’s scaled resolution
        region_resized = region.resize((m["width_scaled"], m["height_scaled"]), Image.LANCZOS)

        # Paste bottom-aligned into the final output
        y_offset = output_height - m["height_scaled"]
        output_img.paste(region_resized, (current_x, y_offset))

        # Advance horizontal position in output image
        current_x += m["width_scaled"]

        # Advance physical layout offset (include gap after this monitor if any)
        running_inch_x += m["width_in"]
        if i < len(gaps_in):
            running_inch_x += gaps_in[i]

    output_img.save(output_path, "PNG")
    print(f"Saved ready-to-use wallpaper to: {output_path}")


if __name__ == "__main__":
    main()
