# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QLabel,
    QPushButton, QSizePolicy, QTextEdit, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(832, 706)
        icon = QIcon(QIcon.fromTheme(u"dialog-warning"))
        Widget.setWindowIcon(icon)
        self.inputTextEdit = QTextEdit(Widget)
        self.inputTextEdit.setObjectName(u"inputTextEdit")
        self.inputTextEdit.setGeometry(QRect(20, 50, 701, 70))
        self.label_3 = QLabel(Widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 10, 231, 31))
        font = QFont()
        font.setPointSize(15)
        font.setItalic(False)
        self.label_3.setFont(font)
        self.outputTextEdit = QTextEdit(Widget)
        self.outputTextEdit.setObjectName(u"outputTextEdit")
        self.outputTextEdit.setGeometry(QRect(20, 280, 701, 111))
        font1 = QFont()
        font1.setFamilies([u"Noto Mono"])
        self.outputTextEdit.setFont(font1)
        self.label_4 = QLabel(Widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(20, 240, 221, 31))
        font2 = QFont()
        font2.setPointSize(15)
        self.label_4.setFont(font2)
        self.pushButton = QPushButton(Widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(20, 200, 791, 23))
        self.label_5 = QLabel(Widget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(20, 410, 221, 31))
        self.label_5.setFont(font2)
        self.statusTextEdit = QTextEdit(Widget)
        self.statusTextEdit.setObjectName(u"statusTextEdit")
        self.statusTextEdit.setGeometry(QRect(20, 450, 701, 231))
        self.statusTextEdit.setFont(font1)
        self.label_6 = QLabel(Widget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(20, 130, 161, 21))
        font3 = QFont()
        font3.setPointSize(12)
        self.label_6.setFont(font3)
        self.checkBox = QCheckBox(Widget)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(170, 130, 21, 21))
        self.label_7 = QLabel(Widget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(300, 130, 431, 21))
        self.label_7.setFont(font3)
        self.label_8 = QLabel(Widget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(20, 160, 161, 21))
        self.label_8.setFont(font3)
        self.comboBox = QComboBox(Widget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(170, 160, 81, 23))
        self.checkBox_2 = QCheckBox(Widget)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setGeometry(QRect(410, 160, 21, 21))
        self.label_9 = QLabel(Widget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(300, 160, 101, 21))
        self.label_9.setFont(font3)
        self.checkBox_3 = QCheckBox(Widget)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setGeometry(QRect(550, 160, 21, 21))
        self.label_10 = QLabel(Widget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(470, 160, 71, 21))
        self.label_10.setFont(font3)
        self.pushButton_2 = QPushButton(Widget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(620, 160, 191, 23))
        self.pushButton_3 = QPushButton(Widget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(730, 280, 81, 111))
        self.pushButton_4 = QPushButton(Widget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(730, 450, 81, 231))
        self.pushButton_5 = QPushButton(Widget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(730, 50, 81, 71))

        self.retranslateUi(Widget)
        self.pushButton.clicked.connect(Widget.send_button_click)
        self.pushButton_3.clicked.connect(Widget.clearOutput)
        self.pushButton_5.clicked.connect(Widget.clearInput)
        self.pushButton_4.clicked.connect(Widget.clearStatus)
        self.pushButton_2.clicked.connect(Widget.newToken)
        self.checkBox_2.clicked.connect(Widget.highPriority)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"Input window:", None))
        self.label_4.setText(QCoreApplication.translate("Widget", u"Output window:", None))
        self.pushButton.setText(QCoreApplication.translate("Widget", u"Send", None))
        self.label_5.setText(QCoreApplication.translate("Widget", u"Status window:", None))
        self.label_6.setText(QCoreApplication.translate("Widget", u"Emulate errors:", None))
        self.checkBox.setText("")
        self.label_7.setText(QCoreApplication.translate("Widget", u"Used ports: ", None))
        self.label_8.setText(QCoreApplication.translate("Widget", u"Destination station:", None))
        self.checkBox_2.setText("")
        self.label_9.setText(QCoreApplication.translate("Widget", u"HIgh priority:", None))
        self.checkBox_3.setText("")
        self.label_10.setText(QCoreApplication.translate("Widget", u"Monitor:", None))
        self.pushButton_2.setText(QCoreApplication.translate("Widget", u"Generate token", None))
        self.pushButton_3.setText(QCoreApplication.translate("Widget", u"Clear", None))
        self.pushButton_4.setText(QCoreApplication.translate("Widget", u"Clear", None))
        self.pushButton_5.setText(QCoreApplication.translate("Widget", u"Clear", None))
    # retranslateUi

