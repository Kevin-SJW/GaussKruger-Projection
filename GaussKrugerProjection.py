# -*- coding: utf-8 -*-
"""
使用方法：
先使用GetCenterLatLon(Lat,Lon):输入坐标原点经纬度[lat,lon]，Lat为纬度，Lon为经度,
无参则默认灵山岛雷达站坐标

然后GetLatLon(X,Y):输入相对于坐标原点的坐标，返回一个列表[纬度，经度]


Lat纬度，Lon经度,X为横轴坐标，Y为纵轴坐标


def XYToLatLon(X, Y):#代码未检查
大地坐标转经纬度
X=大地坐标X
Y=大地坐标Y
IsSix= 6度带或3度带,默认为3

def LatLonToXY(Lat, Lon):
经纬度转大地坐标

def InputCenterLatLon(Lat, Lon):
获取坐标中心经纬度

def GetLatLon(self,X, Y):
获取最后目标的经纬度，假设在雷达范围内地球是一个平面
"""

import math
from math import *

RefCenterLon = 120.1642150#融合中心经度
RefCenterLat = 35.75020333#融合中心纬度
def LatLonToXY(Lat, Lon):
   #fi = (Lat-RefCenterLat)/180*math.pi
   fi = Lat / 180 * math.pi
   la = (Lon - RefCenterLon)/180*math.pi
   zi = RefCenterLat/180*math.pi
   a = 6378137
   b = 6356752.3142
   c = 6399593.6258
   f = 1 / 298.257223563
   E2 = 0.00673949674227
   Eta2 = 0.00673949674227
   V = sqrt(1+Eta2)
   N = c/V
   beta0 = 1.0 - 3.0 / 4.0 * E2 + 45.0 / 64.0 * E2 ** 2.0 - 175.0 / 256.0 * E2 ** 3 + 11025.0 / 16384.0 * E2 ** 4
   beta2 = beta0 - 1
   beta4 = 15.0 / 32.0 * E2 ** 2 - 175.0 / 384.0 * E2 ** 3 + 3675.0 / 8192.0 * E2 ** 4
   beta6 = -35.0 / 96.0 * E2 ** 3 + 735.0 / 2048.0 * E2 ** 4
   beta8 = 315.0 / 1024.0 * E2 ** 4
   Sz = c * (
      beta0 * zi + (beta2 * cos(zi) + beta4 * cos(zi) ** 3 + beta6 * cos(zi) ** 5 + beta8 * cos(zi) ** 7) * sin(
         zi))
   S = c * (
      beta0 * fi + (beta2 * cos(fi) + beta4 * cos(fi) ** 3 + beta6 * cos(fi) ** 5 + beta8 * cos(fi) ** 7) * sin(
      fi))
   X = S + la ** 2 * N / 2.0 * sin(fi) * cos(fi) + la ** 4 * N / 24.0 * sin(fi) * cos(fi) ** 3.0 * (5.0 - tan(fi) ** 2 +
   9.0 * Eta2 + 4 * Eta2 ** 2)+la ** 6 * N / 720.0 * sin(fi) * cos(fi) ** 5 * (61 - 58 * tan(fi) ** 2 + tan(fi) ** 4)
   Y = la * N * cos(fi) + la ** 3 * N / 6.0 * cos(fi) ** 3 * (1 - tan(fi) ** 2 + Eta2) + la ** 5 * N / 120.0 * cos(
      fi) ** 5 * (5 - 18 * tan(fi) ** 2 + tan(fi) ** 4)
   Z = Sz + la ** 2 * N / 2.0 * sin(zi) * cos(zi) + la ** 4 * N / 24.0 * sin(zi) * cos(zi) ** 3.0 * (5.0 - tan(zi) ** 2 +
   9.0 * Eta2 + 4 * Eta2 ** 2)+la ** 6 * N / 720.0 * sin(zi) * cos(zi) ** 5 * (61 - 58 * tan(zi) ** 2 + tan(zi) ** 4)
   X = X - Z
   return [Y,X] #X为纵轴，Y为横轴,因此换为[横，纵]输出

# 高斯投影由大地坐标(Unit:Metres)反算经纬度(UnitD)
def XYToLatLon(X, Y): #
   deltaXY = LatLonToXY(RefCenterLat + 1, RefCenterLon + 1)
   LB1 = X/deltaXY[0] + RefCenterLon
   LB2 = Y/deltaXY[1] + RefCenterLat
   while 1:
      XY2=LatLonToXY(LB2,LB1)
      tempX = XY2[0] - X
      tempY = XY2[1] - Y
      if tempX<100 and tempY<100:
         break
      else:
         LB1 = LB1 - tempX/deltaXY[0]
         LB2 = LB2 - tempY/deltaXY[1]
   return [LB2,LB1]

# 获取融合中心（X,Y坐标原点）经纬度
def InputCenterLatLon(Lat = RefCenterLat, Lon = RefCenterLon):
    global RefCenterLat
    global RefCenterLon
    RefCenterLat = Lat
    RefCenterLon = Lon

# 计算目标的经纬度
def GetLatLon(X, Y):
   return XYToLatLon(X, Y)

def GetXY(Lat,Lon):
   return LatLonToXY(Lat,Lon)


if __name__ == '__main__':
    InputCenterLatLon()
    print "输入坐标获取经纬度示例 输入（X,Y）：(68482.3054318,6111.88293390)，输出 纬度，经度",GetLatLon(-3179.9320142,3389.8387565)
    print "输入经纬度获取坐标示例 输入（纬度,经度)：（35.80541, 120.92219)，输出 纬度，经度:",GetXY(35.80541, 120.92219)


