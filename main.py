import cv2
import os
import shutil
import numpy as np
import difflib

opening = ['1000011010001100010000000000000000000000000000000000000000000000','1100100000010000110010111001011101100100001000000001001011000001']

def phash(img):
    #加载并调整图片为32x32灰度图片
    img = cv2.resize(img, (8, 8), interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img.astype(np.float32)
    #离散余弦变换
    img = cv2.dct(img)
    img = img[0:8, 0:8]
    avg = 0
    hash_str = ''
    #计算均值
    for i in range(8):
        for j in range(8):
            avg += img[i, j]
    avg = avg/64
    #获得hsah
    for i in range(8):
        for j in range(8):
            if img[i, j] > avg:
                hash_str = hash_str+'1'
            else:
                hash_str = hash_str+'0'
    return hash_str

def get_equal_rate(str1, str2):
    #字符相似度
    return difflib.SequenceMatcher(None, str1, str2).quick_ratio()

def get_color_rate(frame,lower,upper):
    # lower=np.array([100,130,216])
    # upper=np.array([110,255,255])
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    # res = cv2.bitwise_and(frame, frame, mask=mask)
    ratio_green = cv2.countNonZero(mask)/(frame.size/3)
    colorPercent = (ratio_green * 100)
    # print('green pixel percentage:', np.round(colorPercent, 2))
    return np.round(colorPercent, 2)

def hamming_distance(str1, str2):
    #计算汉明距离
    if len(str1) != len(str2):
        return 0
    count = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            count += 1
    return count

def isset(v): 
    try : 
        type (eval(v)) 
    except : 
        return  0  
    else : 
        return  1  


def frames_to_timecode(framerate,frames):
    # 视频 通过视频帧转换成时间|framerate: 视频帧率|frames: 当前视频帧数|return:时间（00:00:01.001）
    return '{0:02d}:{1:02d}:{2:02d}.{3:03d}'.format(int(frames / (3600 * framerate)),
                                                    int(frames / (60 * framerate) % 60),
                                                    int(frames / framerate % 60),
                                                    int(frames / framerate % 1 * 1000))

def get_people(img):
    mobuo_rate = get_color_rate(img,np.array([100,130,216]),np.array([110,255,255]))
    flag_rate = get_color_rate(img,np.array([30,140,240]),np.array([40,220,255]))
    if(mobuo_rate > 1):
        # print("mobuo")
        return "mobuo"
    elif(flag_rate > 1):
        # print("flag")
        return "flag"
    else:
        return "未定义"

source_video = cv2.VideoCapture("Temp\\大好.mp4")


# 视频帧总数
current_frame = 0
last_pic_hash = ''
last_frame = 0
begin_frame = 0
op = False
opt = 0
srt = ''
num = 1

# 是否成功打开视频
isOpened = False
if source_video.isOpened():
    isOpened = True

if isOpened:
    while True:
        ret, frame = source_video.read()
        # 读取视频帧
        if ret == False:
            # 判断是否读取成功
            break

        current_pic = frame[950:1045,810:910]
        pic_current_hash = phash(current_pic)
        if(opt != 2):
            match_op_pic = frame
            match_op_hash = phash(match_op_pic)
        if(match_op_hash in opening and opt != 2):
            op = bool(1 - op)
            opt += 1
            print(str(current_frame) + " | " + match_op_hash)
            srt = srt + str(num) + "\n"
            srt = srt + frames_to_timecode(24,begin_frame) + " --> " + frames_to_timecode(24,current_frame) + "\n"
            srt = srt + "op标记" + str(num) + "\n\n"
            num += 1
            begin_frame = current_frame
        if(op):
            current_frame += 1
            continue

        # print(pic_current_hash)
        diff_rate = get_equal_rate(last_pic_hash, pic_current_hash)
        hmdistant = hamming_distance(last_pic_hash,pic_current_hash)
        # print(hmdistant)

        # # if((pic_current_hash != last_pic_hash) and (diff_rate < 0.8) and (current_frame != 0) and ((current_frame-last_frame) > 10) and not(current_frame in range(0,416))):
        if((pic_current_hash != last_pic_hash) and (hmdistant > 10) and (current_frame != 0) and ((current_frame-last_frame) > 5) and not(current_frame in range(0,0))):
            if(begin_frame == 0):
                begin_frame = current_frame - 1
                pic = current_pic
            people = get_people(pic)
            print(str(current_frame)+" : "+pic_current_hash+" | " +str(current_frame-1)+" : "+last_pic_hash+" | "+str(hmdistant)+" | diff: "+str(current_frame-last_frame)+" | 区间: "+frames_to_timecode(24,begin_frame)+" - "+frames_to_timecode(24,current_frame))
            srt = srt + str(num) + "\n"
            srt = srt + frames_to_timecode(24,begin_frame) + " --> " + frames_to_timecode(24,current_frame) + "\n"
            srt = srt + "示范性字幕" + str(num) + people + "\n\n"
            num += 1
            begin_frame = current_frame
            last_frame = current_frame
            
        last_pic_hash = pic_current_hash
        pic = current_pic
        current_frame += 1


print("finish!")  # 提取结束，打印finish


with open("Temp\\大好.srt",'w+',encoding='utf-8') as q:
    q.write(srt)
