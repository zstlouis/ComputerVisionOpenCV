import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)
total = 0

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    if hands:
        # get hand 1
        hand1 = hands[0]
        handType1 = hand1["type"]  # left or right hand

        '''uncomment below to view additional information 
            detected by handDetector module'''

        # lmList1 = hand1["lmList"]  # list of all 21 landmarks
        # bbox1 = hand1["bbox"]  # bounding box info (x,y,w,h)
        # centerPoint1 = hand1["center"]  # center of the hand (cx,cy)
        # print(lmList1)
        # print(bbox1)
        # print(centerPoint1)

        # display which hand is in the frame
        print(handType1)

        fingers1 = detector.fingersUp(hand1)
        total = sum(fingers1)

        # check if both hands on in the frame
        if len(hands) == 2:
            # get hand 2

            hand2 = hands[1]
            handType2 = hand2["type"]
            '''uncomment below to view additional information 
                detected by handDetector module'''

            # lmList2 = hand2["lmList"]
            # bbox2 = hand2["bbox"]
            # centerPoint2 = hand2["center"]
            # print(lmList2)
            # print(bbox2)
            # print(centerPoint2)

            # display which hand is in the frame
            print(handType1, handType2)

            fingers2 = detector.fingersUp(hand2)
            total = sum(np.add(fingers1, fingers2))

    cv2.putText(img, "Total: " + str(int(total)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)