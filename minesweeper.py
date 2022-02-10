import cv2 as cv
import numpy as np
from PIL import ImageGrab
from time import sleep
import pyautogui

pyautogui.PAUSE = 0.001
print(pyautogui.PAUSE)
dx = [0, 1, 0, -1, 1, 1, -1, -1]
dy = [1, 0, -1, 0, 1, -1, 1, -1]
n = 16
m = 30
k = 99
a = [[0] * m for i in range(n)]
clicked = [[False] * m for i in range(n)]

def inbox(x, y):
    return (0 <= x < n and 0 <= y < m)

def find(img, temp, threshold=0.9):
    # r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
    r = img
    # tr, tg, tb = temp[:,:,0], temp[:,:,1], temp[:,:,2]
    tr = temp
    res_r = cv.matchTemplate(r, tr, cv.TM_CCOEFF_NORMED)
    # res_g = cv.matchTemplate(g, tg, cv.TM_CCOEFF_NORMED)
    # res_b = cv.matchTemplate(b, tb, cv.TM_CCOEFF_NORMED)
    res = res_r # * res_g * res_b
    loc = np.where(res >= threshold)
    return loc[1], loc[0]

def show(res_x, res_y):
    w, h = 17, 17
    for pt in zip(res_x, res_y):
        cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    cv.imwrite('res.png', img)

sleep(1)
img = np.array(ImageGrab.grab())
# print(img.shape)
# exit()
# img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
unknown = cv.imread("unknown.png")
unknown = cv.cvtColor(unknown, cv.COLOR_BGR2GRAY)
digits = []
for i in range(8):
    cur = cv.imread(str(i) + ".png")
    cur = cv.cvtColor(cur, cv.COLOR_BGR2GRAY)
    digits.append(cur)
cur = cv.imread("flag.png")
cur = cv.cvtColor(cur, cv.COLOR_BGR2GRAY)
digits.append(cur)
res_x, res_y = find(img, unknown, threshold=0.999)
min_x, max_x, min_y, max_y = -1, -1, -1, -1
print(len(res_x), len(res_y))
for pos in zip(res_x, res_y):
    if min_x == -1:
        min_x = max_x = pos[0]
        min_y = max_y = pos[1]
    min_x = min(min_x, pos[0])
    max_x = max(max_x, pos[0])
    min_y = min(min_y, pos[1])
    max_y = max(max_y, pos[1])
step = (max_x - min_x) // (m - 1)
print(min_x, max_x, min_y, max_y)
print(step)

def update():
    img = np.array(ImageGrab.grab())
    # img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
    img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    res_x, res_y = find(img, unknown, threshold=0.999)
    b = [[0] * m for i in range(n)]
    for pos in zip(res_x, res_y):
        y = (pos[0] - min_x + 4) // step
        x = (pos[1] - min_y + 4) // step
        b[x][y] = -2

    for i in range(1, 9):
        res_x, res_y = find(img, digits[i])
        for pos in zip(res_x, res_y):
            y = (pos[0] - min_x + 4) // step
            x = (pos[1] - min_y + 4) // step
            b[x][y] = i
            if i == 8:
                b[x][y] = -1

    for i in range(n):
        for j in range(m):
            if b[i][j] >= -1 and a[i][j] == -2:
                a[i][j] = b[i][j]

def click(i, j, right=False):
    button = "left"
    if right:
        button = "right"
    x = j * step + min_x + 7
    y = i * step + min_y + 7
    pyautogui.click(x=x, y=y, button=button)

def near(i1, j1, i2, j2):
    return (abs(i1 - i2) <= 1 and abs(j1 - j2) <= 1)

def calc(i, j):
    cnt = 0
    b = 0
    for k in range(len(dx)):
        ii = i + dx[k]
        jj = j + dy[k]
        if not inbox(ii, jj):
            continue
        if a[ii][jj] == -2:
            cnt += 1
        if a[ii][jj] == -1:
            b += 1
    return cnt, b

def easy():
    ch = False
    for i in range(n):
        for j in range(m):
            if a[i][j] == 0:
                continue
            cnt, b = calc(i, j)
            if b == a[i][j] and cnt > 0 and not clicked[i][j]:
                clicked[i][j] = True
                for k in range(len(dx)):
                    ii = i + dx[k]
                    jj = j + dy[k]
                    if inbox(ii, jj) and a[ii][jj] == -2:
                        click(ii, jj)
                        clicked[ii][jj] = True
                        ch = True
            elif a[i][j] - b == cnt:
                for k in range(len(dx)):
                    ii = i + dx[k]
                    jj = j + dy[k]
                    if inbox(ii, jj) and a[ii][jj] == -2:
                        click(ii, jj, right=True)
                        a[ii][jj] = -1
                        ch = True
    if ch:
        pyautogui.moveTo(10, 10)
    return ch

def hard():
    ch = False
    for i in range(n):
        for j in range(m):
            if a[i][j] < 1:
                continue
            for i2 in range(i - 2, i + 3):
                for j2 in range(j - 2, j + 3):
                    if i == i2 and j == j2:
                        continue
                    if not inbox(i2, j2) or a[i2][j2] < 1:
                        continue
                    cnt1, b1 = calc(i, j)
                    cnt2, b2 = calc(i2, j2)
                    y = 0
                    for kk in range(len(dx)):
                        i3 = i + dx[kk]
                        j3 = j + dy[kk]
                        if inbox(i3, j3) and a[i3][j3] == -2 and near(i2, j2, i3, j3):
                            y += 1
                    x = cnt1 - y
                    z = cnt2 - y
                    if x > 0 and a[i][j] - b1 - x == min(a[i2][j2] - b2, y):
                        for kk in range(len(dx)):
                            i3 = i + dx[kk]
                            j3 = j + dy[kk]
                            if inbox(i3, j3) and a[i3][j3] == -2 and not near(i2, j2, i3, j3):
                                click(i3, j3, right=True)
                                a[i3][j3] = -1
                                ch = True
                    if z > 0 and a[i][j] - b1 - x == a[i2][j2] - b2:
                        for kk in range(len(dx)):
                            i3 = i2 + dx[kk]
                            j3 = j2 + dy[kk]
                            if inbox(i3, j3) and a[i3][j3] == -2 and not near(i, j, i3, j3) and not clicked[i3][j3]:
                                click(i3, j3)
                                clicked[i3][j3] = True
                                ch = True
    if ch:
        pyautogui.moveTo(10, 10)
    return ch

def finished():
    cnt = 0
    b = 0
    for i in range(n):
        for j in range(m):
            if a[i][j] == -1:
                b += 1
            if a[i][j] == -2:
                cnt += 1
    return (b == k or cnt == 0)

def clear():
    for i in range(n):
        for j in range(m):
            if a[i][j] == -2:
                click(i, j)

if len(res_x) == n * m:
    click(n // 2, m // 2)
for pos in zip(res_x, res_y):
    y = (pos[0] - min_x + 4) // step
    x = (pos[1] - min_y + 4) // step
    a[x][y] = -2

for i in range(1, 9):
    res_x, res_y = find(img, digits[i])
    if i == 8:
        show(res_x, res_y)
    for pos in zip(res_x, res_y):
        y = (pos[0] - min_x + 4) // step
        x = (pos[1] - min_y + 4) // step
        a[x][y] = i
        if i == 8:
            a[x][y] = -1

while True:
    update()
    if finished():
        clear()
        break
    ch = easy() | hard()
    if ch:
        while ch:
            ch = easy() | hard()
    else:
        sleep(5)
