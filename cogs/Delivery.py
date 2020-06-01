import os
import urllib.request

import cv2
import numpy as np


def get_image(url):
    urllib.request.urlretrieve(url, 'temp/image.jpg')
    img = cv2.imread('temp/image.jpg')
    y = 120
    h = 80
    x = 210
    w = 80
    img = img[y: y + h, x: x + w]
    path = 'temp/crop_image.jpg'
    cv2.imwrite(path, img)
    return path


def delivery(price_image):
    samples = np.loadtxt('data/detection_models/generalsamples.data', np.float32)
    responses = np.loadtxt('data/detection_models/generalresponses.data', np.float32)
    responses = responses.reshape((responses.size, 1))

    model = cv2.ml.KNearest_create()
    model.train(samples, cv2.ml.ROW_SAMPLE, responses)

    im = cv2.imread(price_image)
    im = cv2.bitwise_not(im)
    out = np.zeros(im.shape, np.uint8)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    numbers = []

    for cnt in contours:
        if cv2.contourArea(cnt) > 20:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if h > 35:
                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                roi = thresh[y:y + h, x:x + w]
                roismall = cv2.resize(roi, (10, 10))
                roismall = roismall.reshape((1, 100))
                roismall = np.float32(roismall)
                retval, results, neigh_resp, dists = model.findNearest(roismall, k=1)
                string = str(int((results[0][0])))
                cv2.putText(out, string, (x, y + h), 0, 1, (0, 255, 0))
                numbers.append(string)

    numbers.sort()

    try:
        os.remove('Bombola_bot/temp/image.jpg')
    except:
        pass
    return numbers
