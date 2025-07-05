# import a utility function for loading Roboflow models
from inference import get_model
from take_screenshots import capture_screenshot
import supervision as sv
import cv2

# load a pre-trained yolov8n model
model = get_model(model_id="dino-game-rcopt/14")

bounding_box_annotator = sv.BoxAnnotator()

# define the image url to use for inference
while True:
    image = capture_screenshot()
    # run inference on our screenshot
    results = model.infer(image)[0]

    detections = sv.Detections.from_inference(results)

    annotated_image = bounding_box_annotator.annotate(
        scene=image,
        detections=detections
    )

    # display the image
    cv2.imshow("Annotated Image", annotated_image)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break