import sys
import os
import mfpy
from fit_interface.py_from_ui.main_d import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow,QMessageBox,QDesktopWidget,QFileDialog,QApplication
from PyQt5.QtGui import QDesktopServices, QIcon
from PyQt5.QtCore import  QUrl
from QLed import QLed
from fit_interface.fx_pure_w import FX_pure
from fit_interface.fx_com_w import FX_com
from fit_interface.fy_pure_w import FY_pure
from fit_interface.mz_pure_w import MZ_pure
from fit_interface.fy_com_w import FY_com
from fit_interface.mz_com_w import MZ_com
from fit_interface.write_w import write

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        

        #open tir file to override the fit_data -> Its a way to save the work and comeback after.
        self.ui.actionOpen_tir.triggered.connect(self.open_file)

        #Help button to open github
        self.ui.Help.triggered.connect(self.open_link)

        #MF52 Default structure (data comes from internal .tir file)
        self.tir_data = mfpy.preprocessing.read_tir(resource_path('fit_interface/tir/pacejka_tir52.tir'))
        self.ui.FZ0.setValue(self.tir_data.VERTICAL.FNOMIN)
        self.ui.R0.setValue(self.tir_data.DIMENSION.UNLOADED_RADIUS)
        self.ui.VX0.setValue(self.tir_data.MODEL.LONGVL)
        
        #FX Pure connections
        self.FX_pure_led = QLed(self, onColour=QLed.Yellow, shape=QLed.Circle)
        self.FX_pure_led.value=True
        self.ui.FX_pure_led_layout.addWidget(self.FX_pure_led)
        self.ui.FX_pure_dialog.clicked.connect(self.FX_pure_openFolderDialog)
        self.ui.FX_pure_fit.clicked.connect(self.FX_pure_openFit)

        #FY Pure connections
        self.FY_pure_led = QLed(self, onColour=QLed.Yellow, shape=QLed.Circle)
        self.FY_pure_led.value=True
        self.ui.FY_pure_led_layout.addWidget(self.FY_pure_led)
        self.ui.FY_pure_dialog.clicked.connect(self.FY_pure_openFolderDialog)
        self.ui.FY_pure_fit.clicked.connect(self.FY_pure_openFit)

        #MZ Pure connections
        self.MZ_pure_led = QLed(self, onColour=QLed.Red, shape=QLed.Circle)
        self.MZ_pure_led.value=True
        self.ui.MZ_pure_led_layout.addWidget(self.MZ_pure_led)
        self.ui.MZ_pure_dialog.clicked.connect(self.MZ_pure_openFolderDialog)
        self.ui.MZ_pure_fit.clicked.connect(self.MZ_pure_openFit)

        #FX Combined connections
        self.FX_com_led = QLed(self, onColour=QLed.Red, shape=QLed.Circle)
        self.FX_com_led.value=True
        self.ui.FX_com_led_layout.addWidget(self.FX_com_led)
        self.ui.FX_com_dialog.clicked.connect(self.FX_com_openFolderDialog)
        self.ui.FX_com_fit.clicked.connect(self.FX_com_openFit)

        #FY Combined connections
        self.FY_com_led = QLed(self, onColour=QLed.Red, shape=QLed.Circle)
        self.FY_com_led.value=True
        self.ui.FY_com_led_layout.addWidget(self.FY_com_led)
        self.ui.FY_com_dialog.clicked.connect(self.FY_com_openFolderDialog)
        self.ui.FY_com_fit.clicked.connect(self.FY_com_openFit)

        #MZ Combined connections
        self.MZ_com_led = QLed(self, onColour=QLed.Red, shape=QLed.Circle)
        self.MZ_com_led.value=True
        self.ui.MZ_com_led_layout.addWidget(self.MZ_com_led)
        self.ui.MZ_com_dialog.clicked.connect(self.MZ_com_openFolderDialog)
        self.ui.MZ_com_fit.clicked.connect(self.MZ_com_openFit)


        #Open  the window with the tir creation process
        self.ui.tir_button.clicked.connect(self.open_create_tir)

        #Changing FZ nom, R0 or LONGVL -> change tir_data
        self.ui.FZ0.valueChanged.connect(self.update_FZ_R0_VX)
        self.ui.R0.valueChanged.connect(self.update_FZ_R0_VX)
        self.ui.VX0.valueChanged.connect(self.update_FZ_R0_VX)
        
    #FX pure functions
    def FX_pure_openFolderDialog(self):
        self.FX_pure_folder = QFileDialog.getExistingDirectory(self, "Select FX pure folder")
        if self.FX_pure_folder:
            self.ui.FX_pure_path.setText(self.FX_pure_folder)
            self.ui.FX_pure_fit.setEnabled(True)     

    def FX_pure_openFit(self):
        try:
            FZ0 = self.ui.FZ0.value()
            self.FX_pure_fit = FX_pure(self.FX_pure_folder,self.tir_data,FZ0)
            self.FX_pure_fit.FX_pure_task.connect(self.FX_pure_led_enable)
            self.FX_pure_fit.FX_pure_task.connect(self.update_tir_data)
            self.FX_pure_fit.show()
        except Exception as e:
            self.showErrorDialog(str(e))

    def FX_pure_led_enable(self):
        self.FX_pure_led.setOnColour(QLed.Green)
        #Activating FX comb
        self.FX_com_led.setOnColour(QLed.Yellow)
        self.ui.FX_com_path.setEnabled(True)
        self.ui.FX_com_dialog.setEnabled(True)

    #Fy pure functions
    def FY_pure_openFolderDialog(self):
        self.FY_pure_folder = QFileDialog.getExistingDirectory(self, "Select FY pure folder")
        if self.FY_pure_folder:
            self.ui.FY_pure_path.setText(self.FY_pure_folder)
            #Check the folders (IF the .fit can read the files)
            self.ui.FY_pure_fit.setEnabled(True)     

    def FY_pure_openFit(self):
        try:
            FZ0 = self.ui.FZ0.value()
            self.FY_pure_fit = FY_pure(self.FY_pure_folder,self.tir_data,FZ0)
            self.FY_pure_fit.FY_pure_task.connect(self.FY_pure_led_enable)
            self.FY_pure_fit.FY_pure_task.connect(self.update_tir_data)
            self.FY_pure_fit.show()
        except Exception as e:
            self.showErrorDialog(str(e))

    def FY_pure_led_enable(self):
        self.FY_pure_led.setOnColour(QLed.Green)
        #Activating MZ_pure
        self.MZ_pure_led.setOnColour(QLed.Yellow)
        self.ui.MZ_pure_path.setEnabled(True)
        self.ui.MZ_pure_dialog.setEnabled(True)
        #Activating FY comb
        self.FY_com_led.setOnColour(QLed.Yellow)
        self.ui.FY_com_path.setEnabled(True)
        self.ui.FY_com_dialog.setEnabled(True)


    #Mz pure functions
    def MZ_pure_openFolderDialog(self):
        self.MZ_pure_folder = QFileDialog.getExistingDirectory(self, "Select MZ pure folder")
        if self.MZ_pure_folder:
            self.ui.MZ_pure_path.setText(self.MZ_pure_folder)
            #Check the folders (IF the .fit can read the files)
            self.ui.MZ_pure_fit.setEnabled(True)  

    def MZ_pure_openFit(self):
        try:
            FZ0 = self.ui.FZ0.value()
            R0 = self.ui.R0.value()
            VX = self.ui.VX0.value()
            self.MZ_pure_fit = MZ_pure(self.MZ_pure_folder,self.tir_data,FZ0,R0,VX)
            self.MZ_pure_fit.MZ_pure_task.connect(self.MZ_pure_led_enable)
            self.MZ_pure_fit.MZ_pure_task.connect(self.update_tir_data)
            self.MZ_pure_fit.show()
        except Exception as e:
            self.showErrorDialog(str(e))

    def MZ_pure_led_enable(self):
        self.MZ_pure_led.setOnColour(QLed.Green)
        if self.FX_com_led.onColour == QLed.Green and self.FY_com_led.onColour == QLed.Green:
            self.MZ_com_led.setOnColour(QLed.Yellow)
            self.ui.MZ_com_path.setEnabled(True)
            self.ui.MZ_com_dialog.setEnabled(True)
        
    #FX com functions
    def FX_com_openFolderDialog(self):
        self.FX_com_folder = QFileDialog.getExistingDirectory(self, "Select FX combined folder")
        if self.FX_com_folder:
            self.ui.FX_com_path.setText(self.FX_com_folder)
            #Check the folders (IF the .fit can read the files)
            self.ui.FX_com_fit.setEnabled(True)     

    def FX_com_openFit(self):
        try:
            FZ0 = self.ui.FZ0.value()
            self.FX_com_fit = FX_com(self.FX_com_folder,self.tir_data,FZ0)
            self.FX_com_fit.FX_com_task.connect(self.FX_com_led_enable)
            self.FX_com_fit.FX_com_task.connect(self.update_tir_data)
            self.FX_com_fit.show()
        except Exception as e:
            self.showErrorDialog(str(e))

    def FX_com_led_enable(self):
        self.FX_com_led.setOnColour(QLed.Green)
        if self.MZ_pure_led.onColour == QLed.Green and self.FY_com_led.onColour == QLed.Green:
            self.MZ_com_led.setOnColour(QLed.Yellow)
            self.ui.MZ_com_path.setEnabled(True)
            self.ui.MZ_com_dialog.setEnabled(True)

    #FY com functions
    def FY_com_openFolderDialog(self):
        self.FY_com_folder = QFileDialog.getExistingDirectory(self, "Select FY combined folder")
        if self.FY_com_folder:
            self.ui.FY_com_path.setText(self.FY_com_folder)
            #Check the folders (IF the .fit can read the files)
            self.ui.FY_com_fit.setEnabled(True)     

    def FY_com_openFit(self):
        try:
            FZ0 = self.ui.FZ0.value()
            self.FY_com_fit = FY_com(self.FY_com_folder,self.tir_data,FZ0)
            self.FY_com_fit.FY_com_task.connect(self.FY_com_led_enable)
            self.FY_com_fit.FY_com_task.connect(self.update_tir_data)
            self.FY_com_fit.show()
        except Exception as e:
            self.showErrorDialog(str(e))

    def FY_com_led_enable(self):
        self.FY_com_led.setOnColour(QLed.Green)
        if self.MZ_pure_led.onColour == QLed.Green and self.FX_com_led.onColour == QLed.Green:
            self.MZ_com_led.setOnColour(QLed.Yellow)
            self.ui.MZ_com_path.setEnabled(True)
            self.ui.MZ_com_dialog.setEnabled(True)

    #Mz com functions
    def MZ_com_openFolderDialog(self):
        self.MZ_com_folder = QFileDialog.getExistingDirectory(self, "Select MZ com folder")
        if self.MZ_com_folder:
            self.ui.MZ_com_path.setText(self.MZ_com_folder)
            #Check the folders (IF the .fit can read the files)
            self.ui.MZ_com_fit.setEnabled(True)  

    def MZ_com_openFit(self):
        try:
            FZ0 = self.ui.FZ0.value()
            R0 = self.ui.R0.value()
            VX = self.ui.VX0.value()
            self.MZ_com_fit = MZ_com(self.MZ_com_folder,self.tir_data,FZ0,R0,VX)
            self.MZ_com_fit.MZ_com_task.connect(self.MZ_com_led_enable)
            self.MZ_com_fit.MZ_com_task.connect(self.update_tir_data)
            self.MZ_com_fit.show()
        except Exception as e:
            self.showErrorDialog(str(e))

    def MZ_com_led_enable(self):
        self.MZ_com_led.setOnColour(QLed.Green)
        

    #General functions

    def open_link(self):
         url = QUrl("https://github.com/jmcavalcante/MFPy")
         QDesktopServices.openUrl(url)

    def update_FZ_R0_VX(self):
        self.tir_data.VERTICAL.FNOMIN = self.ui.FZ0.value()
        self.tir_data.DIMENSION.UNLOADED_RADIUS = self.ui.R0.value()
        self.tir_data.MODEL.LONGVL = self.ui.VX0.value()

    def update_tir_data(self,tir_data):
        self.tir_data = tir_data

    def showErrorDialog(self, error_message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText("Error (folder, .csv file or .tir file). Please check the documentation to understand how the files should be organized.")
        msgBox.setInformativeText(error_message)
        msgBox.setWindowTitle("Error")
        msgBox.exec_()

    def open_create_tir(self):
        self.write = write(self.tir_data)
        self.write.show()

    def open_file(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("This will override your fitted data.")
        msg_box.setWindowTitle("Warning")
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        options = QFileDialog.Options()
        response = msg_box.exec_()
        if response == QMessageBox.Ok:
            file_name, _ = QFileDialog.getOpenFileName(self, "Open .tir file", "", "Tir file (*.tir)", options=options)
            if file_name:
                self.ui.tir_label.setText('Using ' + file_name + ' as initial .tir file.')
                #reading tir file and using it as initial input to final tir
                try:
                    self.tir_data = mfpy.preprocessing.read_tir(file_name) #Creating a new tir_data structure using the new .tir file
                    self.ui.FZ0.setValue(self.tir_data.VERTICAL.FNOMIN)
                    self.ui.R0.setValue(self.tir_data.DIMENSION.UNLOADED_RADIUS)
                    self.ui.VX0.setValue(self.tir_data.MODEL.LONGVL)
                except Exception as e:
                    self.showErrorDialog(str(e))


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("fit_interface/design/MFpy_logo.png")))
    window = Main()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()