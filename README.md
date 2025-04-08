# spanpaper

**spanpaper** is a Python script that creates a wallpaper image that spans across multiple monitors with different resolutions, scaling settings, and physical sizes.

It calculates your real-world monitor layout, slices the image accordingly, and combines it into one wallpaper that fits perfectly across all screens.

## Requirements

- Linux system (tested only on Ubuntu 24.04)
- Python 3
- pip (Python package installer)
- Pillow library

## Setup

1. Download the `create_wallpaper.py` script or clone the Repo.
2. Install the required library:

   ```bash
   pip install pillow
   ```

3. Open the script in a text editor.
4. Configure your monitor layout at the top of the file:
   - Enter resolution, scaling, physical size (in inches), and optional vertical offset.
   - Define the gaps (in inches) between monitors.

## Usage

Run the script like this:

```bash
python3 create_wallpaper.py your_input_image.whatever_format_you_have output_image_path.png
```

Replace `your_input_image.whatever_format_you_have` with the path to your wallpaper. The generated wallpaper will be saved as `output_image_path.png`.

To apply the wallpaper:

1. Open GNOME Tweaks
2. Go to Appearance > Background
3. Set the image to the generated wallpaper
4. Set Adjustment to **Spanned**
