import cv2
from face_recognition import FaceRecognizer
from utils.helpers import load_image, display_image

def main():
    # Initialize the face recognizer
    face_recognizer = FaceRecognizer()
    face_recognizer.load_model()

    # Load an image for recognition
    image_path = input("Enter the path to the image: ")
    image = load_image(image_path)

    # Recognize faces in the image
    results = face_recognizer.recognize_face(image)

    # Draw results on the image
    output_image = face_recognizer.draw_results(image, results)

    # Display the output image
    display_image(output_image)

if __name__ == "__main__":
    main()
