import sys
import mfpy
from PyQt5.QtWidgets import QMainWindow, QSizePolicy,QApplication, QMainWindow, QHeaderView, QTableWidgetItem,QMessageBox
from PyQt5.QtCore import Qt,pyqtSignal
from fit_interface.py_from_ui.fy_pure_d import Ui_MainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from cycler import cycler
from matplotlib.lines import Line2D
from fit_interface.toolbar import NavigationToolbar



class FY_pure(QMainWindow):
    FY_pure_task = pyqtSignal(mfpy.mf52_structure.MF52)
    def __init__(self,folder,tir_data,FZ0):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()
        self.folder = folder
        self.tir_data = tir_data
        self.FZ0 = FZ0

        #Resizing table
        self.ui.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #Feed initial guess table using tir_data (first time only)
        self.index_cache = {self.ui.table.verticalHeaderItem(row).text(): row for row in range(self.ui.table.rowCount())} #Row names cache
        self.ui.table.setItem(self.index_cache.get('PCY1'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PCY1)))
        self.ui.table.setItem(self.index_cache.get('PDY1'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PDY1)))
        self.ui.table.setItem(self.index_cache.get('PDY2'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PDY2)))
        self.ui.table.setItem(self.index_cache.get('PDY3'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PDY3)))
        self.ui.table.setItem(self.index_cache.get('PEY1'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PEY1)))
        self.ui.table.setItem(self.index_cache.get('PEY2'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PEY2)))
        self.ui.table.setItem(self.index_cache.get('PEY3'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PEY3)))
        self.ui.table.setItem(self.index_cache.get('PEY4'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PEY4)))
        self.ui.table.setItem(self.index_cache.get('PKY1'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PKY1)))
        self.ui.table.setItem(self.index_cache.get('PKY2'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PKY2)))
        self.ui.table.setItem(self.index_cache.get('PKY3'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PKY3)))
        self.ui.table.setItem(self.index_cache.get('PHY1'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PHY1)))
        self.ui.table.setItem(self.index_cache.get('PHY2'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PHY2)))
        self.ui.table.setItem(self.index_cache.get('PHY3'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PHY3)))
        self.ui.table.setItem(self.index_cache.get('PVY1'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PVY1)))
        self.ui.table.setItem(self.index_cache.get('PVY2'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PVY2)))
        self.ui.table.setItem(self.index_cache.get('PVY3'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PVY3)))
        self.ui.table.setItem(self.index_cache.get('PVY4'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PVY4)))
        self.create_guess()

        #Bounds
        self.bounds()

        #Graph using data from .csv and initial guess        
        #Color cycle
        self.colors = ['r', 'g', 'b', 'y', 'm', 'c','brown','gray','orange']
        self.color_cycle = cycler(color=self.colors)
        plt.rc('axes', prop_cycle=self.color_cycle)


        #Figure
        self.fig = plt.figure()
        self.fig.suptitle('Lateral Force - pure cornering') 

        #Legend
        black_dot = Line2D([0], [0], marker='o', color='w', markerfacecolor='k', markersize=10, label='Data')
        line = Line2D([0], [1], color='black', label='Fit')
        dot_line = Line2D([0], [1], color='black', linestyle=':', label='Initial Guess')
        self.fig.legend(handles=[black_dot, dot_line, line], loc='upper right')

        #Ax
        self.ax = self.fig.add_subplot(111)
        for i in range(len(self.FZ_data)):
            color = self.colors[i % len(self.colors)] 
            self.ax.plot(self.alpha_data[i],self.FY_initial[i],':',color=color)
            self.ax.scatter(self.alpha_data[i],self.FY_data[i],s=10,color=color,label=r'FZ {} N, $\gamma$ = {} rad'.format(self.FZ_data[i],self.gamma_data[i][0]))
        self.ax.grid()
        self.ax.legend(loc='lower left')
        self.ax.set_xlabel('Slip angle (rad)')
        self.ax.set_ylabel('(N)')

        #Canvas
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setStyleSheet('background-color: white;')
        self.ui.graph.addWidget(self.canvas)
        self.ui.graph.addWidget(self.toolbar)
        self.canvas.draw()

        #Saving the fit parameters
        self.ui.save_button.clicked.connect(self.save_close)

        #Fitting again
        self.ui.fit_button.clicked.connect(self.fit)

        #Activate or not initial guess graph
        self.ui.initial_check.stateChanged.connect(self.graph)
        self.ui.fit_check.stateChanged.connect(self.graph)

               
    def create_guess(self):
        #Reading table to create initial guess
        self.p0 = []
        for row in range(self.ui.table.rowCount()):
            item = self.ui.table.item(row, 0)
            self.p0.append(float(item.text()))
        self.FZ_data,self.FY_data,self.alpha_data,self.gamma_data,self.FY_initial = mfpy.fit.FY_pure(self.folder,FZ_nom=self.FZ0,initial_guess=self.p0.copy(),full_output='data_only')
    

    def fit(self):
        self.bounds()
        try:
            self.p_fit,_,_,self.FZ_data,self.FY_data,self.alpha_data,self.gamma_data,self.FY_initial,self.FY_fit = mfpy.fit.FY_pure(self.folder,FZ_nom=self.FZ0,
                                                                                                                                    initial_guess=self.p0.copy(),full_output=2,
                                                                                                                                    lower_bounds=self.lower_bounds,
                                                                                                                                    upper_bounds=self.upper_bounds)
            for row in range(self.ui.table.rowCount()):
                item = QTableWidgetItem(str(self.p_fit[row].round(5)))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.ui.table.setItem(row, 3, item)
            self.ui.save_button.setEnabled(True)
            self.ui.initial_check.setEnabled(True)
            self.ui.initial_check.setChecked(False)
            self.ui.fit_check.setEnabled(True)
            self.ui.fit_check.setChecked(True)
            self.graph()
        except Exception as e:
            self.showErrorDialog(str(e))

    def bounds(self):
        self.lower_bounds,self.upper_bounds = [],[]
        try:
            for row in range(self.ui.table.rowCount()):
                self.lower_bounds.append(float(self.ui.table.item(row,1).text()))
                self.upper_bounds.append(float(self.ui.table.item(row,2).text()))
        except Exception as e:
            self.showErrorDialog(str(e))
        
        

    def edit_tir_data(self):
        self.tir_data.LATERAL_COEFFICIENTS.PCY1 = self.p_fit[0].round(7)
        self.tir_data.LATERAL_COEFFICIENTS.PDY1 = self.p_fit[1].round(7)
        self.tir_data.LATERAL_COEFFICIENTS.PDY2 = self.p_fit[2].round(7)
        self.tir_data.LATERAL_COEFFICIENTS.PDY3 = self.p_fit[3].round(7)
        self.tir_data.LATERAL_COEFFICIENTS.PEY1 = self.p_fit[4].round(7)
        self.tir_data.LATERAL_COEFFICIENTS.PEY2 = self.p_fit[5].round(7)
        self.tir_data.LATERAL_COEFFICIENTS.PEY3 = self.p_fit[6].round(7)
        self.tir_data.LATERAL_COEFFICIENTS.PEY4 = self.p_fit[7].round(7)
        self.tir_data.LATERAL_COEFFICIENTS.PKY1 = self.p_fit[8].round(7)
        self.tir_data.LATERAL_COEFFICIENTS.PKY2 = self.p_fit[9].round(7)
        self.tir_data.LATERAL_COEFFICIENTS.PKY3 = self.p_fit[10].round(7)
        self.tir_data.LATERAL_COEFFICIENTS.PHY1 = self.p_fit[11].round(7)
        self.tir_data.LATERAL_COEFFICIENTS.PHY2 = self.p_fit[12].round(7)
        self.tir_data.LATERAL_COEFFICIENTS.PHY3 = self.p_fit[13].round(7)
        self.tir_data.LATERAL_COEFFICIENTS.PVY1 = self.p_fit[14].round(7)
        self.tir_data.LATERAL_COEFFICIENTS.PVY2 = self.p_fit[15].round(7)
        self.tir_data.LATERAL_COEFFICIENTS.PVY3 = self.p_fit[16].round(7)
        self.tir_data.LATERAL_COEFFICIENTS.PVY4 = self.p_fit[17].round(7)


    def showErrorDialog(self, error_message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText("fit Error")
        msgBox.setInformativeText(error_message)
        msgBox.setWindowTitle("Error")
        msgBox.exec_()

    def save_close(self):
        self.edit_tir_data()
        self.FY_pure_task.emit(self.tir_data)
        self.close()

    def graph(self):
        self.ax.clear()
        for i in range(len(self.FZ_data)):
            color = self.colors[i % len(self.colors)]
            if self.ui.initial_check.isChecked():
                self.ax.plot(self.alpha_data[i],self.FY_initial[i],':',color=color)
            self.ax.scatter(self.alpha_data[i],self.FY_data[i],s=10,color=color,label=r'FZ {} N, $\gamma$ = {} rad'.format(self.FZ_data[i],self.gamma_data[i][0]))
            if self.ui.fit_check.isChecked():
                self.ax.plot(self.alpha_data[i],self.FY_fit[i],'-',color=color)
        self.ax.legend(loc='lower left')
        self.ax.grid()
        self.ax.set_xlabel('Slip angle (rad)')
        self.ax.set_ylabel('(N)')
        self.canvas.draw()

def main():
    app = QApplication(sys.argv)
    window = FY_pure()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()