from PyQt5.QtCore import QTimer, QPropertyAnimation, QSequentialAnimationGroup, QParallelAnimationGroup, QPoint, \
    QPauseAnimation
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, \
    QLabel
from PyQt5 import QtWidgets, QtGui
from PyQt5 import uic
import sys
import pictures_rc
from threading import Thread
from Function import *

app = QApplication(sys.argv)


class ParaEndSignal(QObject):
    paraEndSignal = pyqtSignal(str)


class NextPageSignal(QObject):
    nextPageSignal = pyqtSignal(str)


paraEndSignal = ParaEndSignal()
workEndSignal = NextPageSignal()


class MainUI(QDialog):
    def __init__(self, stackedWidget):
        super(MainUI, self).__init__()
        uic.loadUi('Main.ui', self)
        self.setFixedSize(1152, 864)

        self.stackedWidget = stackedWidget
        self.recordButton.clicked.connect(self.ToRecord)
        self.fileButton.clicked.connect(self.ToUpload)
        self.exitButton.clicked.connect(self.Exit)

    def ToRecord(self):
        self.stackedWidget.setCurrentIndex(1)

    def ToUpload(self):
        self.stackedWidget.setCurrentIndex(1)

    def Exit(self):
        self.stackedWidget.setCurrentIndex(0)
        sys.exit(app.exec())


class RecordingUI(QDialog):
    def __init__(self, stackedWidget):
        super(RecordingUI, self).__init__()
        uic.loadUi('Recording.ui', self)

        self.stackedWidget = stackedWidget
        self.recordButton.clicked.connect(self.Recording)
        self.returnButton.clicked.connect(self.Back)

        self.animationGroup = QSequentialAnimationGroup()
        self.animationGroup.setLoopCount(500)  # 设置闪烁次数

        self.hideAnimation = QPropertyAnimation(self.iconButton, b"pos")
        self.hideAnimation.setDuration(1)
        self.hideAnimation.setStartValue(QPoint(282, 198))
        self.hideAnimation.setEndValue(QPoint(282, 1000))
        self.animationGroup.addAnimation(self.hideAnimation)

        self.waitAnimation = QPauseAnimation(900)  # 2秒的等待动画
        self.animationGroup.addAnimation(self.waitAnimation)

        self.showAnimation = QPropertyAnimation(self.iconButton, b"pos")
        self.showAnimation.setDuration(1)
        self.showAnimation.setStartValue(QPoint(282, 1000))
        self.showAnimation.setEndValue(QPoint(282, 198))
        self.animationGroup.addAnimation(self.showAnimation)

        self.waitAnimation = QPauseAnimation(900)  # 2秒的等待动画
        self.animationGroup.addAnimation(self.waitAnimation)

    def Recording(self):
        recordEndSignal.recordEnd.connect(self.NextPage)
        self.animationGroup.start()
        thread = Thread(target=ReadWave)
        thread.start()

    def Back(self):
        self.stackedWidget.setCurrentIndex(0)

    def NextPage(self):
        self.animationGroup.stop()
        self.stackedWidget.setCurrentIndex(2)


class ParameterUI(QDialog):
    def __init__(self, stackedWidget):
        super(ParameterUI, self).__init__()
        uic.loadUi('Parameter.ui', self)
        # self.setFixedSize(1800, 1350)

        self.stackedWidget = stackedWidget
        self.startButton.clicked.connect(self.ToGenerate)
        self.returnButton.clicked.connect(self.Back)

    def ToGenerate(self):
        Data = {'emotion': self.Emo.checkedButton().text(), 'style': self.Style.checkedButton().text(),
                'tone': self.Tone.checkedButton().text(), 'prop': self.Prop.checkedButton().text()}
        DataAnalysis(Data)
        self.stackedWidget.setCurrentIndex(3)

    def Back(self):
        self.stackedWidget.setCurrentIndex(0)


class WorkingUI(QDialog):
    def __init__(self, stackedWidget):
        super(WorkingUI, self).__init__()
        self.imageLabel = None
        uic.loadUi('Working.ui', self)
        self.stackedWidget = stackedWidget

        self.workButton.clicked.connect(self.ImageGen)

        self.animationGroup = QSequentialAnimationGroup()
        self.animationGroup.setLoopCount(1000)  # 设置闪烁次数
        removeAnimation = []

        positions = [QPoint(65, 512), QPoint(256, 512), QPoint(480, 512), QPoint(698, 512), QPoint(928, 512)]
        for i in range(4):
            iconButton = QPushButton(self)
            iconButton.setGeometry(positions[i].x(), positions[i].y(), 116, 135)
            iconButton.setStyleSheet("background-color: red;")
            iconButton.setStyleSheet("border-image: url(:/background/UIpictures/workingicon.png);")
            moveAnimation = QPropertyAnimation(iconButton, b"pos")
            moveAnimation.setDuration(1)
            moveAnimation.setStartValue(positions[i])
            moveAnimation.setEndValue(QPoint(186, 698))
            self.animationGroup.addAnimation(moveAnimation)
            waitAnimation = QPauseAnimation(700)  # 7ms 的等待动画
            self.animationGroup.addAnimation(waitAnimation)
            moveAnimation = QPropertyAnimation(iconButton, b"pos")
            moveAnimation.setDuration(1)
            moveAnimation.setStartValue(QPoint(186, 698))
            moveAnimation.setEndValue(positions[i])
            removeAnimation.append(moveAnimation)

        for i in range(4):
            self.animationGroup.addAnimation(removeAnimation[i])

        waitAnimation = QPauseAnimation(700)  # 7ms 的等待动画
        self.animationGroup.addAnimation(waitAnimation)

    def ImageGen(self):
        threadIG = Thread(target=ImageGenerate)
        generateEndSignal.generateEnd.connect(self.NextPage)
        threadIG.start()
        self.animationGroup.start()

    def NextPage(self):
        self.animationGroup.stop()
        self.stackedWidget.setCurrentIndex(4)
        workEndSignal.nextPageSignal.emit("NextPage")


class ResultUI(QDialog):
    def __init__(self, stackedWidget):
        super(ResultUI, self).__init__()
        self.imageLabel = QLabel(self)
        uic.loadUi('Result.ui', self)

        workEndSignal.nextPageSignal.connect(self.ShowImage)
        self.stackedWidget = stackedWidget
        self.saveButton.clicked.connect(self.Save)
        self.returnButton.clicked.connect(self.Back)
        self.reworkButton.clicked.connect(self.Change)
        self.nextButton.clicked.connect(self.Next)

    def ShowImage(self):
        image = v2d.image
        ImgMap = QtGui.QPixmap(QtGui.QImage.fromData(base64.b64decode(image)))
        self.imageLabel.setGeometry(0, 140, v2d.size[0], v2d.size[1])
        self.imageLabel.setPixmap(ImgMap.scaled(self.imageLabel.width(), self.imageLabel.height()))
        self.imageLabel.show()

    def Save(self):
        Path = QFileDialog.getSaveFileName(self, 'Save File', '', '*.png')
        print(Path[0])
        SaveImage(Path[0])
        self.stackedWidget.setCurrentIndex(0)

    def Back(self):
        v2d.keywords = []
        self.stackedWidget.setCurrentIndex(0)

    def Change(self):
        self.stackedWidget.setCurrentIndex(2)

    def Next(self):
        self.stackedWidget.setCurrentIndex(4)


def show_MainUI():
    stackedWidget = QStackedWidget()
    mainUI = MainUI(stackedWidget)
    recordingUI = RecordingUI(stackedWidget)
    parameterUI = ParameterUI(stackedWidget)
    workingUI = WorkingUI(stackedWidget)
    resultUI = ResultUI(stackedWidget)

    stackedWidget.addWidget(mainUI)
    stackedWidget.addWidget(recordingUI)
    stackedWidget.addWidget(parameterUI)
    stackedWidget.addWidget(workingUI)
    stackedWidget.addWidget(resultUI)

    # stackedWidget.currentChanged.connect(lambda index: stackedWidget.widget(index).adjustSize())
    stackedWidget.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    show_MainUI()
