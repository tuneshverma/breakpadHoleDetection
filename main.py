import pandas as pd
import os
import cv2
import time
from Camera1Detection import Camera1Detection
from Camera2Detection import Camera2Detection


def resize(img, value):
    if len(img.shape)>2:
        height, width, _ = img.shape
    else:
        height, width = img.shape
    new_width = value
    ratio = new_width / width # (or new_height / height)
    new_height = int(height * ratio)
    img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    return img


def main(imagePath, templateImage, outputPath):

    lastIndex = None
    camera2detection = Camera2Detection()
    # while 
    s = time.time()
    csv = pd.read_csv("csv2.csv")

    lastEntry = csv.iloc[-1]
    lastIndex =  csv.index[-1]

    camera1 = os.path.join(imagePath, lastEntry["camera1"])
    camera2 = os.path.join(imagePath, lastEntry["camera2"])
    breakpadType = lastEntry["type"]

    # print(lastEntry["camera1"], lastEntry["camera2"], breakpadType)

    if breakpadType=="cam":
        numberOfHoles = 14
        camera1Detection_pick, camera1Detection_im = Camera1Detection(camera1, templateImage)
        
        if len(camera1Detection_pick)==numberOfHoles:
            outputImage1 = os.path.join(outputPath, (os.path.split(camera1)[1]))
            camera1Detection_im = resize(camera1Detection_im, 600)
            cv2.imwrite(outputImage1, camera1Detection_im)
            
            outputImage2 = os.path.join(outputPath, (os.path.split(camera2)[1]))
            camera2Detection_im, disHole_1, disHole_2 = camera2detection.detection(camera2)
            
            if 416<disHole_1<423 and 156<disHole_2<163:
    #             print("Number of holes matched, the breakpad is CAM, Distance from the edge is correct, position of holes are correct")
                result = "Number of holes matched, the breakpad is CAM, Distance from the edge is correct, position of holes are correct"
            else:
    #             print("Number of holes matched, the breakpad is CAM, Distance from the edge is wront, position of holes are wrong")
                result = "Number of holes matched, the breakpad is CAM, Distance from the edge is wrong, position of holes are wrong"
            camera2Detection_im = resize(camera2Detection_im, 500)
            cv2.imwrite(outputImage2, camera2Detection_im)
        else:
    #         print("Number of holes doesn't matched, the breakpad is not CAM")
            result = "Number of holes doesn't matched, the breakpad is not CAM"
            outputImage1 = os.path.join(outputPath, (os.path.split(camera1)[1]))
            camera1Detection_im = resize(camera1Detection_im, 600)
            cv2.imwrite(outputImage1, camera1Detection_im)

    elif breakpadType=="anchor":
        numberOfHoles = 16
        camera1Detection_pick, camera1Detection_im = Camera1Detection(camera1, templateImage)
        
        if len(camera1Detection_pick)==numberOfHoles:
            outputImage1 = os.path.join(outputPath, (os.path.split(camera1)[1]))
            camera1Detection_im = resize(camera1Detection_im, 600)
            cv2.imwrite(outputImage1, camera1Detection_im)
            
            outputImage2 = os.path.join(outputPath, (os.path.split(camera2)[1]))
            camera2Detection_im, disHole_1, disHole_2 = camera2detection.detection(camera2)
            
            if 482<disHole_1<489 and 182<disHole_2<189:
    #             print("Number of holes matched, the breakpad is ANCHOR, Distance from the edge is correct, position of holes are correct")
                result = "Number of holes matched, the breakpad is ANCHOR, Distance from the edge is correct, position of holes are correct"
            else:
    #             print("Number of holes matched, the breakpad is ANCHOR, Distance from the edge is wront, position of holes are wrong")
                result = "Number of holes matched, the breakpad is ANCHOR, Distance from the edge is wrong, position of holes are wrong"
            camera2Detection_im = resize(camera2Detection_im, 500)
            cv2.imwrite(outputImage2, camera2Detection_im)
        else:
    #         print("Number of holes doesn't matched, the breakpad is not ANCHOR")
            result = "Number of holes doesn't matched, the breakpad is not ANCHOR"
            outputImage1 = os.path.join(outputPath, (os.path.split(camera1)[1]))
            camera1Detection_im = resize(camera1Detection_im, 600)
            cv2.imwrite(outputImage1, camera1Detection_im)
    else:
    #     print("Breadpad Type not defined")
        result = "Breadpad Type not defined"

    print(time.time()-s)

    data = {
        'camera1': [lastEntry["camera1"]],
        'camera2': [lastEntry["camera2"]],
        'result': [result],
    }
     
    # Make data frame of above data
    df = pd.DataFrame(data)
     
    # append data frame to CSV file
    df.to_csv('results.csv', mode='a', index=False, header=False)

    return None


if __name__="__main__":
    imagePath = "C:/Users/tunes/Maxerience/image_processing/version_2/inputImage"
    templateImage = "version_2/template.png"
    outputPath = "C:/Users/tunes/Maxerience/image_processing/version_2/outputImages"

    main(imagePath, templateImage, outputPath)

