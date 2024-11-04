# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'S0_audio_controls1.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSlider,
    QWidget)

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        if not mainWindow.objectName():
            mainWindow.setObjectName(u"mainWindow")
        mainWindow.resize(276, 240)
        mainWindow.setMaximumSize(QSize(276, 16777215))
        font = QFont()
        font.setFamilies([u"Gadugi"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        mainWindow.setFont(font)
        mainWindow.setWindowTitle(u"S0 AudioControls")
        mainWindow.setAutoFillBackground(False)
        mainWindow.setStyleSheet(u"background-color: rgb(31, 31, 31);\n"
"selection-background-color: rgb(55, 55, 61);\n"
"border-color: rgb(24, 24, 24);")
        mainWindow.setAnimated(True)
        self.centralwidget = QWidget(mainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.percentage_slider = QSlider(self.centralwidget)
        self.percentage_slider.setObjectName(u"percentage_slider")
        self.percentage_slider.setGeometry(QRect(10, 55, 260, 22))
        self.percentage_slider.setMinimum(1)
        self.percentage_slider.setMaximum(100)
        self.percentage_slider.setValue(60)
        self.percentage_slider.setSliderPosition(60)
        self.percentage_slider.setOrientation(Qt.Orientation.Horizontal)
        self.decrease_intencity = QLabel(self.centralwidget)
        self.decrease_intencity.setObjectName(u"decrease_intencity")
        self.decrease_intencity.setGeometry(QRect(43, 36, 189, 20))
        self.decrease_intencity.setFont(font)
        self.Title = QLabel(self.centralwidget)
        self.Title.setObjectName(u"Title")
        self.Title.setGeometry(QRect(70, 10, 141, 21))
        font1 = QFont()
        font1.setFamilies([u"Gadugi"])
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setItalic(False)
        self.Title.setFont(font1)
        self.Title.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.decrease_bind_button = QPushButton(self.centralwidget)
        self.decrease_bind_button.setObjectName(u"decrease_bind_button")
        self.decrease_bind_button.setGeometry(QRect(140, 120, 120, 50))
        self.decrease_bind_button.setFlat(False)
        self.mute_bind_button = QPushButton(self.centralwidget)
        self.mute_bind_button.setObjectName(u"mute_bind_button")
        self.mute_bind_button.setGeometry(QRect(140, 180, 120, 50))
        self.percentage_label = QLabel(self.centralwidget)
        self.percentage_label.setObjectName(u"percentage_label")
        self.percentage_label.setGeometry(QRect(130, 76, 21, 16))
        self.percentage_label.setFrameShape(QFrame.Shape.NoFrame)
        self.percentage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 120, 131, 50))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setMargin(0)
        self.label.setIndent(1)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(0, 180, 131, 50))
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setMargin(0)
        self.label_2.setIndent(1)
        self.percentage_checkbox = QCheckBox(self.centralwidget)
        self.percentage_checkbox.setObjectName(u"percentage_checkbox")
        self.percentage_checkbox.setGeometry(QRect(60, 94, 161, 20))
        mainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainWindow)

        self.decrease_bind_button.setDefault(False)


        QMetaObject.connectSlotsByName(mainWindow)
    # setupUi

    def retranslateUi(self, mainWindow):
#if QT_CONFIG(tooltip)
        mainWindow.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.decrease_intencity.setText(QCoreApplication.translate("mainWindow", u"\u0418\u043d\u0442\u0435\u043d\u0441\u0438\u0432\u043d\u043e\u0441\u0442\u044c \u0437\u0430\u0433\u043b\u0443\u0448\u0435\u043d\u0438\u044f", None))
        self.Title.setText(QCoreApplication.translate("mainWindow", u"S0 AudioControls", None))
        self.decrease_bind_button.setText("")
        self.mute_bind_button.setText("")
        self.percentage_label.setText(QCoreApplication.translate("mainWindow", u"60%", None))
        self.label.setText(QCoreApplication.translate("mainWindow", u"\u041a\u043b\u0430\u0432\u0438\u0448\u0430 \u043f\u043e\u043d\u0438\u0436\u0435\u043d\u0438\u044f \u0433\u0440\u043e\u043c\u043a\u043e\u0441\u0442\u0438:", None))
        self.label_2.setText(QCoreApplication.translate("mainWindow", u"\u041a\u043b\u0430\u0432\u0438\u0448\u0430 \u043e\u0442\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044f \u0437\u0432\u0443\u043a\u0430:", None))
        self.percentage_checkbox.setText(QCoreApplication.translate("mainWindow", u"\u0413\u0440\u043e\u043c\u043a\u043e\u0441\u0442\u044c \u0432 \u043f\u0440\u043e\u0446\u0435\u043d\u0442\u0430\u0445", None))
    # retranslateUi

