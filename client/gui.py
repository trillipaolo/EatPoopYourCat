from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QLineEdit, QColorDialog
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QCursor, QPixmap
from PyQt5.QtCore import Qt, QPoint, QSize
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        title = "Eat Poop Your Cat"
        width = 800
        height = 800
        top = (1080 - height) // 2
        left = (1920 - width) // 2
        print(top, left)

        icon = "../resources/icon.png"

        self.setWindowTitle(title)
        self.setGeometry(left, top, width, height)
        self.setWindowIcon(QIcon(icon))

        self.image = QImage(QSize(800, 600), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.black
        self.last_brush_color = Qt.black
        self.draw_mode = "PEN"
        self.lastPoint = QPoint()
        self.mode_pencil()

        self.textbox = QLineEdit(self)
        self.textbox.resize(800, 200)
        self.textbox.move(0, 600)

        self.current_color = QImage(QSize(50, 50), QImage.Format_RGB32)
        self.current_color.fill(self.brushColor)

        self.button_pencil = QPushButton(QIcon("../resources/pencil.png"), "", self)
        self.button_pencil.resize(50, 50)
        self.button_pencil.move(550, 600)
        self.button_pencil.clicked.connect(self.mode_pencil)

        self.button_brush = QPushButton(QIcon("../resources/brush.png"), "", self)
        self.button_brush.resize(50, 50)
        self.button_brush.move(600, 600)
        self.button_brush.clicked.connect(self.mode_brush)

        self.button_marker = QPushButton(QIcon("../resources/marker.png"), "", self)
        self.button_marker.resize(50, 50)
        self.button_marker.move(650, 600)
        self.button_marker.clicked.connect(self.mode_marker)

        self.button_marker = QPushButton(QIcon("../resources/eraser.png"), "", self)
        self.button_marker.resize(50, 50)
        self.button_marker.move(700, 600)
        self.button_marker.clicked.connect(self.mode_eraser)

        self.button_marker = QPushButton(QIcon("../resources/color-palette.png"), "", self)
        self.button_marker.resize(50, 50)
        self.button_marker.move(750, 600)
        self.button_marker.clicked.connect(self.mode_palette)

        self.red = QPushButton(QIcon(icon), "", self)
        self.red.resize(50, 50)
        self.red.move(10, 10)
        self.red.clicked.connect(self.redColor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if(event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.image.rect(), self.image, self.image.rect())

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if filePath == "":
            return
        self.image.save(filePath)

    def clear(self):
        self.image.fill(Qt.white)
        self.update()

    def mode_pencil(self):
        self.set_pen(2)
        self.change_cursor("../resources/pencil.png")

    def mode_brush(self):
        self.set_pen(5)
        self.change_cursor("../resources/brush.png")

    def mode_marker(self):
        self.set_pen(8)
        self.change_cursor("../resources/marker.png")

    def mode_eraser(self):
        self.set_eraser()
        self.change_cursor("../resources/eraser.png")

    def mode_palette(self):
        if self.draw_mode == "PEN":
            color = QColorDialog.getColor(self.brushColor)
            self.brushColor = color
            self.last_brush_color = color
        else:
            color = QColorDialog.getColor(self.last_brush_color)
            self.last_brush_color = color

    def blackColor(self):
        self.brushColor = Qt.black

    def whiteColor(self):
        self.brushColor = Qt.white

    def redColor(self):
        self.brushColor = Qt.red

    def greenColor(self):
        self.brushColor = Qt.green

    def yellowColor(self):
        self.brushColor = Qt.yellow

    def change_cursor(self, path):
        cursor_pixmap = QPixmap(path).scaled(32, 32)
        self.setCursor(QCursor(cursor_pixmap, 0, cursor_pixmap.height()))

    def set_pen(self, size):
        self.draw_mode = "PEN"
        self.brushSize = size
        self.brushColor = self.last_brush_color

    def set_eraser(self):
        self.draw_mode = "ERASER"
        self.brushSize = 15
        self.last_brush_color = self.brushColor
        self.brushColor = Qt.white

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
