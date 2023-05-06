import pandas as pd
import os
import cv2
import time
import json
from Camera1Detection import Camera1Detection
from Camera2Detection import Camera2Detection


def resize(img, value):
    if len(img.shape) > 2:
        height, width, _ = img.shape
    else:
        height, width = img.shape
    new_width = value
    ratio = new_width / width  # (or new_height / height)
    new_height = int(height * ratio)
    img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    return img


def main(config):
    global msg, referenceD1Range, referenceD2Range, diameter_l

    status = None
    referenceD1Range = None
    referenceD2Range = None
    calculatedD1 = None
    calculatedD2 = None
    detectedHoles = None
    templateImage = config["templateImage"]
    imagePath = config["imagePath"]
    outputPath = config["outputPath"]
    csv_path = config["csv_path"]
    csv_output = config["csv_output"]
    HoleDiameterReferenceRange = config["HoleDiameterReferenceRange"]
    numberOfHoles_4707 = config["numberOfHoles_4707"]
    referenceDistance1Range_4707_CAM = config["referenceDistance1Range_4707_CAM"]
    referenceDistance2Range_4707_CAM = config["referenceDistance2Range_4707_CAM"]
    referenceDistance1Range_4707_ANCHOR = config["referenceDistance1Range_4707_ANCHOR"]
    referenceDistance2Range_4707_ANCHOR = config["referenceDistance2Range_4707_ANCHOR"]
    numberOfHoles_4515 = config["numberOfHoles_4515"]
    referenceDistance1Range_4515_CAM = config["referenceDistance1Range_4515_CAM"]
    referenceDistance2Range_4515_CAM = config["referenceDistance2Range_4515_CAM"]
    referenceDistance1Range_4515_ANCHOR = config["referenceDistance1Range_4515_ANCHOR"]
    referenceDistance2Range_4515_ANCHOR = config["referenceDistance2Range_4515_ANCHOR"]

    old_lastIndex = -1
    counter = 0
    camera2detection = Camera2Detection()

    while True:
        startTime = time.time()
        csv = pd.read_csv(csv_path)
        if len(csv) == 0:
            continue
        lastEntry = csv.iloc[-1]
        new_lastIndex = csv.index[-1]
        if new_lastIndex <= old_lastIndex:
            continue
        old_lastIndex = new_lastIndex
        camera1 = os.path.join(imagePath, lastEntry["camera1"])
        camera2 = os.path.join(imagePath, lastEntry["camera2"])
        breakpadType = lastEntry["type"].split(" ")[0]
        breakpadType2 = lastEntry["type"].split(" ")[-1]

        if breakpadType == "4707":
            numberOfHoles = numberOfHoles_4707
            camera1Detection_pick, camera1Detection_im, diameter_l = Camera1Detection(camera1, templateImage)
            detectedHoles = len(camera1Detection_pick)
            if detectedHoles == numberOfHoles:
                diameterResultList = []
                for diameter in diameter_l:
                    if HoleDiameterReferenceRange[0] <= diameter <= HoleDiameterReferenceRange[1]:
                        diameterResultList.append(True)
                    else:
                        diameterResultList.append(False)
                if not all(diameterResultList):
                    msg = "Number of holes matched, diameters are not correct, the breakpad is not 4707"
                    status = "Fail"
                else:
                    msg = "Number of holes matched, diameters are correct, the breakpad is 4707"
                    status = "Pass"
            else:
                msg = "Number of holes doesn't matched, the breakpad is not 4707"
                status = "Fail"

            outputImage1 = os.path.join(outputPath, (os.path.split(camera1)[1]))
            camera1Detection_im = resize(camera1Detection_im, 600)
            cv2.imwrite(outputImage1, camera1Detection_im)

            if breakpadType2 == "CAM":
                referenceD1Range = referenceDistance1Range_4707_CAM
                referenceD2Range = referenceDistance2Range_4707_CAM
                msg = f"{msg} CAM, "
            elif breakpadType2 == "ANCHOR":
                referenceD1Range = referenceDistance1Range_4707_ANCHOR
                referenceD2Range = referenceDistance2Range_4707_ANCHOR
                msg = f"{msg} ANCHOR, "
            else:
                msg = f"{msg} breakpadType2 (CAM or ANCHOR) is not defined, "

            camera2Detection_im, disHole_1, disHole_2 = camera2detection.detection(camera2)
            calculatedD1 = disHole_1
            calculatedD2 = disHole_2

            if referenceD1Range[0] <= disHole_1 <= referenceD1Range[1] and referenceD2Range[0] <= disHole_2 <= \
                    referenceD2Range[1]:
                msg = f"{msg}Distance from the edge is correct, position of holes are correct"
            else:
                msg = f"{msg}Distance from the edge is wrong, position of holes are wrong"
                status = "Fail"

            outputImage2 = os.path.join(outputPath, (os.path.split(camera2)[1]))
            camera2Detection_im = resize(camera2Detection_im, 500)
            cv2.imwrite(outputImage2, camera2Detection_im)

        elif breakpadType == "4515":
            numberOfHoles = numberOfHoles_4515
            camera1Detection_pick, camera1Detection_im, diameter_l = Camera1Detection(camera1, templateImage)
            detectedHoles = len(camera1Detection_pick)
            if detectedHoles == numberOfHoles:
                diameterResultList = []
                for diameter in diameter_l:
                    if HoleDiameterReferenceRange[0] <= diameter <= HoleDiameterReferenceRange[1]:
                        diameterResultList.append(True)
                    else:
                        diameterResultList.append(False)
                if not all(diameterResultList):
                    msg = "Number of holes matched, diameters are not correct, the breakpad is not 4515"
                    status = "Fail"
                else:
                    msg = "Number of holes matched, diameters are correct, the breakpad is 4515"
                    status = "Pass"
            else:
                msg = "Number of holes doesn't matched, the breakpad is not 4515"
                status = "Fail"

            outputImage1 = os.path.join(outputPath, (os.path.split(camera1)[1]))
            camera1Detection_im = resize(camera1Detection_im, 600)
            cv2.imwrite(outputImage1, camera1Detection_im)

            if breakpadType2 == "CAM":
                referenceD1Range = referenceDistance1Range_4515_CAM
                referenceD2Range = referenceDistance2Range_4515_CAM
                msg = f"{msg} CAM, "
            elif breakpadType2 == "ANCHOR":
                referenceD1Range = referenceDistance1Range_4515_ANCHOR
                referenceD2Range = referenceDistance2Range_4515_ANCHOR
                msg = f"{msg} ANCHOR, "
            else:
                msg = f"{msg} breakpadType2 (CAM or ANCHOR) is not defined, "

            camera2Detection_im, disHole_1, disHole_2 = camera2detection.detection(camera2)
            calculatedD1 = disHole_1
            calculatedD2 = disHole_2

            if referenceD1Range[0] <= disHole_1 <= referenceD1Range[1] and referenceD2Range[0] <= disHole_2 <= \
                    referenceD2Range[1]:
                msg = f"{msg}Distance from the edge is correct, position of holes are correct"
            else:
                msg = f"{msg}Distance from the edge is wrong, position of holes are wrong"
                status = "Fail"

            outputImage2 = os.path.join(outputPath, (os.path.split(camera2)[1]))
            camera2Detection_im = resize(camera2Detection_im, 500)
            cv2.imwrite(outputImage2, camera2Detection_im)
        else:
            msg = "BreakPad Type (4707 or 4515) not defined"
            breakpadType = None

        data = dict(Parameters=['Model', 'Status', 'DetectedHoles', 'HoleDiameterReferenceRange', 'ReferenceD1Range',
                                'ReferenceD2Range', 'CalculatedD1', 'CalculatedD2', 'HoleDiameters', 'Message'],
                    Data=[breakpadType, status, detectedHoles, HoleDiameterReferenceRange, referenceD1Range,
                          referenceD2Range, calculatedD1, calculatedD2, diameter_l, msg])

        df = pd.DataFrame(data)
        fileName = "_".join((lastEntry["camera1"]).split("_")[:-1])
        result_csv = f"{csv_output}/{breakpadType}_{fileName}.csv"
        df.to_csv(result_csv, mode='a', index=False)
        counter += 1
        endTime = time.time()
        print(f"Time taken to process {counter} breakPad -->", endTime-startTime)

    return None


if __name__ == "__main__":
    global msg, referenceD1Range, referenceD2Range, diameter_l
    configFilePath = "config.json"
    configFile = open(configFilePath)
    config = json.load(configFile)
    print(config)
    print("Processing has started ...")
    main(config)
