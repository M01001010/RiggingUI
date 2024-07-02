
from PySide2  import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import maya.cmds as cmds
import maya.OpenMayaUI as omui
import pymel.core as pm
from rigging import util



def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class RigUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(RigUI, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setObjectName('CreatePolygonUI_uniqueId')
        self.setWindowTitle("Light Rig Controller")
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.editMode = False
        self.create_widgets()
        self.connect_widgets()


    def create_widgets(self):
        self.setWindowFlags(QtCore.Qt.Tool)
        self.resize(300, 400) # re-size the window
        label_selection = QtWidgets.QLabel("Selection:")  
        label_selection.setStyleSheet("color: white;background-color: black;")
        label_selection.setFixedHeight(20)    
        label_selection.setAlignment(QtCore.Qt.AlignCenter)
        self.sel_root = QtWidgets.QPushButton("Root")
        self.sel_leaves = QtWidgets.QPushButton("Leaves")
        self.sel_tree = QtWidgets.QPushButton("Hierarchy")
        self.sel_Joints = QtWidgets.QPushButton("Joints")
        selectGrid = QtWidgets.QGridLayout()
        selectGrid.addWidget(self.sel_root, 0, 0)
        selectGrid.addWidget(self.sel_tree, 0, 1)
        selectGrid.addWidget(self.sel_leaves, 1, 0)
        selectGrid.addWidget(self.sel_Joints, 1, 1)
        v_sel = QtWidgets.QVBoxLayout()
        v_sel.addWidget(label_selection)
        v_sel.addSpacerItem(QtWidgets.QSpacerItem(10, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed))
        v_sel.addLayout(selectGrid)
        tab_joint = QtWidgets.QTabWidget()
        tab_joint.addTab(TabJoint(self), "JOINTS")
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(v_sel)
        layout.addWidget(tab_joint)
        layout.addStretch(1)
        self.setLayout(layout)
        
        
    def connect_widgets(self):
        self.sel_root.released.connect(util.Select.root)
        self.sel_leaves.released.connect(util.Select.leaves)
        self.sel_tree.released.connect(util.Select.tree)
        self.sel_Joints.released.connect(util.Select.joints)





class TabJoint(QtWidgets.QWidget):
    def __init__(self, p):
        super(TabJoint, self).__init__(p)
        self.utiljoint = util.Joint()
        self.Axis = util.Axis()
        self.is_edit_mode = False
        self.create_widgets()
        self.setConnection()


    def create_widgets(self):
        header = QtWidgets.QLabel("Functions") 
        header.setStyleSheet("color: white;background-color: black;")
        header.setFixedHeight(20)
        header.setAlignment(QtCore.Qt.AlignCenter)
        self.btn_show = QtWidgets.QPushButton("Show")
        self.btn_hide = QtWidgets.QPushButton("Hide")
        self.btn_edit = QtWidgets.QPushButton("Edit")
        self.btn_edit.setStyleSheet("color: black;background-color: gray;")
        self.btn_freeze = QtWidgets.QPushButton("Freeze")
        self.btn_ikfk = QtWidgets.QPushButton("Make ctrl")
        #self.btn_freeze = QtWidgets.QPushButton("Freeze")
        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.btn_show, 0, 0)
        grid.addWidget(self.btn_hide, 0, 1)
        grid.addWidget(self.btn_edit, 1, 0)
        grid.addWidget(self.btn_freeze, 1, 1)
        grid.addWidget(self.btn_ikfk, 2, 0)
        self.l2 = QtWidgets.QLabel("Axes")   
        self.l2.setStyleSheet("color: white;background-color: black;")
        self.l2.setFixedHeight(20)
        self.l2.setAlignment(QtCore.Qt.AlignCenter)
        self.lPrimary = QtWidgets.QLabel("Primary Axis:")
        self.pX = QtWidgets.QRadioButton("X")
        self.pX.setChecked(True)
        self.pY = QtWidgets.QRadioButton("Y")
        self.pZ = QtWidgets.QRadioButton("Z")
        self.dummy = QtWidgets.QLabel("")
        self.hPrimary = QtWidgets.QHBoxLayout()
        self.hPrimary.addWidget(self.pX)
        self.hPrimary.addWidget(self.pY)
        self.hPrimary.addWidget(self.pZ)
        self.hPrimary.addWidget(self.dummy)
        self.lSecondary = QtWidgets.QLabel("Secondary Axis:")
        self.sX = QtWidgets.QRadioButton("X")
        self.sY = QtWidgets.QRadioButton("Y")
        self.sY.setChecked(True)
        self.sZ = QtWidgets.QRadioButton("Z")
        self.hSecondary = QtWidgets.QHBoxLayout()
        self.hSecondary.addWidget(self.sX)
        self.hSecondary.addWidget(self.sY)
        self.hSecondary.addWidget(self.sZ)
        self.hSecondary.addWidget(self.dummy)
        self.lOrient = QtWidgets.QLabel("Primary Axis World Orientation:")
        self.oX = QtWidgets.QRadioButton("X")
        self.oY = QtWidgets.QRadioButton("Y")
        self.oY.setChecked(True)
        self.oZ = QtWidgets.QRadioButton("Z")
        self.sN = QtWidgets.QRadioButton("None")
        self.oSign = QtWidgets.QComboBox()
        self.oSign.addItem('+')
        self.oSign.addItem('-')
        self.hOrient = QtWidgets.QHBoxLayout()
        self.hOrient.addWidget(self.oX)
        self.hOrient.addWidget(self.oY)
        self.hOrient.addWidget(self.oZ)
        self.hOrient.addWidget(self.oSign)
        self.btnApply = QtWidgets.QPushButton("Apply")
        self.vPrimary = QtWidgets.QVBoxLayout()
        self.vPrimary.addWidget(self.lPrimary)
        self.vPrimary.addLayout(self.hPrimary)
        self.vSecondary = QtWidgets.QVBoxLayout()
        self.vSecondary.addWidget(self.lSecondary)
        self.vSecondary.addLayout(self.hSecondary)
        self.vOrient = QtWidgets.QVBoxLayout()
        self.vOrient.addWidget(self.lOrient)
        self.vOrient.addLayout(self.hOrient)
        self.layV1 = QtWidgets.QVBoxLayout()
        self.layV1.setContentsMargins(0,0,0,0)
        self.layV1.addWidget(header)
        self.layV1.addSpacerItem(QtWidgets.QSpacerItem(10, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed))
        self.layV1.addLayout(grid)
        self.layV2 = QtWidgets.QVBoxLayout()
        self.layV2.addWidget(self.l2)
        self.layV2.addSpacerItem(QtWidgets.QSpacerItem(10, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed))
        self.layV2.addLayout(self.vPrimary)
        self.layV2.addSpacerItem(QtWidgets.QSpacerItem(10, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed))
        self.layV2.addLayout(self.vSecondary)
        self.layV2.addSpacerItem(QtWidgets.QSpacerItem(10, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed))
        self.layV2.addLayout(self.vOrient)
        self.layV2.addSpacerItem(QtWidgets.QSpacerItem(10, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed))
        self.layV2.addWidget(self.btnApply)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(4,4,4,4)
        layout.addLayout(self.layV1)
        layout.addSpacerItem(QtWidgets.QSpacerItem(10, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        layout.addLayout(self.layV2)
        layout.addSpacerItem(QtWidgets.QSpacerItem(10, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        self.setLayout(layout)


    
    def setConnection(self):
        self.btnGrp1 = QtWidgets.QButtonGroup(self)
        [self.btnGrp1.addButton(x) for x in [self.pX, self.pY, self.pZ]]

        self.btnGrp2 = QtWidgets.QButtonGroup(self)
        [self.btnGrp2.addButton(x) for x in [self.sX, self.sY, self.sZ, self.sN]]

        self.btnGrp3 = QtWidgets.QButtonGroup(self)
        [self.btnGrp3.addButton(x) for x in [self.oX, self.oY, self.oZ]]

        self.btn_show.released.connect(self.on_show)
        self.btn_hide.released.connect(self.on_hide)
        self.btn_edit.released.connect(self.on_toggleEdit)
        self.btn_freeze.released.connect(self.on_freeze)
        self.btn_ikfk.released.connect(self.on_ikfk)

        self.btnGrp1.buttonReleased.connect(self.onUpdateChoice0)
        self.btnGrp2.buttonReleased.connect(self.onUpdateChoice1)
        self.btnApply.released.connect(self.onApply)


    def on_show(self):
        util.Joint.show_axis()


    def on_hide(self):
        util.Joint.hide_axis()


    def on_toggleEdit(self):
        if(self.is_edit_mode):
            self.is_edit_mode = False
            self.btn_edit.setStyleSheet("background-color: gray;")
            util.Joint.editOff()
        else:
            self.is_edit_mode = True
            self.btn_edit.setStyleSheet("background-color: orange;")
            util.Joint.editOn()


    def on_freeze(self):
        util.Joint.freeze()


    def on_ikfk(self):
        util.Joint.make_circle_ctrl()


    def onUpdateChoice0(self, n):
        xyz = ["X", "Y", "Z"]
        indx = xyz.index(n.text())
        next = (indx + 1) % 3
        
        if self.btnGrp2.buttons()[indx].isChecked():
            btn = self.btnGrp2.buttons()[next]
            btn.setChecked(True)


    def onUpdateChoice1(self, n):
        xyz = ["X", "Y", "Z", "None"]
        indx = xyz.index(n.text())
        next = (indx + 1) % 3
        
        if (indx < 3):
            self.btnGrp1.buttons()[indx].isChecked()
            btn = self.btnGrp1.buttons()[next]
            btn.setChecked(True)
        
        self.oX.setEnabled(indx != 3)
        self.oY.setEnabled(indx != 3)
        self.oZ.setEnabled(indx != 3)
        self.oSign.setEnabled(indx != 3)
        

    def onApply(self):
        prim = abs(self.btnGrp1.checkedId())-1
        sec = abs(self.btnGrp2.checkedId())-1
        orient = abs(self.btnGrp3.checkedId())-1
        sign = self.oSign.currentIndex()
        self.Axis.run(prim, sec, orient, sign)




try:
    ui.deleteLater()
except:
    pass

ui = RigUI(maya_main_window())
ui.show()
