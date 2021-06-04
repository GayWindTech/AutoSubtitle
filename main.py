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
    mobuo_rate = get_color_rate(img,np.array([100,185,225]),np.array([110,225,255]))
    flag_rate = get_color_rate(img,np.array([27,155,240]),np.array([37,215,255]))
    if(mobuo_rate > 0.2):
        # print("mobuo")
        return "mobuo"
    elif(flag_rate > 0.2):
        # print("flag")
        return "flag"
    else:
        return "未定义"

source_video = cv2.VideoCapture("Temp\\z.mp4")


# 视频帧总数
current_frame_num = 0
last_pic_hash = ''
last_frame = 0
begin_frame_num = 0
op = False
op_match_times = 0
srt = ''
num = 1
switch = False

# 是否成功打开视频
isOpened = False
if source_video.isOpened():
    isOpened = True

if isOpened:
    while True:
        ret, frame = source_video.read()
        if ret == False:
            break

        current_pic = frame[950:1045,810:910]
        pic_current_hash = phash(current_pic)
        if(op_match_times < 2):
            match_op_pic = frame
            match_op_hash = phash(match_op_pic)
        if(match_op_hash in opening and op_match_times < 2):
            op = bool(1 - op)
            op_match_times += 1
            print(str(current_frame_num) + " | " + match_op_hash)
            srt = srt + str(num) + "\n"
            srt = srt + frames_to_timecode(24,begin_frame_num) + " --> " + frames_to_timecode(24,current_frame_num) + "\n"
            srt = srt + "op标记" + str(num) + "\n\n"
            num += 1
            begin_frame_num = current_frame_num
        if(op):
            current_frame_num += 1
            continue
            
            
        hmdistant = hamming_distance(last_pic_hash,pic_current_hash)
            
        if(current_frame_num == 0):
            people_hash = people_pic = frame[940:1060,360:1540]
        if(people_hash == '1010010011000000101010001100000001000100000001011000011010100000'):
            switch = True
            # cv2.imshow("zc",people_pic)
            # cv2.waitKey(0)


        if((pic_current_hash != last_pic_hash) and (hmdistant > 10) and (current_frame_num != 0) and ((current_frame_num-last_frame) > 5)):
            if(begin_frame_num == 0):
                frame_rate = round(source_video.get(5),2)
                begin_frame_num = current_frame_num - 1
                people_pic = frame[940:1060,360:1540]
                people_hash = phash(people_pic)

            people = get_people(people_pic)
            if(switch):
                people = "转场"
                switch = False

            # print(str(current_frame_num)+" : "+pic_current_hash+" | " +str(current_frame_num-1)+" : "+last_pic_hash+" | "+str(hmdistant)+" | gap: "+str(current_frame_num-last_frame)+" | 区间: "+frames_to_timecode(24,begin_frame_num)+" - "+frames_to_timecode(24,current_frame_num))
            print(str(current_frame_num) + " --> " + str(current_frame_num-1) + " | hmdst: " + str(hmdistant)+" | gap: "+str(current_frame_num-last_frame)+" | "+frames_to_timecode(frame_rate,begin_frame_num)+" --> "+frames_to_timecode(frame_rate,current_frame_num) + " | people: " + people)
            srt = srt + str(num) + "\n"
            srt = srt + frames_to_timecode(frame_rate,begin_frame_num) + " --> " + frames_to_timecode(frame_rate,current_frame_num) + "\n"
            srt = srt + "示范性字幕" + str(num) + people + "\n\n"
            num += 1
            
            begin_frame_num = current_frame_num
            last_frame = current_frame_num
            
        last_pic_hash = pic_current_hash
        people_pic = frame[940:1060,360:1540]
        people_hash = phash(people_pic)
        current_frame_num += 1


print("finish!")




with open("Temp\\z.srt",'w+',encoding='utf-8') as q:
    q.write(srt)
