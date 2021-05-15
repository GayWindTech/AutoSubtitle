import cv2
import os
import shutil
import numpy as np
import difflib

def ahash(image):
    image = cv2.resize(image, (8,8), interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    s = 0
    ahash_str = ''
    for i in range(8):
        for j in range(8):
            s = s+gray[i,j]
    avg = s/64
    ahash_str = ''
    for i in range(8):
        for j in range(8):
            if gray[i,j]>avg:
                ahash_str = ahash_str + '1'
            else:
                ahash_str = ahash_str + '0'
    result = ''
    for i in range(0, 64, 4):
        result += ''.join('%x' % int(ahash_str[i: i+4], 2))
    return result


def dhash(image):
    # 将图片转化为8*8
    image = cv2.resize(image,(9,8),interpolation=cv2.INTER_CUBIC )
    # 将图片转化为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    dhash_str = ''
    for i in range(8):
        for j in range(8):
            if gray[i,j]>gray[i, j+1]:
                dhash_str = dhash_str + '1'
            else:
                dhash_str = dhash_str + '0'
    result = ''
    for i in range(0, 64, 4):
        result += ''.join('%x'%int(dhash_str[i: i+4],2))
    # print("dhash值",result)
    return result


def phash(img):
    #加载并调整图片为32x32灰度图片
    img = cv2.resize(img, (32, 32), interpolation=cv2.INTER_CUBIC)
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
    return difflib.SequenceMatcher(None, str1, str2).quick_ratio()

#计算汉明距离

def hamming_distance(str1, str2):
    if len(str1) != len(str2):
        return 0
    count = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            count += 1
    return count

def frames_to_timecode(framerate,frames):
    """
    视频 通过视频帧转换成时间
    :param framerate: 视频帧率
    :param frames: 当前视频帧数
    :return:时间（00:00:01:01）
    """
    return '{0:02d}:{1:02d}:{2:02d}.{3:02d}'.format(int(frames / (3600 * framerate)),
                                                    int(frames / (60 * framerate) % 60),
                                                    int(frames / framerate % 60),
                                                    int(frames / framerate % 1 * 1000))


# 利用VideoCapture捕获视频，这里使用本地视频
cap = cv2.VideoCapture("Temp\\2.mp4")

# 是否成功打开视频
flag = 0
if cap.isOpened():
    flag = 1
else:
    flag = 0

# 视频帧总数
current_frame = 0

last_pic_hash = ''
last_frame = 0
begin_frame = 0

srt = ''
num = 1

if flag == 1:
    while True:
        ret, frame = cap.read()
        # 读取视频帧
        if ret == False:
            # 判断是否读取成功
            break

        current_pic = frame[950:1045,810:910]
        pic_current_hash = phash(current_pic)
        # print(pic_current_hash)
        diff_rate = get_equal_rate(last_pic_hash, pic_current_hash)
        hmdistant = hamming_distance(last_pic_hash,pic_current_hash)
        # print(hmdistant)

        # if((pic_current_hash != last_pic_hash) and (diff_rate < 0.8) and (current_frame != 0) and ((current_frame-last_frame) > 10) and not(current_frame in range(0,416))):
        if((pic_current_hash != last_pic_hash) and (hmdistant > 10) and (current_frame != 0) and ((current_frame-last_frame) > 10) and not(current_frame in range(0,0))):
            if(begin_frame == 0):
                begin_frame = current_frame - 1
            # print("区间: "+frames_to_timecode(29.97,begin_frame)+" - "+frames_to_timecode(29.97,current_frame))
            print(str(current_frame)+" : "+pic_current_hash+" | " +str(current_frame-1)+" : "+last_pic_hash+" | "+str(hmdistant)+" | diff: "+str(current_frame-last_frame)+" | Time: "+frames_to_timecode(29.97,current_frame-1))
            srt = srt + str(num) + "\n"
            srt = srt + frames_to_timecode(29.97,begin_frame) + " --> " + frames_to_timecode(29.97,current_frame) + "\n"
            srt = srt + "示范性字幕" + str(num) + "\n\n"
            num += 1
            begin_frame = current_frame
            last_frame = current_frame
            
        last_pic_hash = pic_current_hash
        pic = current_pic
        current_frame += 1


print("finish!")  # 提取结束，打印finish

with open("Temp\\2-phash.srt",'w+',encoding='utf-8') as q:
    q.write(srt)
