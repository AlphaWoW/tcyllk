from pywinauto.application import Application
from PIL import Image
import cv2
import numpy as np
import zfdfs
import time
import pyautogui
import os
import random

#apppath = r'C:\Program Files (x86)\GameChannel\cjlk\cjlk.exe'

#app = Application().connect(path = apppath)
#app.top_window().set_focus().CaptureAsImage().save(r'img.png')  # caption window image using pywinauto

#img = Image.open('img.png')

#img.show()





## Read the images from the file
#small_image = cv2.imread('small.png', 0)
#large_image = cv2.imread('img.png', 0)
#bgimg = cv2.imread('bg0.png', 0)

#result = cv2.matchTemplate(bgimg, large_image, method)
#minV, maxV, minL, maxL = cv2.minMaxLoc(result)

#w, h = bgimg.shape[::-1]
#cv2.rectangle(large_image, minL, (minL[0]+w, minL[1]+h), (0,0,0), 10)
#cv2.imshow('output', large_image)
#cv2.waitKey(0)

#threshold = 0.05
#loc = np.where(result < threshold)
#for pt in zip(*loc[::-1]):
#    cv2.rectangle(large_image, pt, (pt[0]+w, pt[1]+h), (0,0,0), 10)

#large_image_res = large_image.copy()
#for small_image in templates:
#    result = cv2.matchTemplate(small_image, large_image, method)

#    # Step 2: Get the size of the template. This is the same size as the match.
#    w, h = small_image.shape[::-1]

#    threshold = 0.1
#    loc = np.where(result < threshold)
#    for pt in zip(*loc[::-1]):
#        cv2.rectangle(large_image_res, pt, (pt[0]+w, pt[1]+h), (0,0,0), 10)

## Display the original image with the rectangle around the match.
#cv2.imshow('output',large_image_res)

## The image is only displayed if we call this
#cv2.waitKey(0)

fuck = False

def solve_all():
    ###########开始干活
    # 常量定义
    ROWCNT = 12
    COLCNT = 18
    method = cv2.TM_SQDIFF_NORMED

    # 连接游戏
    apppath = r'C:\Program Files (x86)\GameChannel\cjlk\cjlk.exe'
    if not os.path.exists(apppath):
        apppath = r'C:\Game\GameChannel\cjlk\cjlk.exe'

    app = Application().connect(path = apppath)
    game_window = app.top_window()
    game_window.set_focus()
    game_window.CaptureAsImage().save(r'img.png')  # caption window image using pywinauto

    # 载入游戏画面
    window_image = cv2.imread('img.png', 0)

    ga_top = 307 + 10
    ga_left = 365 + 6
    ga_width = 684
    ga_height = 504
    grid_width = ga_width // COLCNT
    grid_height = ga_height // ROWCNT

    # 读取连连看区域
    game_image = window_image[ga_top:ga_top+ga_height, ga_left:ga_left+ga_width]
    cv2.imwrite('game_area.png', game_image)

    templates = []

    # 读取所有 模板图片
    img = cv2.imread('brick0ex.png', 0)
    w, h = img.shape[::-1]
    print(w, h)
    # 获取所有 模板图片 保存在 templates 列表中
    cnt = 0
    for x in range(0, w, 42):
        for y in range(0, h, 46):
            if cnt == 3 or cnt == 9:
                imgtpl = img[y + 9:y - 14 + 46, x + 7:x - 6 + 42]
            elif cnt == 12:
                imgtpl = img[y + 10:y - 8 + 46, x + 12:x - 4 + 42]
            elif cnt == 38:
                imgtpl = img[y+10:y-14+46, x+9:x-10+42]
            else:
                imgtpl = img[y+3:y-6+46, x+7:x-2+42]
            templates.append(imgtpl)
            cv2.imwrite('img\z_img%d.png' % cnt, imgtpl)
            cnt = cnt + 1

    game_box = [[-1 for col in range(COLCNT)] for row in range(ROWCNT)]
    #for row in range(ROWCNT):
    #    game_box[row] = []
    #    for col in range(COLCNT):
    #        game_box[row][col] = 0

    def get_index(x, y):
        return x // grid_width, y // grid_height
    def get_position(col, row):
        return col * grid_width + grid_width // 2 + ga_left, row * grid_height + grid_height // 2 + ga_top

    # 在当前图片中建立矩阵
    game_image_res = game_image.copy()
    grid_idx = 0
    for small_image in templates:
        result = cv2.matchTemplate(small_image, game_image, method)

        # Step 2: Get the size of the template. This is the same size as the match.
        w, h = small_image.shape[::-1]

        if grid_idx == 12:
            threshold = 0.06
        elif grid_idx == 3 or grid_idx == 9:
            threshold = 0.05
        else:
            threshold = 0.04
        loc = np.where(result < threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(game_image_res, pt, (pt[0]+w, pt[1]+h), (0,0,0), 2)
            cv2.putText(game_image_res, '%d' % (grid_idx), (pt[0]+w//2-6, pt[1]+h//2), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2)
            col, row = get_index(pt[0]+w//2, pt[1]+h//2)
            game_box[row][col] = grid_idx

        grid_idx = grid_idx + 1

    cv2.imwrite('game_area_res.png', game_image_res)

    print(game_box)

    def click_item(row, col):
        x, y = get_position(col, row)
        pyautogui.moveTo(x, y)
        pyautogui.click()

        #game_window.ClickInput(coords=(x,y))
        #game_window.ClickInput(coords=(x,y))

    grid_cnt = 0
    for i in range(ROWCNT):
        for j in range(COLCNT):
            if (game_box[i][j] != -1) and (game_box[i][j] != 38):
                grid_cnt += 1
    cnt = 0
    global fuck
    fuck = False
    while grid_cnt:
        check_cnt = 0
        print(grid_cnt)
        for i1 in range(ROWCNT):
            for j1 in range(COLCNT):
                for i2 in range(ROWCNT):
                    for j2 in range(COLCNT):
                        # if (game_box[i1][j1] == 12):
                        #     continue
                        # if (game_box[i2][j2] == 12):
                        #     continue

                        if not (i1 == i2 and j1 == j2) and (game_box[i1][j1] > -1) and (game_box[i2][j2] > -1) and (game_box[i1][j1] != 38) and (game_box[i2][j2] != 38) and  game_box[i1][j1] and game_box[i2][j2] and (game_box[i1][j1] == game_box[i2][j2]) and zfdfs.is_connected(game_box, i1, j1, i2, j2):
                            check_cnt += 1
                            print(i1, j1, i2, j2, '--', game_box[i1][j1], game_box[i2][j2])
                            click_item(i1, j1)
                            click_item(i2, j2)
                            if not fuck:
                                time.sleep(random.randint(1, 100) / 100)

                            game_box[i1][j1] = game_box[i2][j2] = -1
                            cnt += 1
                            grid_cnt -= 2
                            if cnt > random.randint(8, 18):
                                cnt = 0
                                if not fuck:
                                    time.sleep(2)

                            yield

        if check_cnt == 0:
            break
