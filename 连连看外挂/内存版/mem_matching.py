import win32gui
import win32process
from ReadWriteMemory import ReadWriteMemory
import pyautogui

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
    for b in range(19):
        if b!=j and b!=n and oncecheck(M,kong,i,j,i,b) and twice_check(M,kong,i,b,m,n) and M[i][b]==kong:
            return 1
    for a in range(11):
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

def On_Click(M,kong,game_left,game_top,grid_width,grid_height,i,j,m,n):
    pyautogui.click(game_left + grid_width * (j + 0.5), game_top + grid_height * (i + 0.5), 1, 0.01)
    pyautogui.click(game_left + grid_width * (n + 0.5), game_top + grid_height * (m + 0.5), 1, 0.01)
    M[i][j]=kong
    M[m][n]=kong

def Get_Handle(game_name):
    handle = win32gui.FindWindow(None, game_name)
    if handle == 0:
        print("没有找到窗口!")
        exit(-1)
    win32gui.SetForegroundWindow(handle)
    return handle

def Get_M(handle):
    _, processID = win32process.GetWindowThreadProcessId(handle)
    memory = ReadWriteMemory()
    process = memory.get_process_by_id(processID)
    process.open()
    M=[]
    x=[]
    for i in range(11 * 19):
        pointer = process.get_pointer(0x00181c88 + 0x000187f4, offsets=(0x04, 0x08 + i))
        value = (process.read(pointer) & 0xff)
        x.append(value)
    for i in range(11):
        y=[]
        for j in range(19):
            y.append(x[i*19+j])
        M.append(y)
    return M

def Show_M(M):
    print("#"*40)
    print("输出矩阵: ")
    for i in range(11):
        for j in range(19):
            print("{:>{}}".format(M[i][j],3),end=" ")
        print()
    print("#"*40)

def Get_Game_Rect(handle):
    left, top, right, bottom = win32gui.GetWindowRect(handle)
    window_width = right - left
    window_height = bottom - top
    game_left = left + 14.0 / 800.0 * window_width
    game_right = left + 603 / 800.0 * window_width
    game_top = top + 181.0 / 600.0 * window_height
    game_bottom = top + 566 / 600.0 * window_height
    game_width = game_right - game_left
    game_height = game_bottom - game_top
    grid_width = game_width / 19
    grid_height = game_height / 11
    return (game_left, game_top, grid_width, grid_height)

if __name__ =="__main__":
    game_name="QQ游戏 - 连连看角色版"
    handle=Get_Handle(game_name)
    M=Get_M(handle)
    game_left, game_top, grid_width, grid_height=Get_Game_Rect(handle)
    kong=0
    for i in range(11):
        for j in range(19):
            if M[i][j] != kong:
                for m in range(11):
                    for n in range(19):
                        if M[m][n] != kong and M[i][j] != kong and M[i][j] == M[m][n]:
                            if matching(M,kong,i, j, m, n):
                                M[i][j]=M[m][n]=0
                                print(i,j,"       ",m,n)
                                Show_M(M)
                                On_Click(M,kong,game_left,game_top,grid_width,grid_height,i,j,m,n)


