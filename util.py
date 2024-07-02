
import maya.cmds as cmds
import maya.OpenMayaUI as omui
import pymel.core as pm
import math



class Obj():

    @staticmethod
    def init_attr(joint, attr, type):
        if not joint.hasAttr(attr):
            joint.addAttr(attr, dataType=type)

    @staticmethod
    def delete_joint_obj(joint, attr):
        obj = joint.getAttr(attr)
        if obj is not None and pm.objExists(obj):
            pm.delete(obj)



class Joint():


    @staticmethod
    def make_circle_ctrl(normal=(0,0,1)):
        ctrls = []
        offsets = []
        for joint in pm.ls(sl=True, type="joint"):
            Obj.init_attr(joint, "ctrl", "string")
            Obj.init_attr(joint, "offset", "string")
            Obj.delete_joint_obj(joint, "ctrl")
            Obj.delete_joint_obj(joint, "offset")
            ctrl_node = pm.circle(nr = normal)
            ctrl = ctrl_node[0]
            ctrls.append(ctrl)
            offset = pm.group(ctrl, n="offset")
            offsets.append(offset)
            joint.setAttr("ctrl", ctrl.fullPath())
            joint.setAttr("offset", offset.fullPath())
            cnst = pm.pointConstraint(joint, offset)
            pm.delete(cnst)
            cnst = pm.orientConstraint(joint, offset)
            pm.delete(cnst)
        
        for x in reversed( range(1, len(ctrls) ) ):
            print(offsets[x], ctrls[x-1])
            pm.parent(offsets[x], ctrls[x-1])


    @staticmethod
    def show_axis():
        for j in pm.ls(sl=True, type="joint"):
            pm.setAttr(j + ".displayLocalAxis", True)

    @staticmethod
    def hide_axis():
        for j in pm.ls(sl=True, type="joint"):
            pm.setAttr(j + ".displayLocalAxis", False)

    @staticmethod
    def set_axis():
        pass

    @staticmethod
    def editOn():
        pm.selectMode(component=True)
        pm.selectType(localRotationAxis=True)
        pm.manipRotateContext("Rotate", e=True, mode=10)
    
    @staticmethod
    def editOff():
        pm.selectMode(object=True)
        pm.selectType(localRotationAxis=False)
        pm.manipRotateContext("Rotate", e=True, mode=2)


    @staticmethod
    def freeze():
        pm.joint(e=True, zso=True)




class CTRL():

    def __init__(self, ctrl):
        self.ctrl = ctrl

    def set_orient():
        pass

    def set_size():
        pass

    def set_color():
        pass



class Select():

    @staticmethod
    def root():
        parent = pm.listRelatives(p=True)
        parentJoint = pm.selected()[0]

        while(parent):

            parent = pm.listRelatives(parent, p=True)

            if pm.ls(parent, type="joint"):
                parentJoint = pm.ls(parent, type="joint")

        pm.select(parentJoint)


    @staticmethod
    def tree():
        joints = []
        for sel in pm.selected():
            pm.select(sel, hierarchy=True)
            joints += pm.selected()
            
        pm.select(pm.ls(joints, type="joint"))


    @staticmethod
    def leaves():
        tree = []
        for sel in pm.selected():
            pm.select(sel, hierarchy=True)
            tree += pm.selected()
        leaf_joints = []
        for joint in tree:
            children = pm.listRelatives(joint, children=True, type='joint')
            if not children:
                leaf_joints.append(joint)
        pm.select(pm.ls(leaf_joints, type="joint"))


    @staticmethod
    def joints():
        pm.select(pm.ls(type="joint"))




class Axis():
    def __init__(self):
        self.joint_children = {}
        self.zDirection = 0
    
    def _snapshotJointConnections(self):
        for joint in self.joints:
            self.joint_children[joint] = joint.getChildren()
    
    def _setJointConnections(self, connect):
        for joint in self.joint_children:
            if len(self.joint_children[joint]) > 1:
                for child in self.joint_children[joint]:
                    if connect:
                        pm.parent(child, joint)
                    else:
                        pm.parent(child, world=True)
    
    def _setJointOrient(self, x, y, orient, sign):
        xyz = ['x','y','z']
        updown = ["up", "down"]
        z = [i for i in [1,2,3] if (i != x) and (i != y)][0]
        secondaryAxisOrient="{0}{1}".format(xyz[orient-1], updown[sign])
        oj="{0}{1}{2}".format(xyz[x-1], xyz[y-1], xyz[z-1])
        for joint in self.joints:
            pm.joint(joint, e=True, oj=oj, secondaryAxisOrient=secondaryAxisOrient, zso=True)
    
    def _fixTipsOrient(self):
        for joint in self.joints:
            if len(self.joint_children[joint]) != 1:
                pm.joint(joint, oj="none", e=True, ch=True, zso=True)

    
    def run(self, prim, sec, orient, sign):
        self.joints = pm.ls(sl=True, type="joint")
        currentSel = pm.selected()
        self._snapshotJointConnections()
        self._setJointConnections(False)
        self._setJointOrient(prim, sec, orient, sign)
        self._fixTipsOrient()
        self._setJointConnections(True)
        pm.select(currentSel)





