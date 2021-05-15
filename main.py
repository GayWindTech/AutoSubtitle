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

# cv2.imshow("Img",img1)
# cv2.waitKey (0)

pic_list_len = len(os.listdir('tupian'))

pic_hash = ''

for each_pic in range(pic_list_len):
    # img = cv2.imread('tupian\\' + str(each_pic + 1) +".jpg",cv2.IMREAD_COLOR)[930:1360,555:1060]
    img = cv2.imread('tupian\\' + str(each_pic + 1) +".jpg",cv2.IMREAD_COLOR)[950:1045,810:910]
    # print(ahash(img))
    pic_current_hash = ahash(img)
    diff_rate = get_equal_rate(pic_hash, pic_current_hash)
    if(pic_current_hash != pic_hash and diff_rate < 0.8 and each_pic != 0):
        print(str(each_pic+1) + " : " + pic_current_hash + " | " +str(each_pic) + " : " + pic_hash + " | " + str(diff_rate))
        shutil.copyfile('tupian\\' + str(each_pic + 1) +".jpg", 'result\\' + str(each_pic + 1) +".jpg")
        shutil.copyfile('tupian\\' + str(each_pic) +".jpg", 'result\\' + str(each_pic) +".jpg")
    pic_hash = pic_current_hash
