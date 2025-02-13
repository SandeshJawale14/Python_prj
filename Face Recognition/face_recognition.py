class FaceRecognizer:
    def __init__(self):
        self.model = None

    def load_model(self, model_path):
        import cv2
        self.model = cv2.face.LBPHFaceRecognizer_create()
        self.model.read(model_path)

    def recognize_face(self, image):
        import cv2
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml').detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)
        results = []
        for (x, y, w, h) in faces:
            id_, confidence = self.model.predict(gray_image[y:y+h, x:x+w])
            results.append((id_, confidence, (x, y, w, h)))
        return results

    def draw_results(self, image, results):
        import cv2
        for (id_, confidence, (x, y, w, h)) in results:
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(image, f'ID: {id_}, Conf: {confidence:.2f}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        return image
