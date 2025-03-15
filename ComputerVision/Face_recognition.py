import cv2

# Ładujemy klasyfikator Haar Cascade do wykrywania twarzy
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Uruchamiamy kamerę (0 to domyślna kamera laptopa)
cap = cv2.VideoCapture(0)

# Sprawdzamy, czy kamera została poprawnie otworzona
if not cap.isOpened():
    print("Nie udało się otworzyć kamery")
    exit()

while True:
    # Zbieramy obraz z kamery
    ret, frame = cap.read()

    # Jeśli obraz jest poprawny, przetwarzamy go
    if ret:
        # Konwertujemy obraz do odcieni szarości (potrzebne do wykrywania twarzy)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Wykrywamy twarze na obrazie
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Rysujemy zielone prostokąty wokół wykrytych twarzy
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Pokazujemy obraz w oknie "Camera"
        cv2.imshow('Camera', frame)
    
    # Jeśli naciśniesz 'q', program zakończy działanie
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Zwalniamy kamerę i zamykamy okna
cap.release()
cv2.destroyAllWindows()
