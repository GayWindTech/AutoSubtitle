import sys
from pathlib import Path

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QLineEdit

from GUI_style import Ui_AutoSubtitle
from verifyPath import is_path_exists_or_creatable


class AutoSubtitle_class(QtWidgets.QMainWindow, Ui_AutoSubtitle):
    def  __init__ (self):
        super(AutoSubtitle_class, self).__init__()
        self.setupUi(self)
        self.openPath=self.savePath=str()
        self.videoTypeList.addItems(["全力回避Flag酱","混血万事屋"])
        self.videoType = self.videoTypeList.currentIndex()
        self.finish = False
        self.newOP = True
        
    def closeEvent(self, event):
        if(not self.finish):
            sys.exit()
        
    def updateOpenPath(self):
        path = self.OpenFilePathEdit.text()
        if (Path(path).is_file() == False):
            QMessageBox.warning(self,'无法找到源文件','请重新选择正确的路径!\t\t\n',QMessageBox.StandardButton.Ok)
            print("源文件路径有误")
        elif (self.checkForm(path)):
            print(f"将会打开: {path}")
            self.openPath=path
        else:
            self.askfornonvideo_box = QMessageBox(QMessageBox.Icon.Question, '文件格式未识别','您选择的文件疑似非视频文件，是否重新选择？\t\t\n')
            self.askfornonvideo_box.setFixedSize(380,135)
            status_insist = self.askfornonvideo_box.addButton('确认无误', QMessageBox.ButtonRole.NoRole)
            status_rechoose = self.askfornonvideo_box.addButton('重新选择', QMessageBox.ButtonRole.YesRole)
            self.askfornonvideo_box.exec()
            if (self.askfornonvideo_box.clickedButton() == status_insist):
                print(f"将会打开: {path}")
                self.openPath=path
            else:
                self.OpenFilePathEdit.clear()
    
    def setSavePathToDefault(self):
        path = self.openPath
        defaultSavePath = str(path).rstrip(str(path).split('.')[-1])+"ass" if path != '' else "output.ass"
        self.SaveFilePathEdit.setText(defaultSavePath)
        self.updateSavePath()
    
    def updateSavePath(self):
        path = self.SaveFilePathEdit.text()
        if (is_path_exists_or_creatable(path) == False):
            QMessageBox.warning(self,'保存路径不正确','请重新选择正确的路径!\t\t\n',QMessageBox.StandardButton.Ok)
            print("保存路径有误")
        else:
            print(f"将会保存至: {path}")
            self.savePath=path
            
    def updateVideoType(self):
        self.videoType = self.videoTypeList.currentIndex()
        if(self.videoType == 0):
            self.FlagNewOPcheckBox.setEnabled(True)
        else:
            self.FlagNewOPcheckBox.setEnabled(False)
        print(f'当前视频类型: {str(self.videoType)}')
            
    def raiseOpenFile(self): 
        filePath,openStatus=QFileDialog.getOpenFileName(self,'选择要打开的文件') 
        if openStatus: 
            self.OpenFilePathEdit.setText(filePath)
            self.updateOpenPath()
            
    def raiseSaveFile(self): 
        filePath,openStatus=QFileDialog.getSaveFileName(self,'选择要保存到的位置','out.ass','字幕文件 (*.ass)') 
        if openStatus: 
            self.SaveFilePathEdit.setText(filePath)
            self.updateSavePath()
            
    def checkForm(self,path:str):
        return path.split('.')[-1] in ["webm","mp4","mov","flv","mkv","m4v"]

    def updateOPstyle(self):
        self.newOP = self.FlagNewOPcheckBox.isChecked()
        print(f'NewOP: {str(self.newOP)}')
    
    def tryToStart(self):
        self.updateOpenPath()
        self.updateSavePath()
        self.updateOPstyle()
        if(not(Path(self.openPath).is_file() and is_path_exists_or_creatable(self.savePath))):
            QMessageBox.warning(self,'路径不正确','请选择正确的路径!\t\t\n',QMessageBox.StandardButton.Ok)
        else:
            self.finish = True
            print('开始打轴...')
            self.close()
            # self.setEnabled(False)

def runGUI():
    GUI_APP=QtWidgets.QApplication(sys.argv)
    GUI_mainWindow = AutoSubtitle_class()
    GUI_mainWindow.setFixedSize(GUI_mainWindow.width(), GUI_mainWindow.height())
    GUI_mainWindow.show()
    GUI_APP.exec()
    return GUI_mainWindow.openPath,GUI_mainWindow.savePath,GUI_mainWindow.videoType,GUI_mainWindow.newOP

if __name__ == "__main__":
    print(runGUI())