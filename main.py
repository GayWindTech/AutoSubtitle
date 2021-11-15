import GUI
import argparse
import sys

def getInput():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('videoTypeStr', type=str, help='视频类型,可接受的参数: flag wsw')
    parser.add_argument('openPath', type=str, help='输入视频文件路径')
    parser.add_argument('-o', type=str, default='output.ass', required=False, help='输出字幕文件路径,默认为output.ass')
    args = parser.parse_args()
    videoTypeStr = args.videoTypeStr
    openPath = args.openPath
    savePath = args.o
    if(videoTypeStr=='flag'):
        videoType = 0
    elif(videoTypeStr=='wsw'):
        videoType = 1
    return openPath,savePath,videoType

def main():
    if(len(sys.argv) > 1):
        print("当前为命令行模式")
        print('开始打轴...')
        inputList = getInput()
    else:
        print("当前为GUI模式")
        print("正在呼起GUI...")
        inputList = GUI.runGUI()
    if(inputList[2]==0):
        from flag import autosub
        autosub(inputList[0],inputList[1])
    elif(inputList[2]==1):
        from wsw import autosub
        autosub(inputList[0],inputList[1])
        
if __name__ == '__main__':
    main()