'''
Author: LetMeFly
Date: 2022-09-13 09:17:12
LastEditors: LetMeFly
LastEditTime: 2022-10-01 20:22:26
'''
import sys
import time
import webbrowser
from threading import Thread
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QPoint, QSize, Qt
from PyQt5.QtGui import QMouseEvent, QCursor, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QMenu, QMessageBox, QWidget, qApp


class Main(QWidget):
    _lastTime = None
    _nowCount = 0
    _timeIsCounting = False
    
    # 移动位置
    _leftButtonDownIng = False
    _moveStartPosition = None

    # About Me
    about = "Small desktop timer\nMade by: LetMeFly"  # 小小桌面计时器

    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(300, 70))
        self.setWindowFlags(Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setWindowOpacity(0.8)

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(self.rect())
        self.label.setStyleSheet("font: 75 20pt \"Adobe Arabic\";color:rgb(0, 122, 204)")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.pal = QPalette()
        self.pal.setColor(QPalette.Background, QColor(255, 228, 255, 50))
        self.setPalette(self.pal)

        self.timer = QtCore.QTimer(self)
        self.timer.start(50)
        self.timer.timeout.connect(self.run)

        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.show()
    
    def run(self):
        Thread(target=self.setTime, daemon=True).start()
    
    def setTime(self):
        def strfTime(count: int) -> str:
            H = int(count) // 3600
            M = int(count) % 3600 // 60
            S = int(count) % 60
            mS = int(count * 100) % 100
            return "{:02d}H:{:02d}M:{:02d}S:{:02d}".format(H, M, S, mS)

        def getTime() -> int:
            if self._timeIsCounting:
                nowTime = time.time()
                self._nowCount += nowTime - self._lastTime
                self._lastTime = nowTime
            return self._nowCount

        self.label.setText(strfTime(getTime()))

    def mouseMoveEvent(self, e: QMouseEvent):
        if self._leftButtonDownIng:
            self._endPos = e.pos() - self._moveStartPosition
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._leftButtonDownIng = True
            self._moveStartPosition = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._leftButtonDownIng = False
            self._moveStartPosition = None
        if e.button() == Qt.RightButton:
            menu = QMenu(self)
            clearAction = None
            if self._timeIsCounting:
                startpauseAction = menu.addAction("Pause")
            else:
                if self._nowCount:
                    startpauseAction = menu.addAction("Resume")
                    clearAction = menu.addAction("Clear")
                else:
                    startpauseAction = menu.addAction("Start")
            menu.addSeparator()
            aboutAction = menu.addAction("About")
            websiteAction = menu.addAction("Website")
            quitAction = menu.addAction("Exit")
            action = menu.exec_(self.mapToGlobal(e.pos()))
            if action == startpauseAction:
                if self._timeIsCounting:
                    self._timeIsCounting = False
                else:
                    self._timeIsCounting = True
                    self._lastTime = time.time()
            if action == clearAction:
                self._nowCount = 0
                print("reset to zero")
                print("The left click after a right click will also be recognized as a clearAction.\nI don't know if it is a BUG.")
            if action == quitAction:
                qApp.quit()
            if action == aboutAction:
                selected = QMessageBox.question(self, "About", self.about, QMessageBox.Yes | QMessageBox.Cancel)
                if selected == QMessageBox.Yes:
                    webbrowser.open('https://letmefly.xyz/?from=MyTimer', new=0, autoraise=True)
            if action == websiteAction:
                webbrowser.open('https://desktoptimer.letmefly.xyz/?from=DesktopTimerApp', new=0, autoraise=True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())

