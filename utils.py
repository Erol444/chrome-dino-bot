import cv2
import numpy as np
import os
from pynput.keyboard import Key

# --- Image Loading and Caching ---

ASSETS_DIR = "assets"

def load_icon(filename):
    """Loads a PNG icon and ensures it has a white background."""
    path = os.path.join(ASSETS_DIR, filename)
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if image is None:
        # Return a black square as a fallback
        print(f"Warning: Could not read asset: {path}. Using a placeholder.")
        return np.zeros((64, 64, 3), dtype=np.uint8)

    # If the image has an alpha channel, blend it with a white background
    if image.shape[2] == 4:
        alpha = image[:, :, 3]
        rgb = image[:, :, :3]

        # Create a white background
        white_bg = np.full(rgb.shape, 255, dtype=np.uint8)

        # Create a mask for compositing
        alpha_mask = alpha[:, :, np.newaxis] / 255.0

        # Blend the icon onto the white background
        composite = rgb * alpha_mask + white_bg * (1 - alpha_mask)
        return composite.astype(np.uint8)
    else:
        # If it's a 3-channel image, return it directly
        return image

# Load images once to avoid reading from disk on every frame
UP_IMG = load_icon("up.png")
UP_PRESSED_IMG = load_icon("up-pressed.png")
DOWN_IMG = load_icon("down.png")
DOWN_PRESSED_IMG = load_icon("down-pressed.png")
LEFT_IMG = load_icon("left.png")
RIGHT_IMG = load_icon("right.png")


# --- Image Manipulation ---
def overlay_image(background, overlay, x, y):
    """Overlays an opaque BGR image onto a background image."""
    bg_h, bg_w, _ = background.shape
    h, w, _ = overlay.shape

    if x < 0 or y < 0 or x + w > bg_w or y + h > bg_h:
        return background

    background[y:y+h, x:x+w] = overlay
    return background

# --- Drawing Functions ---
def draw_key_indicators(image, pressed_keys):
    """
    Draws key state indicators on the top-center of the image.

    Args:
        image: The main game image (BGR).
        pressed_keys: A set-like object containing the keys that are currently pressed.
    """
    icon_h, icon_w, _ = UP_IMG.shape
    screen_h, screen_w, _ = image.shape
    margin = 10

    # Center the indicators horizontally
    total_width = 3 * icon_w
    start_x = (screen_w - total_width) // 2

    # Positions for the indicators
    up_x = start_x + icon_w
    up_y = margin

    down_x = start_x + icon_w
    down_y = margin + icon_h

    left_x = start_x
    left_y = margin + icon_h

    right_x = start_x + (2 * icon_w)
    right_y = margin + icon_h

    # UP icon
    up_icon = UP_PRESSED_IMG if Key.space in pressed_keys else UP_IMG
    image = overlay_image(image, up_icon, up_x, up_y)
    
    # DOWN icon
    down_icon = DOWN_PRESSED_IMG if Key.down in pressed_keys else DOWN_IMG
    image = overlay_image(image, down_icon, down_x, down_y)

    # LEFT and RIGHT icons
    image = overlay_image(image, LEFT_IMG, left_x, left_y)
    image = overlay_image(image, RIGHT_IMG, right_x, right_y)

    return image
