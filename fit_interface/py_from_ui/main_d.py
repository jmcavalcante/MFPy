# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fit_interface/ui_design/main_design.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 618)
        MainWindow.setMinimumSize(QtCore.QSize(900, 545))
        MainWindow.setMaximumSize(QtCore.QSize(900, 618))
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout_9.addWidget(self.label_8, 0, 0, 1, 1)
        self.R0 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.R0.setDecimals(5)
        self.R0.setMinimum(0.1)
        self.R0.setMaximum(5.0)
        self.R0.setSingleStep(0.1)
        self.R0.setProperty("value", 0.3)
        self.R0.setObjectName("R0")
        self.gridLayout_9.addWidget(self.R0, 0, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setObjectName("label_11")
        self.gridLayout_9.addWidget(self.label_11, 1, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setObjectName("label_12")
        self.gridLayout_9.addWidget(self.label_12, 2, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setObjectName("label_13")
        self.gridLayout_9.addWidget(self.label_13, 3, 0, 1, 1)
        self.tir_label = QtWidgets.QLabel(self.centralwidget)
        self.tir_label.setObjectName("tir_label")
        self.gridLayout_9.addWidget(self.tir_label, 3, 1, 1, 1)
        self.VX0 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.VX0.setMinimum(1.0)
        self.VX0.setMaximum(100.0)
        self.VX0.setProperty("value", 10.0)
        self.VX0.setObjectName("VX0")
        self.gridLayout_9.addWidget(self.VX0, 1, 1, 1, 1)
        self.FZ0 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.FZ0.setMinimum(100.0)
        self.FZ0.setMaximum(100000.0)
        self.FZ0.setProperty("value", 3000.0)
        self.FZ0.setObjectName("FZ0")
        self.gridLayout_9.addWidget(self.FZ0, 2, 1, 1, 1)
        self.gridLayout_9.setColumnStretch(0, 1)
        self.gridLayout_9.setColumnStretch(1, 10)
        self.gridLayout_9.setRowStretch(0, 1)
        self.gridLayout_9.setRowStretch(1, 1)
        self.gridLayout_9.setRowStretch(2, 1)
        self.gridLayout_9.setRowStretch(3, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_9)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.FX_pure_path = QtWidgets.QLineEdit(self.centralwidget)
        self.FX_pure_path.setReadOnly(True)
        self.FX_pure_path.setObjectName("FX_pure_path")
        self.gridLayout.addWidget(self.FX_pure_path, 0, 1, 1, 1)
        self.FX_pure_dialog = QtWidgets.QPushButton(self.centralwidget)
        self.FX_pure_dialog.setObjectName("FX_pure_dialog")
        self.gridLayout.addWidget(self.FX_pure_dialog, 0, 2, 1, 1)
        self.FX_pure_fit = QtWidgets.QPushButton(self.centralwidget)
        self.FX_pure_fit.setEnabled(False)
        self.FX_pure_fit.setObjectName("FX_pure_fit")
        self.gridLayout.addWidget(self.FX_pure_fit, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setUnderline(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.FX_pure_led_layout = QtWidgets.QVBoxLayout()
        self.FX_pure_led_layout.setObjectName("FX_pure_led_layout")
        self.gridLayout.addLayout(self.FX_pure_led_layout, 1, 2, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 5)
        self.gridLayout.setColumnStretch(2, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.FY_pure_path = QtWidgets.QLineEdit(self.centralwidget)
        self.FY_pure_path.setReadOnly(True)
        self.FY_pure_path.setObjectName("FY_pure_path")
        self.gridLayout_3.addWidget(self.FY_pure_path, 0, 1, 1, 1)
        self.FY_pure_dialog = QtWidgets.QPushButton(self.centralwidget)
        self.FY_pure_dialog.setObjectName("FY_pure_dialog")
        self.gridLayout_3.addWidget(self.FY_pure_dialog, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setUnderline(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.FY_pure_fit = QtWidgets.QPushButton(self.centralwidget)
        self.FY_pure_fit.setEnabled(False)
        self.FY_pure_fit.setObjectName("FY_pure_fit")
        self.gridLayout_3.addWidget(self.FY_pure_fit, 1, 1, 1, 1)
        self.FY_pure_led_layout = QtWidgets.QVBoxLayout()
        self.FY_pure_led_layout.setObjectName("FY_pure_led_layout")
        self.gridLayout_3.addLayout(self.FY_pure_led_layout, 1, 2, 1, 1)
        self.gridLayout_3.setColumnStretch(0, 1)
        self.gridLayout_3.setColumnStretch(1, 5)
        self.gridLayout_3.setColumnStretch(2, 1)
        self.verticalLayout.addLayout(self.gridLayout_3)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.MZ_pure_path = QtWidgets.QLineEdit(self.centralwidget)
        self.MZ_pure_path.setEnabled(False)
        self.MZ_pure_path.setReadOnly(True)
        self.MZ_pure_path.setObjectName("MZ_pure_path")
        self.gridLayout_5.addWidget(self.MZ_pure_path, 0, 1, 1, 1)
        self.MZ_pure_dialog = QtWidgets.QPushButton(self.centralwidget)
        self.MZ_pure_dialog.setEnabled(False)
        self.MZ_pure_dialog.setObjectName("MZ_pure_dialog")
        self.gridLayout_5.addWidget(self.MZ_pure_dialog, 0, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setUnderline(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout_5.addWidget(self.label_4, 0, 0, 1, 1)
        self.MZ_pure_fit = QtWidgets.QPushButton(self.centralwidget)
        self.MZ_pure_fit.setEnabled(False)
        self.MZ_pure_fit.setObjectName("MZ_pure_fit")
        self.gridLayout_5.addWidget(self.MZ_pure_fit, 1, 1, 1, 1)
        self.MZ_pure_led_layout = QtWidgets.QVBoxLayout()
        self.MZ_pure_led_layout.setObjectName("MZ_pure_led_layout")
        self.gridLayout_5.addLayout(self.MZ_pure_led_layout, 1, 2, 1, 1)
        self.gridLayout_5.setColumnStretch(0, 1)
        self.gridLayout_5.setColumnStretch(1, 5)
        self.gridLayout_5.setColumnStretch(2, 1)
        self.verticalLayout.addLayout(self.gridLayout_5)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.FX_com_path = QtWidgets.QLineEdit(self.centralwidget)
        self.FX_com_path.setEnabled(False)
        self.FX_com_path.setReadOnly(True)
        self.FX_com_path.setObjectName("FX_com_path")
        self.gridLayout_4.addWidget(self.FX_com_path, 0, 1, 1, 1)
        self.FX_com_dialog = QtWidgets.QPushButton(self.centralwidget)
        self.FX_com_dialog.setEnabled(False)
        self.FX_com_dialog.setObjectName("FX_com_dialog")
        self.gridLayout_4.addWidget(self.FX_com_dialog, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setUnderline(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_4.addWidget(self.label_3, 0, 0, 1, 1)
        self.FX_com_fit = QtWidgets.QPushButton(self.centralwidget)
        self.FX_com_fit.setEnabled(False)
        self.FX_com_fit.setObjectName("FX_com_fit")
        self.gridLayout_4.addWidget(self.FX_com_fit, 1, 1, 1, 1)
        self.FX_com_led_layout = QtWidgets.QVBoxLayout()
        self.FX_com_led_layout.setObjectName("FX_com_led_layout")
        self.gridLayout_4.addLayout(self.FX_com_led_layout, 1, 2, 1, 1)
        self.gridLayout_4.setColumnStretch(0, 1)
        self.gridLayout_4.setColumnStretch(1, 5)
        self.gridLayout_4.setColumnStretch(2, 1)
        self.verticalLayout.addLayout(self.gridLayout_4)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.FY_com_path = QtWidgets.QLineEdit(self.centralwidget)
        self.FY_com_path.setEnabled(False)
        self.FY_com_path.setReadOnly(True)
        self.FY_com_path.setObjectName("FY_com_path")
        self.gridLayout_6.addWidget(self.FY_com_path, 0, 1, 1, 1)
        self.FY_com_dialog = QtWidgets.QPushButton(self.centralwidget)
        self.FY_com_dialog.setEnabled(False)
        self.FY_com_dialog.setObjectName("FY_com_dialog")
        self.gridLayout_6.addWidget(self.FY_com_dialog, 0, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setUnderline(True)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_6.addWidget(self.label_5, 0, 0, 1, 1)
        self.FY_com_fit = QtWidgets.QPushButton(self.centralwidget)
        self.FY_com_fit.setEnabled(False)
        self.FY_com_fit.setObjectName("FY_com_fit")
        self.gridLayout_6.addWidget(self.FY_com_fit, 1, 1, 1, 1)
        self.FY_com_led_layout = QtWidgets.QVBoxLayout()
        self.FY_com_led_layout.setObjectName("FY_com_led_layout")
        self.gridLayout_6.addLayout(self.FY_com_led_layout, 1, 2, 1, 1)
        self.gridLayout_6.setColumnStretch(0, 1)
        self.gridLayout_6.setColumnStretch(1, 5)
        self.gridLayout_6.setColumnStretch(2, 1)
        self.verticalLayout.addLayout(self.gridLayout_6)
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.MZ_com_path = QtWidgets.QLineEdit(self.centralwidget)
        self.MZ_com_path.setEnabled(False)
        self.MZ_com_path.setReadOnly(True)
        self.MZ_com_path.setObjectName("MZ_com_path")
        self.gridLayout_7.addWidget(self.MZ_com_path, 0, 1, 1, 1)
        self.MZ_com_dialog = QtWidgets.QPushButton(self.centralwidget)
        self.MZ_com_dialog.setEnabled(False)
        self.MZ_com_dialog.setObjectName("MZ_com_dialog")
        self.gridLayout_7.addWidget(self.MZ_com_dialog, 0, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setUnderline(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout_7.addWidget(self.label_6, 0, 0, 1, 1)
        self.MZ_com_fit = QtWidgets.QPushButton(self.centralwidget)
        self.MZ_com_fit.setEnabled(False)
        self.MZ_com_fit.setObjectName("MZ_com_fit")
        self.gridLayout_7.addWidget(self.MZ_com_fit, 1, 1, 1, 1)
        self.MZ_com_led_layout = QtWidgets.QVBoxLayout()
        self.MZ_com_led_layout.setObjectName("MZ_com_led_layout")
        self.gridLayout_7.addLayout(self.MZ_com_led_layout, 1, 2, 1, 1)
        self.gridLayout_7.setColumnStretch(0, 1)
        self.gridLayout_7.setColumnStretch(1, 5)
        self.gridLayout_7.setColumnStretch(2, 1)
        self.verticalLayout.addLayout(self.gridLayout_7)
        self.tir_button = QtWidgets.QPushButton(self.centralwidget)
        self.tir_button.setObjectName("tir_button")
        self.verticalLayout.addWidget(self.tir_button)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(2, 2)
        self.verticalLayout.setStretch(3, 2)
        self.verticalLayout.setStretch(4, 2)
        self.verticalLayout.setStretch(5, 2)
        self.verticalLayout.setStretch(6, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 21))
        self.menubar.setObjectName("menubar")
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_tir = QtWidgets.QAction(MainWindow)
        self.actionOpen_tir.setObjectName("actionOpen_tir")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.Help = QtWidgets.QAction(MainWindow)
        self.Help.setObjectName("Help")
        self.menuOptions.addSeparator()
        self.menuOptions.addAction(self.actionOpen_tir)
        self.menuOptions.addSeparator()
        self.menuOptions.addAction(self.Help)
        self.menubar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MFPy Fit"))
        self.label_8.setText(_translate("MainWindow", "Unloaded radius"))
        self.R0.setSuffix(_translate("MainWindow", " m"))
        self.label_11.setText(_translate("MainWindow", "Measurement speed"))
        self.label_12.setText(_translate("MainWindow", "Nominal load"))
        self.label_13.setText(_translate("MainWindow", ".tir file as a reference:"))
        self.tir_label.setText(_translate("MainWindow", " Default"))
        self.VX0.setSuffix(_translate("MainWindow", " m/s"))
        self.FZ0.setSuffix(_translate("MainWindow", " N"))
        self.FX_pure_dialog.setText(_translate("MainWindow", "..."))
        self.FX_pure_fit.setText(_translate("MainWindow", "FIT"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">FX pure</span></p></body></html>"))
        self.FY_pure_dialog.setText(_translate("MainWindow", "..."))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">FY pure</span></p></body></html>"))
        self.FY_pure_fit.setText(_translate("MainWindow", "FIT"))
        self.MZ_pure_dialog.setText(_translate("MainWindow", "..."))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">MZ pure</span></p></body></html>"))
        self.MZ_pure_fit.setText(_translate("MainWindow", "FIT"))
        self.FX_com_dialog.setText(_translate("MainWindow", "..."))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">FX combined</span></p></body></html>"))
        self.FX_com_fit.setText(_translate("MainWindow", "FIT"))
        self.FY_com_dialog.setText(_translate("MainWindow", "..."))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">FY combined</span></p></body></html>"))
        self.FY_com_fit.setText(_translate("MainWindow", "FIT"))
        self.MZ_com_dialog.setText(_translate("MainWindow", "..."))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">MZ combined</span></p></body></html>"))
        self.MZ_com_fit.setText(_translate("MainWindow", "FIT"))
        self.tir_button.setText(_translate("MainWindow", "Create .TIR"))
        self.menuOptions.setTitle(_translate("MainWindow", "Options"))
        self.actionOpen_tir.setText(_translate("MainWindow", "Open .tir"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.Help.setText(_translate("MainWindow", "Help"))