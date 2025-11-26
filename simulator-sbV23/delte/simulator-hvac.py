import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, QFrame
from PyQt5.QtCore import Qt, QTimer


import time
from scipy.optimize import curve_fit
import numpy as np
import math
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as pltlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

#from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2TkAgg)
import matplotlib.backends.backend_tkagg
import tkinter as Tk
from matplotlib.figure import Figure
import tkinter
from tkinter import *
import scipy as sc

class variables:
    def __init__(self):
        self.side=0.9
        self.airDensity=1.225
        self.noOfSides=[5,1]
        self.cAir=1.01 #J/gram-celcius
        self.diameter=12.0/100.0
        self.transCoeff=[0.1/.02,4]
        self.TRoom=32
        self.TIn=32
        self.inletSpeed=10
        self.stefanBoltzmann=5.670373*(10**(-8))
        self.emissivity=0.4
        self.tungstenArea=3*(10**(-5))
        self.wattageRatio=400/60
        self.tungstenTemp=3000
        self.sample=1
        self.bulbWattage=100
        self.percentOpen=100
        self.wallRoomCoeff=10
        self.measuredTemp=self.TRoom
        self.numberOfHumans=0
        self.numberOfBulbs=2
        self.recalculate()

    def recalculate(self):
        self.boxAirMass=self.airDensity*(self.side**3)
        self.area=self.side**2
        self.specMassAir=self.boxAirMass*self.cAir*1000
        self.massPerSecond=self.sample*(math.pi*self.diameter*self.diameter/4)*self.inletSpeed*self.airDensity*(self.percentOpen/100)
        self.plywoodCMass=(self.area)*(2/100.0)*545*1215*5.2*0.2
        self.wattage=self.numberOfHumans*120+self.numberOfBulbs*self.bulbWattage


##########   Setters   ###########        
    def setSide(self,side):
        self.side=side
        self.recalculate()
    def setAirDensity(self,airDensity):
        self.airDensity=airDensity
        self.recalculate()
    def setNoOfSides(self,noOfSides):
        self.noOfSides=noOfSides
        self.recalculate()
    def setCAir(self,cAir):
        self.cAir=cAir
        self.recalculate()
    def setDiameter(self,diameter):
        self.diameter=diameter
        self.recalculate()
    def setTransCoeff(self,transCoeff):
        self.transCoeff=transCoeff
        self.recalculate()
    def setTRoom(self,TRoom):
        self.TRoom=TRoom
        self.recalculate()
    def setTIn(self,TIn):
        self.TIn=TIn
        self.recalculate()
    def setInletSpeed(self,inletSpeed):
        self.inletSpeed=inletSpeed
        self.recalculate()    
    def setEmissivity(self,emissivity):
        self.emissivity=emissivity
    def setPercentOpen(self,percentOpen):
        self.percentOpen=percentOpen
        self.recalculate()
    def setTungstenArea(self,tungstenArea):
        self.tungstenArea=tungstenArea
        
    def setWattageRatio(self,wattageRatio):
        self.wattageRatio=wattageRatio
       
    def setSample(self,sample):
        self.sample=sample
        self.recalculate() 
    def setTungstenTemp(self,tungstenTemp):
        self.tungstenTemp=tungstenTemp
    def setBulbWattage(self,bulbWattage):
        self.bulbWattage=bulbWattage
    def setNumberOfBulbs(self,n):
        self.numberOfBulbs=n
    def setNumberOfHumans(self,n):
        self.numberOfHumans=n
    def getWattage(self):
        return self.wattage
##################################
class model:
    def __init__(self):
        self.var=variables()
        self.allTemps=[]
        self.i=0
        
        self.setPoint=0
        self.wallTemp=self.var.TRoom
    
    def getConduction(self):
        conduction=0
        for i in range(len(self.var.noOfSides)):
            conduction+=(self.var.transCoeff[i]*self.var.noOfSides[i])
     
        conduction=conduction*(self.wallTemp-self.var.TIn)*self.var.area
        return conduction
     

    def getRadiation(self):
        return (self.var.emissivity*self.var.stefanBoltzmann*self.var.tungstenArea*(self.var.tungstenTemp**4))

    def getRadiation2(self):
        return (self.var.getWattage()*.95/6)

    def getNewMixedHeat(self):
        massLeft=self.var.boxAirMass-self.var.massPerSecond
        t1=(massLeft*self.var.TRoom)
        t2=(self.var.massPerSecond*self.var.TIn)
        t=(t1+t2)*(self.var.cAir*1000)
        #print t1+t2
        return t
    def wallTempFunc(self):
        self.wallTemp+=(.95*self.var.getWattage()*self.var.sample-self.wallsAirTransfer()-self.getConduction()-self.getRadiation2())/self.var.plywoodCMass

    
    def wallsAirTransfer(self):
        return self.var.wallRoomCoeff*self.var.area*5.2*(self.wallTemp-self.var.TRoom)
      
    def getTRoom(self):
        return self.var.TRoom
    def getTIn(self):
        return self.var.TIn

    def setTIn(self,TIn):
        self.var.setTIn(TIn)
    def setTRoom(self,TRoom):
        self.var.setTRoom(TRoom)
    def getBulbWattage(self):
        return self.var.bulbWattage
    def setbulbWattage(self, bulbWattage):
        self.var.bulbWattage=bulbWattage
    def getBoxAirMass(self):
        return self.var.boxAirMass
    def setPercentOpen(self,percentOpen):
        self.var.setPercentOpen(percentOpen)
    def setI(self,i):
        self.i=i
    def setSetPoint(self,setPoint):
        self.setPoint=setPoint
    def getSetPoint(self):
        return self.setPoint



########## MAIN PART OF MODEL####################
 
    def runModel(self):

        newTRoom=self.getTRoom()
        
        self.wallTempFunc()
       
        """
        self.pid.setTRoom(self.var.measuredTemp) #interface with the PID sensor is sending value to PID
        self.pid.setSetPoint(self.setPoint)# PID is being told the setPoint from the GUI
        if self.tuningStatus='Autotune':
        
        self.setPercentOpen(50)#self.pid.getPid()) #PID is retruning the control variable.
        """
        #do emissivity of walls -> which takes the radiation and heats up and then the walls supply the air with heat. Conduction is with the walls temps
        deltaNewTRoom=(self.getNewMixedHeat()+self.wallsAirTransfer())/(self.getBoxAirMass()*self.var.cAir*1000)
        newTRoom=deltaNewTRoom
        self.setTRoom(newTRoom)
       
    def getAllTemps(self):
        self.runModel()
        return self.allTemps




####   PID   ######

class PID:
    def __init__(self,model):
        
        self.model=model
        self.heur=heuristic(self.model)
        self.TRoom=self.model.getTRoom()
        self.setPoint=0
        self.Ku=3.14*(100)/(2*.47)
        self.Pu=8
        self.Kp=12.9595829#.75*self.Ku*20
        self.Ki=0.044444#0.5/(0.625*self.Pu)
        self.Kd=5.625*100#self.Pu/10
        self.prevError=0
        self.sumError=2000
        self.prop_min=0
        self.prop_max=100
        self.prop=0
        self.measured=self.TRoom
        self.alpha=0.95
        self.prevProp=self.prop
        self.it=0
        self.currentIt=0
        self.riseStatus=True
        self.trend=0
        self.TRoomArray=[]
        
    def getProp(self):
        prop=self.Kp*(self.TRoom-self.setPoint)
        
        return prop  
    def getInt(self):
        if self.prop!=self.prop_max and self.prop!=self.prop_min:
            self.sumError+=(self.TRoom-self.setPoint)
        print(self.sumError)
        return self.Ki*self.sumError
    def getDiff(self):
        error=(self.TRoom-self.setPoint)
        diff=self.Kd*(error-self.prevError)
        self.prevError=error
        return diff
 
                  #  main #  method  #  for  #  PID #
    def Pid(self):
        self.measured=np.random.normal(loc=self.model.getTRoom(),scale=0.5)
        self.filtered= self.alpha*self.TRoom+(1-self.alpha)*self.measured
        self.TRoom=self.filtered
        self.TRoomArray.append(self.TRoom)
        self.prop= self.getProp()+self.getDiff()+self.getInt()
        if (self.prop<self.prop_min):
            self.prop= self.prop_min
        if (self.prop>self.prop_max):    
            self.prop= self.prop_max
        #print self.prop
        #self.prop=0.95*self.prevProp+0.05*self.prop
        self.prevProp=self.prop
        self.model.setPercentOpen(self.prop)
        self.heur.setPercentOpen(self.prop)
        self.heur.calcCostFunction()
        #self.Kp+=self.heur.delKp()
        #print self.heur.delKp()
        #print self.Kp
        #print 'KP', self.Kp, 'Ki ', self.Ki, 'Kd ', self.Kd
        #print '_____________'
        self.it+=1
        
        self.trend+=(self.setPoint-self.TRoom)


        if abs(self.setPoint-np.mean([temp for temp in self.TRoomArray[-10:]]))<0.1 and self.riseStatus==True and self.it-self.currentIt>20:
            
            self.Kp+=self.heur.timeToReach((self.it-self.currentIt),(self.trend/abs(self.trend)))
            self.riseStatus=False
            self.heur.reset()
            #b=curveFit(self.TRoomArray[-self.currentIt+100:-self.currentIt+150]).curvefit()
            #print 'Time Contant=  ', 1.0/b[1]
        self.model.runModel()

                    #       #         #        #      #
  
    def setKu(self,Ku):
        self.Ku=Ku
        self.autoSet()
    def setPu(self,Pu):
        self.Pu=Pu
        self.autoSet()
    def autoSet(self):
        self.Kp=0.6*self.Ku
        self.Ki=1/(0.5*self.Pu)
        self.Kd=0.125*self.Pu
        #print 'KP', self.Kp, 'Ki ', self.Ki, 'Kd ', self.Kd
    def setKp(self,Kp):
        self.Kp=Kp
    def setKi(self,Ki):
        self.Ki=Ki
    def setKd(self,Kd):
        self.Kd=Kd
    def getKp(self):
        return self.Kp
    def setKi(self):
        return self.Ki
    def setKd(self):
        return self.Kd
    def setTRoom(self,TRoom):
        self.TRoom=TRoom
    def setSetPoint(self,setPoint):
        self.setPoint=setPoint
    def getTRoom(self):
        return self.TRoom
    
#########################################
class autoTuneRelay:
    def __init__(self,model):
        self.model=model
        self.open=0
        self.status=True
        self.setPoint=0
        self.alpha=0.6
        self.TRoom=self.model.getTRoom()
        self.openTime=[]
        self.closedTime=[]
        self.previ=self.model.i
        self.peakStatus=False
        self.peaknumber=0
        self.cycles=5
        self.closedPercent=0.0
        self.openPercent=100.0
        self.allTemps=[]
    def autoTune(self):
        measured=np.random.normal(loc=self.model.getTRoom(),scale=.5)
        filtered= self.alpha*self.TRoom+(1-self.alpha)*measured
        self.TRoom=filtered#self.model.getTRoom()
        if(self.TRoom<self.setPoint*0.98 and self.status):
            self.status=False
            self.open=self.closedPercent
            self.closedTime.append(self.model.i-self.previ)
            self.previ=self.model.i
            self.model.setPercentOpen(self.open)
            self.peakStatus=True
            self.peaknumber+=1
        elif (self.TRoom>=self.setPoint*1.02 and not self.status):
            self.status=True
            self.open=self.openPercent
            self.openTime.append(self.model.i-self.previ)
            self.model.setPercentOpen(self.open)
            self.peakStatus=True
            self.previ=self.model.i
        self.model.runModel()
        if self.peaknumber>=2:
            self.allTemps.append(self.TRoom)
        #print self.status
        if self.peaknumber>=self.cycles  and self.peakStatus==True:
            openTimeAvg=(sum([time for time in self.openTime[1:]])/(len(self.openTime)-1))
            closedTimeAvg=(sum([time for time in self.closedTime[1:]])/(len(self.closedTime)-1))
            a=max(self.allTemps)-min(self.allTemps)
            e=.02*self.setPoint
            pi=3.14
            delta=self.openPercent-self.closedPercent
            self.ku=4*delta/(pi*(((a**2)-(e**2))**.5))
            self.pu=openTimeAvg+closedTimeAvg
            self.peakStatus=False
            
         
   
    def setSetPoint(self,setPoint):
        self.setPoint=setPoint
    def getTRoom(self):
        return self.TRoom
        
    
 
################ Auto Tune Heuristic#########################    
class heuristic:
    def __init__(self,model):
        self.model=model
        self.costFunction=0
        self.air=0
        self.percentOpen=0
        self.i=1
        self.prevAvgAir=0
        #self.timeToReach=0
    def calcCostFunction(self):
        if self.percentOpen!= 0.0:
            self.air+=self.percentOpen
            self.i+=1
        
    def delKp(self):
        if self.percentOpen!=0:
            return (-self.avgAirDiff/100)
        else: return 0.0
    def timeToReach(self, riseTime, trend):
        if trend==-1:
            self.avgAir=self.air/self.i
            self.avgAirDiff=self.prevAvgAir-self.avgAir
            self.prevAvgAir=self.avgAir
            print('Difference in air volume: ',self.avgAirDiff) 
            print(riseTime)
            return riseTime/50.0+self.avgAirDiff/5
        return 0
    def reset(self):
        self.i=1
        self.air=0
        self.avgAir=0
    def setPercentOpen(self,percent):
        self.percentOpen=percent
#############################################################
class curveFit:
    def __init__(self, y):
         
         self.x=np.array(list(range(len(y))))
         self.y=np.array(y)
         self.y=self.y-(min(self.y)*np.ones(len(self.y)))
    def func(self,x,a,b,c):
        return a * np.exp(-b * x)+c 
    
    def curvefit(self):
        self.popt,self.pcov=curve_fit(self.func,self.x,self.y)

        return self.popt
      
################  Graphical User Interface     ############


# Replace these placeholders with actual imports or definitions
# from model import model
# from PID import PID
# from autoTuneRelay import autoTuneRelay

class App_Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initialize()

    def initialize(self):
        self.setWindowTitle("HVAC Model with AutoTune PID")
        self.it = 0
        self.model = model()  # Placeholder for actual model class instance
        self.pid = PID(self.model)  # Placeholder for actual PID class instance
        self.ATR = autoTuneRelay(self.model)  # Placeholder for actual autoTuneRelay class instance
        self.model.setTRoom(32)
        self.model.setTIn(32)



        self.autoTuningStatus=False
        self.canvasFig=pltlib.figure(1)
        Fig=matplotlib.figure.Figure(figsize=(5,4), dpi=100)
        FigSubPlot=Fig.add_subplot(111)
        x=[]
        y=[]
        y1=[]
        y2=[]
        self.job=[]
        self.X=[]
        self.allTemps=[]
        self.setPointArray=[]
        self.dampPos=[]

        
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        self.layout = QGridLayout(centralWidget)

        # Frames
        box1 = QFrame(self, frameShape=QFrame.Box, lineWidth=1)
        box2 = QFrame(self, frameShape=QFrame.Box, lineWidth=1)
        box3 = QFrame(self, frameShape=QFrame.Box, lineWidth=1)

        # Labels
        self.secLabel = QLabel("Time= " + str(self.it) + " secs")
        self.tempLabel = QLabel("Room Temperature= %.2f" % self.model.getTRoom() + " degree C")
        self.dampLabel = QLabel("Damper Position= %.2f" % self.model.var.percentOpen + "%")

        # Buttons
        button = QPushButton("Start Process \n Submit SetPoint")
        button.clicked.connect(self.OnStartClick)
        button2 = QPushButton("Start Relay Tune")
        button2.clicked.connect(self.startRelayTune)
        closeButton = QPushButton("Close Window")
        closeButton.clicked.connect(self.close_window)

        # Entry
        self.entryVariable = QLineEdit()
        self.entryVariable.setPlaceholderText("Enter Set Point")
        self.entryVariable.returnPressed.connect(self.OnSetpointEnter)

        # Bulb and Human Buttons
        buttonBulbRise = QPushButton("Increase bulb")
        buttonBulbRise.clicked.connect(self.incrementBulb)
        buttonBulbFall = QPushButton("Decrease bulb")
        buttonBulbFall.clicked.connect(self.decrementBulb)
        self.bulbNumberLabel = QLabel('No of Bulbs= %d' % self.model.var.numberOfBulbs)
        buttonHumanRise = QPushButton("Increase human")
        buttonHumanRise.clicked.connect(self.incrementHuman)
        buttonHumanFall = QPushButton("Decrease human")
        buttonHumanFall.clicked.connect(self.decrementHuman)
        self.humanNumberLabel = QLabel('No of Humans= %d' % self.model.var.numberOfHumans)

        # Adding widgets to layouts
        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.secLabel)
        vbox2.addWidget(self.tempLabel)
        vbox2.addWidget(self.dampLabel)
        vbox2.addWidget(button)
        vbox2.addWidget(button2)
        vbox2.addWidget(closeButton)
        box2.setLayout(vbox2)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(buttonBulbRise)
        hbox3.addWidget(buttonBulbFall)
        hbox3.addWidget(self.bulbNumberLabel)
        vbox3 = QVBoxLayout()
        vbox3.addLayout(hbox3)
        hbox4 = QHBoxLayout()
        hbox4.addWidget(buttonHumanRise)
        hbox4.addWidget(buttonHumanFall)
        hbox4.addWidget(self.humanNumberLabel)
        vbox3.addLayout(hbox4)
        box3.setLayout(vbox3)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.entryVariable)
        box1.setLayout(vbox1)

        self.layout.addWidget(box1, 1, 0, 1, 3)
        self.layout.addWidget(box2, 3, 0)
        self.layout.addWidget(box3, 4, 0)

        # Matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')
        self.layout.addWidget(self.canvas, 0, 3, 9, 1)

        self.refreshFigure(np.array([]), np.array([]), np.array([]), np.array([]))

        self.show()

    def refreshFigure(self, x, y, setPoint, z):
        self.ax.clear()
        self.ax.plot(x, y, 'r-', label='Line 1')
        self.ax.plot(x, setPoint, 'b--', label='Line 2')
        self.ax.plot(x, z, 'g-', label='Line 3')
        self.ax.legend()
        self.canvas.draw()

    # Button Methods
    def OnStartClick(self):
        self.setPoint = float(self.entryVariable.text())
        self.pid.setSetPoint(self.setPoint)
        self.pid.it = self.it
        self.pid.currentIt = self.it
        self.pid.riseStatus = True
        self.pid.trend = 0
        self.compute()

    def OnSetpointEnter(self):
        self.OnStartClick()

    def startRelayTune(self):
        self.setPoint = float(self.entryVariable.text())
        self.ATR.setSetPoint(self.setPoint)
        self.autoTuningStatus = True
        self.startIter = self.it
        self.autoTune()

    def incrementBulb(self):
        self.model.var.numberOfBulbs += 1
        self.bulbNumberLabel.setText('No of Bulbs= %d' % self.model.var.numberOfBulbs)

    def decrementBulb(self):
        if self.model.var.numberOfBulbs > 0:
            self.model.var.numberOfBulbs -= 1
            self.bulbNumberLabel.setText('No of Bulbs= %d' % self.model.var.numberOfBulbs)

    def incrementHuman(self):
        self.model.var.numberOfHumans += 1
        self.humanNumberLabel.setText('No of Humans= %d' % self.model.var.numberOfHumans)

    def decrementHuman(self):
        if self.model.var.numberOfHumans > 0:
            self.model.var.numberOfHumans -= 1
            self.humanNumberLabel.setText('No of Humans= %d' % self.model.var.numberOfHumans)

    def close_window(self):
        self.close()

    # AutoTuning and Computing Methods
    def autoTune(self):
        self.allTemps.append(self.ATR.getTRoom())
        self.TRoom = self.ATR.getTRoom()
        self.X.append(self.it)
        self.setPointArray.append(self.setPoint)
        self.dampPos.append(self.model.var.percentOpen)
        X = np.array(self.X)
        Y = np.array(self.allTemps)
        Z = np.array(self.dampPos)
        setPointArray = np.array(self.setPointArray)
        self.refreshFigure(X, Y, setPointArray, Z)
        self.model.setI(self.it)
        self.cleanup()
        self.it += 1
        self.ATR.autoTune()
        if self.ATR.peaknumber < self.ATR.cycles:
            self.pid.setTRoom(self.ATR.getTRoom())
            QTimer.singleShot(1, self.autoTune)
        else:
            self.autoTuningStatus = False
            self.pid.setSetPoint(self.entryVariable.get())
            print("Ku= ", self.ATR.ku, " |  Pu= ", self.ATR.pu)
            self.pid.setKu(self.ATR.ku)
            self.pid.setPu(self.ATR.pu)
            self.pid.sumError = 0
            self.compute()

    def compute(self):
        self.pid.Pid()
        self.allTemps.append(self.pid.getTRoom())
        self.TRoom = self.model.getTRoom()
        self.X.append(self.it)
        self.setPointArray.append(self.setPoint)
        self.dampPos.append(self.model.var.percentOpen)
        X = np.array(self.X)
        Y = np.array(self.allTemps)
        Z = np.array(0)  # self.dampPos
        setPointArray = np.array(self.setPointArray)
        self.refreshFigure(X, Y, setPointArray, Z)
        self.model.setI(self.it)
        self.it += 1
        self.cleanup()
        if not self.autoTuningStatus:
            QTimer.singleShot(1, self.compute)

    def cleanup(self):
        self.secLabel.setText("Time= " + str(self.it) + " secs")
        self.tempLabel.setText("Room Temperature= %.2f" % self.TRoom + " degree C")
        self.dampLabel.setText("Damper Position= %.2f" % self.model.var.percentOpen + "%")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = App_Window()
    MainWindow.show()
    sys.exit(app.exec_())


###GUI tkinter to put set point and do PID
#see reinforcement learning







