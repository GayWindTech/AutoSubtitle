import easygui as eg
import sys

def gate_gui():
    _type = eg.buttonbox(msg='\t\t\t        请选择视频类型', title='AutoSubtitle', choices=('全力回避Flag酱!', '混血万事屋'))
    if(_type=='全力回避Flag酱!'):
        import main_flag
    if(_type=='混血万事屋'):
        import main_wsw

if(len(sys.argv) == 1):
    gate_gui()

if(len(sys.argv) != 4 and len(sys.argv) != 1):
    print(r"----------------")
    print(r"使用帮助：\n")
    print(r"GUI模式触发条件为无传入参数\n")
    print(r"命令行模式：")
    print(r"python main.py 参数1 参数2 参数3")
    print(r"AutoSubtitle.exe 参数1 参数2 参数3 \n")
    print(r"参数1 视频类型 如 flag 或 wsw")
    print(r"参数2 原视频路径 如 C:\xxx\xxx\xx.mp4")
    print(r"参数3 字幕输出路径 如 C:\xxx\xxx\xx.ass \n")
    print(r"完整示例：python main.py flag C:\xxx\xxx\xx.mp4 C:\xxx\xxx\xx.ass")
    print(r"AutoSubtitle.exe flag C:\xxx\xxx\xx.mp4 C:\xxx\xxx\xx.ass")
    print(r"----------------")
    input("按回车退出...")

if(len(sys.argv) == 4):
    if(sys.argv[1] not in ["flag","wsw"]):
        print(r"无效的视频类型，请查正后重试")
        input("按回车退出...")
    elif(sys.argv[1]=='flag'):
        sys.argv.remove("flag")
        import main_flag
    elif(sys.argv[1]=='wsw'):
        sys.argv.remove("wsw")
        import main_flag

