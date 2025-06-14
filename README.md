# spanpaper

**spanpaper** is a Python script that creates a wallpaper image that spans across multiple monitors with different resolutions, scaling settings, and physical sizes.

It calculates your real-world monitor layout, slices the image accordingly, and combines it into one wallpaper that fits perfectly across all screens.

## Online Version

You can now use spanpaper directly in your browser without downloading anything!  
Visit **[karl-funke.com/spanpaper](https://karl-funke.com/spanpaper)** to create perfectly spanning wallpapers through the web interface.

## Requirements

- Linux system with a desktop environment that supports "spanned" wallpapers (e.g., GNOME)
- Python 3
- Pillow library

## Setup

1. Download the `create_wallpaper.py` script or clone the repo.
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

### Applying the wallpaper

**GNOME:**
1. Open GNOME Tweaks
2. Go to Appearance > Background
3. Set the image to the generated wallpaper
4. Set Adjustment to **Spanned**

⚠️⚠️⚠️ IMPORTANT: In "Displays" settings, all monitor bottoms should be aligned!  
Even if a monitor is physically higher, leave them aligned in the OS.  
Why? Because where the mouse lands is quite cursed anyway — may as well go full cursed.  
Also, the wallpaper won’t line up correctly if they are not bottom-aligned.

## Example

Here's a full example showing how the script transforms a wallpaper image to span across multiple monitors.

**Original image:**

![Original wallpaper](images/original.jpg)

**Transformed by spanpaper into:**

![Transformed output](images/transformed.jpg)

**Transformed result applied on my cursed multi-monitor setup:**

![Setup result](images/setup.jpg)

_Image used from [Unsplash](https://unsplash.com/photos/a-scenic-view-of-a-lake-surrounded-by-mountains-c8lfnNZyGFg) by Simon Gamma._

