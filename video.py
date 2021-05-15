import cv2
import os
import shutil
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

def get_equal_rate(str1, str2):
    return difflib.SequenceMatcher(None, str1, str2).quick_ratio()

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
cap = cv2.VideoCapture("1.mp4")
# 创建文件用来保存视频帧
# save_path = os.makedirs("tupian")

# 是否成功打开视频
flag = 0
if cap.isOpened():
    flag = 1
else:
    flag = 0

# 视频帧总数
i = 0
# 截图的图片命名
imgPath = ""

pic_hash = ''
diff_pic = 0
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
        pic_current_hash = ahash(current_pic)
        diff_rate = get_equal_rate(pic_hash, pic_current_hash)

        if(pic_current_hash != pic_hash and diff_rate < 0.8 and i != 0 and (i-diff_pic) > 10 and i > 416):

            print("区间: "+frames_to_timecode(29.97,begin_frame)+" - "+frames_to_timecode(29.97,i))
            srt = srt + str(num) + "\n"
            srt = srt + frames_to_timecode(29.97,begin_frame) + " --> " + frames_to_timecode(29.97,i) + "\n"
            srt = srt + "示范性字幕" + str(num) + "\n\n"
            num += 1

            begin_frame = i
            # print(str(i)+" : "+pic_current_hash+" | " +str(i-1)+" : "+pic_hash+" | "+str(diff_rate)+" | diff: "+str(i-diff_pic)+" | Time: "+frames_to_timecode(29.97,i-1))
            # print("前: "+str(i-1)+" | 后: "+str(i)+" | "+str(diff_rate)+" | diff: "+str(i-diff_pic)+" | 当前时间: "+frames_to_timecode(29.97,i-1))
            # cv2.imshow(str(i),pic)
            # cv2.waitKey(0)
            # cv2.destroyWindow(str(i))
            # cv2.imshow(str(i+1),current_pic)
            # cv2.waitKey(0)
            # cv2.destroyWindow(str(i+1))
            diff_pic = i
        else:
            last_frame = i
            
        pic_hash = pic_current_hash
        pic = current_pic = frame[950:1045,810:910]
        i += 1


        # print(pic_current_hash)
        # i += 1
        # 使用i为图片命名
        # imgPath = "tupian/%s.jpg" % str(i)
        # 将提取的视频帧存储进imgPath
        # cv2.imwrite(imgPath, frame)

print("finish!")  # 提取结束，打印finish

with open("1.srt",'w+',encoding='utf-8') as q:
    q.write(srt)