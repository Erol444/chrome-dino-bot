from inference import get_model
from take_screenshots import capture_screenshot
import supervision as sv
import cv2
import time
import numpy as np
from pynput.keyboard import Key, Controller

from controller import get_action
from utils import draw_key_indicators


model = get_model(model_id="dino-game-rcopt/14")

palette = sv.ColorPalette(colors=[sv.Color(112, 153, 223), sv.Color(124, 221, 161), sv.Color(163, 81, 251)])

bounding_box_annotator = sv.BoxAnnotator(color=palette)
label_annotator = sv.LabelAnnotator(color=palette)

keyboard = Controller()

keyboard_img = np.ones((64 * 2 + 20, 624, 3), dtype=np.uint8) * 255

key_release_queue = {}

# Capture screenshot from specified coordinates
while True:
    # Release (up/down) keys that are ready to be released
    current_time = time.time()
    keys_to_release = []
    for key, release_time in key_release_queue.items():
        if current_time >= release_time:
            keyboard.release(key)
            keys_to_release.append(key)
    for key in keys_to_release:
        del key_release_queue[key]

    image = capture_screenshot()
    # Run inference on our screenshot
    results = model.infer(image)

    # load the results into the supervision Detections api
    detections = sv.Detections.from_inference(results[0].dict(by_alias=True, exclude_none=True))
    detections = detections[detections.confidence > 0.6]

    # Annotate bounding boxes and labels
    image = bounding_box_annotator.annotate(
        scene=image,
        detections=detections
    )
    image = label_annotator.annotate(
        scene=image,
        detections=detections,
    )

    # Get desired action from the controller (either duck, jump, or nothing)
    action = get_action(detections)

    # Execute the action
    if action == "up":
        if Key.space not in key_release_queue:
            keyboard.press(Key.space)
            key_release_queue[Key.space] = time.time() + 0.3
    elif action == "down":
        if Key.down not in key_release_queue:
            keyboard.press(Key.down)
            key_release_queue[Key.down] = time.time() + 0.4

    # Draw UI indicators (arrow keys)
    keyboard_img = draw_key_indicators(keyboard_img, key_release_queue.keys())

    # display the image
    cv2.imshow("Gameplay", cv2.vconcat([image, keyboard_img]))
    key = cv2.waitKey(1)
    if key == ord('q'):
        break