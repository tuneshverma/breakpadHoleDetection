from imutils.object_detection import non_max_suppression
import numpy as np
import cv2
import time
import math
import sys
import os


def creating_contour(img):
    global diameter
    height, width, _ = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 31)
    ret, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_OTSU)
    canny = cv2.Canny(thresh, 75, 200)
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    contour_list = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)
        if 1000 < area < 15000:
            contour_list.append(contour)
            diameter = math.sqrt(area / 3.14)
            # print(dia)
    cv2.drawContours(img, contour_list, -1, (0, 255, 0), 2)

    return img, diameter


def Camera1Detection(inputImage, templateImage):

    im = cv2.imread(inputImage)
    im2 = im.copy()
    template = cv2.imread(templateImage, cv2.IMREAD_GRAYSCALE)
    (tH, tW) = template.shape[:2]

    height, width, _ = im.shape
    new_width = 800
    ratio = new_width / width  # (or new_height / height)
    new_height = int(height * ratio)
    im = cv2.resize(im, (new_width, new_height))
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 3)
    result = cv2.matchTemplate(blur, template, cv2.TM_CCOEFF_NORMED)
    (yCoords, xCoords) = np.where(result >= 0.8)
    # initialize our list of rectangles
    rects = []
    # loop over the starting (x, y)-coordinates again
    for (x, y) in zip(xCoords, yCoords):
        # update our list of rectangles
        rects.append((x, y, x + tW, y + tH))
    # apply non-maxima suppression to the rectangles
    pick = non_max_suppression(np.array(rects))
    dia_l = []
    for (startX, startY, endX, endY) in pick:
        if any(ele == 0 for ele in [startX, startY, endX, endY]):
            continue
        # draw the bounding box on the image
        startX_new = int(startX / ratio) - 15
        startY_new = int(startY / ratio) - 15
        endX_new = int(endX / ratio)
        endY_new = int(endY / ratio)
        box = im2[startY_new:endY_new, startX_new:endX_new]

        drawn_img, dia = creating_contour(box)
        dia_l.append(dia)
        image = cv2.rectangle(im2, (startX_new, startY_new), (endX_new, endY_new), (0, 255, 0), 2)
        # output_filename = str(startX_new)+"_"+str(startY_new) + '_blobs.jpg'
        # directory = 'C:/Users/tunes/Maxerience/image_processing/inputImages/sample_images/4515_New/ok/crops'
        # cv2.imwrite(os.path.join(directory, output_filename), drawn_img)

    return pick, im2, dia_l


if __name__ == '__main__':
    global diameter
    inputImage = sys.argv[1]
    templateImage = sys.argv[2]
    # outputPath = sys.argv[3]
    outputPath = "outputImages"
    outputImage = os.path.join(outputPath, (os.path.split(inputImage)[1]))
    s_time = time.time()
    Camera1Detection_pick, Camera1Detection_im2, dia_l = Camera1Detection(inputImage, templateImage)
    print("time taken", time.time() - s_time)
    cv2.imwrite(outputImage, Camera1Detection_im2)
    print("[INFO] {} matched locations".format(len(Camera1Detection_pick)))
    # print(Camera1Detection_pick)
    cv2.namedWindow("Resize", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Resize", 800, 750)
    cv2.imshow('Resize', Camera1Detection_im2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
