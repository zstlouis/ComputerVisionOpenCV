import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import cvzone

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)
colorR = (255, 0, 255)


class DragRect:
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        # if index fingertip is in rectangle region then change pos
        if cx - w // 2 < cursor[0] < cx + w // 2 \
                and cy - w // 2 < cursor[1] < cy + h // 2:
            # move rectangle
            self.posCenter = cursor


# make multiple rectangles
rectList = []
for x in range(5):
    rectList.append(DragRect([x * 250 + 150, 150]))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands = detector.findHands(img, draw=False)

    '''
        test
    '''
    if len(hands) == 1:

        hand1 = hands[0]
        lmList1 = hand1['lmList']

        # find distance
        length, _, _ = detector.findDistance(lmList1[8][:2], lmList1[12][:2], img)
        print(length)

        # length is distance between finger points
        # check if clicked
        if length < 30:
            cursor = lmList1[8][:2]
            # call update
            for rect in rectList:
                rect.update(cursor)

    # Draw rectangles
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        # x1,x2, y1,y2
        cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
