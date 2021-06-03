import rtde_control
import rtde_receive
import numpy as np 

UR_IP = "192.168.1.102"

rtde_c = rtde_control.RTDEControlInterface(UR_IP)
rtde_r = rtde_receive.RTDEReceiveInterface(UR_IP)


def GetActualTCPPose():
    return np.array(rtde_r.GetActualTCPPose())


def Pose(position, wxyz):
    return np.concatenate([position, wxyz])

def Pose(position, zyx_euler_angle):
    pass 
