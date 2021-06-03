import socket 
import numpy as np 

def rpy2rv(roll, pitch, yaw):
    alpha = np.deg2rad(yaw)
    beta = np.deg2rad(pitch)
    gamma = np.deg2rad(roll)
    
    ca, cb, cg = np.cos(alpha), np.cos(beta), np.cos(gamma)
    sa, sb, sg = np.sin(alpha), np.sin(beta), np.sin(gamma)
    
    r11 = ca*cb
    r12 = ca*sb*sg-sa*cg
    r13 = ca*sb*cg+sa*sg
    r21 = sa*cb
    r22 = sa*sb*sg+ca*cg
    r23 = sa*sb*cg-ca*sg
    r31 = -sb
    r32 = cb*sg
    r33 = cb*cg
    
    theta = np.arccos((r11+r22+r33-1)/2)
    sth = np.sin(theta)
    kx = (r32-r23)/(2*sth)
    ky = (r13-r31)/(2*sth)
    kz = (r21-r12)/(2*sth)
    
    return theta, [kx, ky , kz]


def GetWitMitionSensor():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(("8.8.8.8", 1))

    local_ip = s.getsockname()[0]
    s.sendto(("WIT"+local_ip+"\r\n").encode("UTF-8"), ("<broadcast>", 9250))

    reciever =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    reciever.bind(('', 1399))

while True:
    # WT5300000868030.000,-0.009,1.008,0.000,0.000,0.000,-0.670,-0.071,-161.471,-159,-370,-502,39.65,3.33,-61,13003,0\r\n
    data, addr = reciever.recvfrom(1024)
    raw_data = data.decode("utf-8").split(',')
    roll, pitch, yaw = [ float(s) for s in raw_data[6:9] ]
    print(roll, pitch, yaw, rpy2rv(roll, pitch, yaw))

