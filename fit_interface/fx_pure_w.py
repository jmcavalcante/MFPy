import sys
import mfpy
from PyQt5.QtWidgets import QMainWindow, QSizePolicy,QApplication, QMainWindow, QHeaderView, QTableWidgetItem,QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal, QThread, pyqtSlot
from fit_interface.py_from_ui.fx_pure_d import Ui_MainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from cycler import cycler
from fit_interface.toolbar import NavigationToolbar
from fit_interface.loading_window import LoadingWindow
from matplotlib.lines import Line2D


class FitThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    canceled = pyqtSignal()

    def __init__(self, parent, folder, FZ0, p0, lower_bounds, upper_bounds):
        super().__init__(parent)
        self.folder = folder
        self.FZ0 = FZ0
        self.p0 = p0
        self.lower_bounds = lower_bounds
        self.upper_bounds = upper_bounds
        self._is_canceled = False

    def run(self):
        try:
            # Check if the thread has been canceled before starting
            if self._is_canceled:
                self.canceled.emit()
                return

            # Run the fitting process
            self.p_fit,_,_,self.FZ_data,self.FX_data,self.kappa_data,self.gamma_data,self.FX_initial,self.FX_fit = \
                mfpy.fit.FX_pure(self.folder, FZ_nom=self.FZ0, initial_guess=self.p0.copy(), full_output=2,
                                 lower_bounds=self.lower_bounds, upper_bounds=self.upper_bounds)
            if not self._is_canceled:
                self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))
            
    def cancel(self):
        """Method to cancel the fitting process"""
        self._is_canceled = True
        self.quit()  # Stop the thread
        self.wait()  # Wait until the thread stops

class FX_pure(QMainWindow):
    FX_pure_task = pyqtSignal(mfpy.mf52_structure.MF52)
    def __init__(self,folder,tir_data,FZ0):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()
        self.folder = folder
        self.tir_data = tir_data
        self.FZ0 = FZ0
        self.FX_fit = None 
        self.p_fit = None
        self.fit_thread = None  # Ensure fit_thread is None initially


        # Other UI components and initialization
        self.ui.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)


        #Feed initial guess table using tir_data (first time only)
        self.index_cache = {self.ui.table.verticalHeaderItem(row).text(): row for row in range(self.ui.table.rowCount())} #Row names cache
        self.ui.table.setItem(self.index_cache.get('PCX1'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PCX1)))
        self.ui.table.setItem(self.index_cache.get('PDX1'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PDX1)))
        self.ui.table.setItem(self.index_cache.get('PDX2'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PDX2)))
        self.ui.table.setItem(self.index_cache.get('PDX3'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PDX3)))
        self.ui.table.setItem(self.index_cache.get('PEX1'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PEX1)))
        self.ui.table.setItem(self.index_cache.get('PEX2'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PEX2)))
        self.ui.table.setItem(self.index_cache.get('PEX3'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PEX3)))
        self.ui.table.setItem(self.index_cache.get('PEX4'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PEX4)))
        self.ui.table.setItem(self.index_cache.get('PKX1'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PKX1)))
        self.ui.table.setItem(self.index_cache.get('PKX2'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PKX2)))
        self.ui.table.setItem(self.index_cache.get('PKX3'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PKX3)))
        self.ui.table.setItem(self.index_cache.get('PHX1'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PHX1)))
        self.ui.table.setItem(self.index_cache.get('PHX2'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PHX2)))
        self.ui.table.setItem(self.index_cache.get('PVX1'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PVX1)))
        self.ui.table.setItem(self.index_cache.get('PVX2'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PVX2)))
        self.create_guess()     

        # Graph configuration
        self.fig = plt.figure()
        self.fig.suptitle('Longitudinal Force - pure slip fit') 

        #Legend
        black_dot = Line2D([0], [0], marker='o', color='w', markerfacecolor='k', markersize=10, label='Data')
        line = Line2D([0], [1], color='black', label='Fit')
        dot_line = Line2D([0], [1], color='black', linestyle=':', label='Initial Guess')
        self.fig.legend(handles=[black_dot, dot_line, line], loc='upper right')
        self.colors = ['r', 'g', 'b', 'y', 'm', 'c','brown','gray','orange']
        self.color_cycle = cycler(color=self.colors)
        plt.rc('axes', prop_cycle=self.color_cycle)

        # Graph configuration
        self.ax = self.fig.add_subplot(111)
        for i in range(len(self.FZ_data)):
            color = self.colors[i % len(self.colors)]
            self.ax.plot(self.kappa_data[i], self.FX_initial[i], ':', color=color)
            self.ax.scatter(self.kappa_data[i], self.FX_data[i], s=10, color=color,
                            label=r'FZ {} N, $\gamma$ = {} rad'.format(self.FZ_data[i], self.gamma_data[i][0]))
        self.ax.grid()
        self.ax.legend(loc='lower left')
        self.ax.set_xlabel('Slip ratio (%/100)')
        self.ax.set_ylabel('(N)')

        # Canvas for the graph
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setStyleSheet('background-color: white;')
        self.ui.graph.addWidget(self.canvas)
        self.ui.graph.addWidget(self.toolbar)
        self.canvas.draw()

        self.loading_fit = LoadingWindow(parent=self)
        # Connect buttons and actions
        self.ui.table.cellChanged.connect(self.reStart)
        self.ui.save_button.clicked.connect(self.save_close)
        self.ui.fit_button.clicked.connect(self.start_fit)
        self.loading_fit.stop_button.clicked.connect(self.stop_fit)  # Connect stop button to function
        self.ui.initial_check.stateChanged.connect(self.graph)
        self.ui.fit_check.stateChanged.connect(self.graph)

    def reStart(self,row,column):
        if column == 0:
            for row in range(self.ui.table.rowCount()):
                item = QTableWidgetItem('')
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.ui.table.setItem(row, 3, item)
            self.create_guess()
            self.ui.fit_check.setChecked(False)
            self.ui.fit_check.setEnabled(False)
            self.ui.initial_check.setChecked(True)
            self.ui.initial_check.setEnabled(False)
            self.ui.save_button.setEnabled(False)
            self.graph()
        elif column == 1:
            self.bounds()
        elif column == 2:
            self.bounds()
                
    def create_guess(self):
        """Load initial guess values from the table"""
        self.p0 = []
        for row in range(self.ui.table.rowCount()):
            item = self.ui.table.item(row, 0)
            self.p0.append(float(item.text()))
        self.FZ_data,self.FX_data,self.kappa_data,self.gamma_data,self.FX_initial = mfpy.fit.FX_pure(self.folder,FZ_nom=self.FZ0,initial_guess=self.p0.copy(),full_output='data_only')

    def start_fit(self):
        """Start the fitting process in a separate thread"""
        self.bounds() #bounds values from table

        # Open loading window
        self.loading_fit.show()

        # Disable the "Start" button during fitting
        self.ui.fit_button.setEnabled(False)

        # If no fitting process is running, start a new thread
        if self.fit_thread is None or not self.fit_thread.isRunning():
            self.fit_thread = FitThread(self, self.folder, self.FZ0, self.p0, self.lower_bounds, self.upper_bounds)
            self.fit_thread.finished.connect(self.on_fit_finished)
            self.fit_thread.error.connect(self.on_fit_canceled)
            self.fit_thread.error.connect(self.showErrorDialog)
            self.fit_thread.canceled.connect(self.on_fit_canceled)
            self.fit_thread.start()
        else:
            print("Fitting thread is already running.")
    
    @pyqtSlot()
    def on_fit_finished(self):

        # Hide the loading window
        self.loading_fit.close()

        self.FX_fit = self.fit_thread.FX_fit
        self.p_fit = self.fit_thread.p_fit

        """Update the UI when the fitting is finished"""
    
        # Populate the table with the fitted parameters
        for row in range(self.ui.table.rowCount()):
            item = QTableWidgetItem(str(self.fit_thread.p_fit[row].round(5)))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make the item non-editable
            self.ui.table.setItem(row, 3, item)
        
        self.ui.save_button.setEnabled(True)
        self.ui.initial_check.setEnabled(True)
        self.ui.initial_check.setChecked(False)
        self.ui.fit_check.setEnabled(True)
        self.ui.fit_check.setChecked(True)
        self.graph()

        # Re-enable the "Start" button
        self.ui.fit_button.setEnabled(True)

    @pyqtSlot()
    def on_fit_canceled(self):
        # Hide the loading window
        self.loading_fit.close()

        """Update the UI when the fitting is canceled"""

        # Re-enable the "Start" button after cancellation
        self.ui.fit_button.setEnabled(True)
        print("Fitting was canceled.")

    def stop_fit(self):
        """Cancel the fitting process"""
        if self.fit_thread:
            self.fit_thread.cancel()  # Call the cancel method of the thread
            self.fit_thread.finished.disconnect(self.on_fit_finished)  # Remove the finished connection to avoid conflicts
            self.fit_thread.canceled.connect(self.on_fit_canceled)  # Ensure the canceled signal is connected
            # Re-enable the "Start" button immediately after stop is pressed
            self.ui.fit_button.setEnabled(True)


    def bounds(self):
        """Read the lower and upper bounds from the table"""
        self.lower_bounds, self.upper_bounds = [], []
        try:
            for row in range(self.ui.table.rowCount()):
                self.lower_bounds.append(float(self.ui.table.item(row, 1).text()))
                self.upper_bounds.append(float(self.ui.table.item(row, 2).text()))
        except Exception as e:
            self.showErrorDialog(str(e))

    def edit_tir_data(self):
        self.tir_data.LONGITUDINAL_COEFFICIENTS.PCX1 = self.p_fit[0].round(7)
        self.tir_data.LONGITUDINAL_COEFFICIENTS.PDX1 = self.p_fit[1].round(7)
        self.tir_data.LONGITUDINAL_COEFFICIENTS.PDX2 = self.p_fit[2].round(7)
        self.tir_data.LONGITUDINAL_COEFFICIENTS.PDX3 = self.p_fit[3].round(7)
        self.tir_data.LONGITUDINAL_COEFFICIENTS.PEX1 = self.p_fit[4].round(7)
        self.tir_data.LONGITUDINAL_COEFFICIENTS.PEX2 = self.p_fit[5].round(7)
        self.tir_data.LONGITUDINAL_COEFFICIENTS.PEX3 = self.p_fit[6].round(7)
        self.tir_data.LONGITUDINAL_COEFFICIENTS.PEX4 = self.p_fit[7].round(7)
        self.tir_data.LONGITUDINAL_COEFFICIENTS.PKX1 = self.p_fit[8].round(7)
        self.tir_data.LONGITUDINAL_COEFFICIENTS.PKX2 = self.p_fit[9].round(7)
        self.tir_data.LONGITUDINAL_COEFFICIENTS.PKX3 = self.p_fit[10].round(7)
        self.tir_data.LONGITUDINAL_COEFFICIENTS.PHX1 = self.p_fit[11].round(7)
        self.tir_data.LONGITUDINAL_COEFFICIENTS.PHX2 = self.p_fit[12].round(7)
        self.tir_data.LONGITUDINAL_COEFFICIENTS.PVX1 = self.p_fit[13].round(7)
        self.tir_data.LONGITUDINAL_COEFFICIENTS.PVX2 = self.p_fit[14].round(7)


    def showErrorDialog(self, error_message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText("fit Error")
        msgBox.setInformativeText(error_message)
        msgBox.setWindowTitle("Error")
        msgBox.exec_()

    def save_close(self):
        self.edit_tir_data()
        self.FX_pure_task.emit(self.tir_data)
        self.close()

    def graph(self):
        self.ax.clear()
        for i in range(len(self.FZ_data)):
            color = self.colors[i % len(self.colors)]
            if self.ui.initial_check.isChecked():
                self.ax.plot(self.kappa_data[i],self.FX_initial[i],':',color=color)
            self.ax.scatter(self.kappa_data[i],self.FX_data[i],s=10,color=color,label=r'FZ {} N, $\gamma$ = {} rad'.format(self.FZ_data[i],self.gamma_data[i][0]))
            if self.ui.fit_check.isChecked():
                self.ax.plot(self.kappa_data[i],self.FX_fit[i],'-',color=color)
        self.ax.legend(loc='upper left')
        self.ax.grid()
        self.ax.set_xlabel('Slip ratio (%/100)')
        self.ax.set_ylabel('(N)')
        self.fig.tight_layout()
        self.canvas.draw()

def main():
    app = QApplication(sys.argv)
    window = FX_pure()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()