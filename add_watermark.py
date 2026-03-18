"""Add a repeating watermark to an image.

The watermark (watermark.png) is tiled across the image and saved as a new file.

Usage:
  python add_watermark.py
"""
#python -u add_watermark.py

import os
from pathlib import Path
from PIL import Image


def get_valid_image_path() -> str:
    """Prompt user for image path until a valid image file is provided."""
    while True:
        image_path = input("Enter the path to the image: ").strip().replace('"','')
        if not image_path:
            print("Path cannot be empty. Try again.")
            continue
        if not os.path.isfile(image_path):
            print(f"File not found: {image_path}")
            continue
        try:
            Image.open(image_path)
            return image_path
        except Exception as e:
            print(f"Error opening image: {e}")


def tile_watermark(image: Image.Image, watermark: Image.Image) -> Image.Image:
    """Tile the watermark across the entire image."""
    result = image.copy()
    watermark_width, watermark_height = watermark.size
    image_width, image_height = image.size

    # Paste watermark repeatedly across the image
    y = 0
    while y < image_height:
        x = 0
        while x < image_width:
            result.paste(watermark, (x, y), watermark if watermark.mode == "RGBA" else None)
            x += watermark_width
        y += watermark_height

    return result


def process_gif(image_path: str, watermark: Image.Image) -> None:
    """Process an animated GIF and apply watermark to each frame."""
    try:
        gif = Image.open(image_path)
    except Exception as e:
        print(f"Error opening GIF: {e}")
        return

    # Extract GIF metadata
    frames = []
    durations = []

    try:
        for frame_idx in range(gif.n_frames):
            gif.seek(frame_idx)
            frame = gif.convert("RGBA")
            frames.append(frame)
            durations.append(gif.info.get("duration", 100))
    except EOFError:
        pass

    if not frames:
        print("Error: Could not extract frames from GIF")
        return

    # Apply watermark to each frame
    print(f"Processing {len(frames)} frames...")
    watermarked_frames = [tile_watermark(frame, watermark) for frame in frames]

    # Save as new GIF
    base, ext = os.path.splitext(image_path)
    output_path = f"{base}_watermarked.gif"

    watermarked_frames[0].save(
        output_path,
        save_all=True,
        append_images=watermarked_frames[1:],
        duration=durations,
        loop=0
    )

    print(f"Watermarked GIF saved to: {output_path}")


def main() -> None:
    HERE = os.path.dirname(os.path.abspath(__file__))
    WATERMARK_PATH = os.path.join(HERE, "watermark.png")

    # Check if watermark exists
    if not os.path.isfile(WATERMARK_PATH):
        print(f"Error: watermark.png not found in {HERE}")
        print("Please place watermark.png in the same directory as this script.")
        return

    # Get image path from user
    image_path = get_valid_image_path()

    # Open images
    try:
        watermark = Image.open(WATERMARK_PATH).convert("RGBA")
    except Exception as e:
        print(f"Error opening watermark: {e}")
        return

    # Check if it's a GIF
    _, ext = os.path.splitext(image_path)
    if ext.lower() == ".gif":
        process_gif(image_path, watermark)
    else:
        try:
            original_image = Image.open(image_path)
            # Apply watermark
            print("Applying watermark...")
            watermarked = tile_watermark(original_image, watermark)

            # Save result
            base, ext = os.path.splitext(image_path)
            
            #output_path = f"{base}_watermarked{ext}"
            #output_path

            output_path = f'{HERE}\\images\\{base.split("\\")[-1]}_watermarked{ext}'
            watermarked.save(output_path)

            print(f"Watermarked image saved to: {output_path}")
        except Exception as e:
            print(f"Error processing image: {e}")


if __name__ == "__main__":
    main()
