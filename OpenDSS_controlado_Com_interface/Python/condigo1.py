__author__ = 'Paulo Radatz'

import win32com.client

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

        self.dssSolution.Solve()

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

if __name__ == '__main__':
    myObject = DSS("C:\Users\PauloRicardo\Desktop\TCC-Rede13\MASTER_RedeTeste13Barras.dss")
    myObject.myShow()

    opendssversion = myObject.versionDSS()
    print opendssversion







