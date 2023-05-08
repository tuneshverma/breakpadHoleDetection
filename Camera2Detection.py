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
        global edge, edge_V, DisHole_1_x, DisHole_2_x
        DisHole_1_x = None
        DisHole_2_x = None
        DisHole_1_y = None
        DisHole_2_y = None
        msg = False
        img = cv2.imread(inputImage, cv2.IMREAD_GRAYSCALE)
        # img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
        height, width = img.shape
        new_width = 1000
        ratio = new_width / width  # (or new_height / height)
        new_height = int(height * ratio)
        img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

        ret, thresh1 = cv2.threshold(img, 60, 255, cv2.THRESH_BINARY)
        ret, thresh2 = cv2.threshold(img, 30, 255, cv2.THRESH_BINARY)
        keypoints = self.detector.detect(img)
        holeCoorList = []

        for k in keypoints:
            x, y = int(k.pt[0]), int(k.pt[1])
            d = int(k.size)
            r = int(k.size / 2)
            cv2.circle(img, (int(k.pt[0]), int(k.pt[1])), int(k.size / 2), (255, 255, 255), -1)
            holeCoorList.append([x, y, d, r])
        try:
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

            stride = 1

            for i in range(0, portion_w):
                if (i * stride + kernal_w) >= portion_w:
                    break
                multi = kernal * imgPortion[0:kernal_h, i * stride:i * stride + kernal_w]
                array_sum = sum(sum(multi - compareKernal))
                if array_sum < 0:
                    edge = x + d + i * stride + int(kernal_w / 2)
                    cv2.line(img, (edge, 0), (edge, new_height), (255, 255, 255), 2)
                    break

            imgPortion_V = thresh2[0:y, edge - int(30):edge - 2]
            portion_h_V, portion_w_V = imgPortion_V.shape
            kernal_V = np.ones((14, 28))
            kernal_h_V, kernal_w_V = kernal_V.shape
            compareKernal_1_V = np.zeros((7, 28))
            compareKernal_2_V = np.ones((7, 28)) * 255
            compareKernal_V = np.concatenate((compareKernal_1_V, compareKernal_2_V), axis=0)
            for j in range(0, portion_h_V):
                if (j * stride + kernal_h_V) >= portion_h_V:
                    break
                multi_V = kernal_V * imgPortion_V[j * stride:j * stride + kernal_h_V, 0:kernal_w_V]
                array_sum_V = sum(sum(multi_V - compareKernal_V))
                # print(array_sum_V)
                if j == 0 and 0 < array_sum_V:
                    edge_V = 0
                    cv2.line(img, (0, edge_V), (new_width, edge_V), (255, 255, 255), 2)
                    break
                elif j != 0 and array_sum_V > 4500:
                    edge_V = j * stride + int(kernal_h_V / 2) - 5
                    cv2.line(img, (0, edge_V), (new_width, edge_V), (255, 255, 255), 2)
                    break

            DisHole_1_x = edge - holeCoorList[1][0]
            DisHole_2_x = edge - holeCoorList[0][0]

            DisHole_1_y = holeCoorList[1][1] - edge_V
            DisHole_2_y = holeCoorList[0][1] - edge_V

            cv2.putText(img, str(DisHole_1_x), (holeCoorList[1][0] + 60, holeCoorList[1][1]), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 255), 2)
            cv2.putText(img, str(DisHole_2_x), (holeCoorList[0][0] + 60, holeCoorList[0][1]), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 255), 2)
            cv2.line(img, (holeCoorList[1][0], y + 5), (edge, y + 5), (255, 255, 255), 2)
            cv2.line(img, (holeCoorList[0][0], y), (edge, y), (255, 255, 255), 2)

            cv2.putText(img, str(DisHole_1_y), (holeCoorList[1][0], holeCoorList[1][1] - 90), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 255), 2)
            cv2.putText(img, str(DisHole_2_y), (holeCoorList[0][0], holeCoorList[0][1] - 90), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 255), 2)
            cv2.line(img, (holeCoorList[1][0], edge_V), (holeCoorList[1][0], holeCoorList[1][1]), (255, 255, 255), 2)
            cv2.line(img, (holeCoorList[0][0], edge_V), (holeCoorList[0][0], holeCoorList[0][1]), (255, 255, 255), 2)

            if DisHole_1_x < DisHole_2_x:
                temp1 = DisHole_1_x
                temp2 = DisHole_1_y
                DisHole_1_x = DisHole_2_x
                DisHole_1_y = DisHole_2_y
                DisHole_2_x = temp1
                DisHole_2_y = temp2

            # print("DisHole_1", DisHole_1)
            # print("DisHole_2", DisHole_2)
        except:
            msg = True
            print("Either orientation is incorrect or there is no product")

        return img, DisHole_1_x, DisHole_2_x, DisHole_1_y, DisHole_2_y, msg


if __name__ == '__main__':
    global edge
    s_time = time.time()
    camera2detection = Camera2Detection()
    print("time for loading the things", time.time() - s_time)

    ss_time = time.time()
    imagePath = sys.argv[1]
    Camera2Detection_im, DisHole_1_x, DisHole_2_x, DisHole_1_y, DisHole_2_y, msg2 = \
        camera2detection.detection(imagePath)
    print("time for actual run", time.time() - ss_time)
    outputPath = "outputImages"
    print(msg2)
    outputImage = os.path.join(outputPath, (os.path.split(imagePath)[1]))
    cv2.imwrite(outputImage, Camera2Detection_im)
    cv2.imshow('img', Camera2Detection_im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
