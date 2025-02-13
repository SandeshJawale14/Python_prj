def load_image(image_path):
    import cv2
    image = cv2.imread(image_path)
    return image

def preprocess_image(image):
    import cv2
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized_image = cv2.resize(gray_image, (224, 224))  # Resize to match model input
    return resized_image

def display_image(image, window_name='Image'):
    import cv2
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
