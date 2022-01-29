import cv2
import numpy as np
import os
import random
from pynput.mouse import Button, Controller
from windowcapture import WindowCapture

mouse = Controller()

wincap = WindowCapture('NoxPlayer')

def getrekt(filename, screenshot):
    ads1 = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    w = ads1.shape[1]
    h = ads1.shape[0]

    result = cv2.matchTemplate(screenshot, ads1, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    threshold = .85
    yloc, xloc = np.where(result >= threshold)

    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    #for rect in rectangles:
    #    rect.append(filename)

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

# # screen = cv2.imread('img/screen.png', cv2.IMREAD_UNCHANGED)
# # ads1 = cv2.imread('img/ads1.png', cv2.IMREAD_UNCHANGED)
# # w = ads1.shape[1]
# # h = ads1.shape[0]

# # result = cv2.matchTemplate(screen, ads1, cv2.TM_CCOEFF_NORMED)
# # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# # threshold = .80
# # yloc, xloc = np.where(result >= threshold)

# # rectangles = []
# # for (x, y) in zip(xloc, yloc):
# #     rectangles.append([int(x), int(y), int(w), int(h)])
# #     rectangles.append([int(x), int(y), int(w), int(h)])

# # rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
# # for (x, y, w, h) in rectangles:
# #     cv2.rectangle(screen, (x, y), (x + w, y + h), (0, 255, 255), 2)


# # cv2.imshow('Screen', screen)
# # cv2.waitKey()
# # cv2.destroyAllWindows()

# class BotState:
#     IN_MENU = 0
#     WATCHING = 1
#     CLOSING = 2
#     COLLECTING = 3

# state = BotState.IN_MENU
# while(True):
#     if cv2.waitKey(1) == ord('q'):
#         cv2.destroyAllWindows()
#         break
#     screenshot = wincap.get_screenshot()
#     screenshot = np.array(screenshot)

#     if state == BotState.IN_MENU:
        
#         #screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
#         adfiles = [filename for filename in os.listdir('.\\img\\') if filename.startswith("ads")]
#         rectangles = []
#         for adf in adfiles:
#             rects = getrekt('img\\'+ adf, screenshot)
#             rectangles.extend(rects)

#         if len(rectangles) > 0:            
#             (x, y, w, h) = random.choice(rectangles)
#             mouse.position = wincap.get_screen_position((x + w / 2, y + h / 2))
#             mouse.click(Button.left, 1)
#             state = BotState.WATCHING
#             continue

#     if state == BotState.WATCHING:

#         #проверяем не ругается ли что нет рекламы или не отдает ли награду сразу
#         rewardfiles = [filename for filename in os.listdir('.\\img\\') if filename.startswith("get")]
#         rectangles = []
#         for adf in rewardfiles:
#             rects = getrekt('img\\'+ adf, screenshot)
#             rectangles.extend(rects)

#         if len(rectangles) > 0:            
#             (x, y, w, h) = random.choice(rectangles)
#             mouse.position = wincap.get_screen_position((x + w / 2, y + h / 2))
#             mouse.click(Button.left, 1)
#             state = BotState.IN_MENU
#             continue
        
#         # ждем 30 секунд и ищем кнопку Х
#         if cv2.waitKey(30000) == ord('q'):
#             cv2.destroyAllWindows()
#             break
#         state = BotState.CLOSING
#         continue
        
#     if state == BotState.CLOSING:
#         xfiles = [filename for filename in os.listdir('.\\img\\') if filename.startswith("x")]
#         rectangles = []
#         for adf in xfiles:
#             rects = getrekt('img\\'+ adf, screenshot)
#             rectangles.extend(rects)

#         if len(rectangles) > 0:            
#             (x, y, w, h) = random.choice(rectangles)
#             mouse.position = wincap.get_screen_position((x + w / 2, y + h / 2))
#             mouse.click(Button.left, 1)
#             state = BotState.COLLECTING
#             continue

#     if state == BotState.COLLECTING:
#         rewardfiles = [filename for filename in os.listdir('.\\img\\') if filename.startswith("get")]
#         rectangles = []
#         for adf in rewardfiles:
#             rects = getrekt('img\\'+ adf, screenshot)
#             rectangles.extend(rects)

#         if len(rectangles) > 0:            
#             (x, y, w, h) = random.choice(rectangles)
#             mouse.position = wincap.get_screen_position((x + w / 2, y + h / 2))
#             mouse.click(Button.left, 1)
#             state = BotState.IN_MENU
#             continue

#         # for (x, y, w, h) in rectangles:
#         #     cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0, 255, 255), 2)

#         # cv2.imshow('Screen', screenshot)
#         # if cv2.waitKey(1) == ord('q'):
#         #     cv2.destroyAllWindows()
#         #     break


# print('Done.')

def getcolor(filename):
    if filename.startswith('ads'):
        return (0, 255,255)
    if filename.startswith('x'):
        return (255, 0, 0)
    return (255,255,255)

while(True):

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
        
    screenshot = wincap.get_screenshot()
    screenshot = np.array(screenshot)



    rectangles = []
    files = [filename for filename in os.listdir('.\\img\\')]
    for f in files:
        rects = getrekt('img\\'+ f, screenshot)
        for (x, y, w, h) in rects:
            cv2.rectangle(screenshot, (x, y), (x + w, y + h), getcolor(f), 2)
        rectangles.extend(rects)

    cv2.imshow('Screen', screenshot)

    if len(rectangles) > 0:            
        (x, y, w, h) = random.choice(rectangles)
        mouse.position = wincap.get_screen_position((x + w / 2, y + h / 2))
        mouse.click(Button.left, 1)
        if cv2.waitKey(32000) == ord('c'):
            continue