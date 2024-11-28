
import mfpy
from fit_interface.py_from_ui.write_d import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QTableWidgetItem,QFileDialog
from PyQt5 import QtWidgets

class write(QMainWindow):
    def __init__(self,tir_data):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()
        self.tir_data = tir_data
        self.header = {}

        #Resizing table
        for widget in self.findChildren(QtWidgets.QTableWidget):
            widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            widget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)


        self.feeding_table()
        self.create_header()

        for widget in self.findChildren(QtWidgets.QTableWidget):
            widget.cellChanged.connect(self.create_header)

        self.ui.write_button.clicked.connect(self.write_tir)



    def feeding_table(self):
        #mdi_header
        self.mdi_index_cache = {self.ui.mdi_header.verticalHeaderItem(row).text(): row for row in range(self.ui.mdi_header.rowCount())}
        self.ui.mdi_header.setItem(self.mdi_index_cache.get('FILE_TYPE'),0,QTableWidgetItem(str(self.tir_data.MDI_HEADER.FILE_TYPE)))
        self.ui.mdi_header.setItem(self.mdi_index_cache.get('FILE_VERSION'),0,QTableWidgetItem(str(self.tir_data.MDI_HEADER.FILE_VERSION)))

        #units
        self.units_index_cache = {self.ui.units.verticalHeaderItem(row).text(): row for row in range(self.ui.units.rowCount())}
        self.ui.units.setItem(self.units_index_cache.get('LENGTH'),0,QTableWidgetItem(str(self.tir_data.UNITS.LENGTH)))
        self.ui.units.setItem(self.units_index_cache.get('FORCE'),0,QTableWidgetItem(str(self.tir_data.UNITS.FORCE)))
        self.ui.units.setItem(self.units_index_cache.get('ANGLE'),0,QTableWidgetItem(str(self.tir_data.UNITS.ANGLE)))
        self.ui.units.setItem(self.units_index_cache.get('MASS'),0,QTableWidgetItem(str(self.tir_data.UNITS.MASS)))
        self.ui.units.setItem(self.units_index_cache.get('TIME'),0,QTableWidgetItem(str(self.tir_data.UNITS.TIME)))

        #model
        self.model_index_cache = {self.ui.model.verticalHeaderItem(row).text(): row for row in range(self.ui.model.rowCount())}
        self.ui.model.setItem(self.model_index_cache.get('FITTYP '),0,QTableWidgetItem(str(self.tir_data.MODEL.FITTYP)))
        self.ui.model.setItem(self.model_index_cache.get('USE_MODE'),0,QTableWidgetItem(str(self.tir_data.MODEL.USE_MODE)))
        self.ui.model.setItem(self.model_index_cache.get('VXLOW'),0,QTableWidgetItem(str(self.tir_data.MODEL.VXLOW)))
        self.ui.model.setItem(self.model_index_cache.get('LONGVL'),0,QTableWidgetItem(str(self.tir_data.MODEL.LONGVL)))
        self.ui.model.setItem(self.model_index_cache.get('TYRESIDE'),0,QTableWidgetItem(str(self.tir_data.MODEL.TYRESIDE)))

        #dimension
        self.dimension_index_cache = {self.ui.dimension.verticalHeaderItem(row).text(): row for row in range(self.ui.dimension.rowCount())}
        self.ui.dimension.setItem(self.dimension_index_cache.get('UNLOADED_RADIUS'),0,QTableWidgetItem(str(self.tir_data.DIMENSION.UNLOADED_RADIUS)))
        self.ui.dimension.setItem(self.dimension_index_cache.get('WIDTH'),0,QTableWidgetItem(str(self.tir_data.DIMENSION.WIDTH)))
        self.ui.dimension.setItem(self.dimension_index_cache.get('ASPECT_RATIO'),0,QTableWidgetItem(str(self.tir_data.DIMENSION.ASPECT_RATIO)))
        self.ui.dimension.setItem(self.dimension_index_cache.get('RIM_RADIUS'),0,QTableWidgetItem(str(self.tir_data.DIMENSION.RIM_RADIUS)))
        self.ui.dimension.setItem(self.dimension_index_cache.get('RIM_WIDTH'),0,QTableWidgetItem(str(self.tir_data.DIMENSION.RIM_WIDTH)))

        #vertical
        self.vertical_index_cache = {self.ui.vertical.verticalHeaderItem(row).text(): row for row in range(self.ui.vertical.rowCount())}
        self.ui.vertical.setItem(self.vertical_index_cache.get('FNOMIN'),0,QTableWidgetItem(str(self.tir_data.VERTICAL.FNOMIN)))
        self.ui.vertical.setItem(self.vertical_index_cache.get('VERTICAL_STIFFNESS'),0,QTableWidgetItem(str(self.tir_data.VERTICAL.VERTICAL_STIFFNESS)))
        self.ui.vertical.setItem(self.vertical_index_cache.get('VERTICAL_DAMPING'),0,QTableWidgetItem(str(self.tir_data.VERTICAL.VERTICAL_DAMPING)))
        self.ui.vertical.setItem(self.vertical_index_cache.get('BREFF'),0,QTableWidgetItem(str(self.tir_data.VERTICAL.BREFF)))
        self.ui.vertical.setItem(self.vertical_index_cache.get('DREFF'),0,QTableWidgetItem(str(self.tir_data.VERTICAL.DREFF)))
        self.ui.vertical.setItem(self.vertical_index_cache.get('FREFF'),0,QTableWidgetItem(str(self.tir_data.VERTICAL.FREFF)))

        #long_slip_range
        self.long_slip_range_index_cache = {self.ui.long_slip_range.verticalHeaderItem(row).text(): row for row in range(self.ui.long_slip_range.rowCount())}
        self.ui.long_slip_range.setItem(self.long_slip_range_index_cache.get('KPUMIN'),0,QTableWidgetItem(str(self.tir_data.LONG_SLIP_RANGE.KPUMIN )))
        self.ui.long_slip_range.setItem(self.long_slip_range_index_cache.get('KPUMAX'),0,QTableWidgetItem(str(self.tir_data.LONG_SLIP_RANGE.KPUMAX)))

        #slip_angle_range
        self.slip_angle_range_index_cache = {self.ui.slip_angle_range.verticalHeaderItem(row).text(): row for row in range(self.ui.slip_angle_range.rowCount())}
        self.ui.slip_angle_range.setItem(self.slip_angle_range_index_cache.get('ALPMIN'),0,QTableWidgetItem(str(self.tir_data.SLIP_ANGLE_RANGE.ALPMIN )))
        self.ui.slip_angle_range.setItem(self.slip_angle_range_index_cache.get('ALPMAX'),0,QTableWidgetItem(str(self.tir_data.SLIP_ANGLE_RANGE.ALPMAX)))

        #inclination_angle_range
        self.inclination_angle_range_index_cache = {self.ui.inclination_angle_range.verticalHeaderItem(row).text(): row for row in range(self.ui.inclination_angle_range.rowCount())}
        self.ui.inclination_angle_range.setItem(self.inclination_angle_range_index_cache.get('CAMMIN'),0,QTableWidgetItem(str(self.tir_data.INCLINATION_ANGLE_RANGE.CAMMIN )))
        self.ui.inclination_angle_range.setItem(self.inclination_angle_range_index_cache.get('CAMMAX'),0,QTableWidgetItem(str(self.tir_data.INCLINATION_ANGLE_RANGE.CAMMAX)))

        #vertical_force_range
        self.vertical_force_range_index_cache = {self.ui.vertical_force_range.verticalHeaderItem(row).text(): row for row in range(self.ui.vertical_force_range.rowCount())}
        self.ui.vertical_force_range.setItem(self.vertical_force_range_index_cache.get('FZMIN'),0,QTableWidgetItem(str(self.tir_data.VERTICAL_FORCE_RANGE.FZMIN )))
        self.ui.vertical_force_range.setItem(self.vertical_force_range_index_cache.get('FZMAX'),0,QTableWidgetItem(str(self.tir_data.VERTICAL_FORCE_RANGE.FZMAX)))

        #scaling_coefficients
        self.scaling_coefficients_index_cache = {self.ui.scaling.verticalHeaderItem(row).text(): row for row in range(self.ui.scaling.rowCount())}
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LFZO'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LFZO )))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LCX'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LCX )))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LMUX'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LMUX )))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LEX'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LEX )))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LKX'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LKX )))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LHX'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LHX )))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LVX'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LVX )))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LGAX'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LGAX )))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LCY'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LCY )))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LMUY'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LMUY )))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LEY'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LEY )))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LKY'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LKY )))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LHY'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LHY )))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LVY'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LVY )))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LGAY'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LGAY )))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LTR'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LTR )))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LRES'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LRES )))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LGAZ'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LGAZ )))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LMX'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LMX )))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LVMX'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LVMX )))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LMY'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LMY )))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LXAL'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LXAL)))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LYKA'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LYKA )))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LVYKA'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LVYKA )))
        self.ui.scaling.setItem(self.scaling_coefficients_index_cache.get('LS'),0,QTableWidgetItem(str(self.tir_data.SCALING_COEFFICIENTS.LS)))
  
        #longitudinal_coefficients
        self.longitudinal_coefficients_index_cache = {self.ui.longitudinal.verticalHeaderItem(row).text(): row for row in range(self.ui.longitudinal.rowCount())}
        self.ui.longitudinal.setItem(self.longitudinal_coefficients_index_cache.get('PCX1'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PCX1 )))
        self.ui.longitudinal.setItem(self.longitudinal_coefficients_index_cache.get('PDX1'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PDX1)))
        self.ui.longitudinal.setItem(self.longitudinal_coefficients_index_cache.get('PDX2'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PDX2 )))
        self.ui.longitudinal.setItem(self.longitudinal_coefficients_index_cache.get('PDX3'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PDX3)))
        self.ui.longitudinal.setItem(self.longitudinal_coefficients_index_cache.get('PEX1'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PEX1)))
        self.ui.longitudinal.setItem(self.longitudinal_coefficients_index_cache.get('PEX2'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PEX2)))
        self.ui.longitudinal.setItem(self.longitudinal_coefficients_index_cache.get('PEX3'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PEX3)))
        self.ui.longitudinal.setItem(self.longitudinal_coefficients_index_cache.get('PEX4'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PEX4 )))
        self.ui.longitudinal.setItem(self.longitudinal_coefficients_index_cache.get('PKX1'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PKX1 )))
        self.ui.longitudinal.setItem(self.longitudinal_coefficients_index_cache.get('PKX2'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PKX2 )))
        self.ui.longitudinal.setItem(self.longitudinal_coefficients_index_cache.get('PKX3'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PKX3)))
        self.ui.longitudinal.setItem(self.longitudinal_coefficients_index_cache.get('PHX1'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PHX1)))
        self.ui.longitudinal.setItem(self.longitudinal_coefficients_index_cache.get('PHX2'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PHX2)))
        self.ui.longitudinal.setItem(self.longitudinal_coefficients_index_cache.get('PVX1'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PVX1 )))
        self.ui.longitudinal.setItem(self.longitudinal_coefficients_index_cache.get('PVX2'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.PVX2)))
        self.ui.longitudinal.setItem(self.longitudinal_coefficients_index_cache.get('RBX1'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.RBX1 )))
        self.ui.longitudinal.setItem(self.longitudinal_coefficients_index_cache.get('RBX2'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.RBX2 )))
        self.ui.longitudinal.setItem(self.longitudinal_coefficients_index_cache.get('RCX1'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.RCX1)))
        self.ui.longitudinal.setItem(self.longitudinal_coefficients_index_cache.get('REX1'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.REX1 )))
        self.ui.longitudinal.setItem(self.longitudinal_coefficients_index_cache.get('REX2'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.REX2)))
        self.ui.longitudinal.setItem(self.longitudinal_coefficients_index_cache.get('RHX1'),0,QTableWidgetItem(str(self.tir_data.LONGITUDINAL_COEFFICIENTS.RHX1 )))

        #lateral_coefficients
        self.lateral_coefficients_index_cache = {self.ui.lateral.verticalHeaderItem(row).text(): row for row in range(self.ui.lateral.rowCount())}
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('PCY1'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PCY1 )))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('PDY1'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PDY1)))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('PDY2'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PDY2 )))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('PDY3'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PDY3)))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('PEY1'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PEY1)))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('PEY2'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PEY2)))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('PEY3'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PEY3)))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('PEY4'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PEY4 )))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('PKY1'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PKY1 )))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('PKY2'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PKY2 )))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('PKY3'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PKY3)))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('PHY1'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PHY1)))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('PHY2'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PHY2)))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('PHY3'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PHY3)))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('PVY1'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PVY1 )))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('PVY2'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PVY2)))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('PVY3'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PVY3)))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('PVY4'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.PVY4)))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('RBY1'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.RBY1 )))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('RBY2'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.RBY2 )))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('RBY3'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.RBY3 )))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('RCY1'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.RCY1)))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('REY1'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.REY1 )))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('REY2'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.REY2)))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('RHY1'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.RHY1 )))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('RHY2'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.RHY2 )))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('RVY1'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.RVY1 )))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('RVY2'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.RVY2 )))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('RVY3'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.RVY3 )))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('RVY4'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.RVY4 )))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('RVY5'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.RVY5 )))
        self.ui.lateral.setItem(self.lateral_coefficients_index_cache.get('RVY6'),0,QTableWidgetItem(str(self.tir_data.LATERAL_COEFFICIENTS.RVY6 )))

        #aligning_coefficients
        self.aligning_coefficients_index_cache = {self.ui.aligning.verticalHeaderItem(row).text(): row for row in range(self.ui.aligning.rowCount())}
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QBZ1'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QBZ1 )))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QBZ2'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QBZ2)))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QBZ3'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QBZ3 )))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QBZ4'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QBZ4)))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QBZ5'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QBZ5)))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QBZ9'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QBZ9)))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QBZ10'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QBZ10)))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QCZ1'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QCZ1 )))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QDZ1'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QDZ1 )))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QDZ2'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QDZ2 )))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QDZ3'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QDZ3)))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QDZ4'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QDZ4)))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QDZ6'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QDZ6)))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QDZ7'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QDZ7 )))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QDZ8'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QDZ8)))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QDZ9'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QDZ9 )))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QEZ1'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QEZ1 )))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QEZ2'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QEZ2)))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QEZ3'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QEZ3 )))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QEZ4'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QEZ4)))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QEZ5'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QEZ5 )))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QHZ1'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QHZ1)))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QHZ2'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QHZ2 )))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QHZ3'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QHZ3 )))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('QHZ4'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.QHZ4)))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('SSZ1'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.SSZ1 )))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('SSZ2'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.SSZ2)))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('SSZ3'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.SSZ3 )))
        self.ui.aligning.setItem(self.aligning_coefficients_index_cache.get('SSZ4'),0,QTableWidgetItem(str(self.tir_data.ALIGNING_COEFFICIENTS.SSZ4)))

        #overturning_coefficients
        self.overturning_coefficients_index_cache = {self.ui.overturning.verticalHeaderItem(row).text(): row for row in range(self.ui.overturning.rowCount())}
        self.ui.overturning.setItem(self.overturning_coefficients_index_cache.get('QSX1'),0,QTableWidgetItem(str(self.tir_data.OVERTURNING_COEFFICIENTS.QSX1 )))
        self.ui.overturning.setItem(self.overturning_coefficients_index_cache.get('QSX2'),0,QTableWidgetItem(str(self.tir_data.OVERTURNING_COEFFICIENTS.QSX2)))
        self.ui.overturning.setItem(self.overturning_coefficients_index_cache.get('QSX3'),0,QTableWidgetItem(str(self.tir_data.OVERTURNING_COEFFICIENTS.QSX3 )))

        #rolling_coefficients
        self.rolling_coefficients_index_cache = {self.ui.rolling.verticalHeaderItem(row).text(): row for row in range(self.ui.rolling.rowCount())}
        self.ui.rolling.setItem(self.rolling_coefficients_index_cache.get('QSY1'),0,QTableWidgetItem(str(self.tir_data.ROLLING_COEFFICIENTS.QSY1 )))
        self.ui.rolling.setItem(self.rolling_coefficients_index_cache.get('QSY2'),0,QTableWidgetItem(str(self.tir_data.ROLLING_COEFFICIENTS.QSY2)))
        self.ui.rolling.setItem(self.rolling_coefficients_index_cache.get('QSY3'),0,QTableWidgetItem(str(self.tir_data.ROLLING_COEFFICIENTS.QSY3 )))
        self.ui.rolling.setItem(self.rolling_coefficients_index_cache.get('QSY4'),0,QTableWidgetItem(str(self.tir_data.ROLLING_COEFFICIENTS.QSY4 )))

    def create_header(self):
        self.header = {}
        for index in range(self.ui.tabWidget.count()):
            self.header[self.ui.tabWidget.tabText(index)] = {}
            tab = self.ui.tabWidget.widget(index)
            table = tab.findChild(QtWidgets.QTableWidget)
            for row in range(table.rowCount()):
                item = table.item(row, 0)
                row_label = table.verticalHeaderItem(row).text()
                try:
                    var_value = float(item.text())
                except:
                    var_value = item.text()
                self.header[self.ui.tabWidget.tabText(index)][row_label] = var_value

    def write_tir(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save tir", "", "Tir file (*.tir)", options=options)
        if file_name:
            if not file_name.endswith('.tir'):
                file_name += '.tir'
            mfpy.preprocessing.write_tir(file_name,self.header)


        

        