import cv2, pyautogui, mss, threading, time
import numpy as np


def capture_screen(res= (0, 0, 600, 1000)):

    with mss.mss() as sct:
        screenshot = sct.grab(res)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        coin = cv2.inRange(hsv, np.array([35, 100, 150]), np.array([70, 255, 255]))
        #bomb = cv2.inRange(hsv, np.array([0, 0, 50]), np.array([0, 0, 130]))

        # cv2.imwrite("A_Main.png", img)
        # cv2.imwrite("B_2HSV.png", hsv)
        # cv2.imwrite("C_Mask.png", coin)

        return coin

def find_green_areas(img):
    coins, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    centroids = []
    for coin in coins:
        M = cv2.moments(coin)
        if M["m00"] != 0:
            pos = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            centroids.append(pos)

    # img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    # img[:] = 0
    # cv2.drawContours(img, coins, -1, (0, 0, 255), 1)
    # cv2.imwrite(f"D_Edges.png", img)
    # [cv2.circle(img, pos, 5, (255, 255, 0), -1) for pos in centroids]
    # cv2.imwrite(f"E_Centroids.png", img) 

    return centroids

res = (0, 0, 600, 1000)

x = time.time()
while time.time() - x < 30:
    print(time.time() - x)
    coin = capture_screen(res)
    centroids = find_green_areas(coin)

    threads = []
    for pos in centroids:
        thread = threading.Thread(target=pyautogui.click, args=(pos[0], pos[1]))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()