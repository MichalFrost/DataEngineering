import cv2
import numpy as np

# Parametry śledzenia piłki
tracker = cv2.TrackerCSRT_create()  # Można użyć różnych trackerów, np. KLT, CSRT, MIL

# Funkcja do wykrywania piłki w obrazie na podstawie koloru
def detect_ball_by_color(frame):
    # Konwersja obrazu na przestrzeń kolorów HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Zakresy kolorów dla piłki ręcznej (zwykle pomarańczowe, ale może być różnie w zależności od oświetlenia)
    lower_orange = np.array([5, 150, 150])  # Dolny zakres koloru pomarańczowego w HSV
    upper_orange = np.array([15, 255, 255]) # Górny zakres koloru pomarańczowego w HSV
    
    # Maskowanie obrazu, aby wyodrębnić piłkę ręczną
    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Wykrywanie konturów w masce
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    ball_center = None
    max_area = 0
    
    # Wybieramy największy kontur, który będzie piłką
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            ball_center = contour

    return ball_center

# Funkcja do śledzenia piłki
def track_ball(frame):
    global tracker

    # Wykrywanie piłki na podstawie koloru
    ball_center = detect_ball_by_color(frame)

    # Jeśli wykryto piłkę, inicjalizujemy tracker
    if ball_center is not None:
        # Obliczaj prostokąt ograniczający dla wykrytej piłki
        x, y, w, h = cv2.boundingRect(ball_center)
        tracker.init(frame, (x, y, w, h))

        return (x, y, w, h)  # Zwróć prostokąt ograniczający
    return None

# Załaduj wideo lub strumień z kamery
cap = cv2.VideoCapture(0)  # Możesz zmienić na plik wideo: "handball_video.mp4"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 1. Zmienna do przechowywania położenia piłki
    ball_position = track_ball(frame)
    
    # 2. Jeżeli piłka została wykryta, śledzimy jej położenie
    if ball_position is not None:
        x, y, w, h = ball_position
        # Rysowanie prostokąta wokół piłki
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Wyświetlanie obrazu z wykrytą piłką
    cv2.imshow("Handball Ball Detection and Tracking", frame)

    # Zatrzymaj program, jeśli naciśniesz klawisz 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Zakończenie i zwolnienie zasobów
cap.release()
cv2.destroyAllWindows()
