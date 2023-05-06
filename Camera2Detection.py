import cv2
import sys
import numpy as np
import time
import os
import math


class Camera2Detection:

    def __init__(self):
        self.detector = cv2.SimpleBlobDetector_create()
        self.params = cv2.SimpleBlobDetector_Params()

        self.params.filterByColor = True
        self.params.blobColor = 0

        self.params.minThreshold = 50
        self.params.maxThreshold = 200
        # Filter by Area.
        self.params.filterByArea = True
        self.params.minArea = 2000
        self.params.maxArea = 40000

        # Filter by Circularity
        self.params.filterByCircularity = True
        self.params.minCircularity = 0.1

        # Filter by Convexity
        self.params.filterByConvexity = True
        self.params.minConvexity = 0.70

        # Filter by Inertia
        self.params.filterByInertia = True
        self.params.minInertiaRatio = 0.1

        # Distance Between Blobs
        self.params.minDistBetweenBlobs = 200

        self.detector = cv2.SimpleBlobDetector_create(self.params)

    def detection(self, inputImage):
        global edge
        img = cv2.imread(inputImage, cv2.IMREAD_GRAYSCALE)
        # img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
        height, width = img.shape
        new_width = 700
        ratio = new_width / width  # (or new_height / height)
        new_height = int(height * ratio)
        img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

        ret, thresh1 = cv2.threshold(img, 60, 255, cv2.THRESH_BINARY)
        keypoints = self.detector.detect(img)
        holeCoorList = []

        for k in keypoints:
            x, y = int(k.pt[0]), int(k.pt[1])
            d = int(k.size)
            r = int(k.size / 2)
            cv2.circle(img, (int(k.pt[0]), int(k.pt[1])), int(k.size / 2), (255, 255, 255), -1)
            holeCoorList.append([x, y, d, r])

        if holeCoorList[0][0] > holeCoorList[1][0]:
            x, y, d, r = holeCoorList[0]
        else:
            x, y, d, r = holeCoorList[1]

        imgPortion = thresh1[y - int(r / 2):y + int(r / 2), x + d:new_width]
        portion_h, portion_w = imgPortion.shape
        kernal = np.ones((r - 1, r - 1))
        kernal_h, kernal_w = kernal.shape
        compareKernal_1 = np.zeros((r - 1, int((r - 1) / 2)))

        if int((r - 1)) % 2 != 0:
            compareKernal_2 = np.ones((r - 1, 1 + int((r - 1) / 2))) * 255
        else:
            compareKernal_2 = np.ones((r - 1, int((r - 1) / 2))) * 255
        compareKernal = np.concatenate((compareKernal_2, compareKernal_1), axis=1)

        stride = 2

        for i in range(0, portion_w):
            if (i * stride + kernal_w) >= portion_w:
                break
            multi = kernal * imgPortion[0:kernal_h, i * stride:i * stride + kernal_w]
            array_sum = sum(sum(multi - compareKernal))
            if array_sum < 0:
                edge = x + d + i * stride + int(kernal_w / 2)
                cv2.line(img, (edge, 0), (edge, new_height), (255, 255, 255), 2)
                break

        DisHole_1 = edge - holeCoorList[1][0]
        DisHole_2 = edge - holeCoorList[0][0]

        cv2.putText(img, str(DisHole_1), (holeCoorList[1][0] + 30, holeCoorList[1][1]), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 2)
        cv2.putText(img, str(DisHole_2), (holeCoorList[0][0] + 30, holeCoorList[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 2)
        cv2.line(img, (holeCoorList[1][0], y + 5), (edge, y + 5), (255, 255, 255), 2)
        cv2.line(img, (holeCoorList[0][0], y), (edge, y), (255, 255, 255), 2)

        if DisHole_1 < DisHole_2:
            temp = DisHole_1
            DisHole_1 = DisHole_2
            DisHole_2 = temp

        # print("DisHole_1", DisHole_1)
        # print("DisHole_2", DisHole_2)

        return img, DisHole_1, DisHole_2


if __name__ == '__main__':
    global edge
    s_time = time.time()
    camera2detection = Camera2Detection()
    print("time for loading the things", time.time() - s_time)

    ss_time = time.time()
    imagePath = sys.argv[1]
    Camera2Detection_im, DisHole_1, DisHole_2 = camera2detection.detection(imagePath)
    print("time for actual run", time.time() - ss_time)
    outputPath = "outputImages"
    outputImage = os.path.join(outputPath, (os.path.split(imagePath)[1]))
    cv2.imwrite(outputImage, Camera2Detection_im)
    cv2.imshow('img', Camera2Detection_im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
