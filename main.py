import cv2, re, webbrowser, validators
import numpy as np

from pyzbar.pyzbar import decode

vid = cv2.VideoCapture(0)
visited_urls = []


def url_extractor(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s(" \
            r")<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]  # get all urls in the data_string from the qr-code


def get_qr_data(img) -> list:
    qr_datas = []
    for qr in decode(img):
        draw_border(qr, img)
        data = qr.data.decode()
        if data:
            qr_datas.append(data)
    return qr_datas  # Get list of data property of all qr-codes in the image


def url_opener(datas: list) -> None:
    global visited_urls
    for data in datas:
        urls = url_extractor(data)
        for url in urls:
            if validators.url(url) and (url not in visited_urls):
                webbrowser.open_new(url)  # Open valid url in default browser
                visited_urls.append(url)  # Add to visited to avoid revisiting url


def draw_border(qr, img_, color=(240, 0, 240), thickness=5):
    pts = np.array([qr.polygon], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(img_, [pts], True, color, thickness)


while True:

    # Capture the video frame
    ret, img = vid.read()
    datas = get_qr_data(img)
    url_opener(datas)

    cv2.imshow('frame', img)  # Display the resulting frame

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Quit when 'q' is pressed
        break

    if cv2.waitKey(1) & 0xFF == ord('r'):  # Reset visited_urls for revisiting
        visited_urls = []

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
