#!/usr/bin/python
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect, QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QWidget, QLabel, QApplication, QMainWindow
from pyvistaqt import QtInteractor
import numpy as np 
import pyvista as pv
import vtk 
 

from functools import partial

url = "./URController/icons/"

class SceneViewer(QtInteractor):
    def __init__(self, parent):
        super().__init__(parent, multi_samples=4 )

    def add_tms_coil(self, coil_file_path):
        reader = vtk.vtkOBJReader()
        reader.SetFileName(coil_file_path)
        reader.Update()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(reader.GetOutput())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        self.add_actor(actor) # culling='back'
        _prop = actor.GetProperty()
        _prop.SetColor((0.2, 0.2, 1.))
        # if self.use_pbr_shading:  _prop.SetInterpolationToPBR()
        # else: 
        #     _prop.SetAmbient(0.06)
        #     _prop.SetDiffuse(0.75)
        #     _prop.SetOpacity(1.0)
        return actor

class URRtdeGui(QDialog):
    def __init__(self, pose = np.r_[0, 0, 0, 1, 0, 0]):
        super().__init__()
        self.setWindowTitle('UR-TRDE RPY Controller')
        self.initUI()
        self.tms_coil = self.visual.add_tms_coil("./data/tms_coil_oriented.obj")
        self.visual.link_views()
        # self.visual.show_bounds(self.tms_coil)
        # self.visual.show_axes()
        # self.visual.tot

    
    def axis_rotate(self, axis='r', dir = 1):
        print(self.tms_coil.GetOrientationWXYZ())

        if axis == 'r':
            self.tms_coil.RotateX(6*dir)
        elif axis == 'p':
            self.tms_coil.RotateY(6*dir)
        elif axis == 'y':
            self.tms_coil.RotateZ(6*dir)
        print(self.tms_coil.GetOrientationWXYZ())
    def axis_translate(self, axis='x', dir = 1):
        pass 
        # if axis == 'x':
        #     self.tms_coil.translate(np.r_[dir*0.0005, 0, 0])
        # elif axis == 'y':
        #     self.tms_coil.translate(np.r_[0, dir*0.0005, 0])

    def initUI(self):
        self.resize(600+10, 700)

        self.visual = SceneViewer(self)
        self.visual.interactor.setGeometry(QRect(5, 5, 600, 400))
        self.buttonGroup = QtWidgets.QGroupBox(self)
        self.buttonGroup.setGeometry(QRect(5, 400+10, 600, 300))
        self._hint_images = []
        self._up_buttons = []
        self._down_buttons = []
        button_size = 60
        margin_size = 20

    
        for i, img in enumerate(("rpy.png", "rpy.png", "roll.png", "pitch.png", "yaw.png")):
            offset = (100-button_size)//2 + 10
            self._hint_images.append ( QtWidgets.QPushButton(self.buttonGroup) )
            self._hint_images[i].setGeometry(QRect(10+(100+margin_size)*i, 10, 100, 100))
            self._hint_images[i].setIcon(QIcon(url+img))
            self._hint_images[i].setIconSize( QSize( 80, 80) )

            self._up_buttons.append (  QtWidgets.QPushButton(self.buttonGroup) )
            self._up_buttons[i].setGeometry(QRect(offset+(100+margin_size)*i, 10+110,  button_size, button_size))
            self._up_buttons[i].setIcon(QIcon(url+"up_arrow.png"))
            self._up_buttons[i].setIconSize( QSize( button_size, button_size) )

            self._down_buttons.append (  QtWidgets.QPushButton(self.buttonGroup) )
            self._down_buttons[i].setGeometry(QRect(offset+(100+margin_size)*i, 10+110+80+5, button_size, button_size))
            self._down_buttons[i].setIcon(QIcon(url+"down_arrow.png"))
            self._down_buttons[i].setIconSize( QSize( button_size, button_size) )
        
        self.Btn_roll_cw,  self.Btn_pitch_cw,   self.Btn_yaw_cw  = self._down_buttons[2:]
        self.Btn_roll_ccw, self.Btn_pitch_ccw,  self.Btn_yaw_ccw = self._up_buttons[2:]

        self.Btn_roll_ccw.clicked.connect(partial(self.axis_rotate, 'r' , 1))
        self.Btn_pitch_ccw.clicked.connect(partial(self.axis_rotate, 'p', 1))
        self.Btn_yaw_ccw.clicked.connect(partial(self.axis_rotate, 'y', 1))

        self.Btn_roll_cw.clicked.connect(partial(self.axis_rotate, 'r' , -1))
        self.Btn_pitch_cw.clicked.connect(partial(self.axis_rotate, 'p', -1))
        self.Btn_yaw_cw.clicked.connect(partial(self.axis_rotate, 'y', -1))

        self._up_buttons[0].clicked.connect(partial(self.axis_translate, 'x' , 1))
        self._up_buttons[1].clicked.connect(partial(self.axis_translate, 'y' , 1))
        self._down_buttons[0].clicked.connect(partial(self.axis_translate, 'x' , -1))
        self._down_buttons[1].clicked.connect(partial(self.axis_translate, 'y' , -1))
        
        self.show()



def main():
    app = QApplication(sys.argv)
    ex = URRtdeGui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()