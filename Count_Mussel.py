import numpy as np
import cv2 as cv

class CountMussel:
    def __init__(self, img,
                 min_aspect_ratio=0.95,
                 max_aspect_ratio=1.05):
        self.img_copy = img.copy()
        self.height = img.shape[0]
        self.width = img.shape[1]
        self.min_aspect_ratio = min_aspect_ratio
        self.max_aspect_ratio = max_aspect_ratio

    def bgr2gray(self):
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        return img_gray

    def findCont(self):
        img_gray = self.bgr2gray()
        _, thresh = cv.threshold(img_gray, 240, 255, cv.THRESH_BINARY)
        contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        return contours

    def find_square(self):
        contours = self.findCont()
        for c in contours:
            approx = cv.approxPolyDP(c, 0.005 * cv.arcLength(c, True), True)
            cv.drawContours(self.img_copy, [approx], 0, (0, 0, 255), 1)  # kalınlığı -1 yapınca içini dolduruyor :D
            approx_array = approx.ravel()

            if len(approx) == 4:
                x1, y1, w, h = cv.boundingRect(approx)
                aspect_ratio = float(w) / float(h)

                if aspect_ratio >= self.min_aspect_ratio and aspect_ratio <= self.max_aspect_ratio:
                    i = 0
                    point_list = []
                    for _ in approx_array:
                        if (i % 2 == 0):
                            x = approx_array[i]
                            y = approx_array[i + 1]
                            point_list.append([x, y])
                        i = i + 1
                    return point_list
                else:
                    continue
            else:
                continue

    def point_crop_image(self):
        point_list = self.find_square()
        mask = np.zeros((self.height, self.width), dtype=np.uint8)
        points = np.array([
            point_list
        ])

        cv.fillPoly(mask, points, (255))

        res = cv.bitwise_and(img, img, mask=mask)

        rect = cv.boundingRect(points)  # returns (x,y,w,h) of the rect
        cropped = res[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]

        return res

    def count_mussels(self, param1, param2):
        img_count = self.point_crop_image()
        gray = cv.cvtColor(img_count, cv.COLOR_BGR2GRAY)
        minDist = 1
        minRadius = 0
        maxRadius = 10  # 10
        circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, minDist, param1=param1, param2=param2,
                                  minRadius=minRadius,
                                  maxRadius=maxRadius)
        counter = 0
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                cv.circle(img_count, (i[0], i[1]), i[2], (0, 255, 0), 2)
                counter = counter + 1

        return counter, img_count


def tracker():
    cv.namedWindow("Parameters")
    cv.resizeWindow("Parameters", 640, 240)
    cv.createTrackbar("Param1", "Parameters", 210, 500, lambda x: x)
    cv.createTrackbar("Param2", "Parameters", 20, 200, lambda x: x)
    return cv

tracker_cv = tracker()
img = cv.imread("mussel_square.png")
while True:
    param1 = tracker_cv.getTrackbarPos("Param1", "Parameters")
    param2 = tracker_cv.getTrackbarPos("Param2", "Parameters")

    if (cv.waitKey(1) & 0xFF) == ord("q"):
        break

    sayi, img_count = CountMussel(img).count_mussels(param1, param2)

    print(sayi)
    cv.imshow("image", img)
    cv.imshow("count", img_count)

cv.destroyAllWindows()
