def get_action(detections):
    """
    Determines the action to take based on game detections.
    Could be later replaced with a more sophisticated model, like
    an evolution algorithm or a neural network.

    Args:
        detections: A supervision.Detections object from the inference model.

    Returns:
        A string representing the action: "up" (jump), "down" (duck), or None.
    """
    for i in range(len(detections.xyxy)):
        box = detections.xyxy[i]
        y_centroid = (box[1] + box[3]) / 2

        if detections.data['class_name'][i] == 'cactus':
            # Check if the cactus is in the "jump zone"
            if not (110 < y_centroid < 144):
                continue
            # left corner on the X axis between 130 and 170
            if 130 < box[0] < 170:
                return "up"  # Jump over cactus

        elif detections.data['class_name'][i] == 'bird':
            # Check if the bird is in the action zone
            if not (100 < box[0] < 200):
                continue

            # Act based on the first detected bird in the zone
            if y_centroid > 121:  # Low bird -> JUMP
                return "up"
            else:  # High bird -> DUCK
                return "down"

    return None
