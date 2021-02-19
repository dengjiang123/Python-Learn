import win32gui
import win32api
import pyautogui  # 加入pyautogui库能让ImageGrab正常截屏
from PIL import ImageGrab
import cv2
import numpy as np

m_differ = 0.85

blocks_x = 19
blocks_y = 11
name = "QQ游戏 - 连连看角色版"
hwnd = win32gui.FindWindow(None, name)
if hwnd:
    print("成功找到")
else:
    print("没有找到窗口，请重试!")
    exit()

width = win32api.GetSystemMetrics(0)
height = win32api.GetSystemMetrics(1)
win32gui.SetForegroundWindow(hwnd, )
left, top, right, bottom = win32gui.GetWindowRect(hwnd)

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


def Image_Get():
    M_Image = []
    for i in range(blocks_x):
        temp_M = []
        for j in range(blocks_y):
            temp_image = game_image.crop((i * grid_width, j * grid_height, (i + 1) * grid_width, (j + 1) * grid_height))
            temp_M.append(
                temp_image.crop((1 / 10 * grid_width, 1 / 10 * grid_height, 9 / 10 * grid_width, 9 / 10 * grid_height)))

        M_Image.append(temp_M)
    return M_Image


M_Image = Image_Get()


def Mark_M(x):
    start = 0
    mark = []
    hash_m = []
    M = []
    get_max = []
    for i in range(blocks_x):
        M_T = []
        for j in range(blocks_y):
            f = 0
            x[i][j].save("test1.jpg")
            yuan = cv2.imread("test1.jpg")
            for k in hash_m:
                k.save("test2.jpg")
                bijiao = cv2.imread("test2.jpg")
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
                    get_max[mark[hash_m.index(k)]] += 1
                    break  # 合适时机跳出k循环
            if (f == 0):
                get_max.append(1)
                mark.append(start)
                M_T.append(start)
                hash_m.append(x[i][j])
                start += 1
        M.append(M_T)
    kong = get_max.index(max(get_max))
    return M, kong


M, kong = Mark_M(M_Image)

for j in range(blocks_y):
    for i in range(blocks_x):
        print(M[i][j], end=" ")
    print()

print(kong)


def oncecheck(i, j, m, n):
    max_row = max(i, m)
    min_row = min(i, m)
    max_col = max(j, n)
    min_col = min(j, n)

    if max_row == min_row:
        for k in range(min_col + 1, max_col):
            if M[i][k] != kong:
                return 0
        return 1
    elif max_col == min_col:
        for k in range(min_row + 1, max_row):
            if M[k][j] != kong:
                return 0
        return 1
    return 0


def twice_check(i, j, m, n):
    if oncecheck(i, j, i, n) and oncecheck(i, n, m, n) and M[i][n] == kong:
        return 1
    elif oncecheck(i, j, m, j) and oncecheck(m, j, m, n) and M[m][j] == kong:
        return 1
    else:
        return 0


def three_check(i, j, m, n):
    for b in range(blocks_y):
        if b != j and b != n and oncecheck(i, j, i, b) and twice_check(i, b, m, n) and M[i][b] == kong:
            return 1
    for a in range(blocks_x):
        if a != i and a != m and oncecheck(i, j, a, j) and twice_check(a, j, m, n) and M[a][j] == kong:
            return 1
    return 0


def matching(i, j, m, n):
    if i == m and j == n:
        return 0
    if oncecheck(i, j, m, n):
        print("one", i, j, m, n)
        return 1
    elif twice_check(i, j, m, n):
        print("two", i, j, m, n)
        return 1
    elif three_check(i, j, m, n):
        print("three", i, j, m, n)
        return 1
    else:
        return 0


def On_Click(i, j, m, n):
    pyautogui.click(game_left + grid_width * (i + 0.5), game_top + grid_height * (j + 0.5), 1, 0.01)
    pyautogui.click(game_left + grid_width * (m + 0.5), game_top + grid_height * (n + 0.5), 1, 0.01)
    M[i][j] = kong
    M[m][n] = kong


def test():
    for j in range(blocks_y):
        for i in range(blocks_x):
            if M[i][j] != kong:
                return 1
    return 0


while (test()):
    '''M_Image=Image_Get()
    M, kong = Mark_M(M_Image)
    m_differ+=0.01'''
    j = i = m = n = 0
    for j in range(blocks_y):
        for i in range(blocks_x):
            if M[i][j] != kong:
                for n in range(blocks_y):
                    for m in range(blocks_x):
                        if M[m][n] != kong and M[i][j] != kong and M[i][j] == M[m][n]:
                            if matching(i, j, m, n):
                                On_Click(i, j, m, n)

for j in range(blocks_y):
    for i in range(blocks_x):
        print(M[i][j], end=" ")
    print()

'''
def Get_V(x,i,j):
    return i+j

def Get_M_value():
    M=[]
    for i in range(blocks_x):
        temp=[]
        for j in range(blocks_y):
            temp.append(Get_V(M_Image[i][j],i,j))
        M.append(temp)
    return M

def judge(x1,x2):       #判断两图片相应指标是否一致
    maxdiffer=10
    if (x1-x2)<maxdiffer and (x1-x2)>=0:
        return 1
    elif (x2-x1)<maxdiffer and (x2-x1)>=0:
        return 1
    else:
        return 0



def dHash(img):
    # 缩放8*8
    img = cv2.resize(img, (9, 8), interpolation=cv2.INTER_CUBIC)
    # 转换灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hash_str = ''
    # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
    for i in range(8):
        for j in range(8):
            if gray[i, j] > gray[i, j + 1]:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str

def cmpHash(hash1, hash2):
    n = 0
    # hash长度不同则返回-1代表传参出错
    if len(hash1) != len(hash2):
        return -1
    # 遍历判断
    for i in range(len(hash1)):
        # 不相等则n计数+1，n最终为相似度
        if hash1[i] != hash2[i]:
            n = n + 1
    return n

def get_image_matrix():
    y_m=[]
    for j in range(blocks_y):
        x_m=[]
        for i in range(blocks_x):
            M_Image[i][j].save("test4.jpg","JPEG")
            img1 = cv2.imread("test4.jpg")
            hash_1 = dHash(img1)
            x_m.append(hash_1)
        y_m.append(x_m)
    return y_m

def M_mark(Mori,imax,jmax):
    start=0
    mark=[]
    hash_m=[]
    M=[]
    Max_diff=12
    f=0
    for i in range(jmax): #11
        M_T=[]
        for j in range(imax):   #19
            f=0
            for k in hash_m:
                dif=cmpHash(Mori[i][j],k)
                if dif<Max_diff:
                    M_T.append(mark[hash_m.index(k)])
                    f=1
            if(f==0):
                mark.append(start)
                M_T.append(start)
                hash_m.append(Mori[i][j])
                start+=1
                print(start)
        M.append(M_T)
    return M

matrix=get_image_matrix()

print(len(matrix),len(matrix[0]))
for i in range(blocks_y):
    for j in range(blocks_x):
        print(matrix[i][j],end=" ")
    print()

M=M_mark(matrix,blocks_x,blocks_y)

for i in range(blocks_y):
    for j in range(blocks_x):
        print(M[i][j],end=" ")
    print()

'''