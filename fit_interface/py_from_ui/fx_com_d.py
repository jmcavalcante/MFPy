# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_design\fx_com_design.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setRowCount(6)
        self.table.setColumnCount(4)
        self.table.setObjectName("table")
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsEnabled)
        self.table.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsEnabled)
        self.table.setItem(1, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(2, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsEnabled)
        self.table.setItem(2, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(3, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsEnabled)
        self.table.setItem(3, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(4, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(4, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsEnabled)
        self.table.setItem(4, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(5, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setItem(5, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsEnabled)
        self.table.setItem(5, 3, item)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.table, 0, 0, 1, 1)
        self.graph = QtWidgets.QVBoxLayout()
        self.graph.setObjectName("graph")
        self.gridLayout.addLayout(self.graph, 0, 1, 1, 1)
        self.fit_button = QtWidgets.QPushButton(self.centralwidget)
        self.fit_button.setObjectName("fit_button")
        self.gridLayout.addWidget(self.fit_button, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.initial_check = QtWidgets.QCheckBox(self.centralwidget)
        self.initial_check.setEnabled(False)
        self.initial_check.setChecked(True)
        self.initial_check.setObjectName("initial_check")
        self.verticalLayout.addWidget(self.initial_check)
        self.fit_check = QtWidgets.QCheckBox(self.centralwidget)
        self.fit_check.setEnabled(False)
        self.fit_check.setCheckable(True)
        self.fit_check.setChecked(False)
        self.fit_check.setObjectName("fit_check")
        self.verticalLayout.addWidget(self.fit_check)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.save_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_button.setEnabled(False)
        self.save_button.setObjectName("save_button")
        self.horizontalLayout.addWidget(self.save_button)
        self.horizontalLayout.setStretch(1, 5)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 5)
        self.gridLayout.setColumnStretch(1, 10)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FX combined"))
        item = self.table.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "RBX1"))
        item = self.table.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "RBX2"))
        item = self.table.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "RCX1"))
        item = self.table.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "REX1"))
        item = self.table.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "REX2"))
        item = self.table.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "RHX1"))
        item = self.table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Initial Guess"))
        item = self.table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Min"))
        item = self.table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Max"))
        item = self.table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Fit"))
        __sortingEnabled = self.table.isSortingEnabled()
        self.table.setSortingEnabled(False)
        item = self.table.item(0, 1)
        item.setText(_translate("MainWindow", "-100"))
        item = self.table.item(0, 2)
        item.setText(_translate("MainWindow", "100"))
        item = self.table.item(1, 1)
        item.setText(_translate("MainWindow", "-100"))
        item = self.table.item(1, 2)
        item.setText(_translate("MainWindow", "100"))
        item = self.table.item(2, 1)
        item.setText(_translate("MainWindow", "-100"))
        item = self.table.item(2, 2)
        item.setText(_translate("MainWindow", "100"))
        item = self.table.item(3, 1)
        item.setText(_translate("MainWindow", "-100"))
        item = self.table.item(3, 2)
        item.setText(_translate("MainWindow", "100"))
        item = self.table.item(4, 1)
        item.setText(_translate("MainWindow", "-100"))
        item = self.table.item(4, 2)
        item.setText(_translate("MainWindow", "100"))
        item = self.table.item(5, 1)
        item.setText(_translate("MainWindow", "-100"))
        item = self.table.item(5, 2)
        item.setText(_translate("MainWindow", "100"))
        self.table.setSortingEnabled(__sortingEnabled)
        self.fit_button.setText(_translate("MainWindow", "Fit"))
        self.initial_check.setText(_translate("MainWindow", "Initial guess"))
        self.fit_check.setText(_translate("MainWindow", "Fit"))
        self.save_button.setText(_translate("MainWindow", "Save and Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
