import win32gui
import win32api
import pyautogui  # 加入pyautogui库能让ImageGrab正常截屏
from PIL import ImageGrab
import cv2
import numpy as np
import time

blocks_x=19
blocks_y=11
m_differ=0.95

def Get_Hand(name):
    hwnd=win32gui.FindWindow(None,name)
    if hwnd:
        print("成功找到")
    else:
        print("没有找到窗口，请重试!")
        exit()
    win32gui.SetForegroundWindow(hwnd)
    left,top,right,bottom=win32gui.GetWindowRect(hwnd)
    return (hwnd,left,top,right,bottom)

def Get_Game(left,top,right,bottom):
    window_width = right - left
    window_height = bottom - top
    game_left = left + 14.0 / 800.0 * window_width
    game_right = left + 603 / 800.0 * window_width
    game_top = top + 181.0 / 600.0 * window_height
    game_bottom = top + 566 / 600.0 * window_height
    game_width = game_right - game_left
    game_height = game_bottom - game_top
    grid_width = game_width / blocks_x
    grid_height = game_height / blocks_y
    game_image = ImageGrab.grab((game_left, game_top, game_right, game_bottom))
    return (game_image,game_left,game_top,grid_width,grid_height)

def Image_get(game_image,grid_width,grid_height):
    M_Image = []
    for i in range(blocks_x):
        temp_M = []
        for j in range(blocks_y):
            temp_image = game_image.crop((i * grid_width, j * grid_height, (i + 1) * grid_width, (j + 1) * grid_height))
            temp_M.append(
                temp_image.crop((1 / 7 * grid_width, 1 / 7 * grid_height, 6 / 7 * grid_width, 6 / 7 * grid_height)))
        M_Image.append(temp_M)
    return M_Image

def Mark_M(x):
    start=0
    mark=[]
    hash_m=[]
    M=[]
    get_max=[]
    for i in range(blocks_x):
        M_T=[]
        for j in range(blocks_y):
            f=0
            x[i][j].save("test1.jpg")
            yuan=cv2.imread("test1.jpg")
            for k in hash_m:
                k.save("test2.jpg")
                bijiao=cv2.imread("test2.jpg")
                img1 = np.float32(yuan)
                img2 = np.float32(bijiao)
                first = np.ndarray.flatten(img1)
                second = np.ndarray.flatten(img2)
                differ = np.corrcoef(first, second)
                if differ[0, 1] < 0:
                    differ[0, 1] = -differ[0, 1]
                if differ[0, 1] > m_differ:
                    f = 1
                    M_T.append(mark[hash_m.index(k)])
                    get_max[mark[hash_m.index(k)]]+=1
                    break  # 合适时机跳出k循环
            if(f==0):
                get_max.append(1)
                mark.append(start)
                M_T.append(start)
                hash_m.append(x[i][j])
                start+=1
        M.append(M_T)
    kong=get_max.index(max(get_max))
    return M,kong

def oncecheck(M,kong,i,j,m,n):
    max_row = max(i, m)
    min_row = min(i, m)
    max_col = max(j, n)
    min_col = min(j, n)

    if max_row == min_row:
        for k in range(min_col+1, max_col):
            if M[i][k] != kong:
                return 0
        return 1
    elif max_col == min_col:
        for k in range(min_row+1, max_row):
            if M[k][j] != kong:
                return 0
        return 1
    return 0

def twice_check(M,kong,i,j,m,n):
    if oncecheck(M,kong,i,j,i,n) and oncecheck(M,kong,i,n,m,n) and M[i][n]==kong:
        return 1
    elif oncecheck(M,kong,i,j,m,j) and oncecheck(M,kong,m,j,m,n) and M[m][j]==kong:
        return 1
    else:
        return 0

def three_check(M,kong,i,j,m,n):
    for b in range(blocks_y):
        if b!=j and b!=n and oncecheck(M,kong,i,j,i,b) and twice_check(M,kong,i,b,m,n) and M[i][b]==kong:
            return 1
    for a in range(blocks_x):
        if a!=i and a!=m and oncecheck(M,kong,i,j,a,j) and twice_check(M,kong,a,j,m,n) and M[a][j]==kong:
            return 1
    return 0

def matching(M,kong,i,j,m,n):
    if i==m and j==n:
        return 0
    if oncecheck(M,kong,i,j,m,n):
        print("one",i,j,m,n)
        return 1
    elif twice_check(M,kong,i,j,m,n):
        print("two",i,j,m,n)
        return 1
    elif three_check(M,kong,i,j,m,n):
        print("three",i,j,m,n)
        return 1
    else:
        return 0

def show(M,kong):
    for j in range(blocks_y):
        for i in range(blocks_x):
            print(M[i][j], end=" ")
        print()
    print("kong ",kong)
    print("m_differ ",m_differ)

def On_Click(M,kong,game_left,game_top,grid_width,grid_height,i,j,m,n):
    pyautogui.click(game_left+grid_width*(i+0.5),game_top+grid_height*(j+0.5),1,0.01)
    pyautogui.click(game_left+grid_width*(m+0.5),game_top+grid_height*(n+0.5),1,0.01)
    M[i][j]=kong
    M[m][n]=kong

def start():
    name="QQ游戏 - 连连看角色版"
    hwnd,left,top,right,bottom=Get_Hand(name)
    game_image,game_left, game_top, grid_width, grid_height=Get_Game(left,top,right,bottom)
    M_Image=Image_get(game_image,grid_width,grid_height)
    M, kong = Mark_M(M_Image)
    show(M,kong)
    for j in range(blocks_y):
        for i in range(blocks_x):
            if M[i][j] != kong:
                for n in range(blocks_y):
                    for m in range(blocks_x):
                        if M[m][n] != kong and M[i][j] != kong and M[i][j] == M[m][n]:
                            if matching(M,kong,i, j, m, n):
                                On_Click(M,kong,game_left,game_top,grid_width,grid_height,i,j,m,n)

def main():
    start()

for i in range(4):
    main()
    print("#####################3")
    print()
    print()
    time.sleep(3)
    m_differ -= 0.04

