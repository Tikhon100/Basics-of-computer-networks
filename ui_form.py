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
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QPushButton,
    QSizePolicy, QTextEdit, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(836, 547)
        self.comboBox = QComboBox(Widget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(200, 130, 161, 23))
        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(90, 130, 161, 21))
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label_2 = QLabel(Widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(450, 130, 161, 21))
        self.label_2.setFont(font)
        self.comboBox_2 = QComboBox(Widget)
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setGeometry(QRect(570, 130, 161, 23))
        self.inputTextEdit = QTextEdit(Widget)
        self.inputTextEdit.setObjectName(u"inputTextEdit")
        self.inputTextEdit.setGeometry(QRect(20, 50, 791, 70))
        self.label_3 = QLabel(Widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 10, 231, 31))
        font1 = QFont()
        font1.setPointSize(15)
        font1.setItalic(False)
        self.label_3.setFont(font1)
        self.outputTextEdit = QTextEdit(Widget)
        self.outputTextEdit.setObjectName(u"outputTextEdit")
        self.outputTextEdit.setGeometry(QRect(20, 250, 791, 70))
        self.label_4 = QLabel(Widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(20, 210, 221, 31))
        font2 = QFont()
        font2.setPointSize(15)
        self.label_4.setFont(font2)
        self.pushButton = QPushButton(Widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(20, 170, 791, 23))
        self.label_5 = QLabel(Widget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(20, 340, 221, 31))
        self.label_5.setFont(font2)
        self.statusTextEdit = QTextEdit(Widget)
        self.statusTextEdit.setObjectName(u"statusTextEdit")
        self.statusTextEdit.setGeometry(QRect(20, 380, 791, 141))

        self.retranslateUi(Widget)
        self.pushButton.clicked.connect(Widget.send_button_click)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.label.setText(QCoreApplication.translate("Widget", u"Choose ports:", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"Choose speed:", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"Input window:", None))
        self.label_4.setText(QCoreApplication.translate("Widget", u"Output window:", None))
        self.pushButton.setText(QCoreApplication.translate("Widget", u"Send", None))
        self.label_5.setText(QCoreApplication.translate("Widget", u"Status window:", None))
    # retranslateUi

