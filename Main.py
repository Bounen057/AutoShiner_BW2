import cv2
from matplotlib import pyplot as plt
import time
import serial

# VideoCapture オブジェクトを取得します
capture = cv2.VideoCapture(1)

# どの場面にいるか
# 0... フィールド
# 1... 遭遇直後の真っ黒な画面
# 2... 戦闘中(緑色の「ポケモン」が出てきたとき)
# 3... 逃げる後の真っ黒な画面
# 4... 色違い出現！
mode = 0 

# 時間測定
time_start = 0 # 開始
time_end = 0 # 終わり
time_span = 0  # 間の時間

# Serial
ser = serial.Serial('/dev/cu.usbmodem14201', 9600)
ser.write(b"0")

def main():
    while(True):
        change_mode()

        # 終了コマンド
        if cv2.waitKey(1) & 0xFF == ord('q'):
            ser.close()
            capture.release()
            cv2.destroyAllWindows()
            break

        # 色違い 判定
        if(mode == 2 and 11.0 <= time_span <= 14.0):
            mode = 4
            ser.write(b"4")
            print("Shiny! ♪~ 💃💃 🌵🐱🌵 💃💃 ~♪")

        # Debug 用メッセージ
        print(" ")    
        print("現在のモード: " + str(mode))
        print("間隔の時間: " + str(time_span))
        #    print("赤の画素数 : " + str(amount[0]))
        #    print("緑の画素数 : " + str(amount[1]))
        #    print("青の画素数 : " + str(amount[2]))


# 場面遷移
def change_mode():
    global mode
    ret, frame = capture.read()

    # 編集
    frame = cv2.resize(frame, (128, 128))
    cv2.imshow('frame',frame)

    img_1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    colors = ("r", "g", "b")
    amount = [0] * 3 # RGB
    for i, channel in enumerate(colors):
        histgram = cv2.calcHist([img_1], [i], None, [256], [0, 256])
        
        for j in range(200, 256):
            if channel == "r": color_number = 0
            if channel == "g": color_number = 1
            if channel == "b": color_number = 2
            amount[color_number] += histgram[j][0]

    # 今どの場面にいるか判定
    if(mode == 0):
        if (amount[0] <= 1000 and amount[1] <= 1000 and amount[2] <= 1000):
            timer()
            mode = 1
            ser.write(b"1")
            return

    if(mode ==1):
        if (amount[0] >= 1000 and amount[1] >= 4000 and amount[2] >= 1000):
            timer()
            mode = 2
            ser.write(b"2")
            return

    if(mode == 2):
        if (amount[0] <= 1000 and amount[1] <= 1000 and amount[2] <= 1000):
            timer()
            mode = 3
            ser.write(b"3")
            return
    
    if(mode==3):
        if (amount[0] >= 2000 and amount[1] >= 1000 and amount[2] >= 1000):
            timer()
            mode = 0
            ser.write(b"0")
            return

# 時間測定
def timer():
    global time_start, time_span, time_end
    time_end = time.time()
    time_span = time_end - time_start
    time_start = time.time()

    return