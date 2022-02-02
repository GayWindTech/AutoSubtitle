# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\GUI_style.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AutoSubtitle(object):
    def setupUi(self, AutoSubtitle):
        AutoSubtitle.setObjectName("AutoSubtitle")
        AutoSubtitle.resize(635, 204)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AutoSubtitle.sizePolicy().hasHeightForWidth())
        AutoSubtitle.setSizePolicy(sizePolicy)
        AutoSubtitle.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        AutoSubtitle.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(AutoSubtitle)
        self.centralwidget.setObjectName("centralwidget")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(120, 150, 331, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        self.startButton.setFont(font)
        self.startButton.setObjectName("startButton")
        self.Title = QtWidgets.QLabel(self.centralwidget)
        self.Title.setEnabled(True)
        self.Title.setGeometry(QtCore.QRect(20, 10, 341, 31))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(15)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.Title.setFont(font)
        self.Title.setObjectName("Title")
        self.chooseButtom = QtWidgets.QToolButton(self.centralwidget)
        self.chooseButtom.setGeometry(QtCore.QRect(520, 70, 81, 31))
        self.chooseButtom.setObjectName("chooseButtom")
        self.saveButtom = QtWidgets.QToolButton(self.centralwidget)
        self.saveButtom.setGeometry(QtCore.QRect(520, 110, 81, 31))
        self.saveButtom.setObjectName("saveButtom")
        self.OpenFilePathEdit = DragAcceptableQLine(self.centralwidget)
        self.OpenFilePathEdit.setGeometry(QtCore.QRect(20, 70, 481, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.OpenFilePathEdit.setFont(font)
        self.OpenFilePathEdit.setStatusTip("")
        self.OpenFilePathEdit.setObjectName("OpenFilePathEdit")
        self.SaveFilePathEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.SaveFilePathEdit.setGeometry(QtCore.QRect(20, 110, 481, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.SaveFilePathEdit.setFont(font)
        self.SaveFilePathEdit.setObjectName("SaveFilePathEdit")
        self.videoTypeList = QtWidgets.QComboBox(self.centralwidget)
        self.videoTypeList.setGeometry(QtCore.QRect(370, 40, 231, 21))
        self.videoTypeList.setObjectName("videoTypeList")
        self.Title_2 = QtWidgets.QLabel(self.centralwidget)
        self.Title_2.setEnabled(True)
        self.Title_2.setGeometry(QtCore.QRect(360, 10, 251, 21))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(13)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.Title_2.setFont(font)
        self.Title_2.setObjectName("Title_2")
        self.startButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.startButton_2.setGeometry(QtCore.QRect(460, 140, 41, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        self.startButton_2.setFont(font)
        self.startButton_2.setObjectName("startButton_2")
        self.FlagNewOPcheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.FlagNewOPcheckBox.setGeometry(QtCore.QRect(510, 11, 91, 20))
        self.FlagNewOPcheckBox.setObjectName("FlagNewOPcheckBox")
        AutoSubtitle.setCentralWidget(self.centralwidget)

        self.retranslateUi(AutoSubtitle)
        self.chooseButtom.clicked.connect(AutoSubtitle.raiseOpenFile) # type: ignore
        self.saveButtom.clicked.connect(AutoSubtitle.raiseSaveFile) # type: ignore
        self.startButton.clicked.connect(AutoSubtitle.tryToStart) # type: ignore
        self.OpenFilePathEdit.editingFinished.connect(AutoSubtitle.updateOpenPath) # type: ignore
        self.SaveFilePathEdit.editingFinished.connect(AutoSubtitle.updateSavePath) # type: ignore
        self.videoTypeList.currentIndexChanged['int'].connect(AutoSubtitle.updateVideoType) # type: ignore
        self.startButton_2.clicked.connect(AutoSubtitle.updateOpenPath) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(AutoSubtitle)

    def retranslateUi(self, AutoSubtitle):
        _translate = QtCore.QCoreApplication.translate
        AutoSubtitle.setWindowTitle(_translate("AutoSubtitle", "AutoSubtitle"))
        self.startButton.setText(_translate("AutoSubtitle", "开始打轴"))
        self.Title.setText(_translate("AutoSubtitle", "<html><head/><body><p>自动打轴机<span style=\" color:#353535;\"> - By Yellowstone</span></p></body></html>"))
        self.chooseButtom.setText(_translate("AutoSubtitle", "选择打开视频"))
        self.saveButtom.setText(_translate("AutoSubtitle", "选择保存位置"))
        self.OpenFilePathEdit.setPlaceholderText(_translate("AutoSubtitle", "请选择输入视频文件路径"))
        self.SaveFilePathEdit.setPlaceholderText(_translate("AutoSubtitle", "请选择轴保存路径"))
        self.Title_2.setText(_translate("AutoSubtitle", "  请选择视频类型"))
        self.startButton_2.setText(_translate("AutoSubtitle", "默认"))
        self.FlagNewOPcheckBox.setText(_translate("AutoSubtitle", "Flag系列新OP"))
from DragAcceptableQLine import DragAcceptableQLine
