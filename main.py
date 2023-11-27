from PyQt5.QtCore import QTimer, QPropertyAnimation, QSequentialAnimationGroup, QParallelAnimationGroup, QPoint, \
    QPauseAnimation
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5 import QtWidgets
from PyQt5 import uic
import sys
import pictures_rc
from Function import *

class MainUI(QDialog):
    def __init__(self, stackedWidget):
        super(MainUI, self).__init__()
        uic.loadUi('Main.ui', self)
        self.setFixedSize(1152, 864)

        self.stackedWidget = stackedWidget
        self.recordButton.clicked.connect(self.test1)
        self.fileButton.clicked.connect(self.test2)
        self.exitButton.clicked.connect(self.test3)

    def test1(self):
        self.stackedWidget.setCurrentIndex(1)

    def test2(self):
        self.stackedWidget.setCurrentIndex(1)

    def test3(self):
        self.stackedWidget.setCurrentIndex(0)


class RecordingUI(QDialog):
    def __init__(self, stackedWidget):
        super(RecordingUI, self).__init__()
        uic.loadUi('Recording.ui', self)

        self.stackedWidget = stackedWidget
        self.recordButton.clicked.connect(self.test1)
        self.returnButton.clicked.connect(self.test2)

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

    def test1(self):
        self.animationGroup.start()
        ReadWave()
        self.test3()

    def test2(self):
        self.stackedWidget.setCurrentIndex(0)

    def test3(self):
        self.animationGroup.stop()
        self.stackedWidget.setCurrentIndex(2)


class ParameterUI(QDialog):
    def __init__(self, stackedWidget):
        super(ParameterUI, self).__init__()
        uic.loadUi('Parameter.ui', self)
        # self.setFixedSize(1800, 1350)

        self.stackedWidget = stackedWidget
        self.startButton.clicked.connect(self.test1)
        self.returnButton.clicked.connect(self.test2)

    def test1(self):
        self.stackedWidget.setCurrentIndex(3)

    def test2(self):
        self.stackedWidget.setCurrentIndex(0)


class WorkingUI(QDialog):
    def __init__(self, stackedWidget):
        super(WorkingUI, self).__init__()
        uic.loadUi('Working.ui', self)
        self.stackedWidget = stackedWidget

        self.workButton.clicked.connect(self.test1)

        self.animationGroup = QSequentialAnimationGroup()
        self.animationGroup.setLoopCount(1000)  # 设置闪烁次数
        removeAnimation = []

        positions = [QPoint(65, 512), QPoint(256, 512), QPoint(480, 512), QPoint(698, 512), QPoint(928, 512)]
        for i in (0, 1, 2, 3, 4):
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

        for i in (0, 1, 2, 3, 4):
            self.animationGroup.addAnimation(removeAnimation[i])

        waitAnimation = QPauseAnimation(700)  # 7ms 的等待动画
        self.animationGroup.addAnimation(waitAnimation)

    def test1(self):
        self.animationGroup.start()
        ExtraKeywords("a girl is singing")
        EmotionSelect('happy')
        ImageGenerate()
        self.test2()

    def test2(self):
        self.animationGroup.stop()
        self.stackedWidget.setCurrentIndex(4)


class ResultUI(QDialog):
    def __init__(self, stackedWidget):
        super(ResultUI, self).__init__()
        uic.loadUi('Result.ui', self)

        self.stackedWidget = stackedWidget
        self.saveButton.clicked.connect(self.test1)
        self.returnButton.clicked.connect(self.test2)
        self.reworkButton.clicked.connect(self.test3)
        self.nextButton.clicked.connect(self.test4)

    def test1(self):
        self.stackedWidget.setCurrentIndex(0)

    def test2(self):
        self.stackedWidget.setCurrentIndex(0)

    def test3(self):
        self.stackedWidget.setCurrentIndex(2)

    def test4(self):
        self.stackedWidget.setCurrentIndex(4)


def show_MainUI():
    app = QApplication(sys.argv)
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
