import time
import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)

# window dimensions
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)

# create keyboard buttons
keys = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/']]

finalText = ""
buttonList = []

# function to draw buttons onto the screen
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        # img, location, size, colour, filled
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
    return img


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.text = text
        self.size = size


for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    img = cv2.flip(img, i)
    hands, img = detector.findHands(img)
    img = drawAll(img, buttonList)

    if hands:
        hand1 = hands[0]
        lmList1 = hand1['lmList']
        if lmList1:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                if x < lmList1[8][0] < x + w and y < lmList1[8][1] < y + h:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

                    length, _, _ = detector.findDistance(lmList1[8][:2], lmList1[12][:2], img)
                    print(length)

                    # clicka button
                    if length < 30:

                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
                        finalText += button.text

                        # add delay to simulate keyboard
                        time.sleep(0.15)

    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 425),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    '''Uncomment to write to a text file.'''
    # with open('text.txt','a') as f:
    #     f.write(finalText)
    #     f.close()

    cv2.imshow("Image", img)
    cv2.waitKey(1)
