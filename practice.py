import cv2

img = cv2.imread(r"assets/img.png")
detector = cv2.QRCodeDetector()
val, a, b = detector.detectAndDecode(img=img)

print(val)


