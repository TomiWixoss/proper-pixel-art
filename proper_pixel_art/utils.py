"""Utility functions"""

from proper_pixel_art import colors
from PIL import Image, ImageDraw
import numpy as np

Lines = list[int]  # Lines are a list of pixel indices for an image
Mesh = tuple[
    Lines, Lines
]  # A mesh is a tuple of lists of x coordinates and y coordinates for lines


def crop_border(image: Image.Image, num_pixels: int = 1) -> Image.Image:
    """
    Crop the boder of an image by a few pixels.
    Sometimes when requesting an image from GPT-4o with a transparent background,
    the boarder pixels will not be transparent, so just remove them.
    """
    width, height = image.size
    box = (num_pixels, num_pixels, width - num_pixels, height - num_pixels)
    cropped = image.crop(box)
    return cropped


def remove_generative_watermark(image: Image.Image) -> Image.Image:
    """
    Detects and removes a watermark (like Gemini's) in the bottom right corner
    by filling it with the surrounding background color.
    """
    arr = np.array(image.convert("RGBA"))
    h, w = arr.shape[:2]

    # Ensure image is large enough
    if h < 300 or w < 300:
        return image

    # Look at bottom-right 250x250
    bottom_right = arr[h - 250 : h, w - 250 : w]

    # Calculate median color of the bottom right corner (background color)
    bg_color = np.median(bottom_right, axis=(0, 1))

    # Calculate difference using float to avoid uint8 underflow
    diff = np.linalg.norm(bottom_right[:, :, :3].astype(np.float32) - bg_color[:3], axis=2)
    watermark_mask = diff > 30  # Threshold

    # Fill the watermark area with the background color
    if np.any(watermark_mask):
        rows, cols = np.where(watermark_mask)
        r_min, r_max = rows.min(), rows.max()
        c_min, c_max = cols.min(), cols.max()

        # Give some padding to ensure smooth removal
        r_min = max(0, r_min - 5)
        r_max = min(250, r_max + 5)
        c_min = max(0, c_min - 5)
        c_max = min(250, c_max + 5)

        # If the detected bounding box covers too much area, it might not be a watermark
        if (r_max - r_min) < 180 and (c_max - c_min) < 220:
            bottom_right[r_min:r_max, c_min:c_max] = bg_color.astype(np.uint8)
            arr[h - 250 : h, w - 250 : w] = bottom_right
            return Image.fromarray(arr, image.mode)

    return image



def overlay_grid_lines(
    image: Image.Image,
    mesh: Mesh,
    line_color: tuple[int, int, int] = (255, 0, 0),
    line_width: int = 1,
) -> Image.Image:
    """
    Overlay mesh which includes vertical (lines_x) and horizontal (lines_y) grid lines
    over image for visualization.
    """
    # Ensure we draw on an RGBA canvas
    canvas = image.convert("RGBA")
    draw = ImageDraw.Draw(canvas)

    lines_x, lines_y = mesh

    w, h = canvas.size
    # Draw each vertical line
    for x in lines_x:
        draw.line([(x, 0), (x, h)], fill=(*line_color, 255), width=line_width)

    # Draw each horizontal line
    for y in lines_y:
        draw.line([(0, y), (w, y)], fill=(*line_color, 255), width=line_width)

    return canvas


def scale_img(img: Image.Image, scale: int) -> Image.Image:
    """Scales the image up via nearest neightbor by scale factor."""
    w, h = img.size
    w_new, h_new = int(w * scale), int(h * scale)
    new_size = w_new, h_new
    scaled_img = img.resize(new_size, resample=Image.Resampling.NEAREST)
    return scaled_img
