import GUI
import argparse
import sys

def getInput():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('videoTypeStr', type=str, help='视频类型，可接受的参数: flag wsw',choices=['flag', 'wsw'])
    parser.add_argument('openPath', type=str, help='输入视频文件路径')
    parser.add_argument('-o', type=str, default=None, required=False, help='输出字幕文件路径，默认输出为视频目录下同名ass文件')
    parser.add_argument('-s', type=str, default='new', required=False, help='flag系列OP类型，可接受：old、new，默认为new', choices=['old', 'new'])
    args = parser.parse_args()
    videoTypeStr = args.videoTypeStr
    videoSeries = args.s
    openPath = args.openPath
    savePath = args.o
    savePath = str(openPath).rstrip(str(openPath).split('.')[-1])+"ass" if savePath is None else savePath
    newOP = True if videoSeries == 'new' else False if args.s == 'old' else exit()
    videoType = 0 if videoTypeStr == 'flag' else 1 if videoTypeStr == 'wsw' else exit()
    return openPath, savePath, videoType, newOP

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
        autosub(inputList[0],inputList[1],inputList[3])
    elif(inputList[2]==1):
        from wsw import autosub
        autosub(inputList[0],inputList[1])
        
if __name__ == '__main__':
    main()