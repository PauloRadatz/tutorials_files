__author__ = 'Paulo Radatz'

import win32com.client
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.font_manager import FontProperties

fontP = FontProperties()
fontP.set_size("small")

class DSS(object):

    #------------------------------------------------------------------------------------------------------------------#
    def __init__(self, dssFileName):
        """ Compile OpenDSS model and initialize variables."""

        # Create a new instance of the DSS
        self.dssObj = win32com.client.Dispatch("OpenDSSEngine.DSS")

        # Start the DSS
        if self.dssObj.Start(0) == False:
            ### I need to add a window
            print "DSS Failed to Start"
        else:
            #Assign a variable to each of the interfaces for easier access
            self.dssText = self.dssObj.Text
            self.dssCircuit = self.dssObj.ActiveCircuit # Maybe this one can help
            self.dssSolution = self.dssCircuit.Solution
            self.dssCktElement = self.dssCircuit.ActiveCktElement
            self.dssBus = self.dssCircuit.ActiveBus
            self.dssMeters = self.dssCircuit.Meters
            self.dssPDElement = self.dssCircuit.PDElements

        # Always a good idea to clear the DSS when loading a new circuit
        self.dssObj.ClearAll()

        # Load the given circuit master file into OpenDSS
        self.dssText.Command = "compile " + dssFileName



    #------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------#
    def versionDSS(self):

        self.version = self.dssObj.Version
        return self.version

    #------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------#
    def myShow(self):

        self.dssText.Command = "show voltage LN nodes"

    #------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------#
    def mySolve(self, loadmult):

        self.dssSolution.LoadMult = loadmult
        self.dssSolution.Solve()

    #------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------#
    def plot_profile(self, loadmult):

        VA = self.dssCircuit.AllNodeVmagPUByPhase(1)
        DistA = self.dssCircuit.AllNodeDistancesByPhase(1)
        VB = self.dssCircuit.AllNodeVmagPUByPhase(2)
        DistB = self.dssCircuit.AllNodeDistancesByPhase(2)
        VC = self.dssCircuit.AllNodeVmagPUByPhase(3)
        DistC = self.dssCircuit.AllNodeDistancesByPhase(3)

        plt.subplot(1, 1, 1).set_xlim([0, 1.6])
        plt.subplot(1, 1, 1).set_ylim([0.9, 1.1])
        plt.title("Voltage Profile")
        plt.plot(DistA, VA, "k*", label="VA")
        plt.plot(DistB, VB, "b+", label="VB")
        plt.plot(DistC, VC, "gd", label="VC")
        plt.plot([0, 1.6], [0.95, 0.95], "r")
        plt.plot([0, 1.6], [1.05, 1.05], "r")
        plt.ylabel("Volts (pu)")
        plt.xlabel("Distance from Energy Meter")
        legend(bbox_to_anchor=(0, 0.96, 1, .102), loc=3, ncol=4, borderaxespad=0, shadow=True,fancybox=True, prop = fontP)
        grid(True)
        plt.show()


    #------------------------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    myObject = DSS("C:\Users\PauloRicardo\Desktop\TCC-Rede13\MASTER_RedeTeste13Barras.dss")

    myLoadMult = 1.2
    myObject.mySolve(myLoadMult)
    myObject.plot_profile(myLoadMult)









