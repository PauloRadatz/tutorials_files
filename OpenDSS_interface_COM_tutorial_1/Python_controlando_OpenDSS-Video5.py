# coding: utf-8

import win32com.client
from pylab import *

class DSS():

    def __init__(self):

        # Criar a conexão entre Python e OpenDSS
        self.dssObj = win32com.client.Dispatch("OpenDSSEngine.DSS")

        # Iniciar o Objeto DSS
        if self.dssObj.Start(0) == False:
            print "Problemas em iniciar o OpenDSS"
        else:
            # Criar variáveis paras as principais interfaces
            self.dssText = self.dssObj.Text
            self.dssCircuit = self.dssObj.ActiveCircuit
            self.dssSolution = self.dssCircuit.Solution
            self.dssCktElement = self.dssCircuit.ActiveCktElement
            self.dssBus = self.dssCircuit.ActiveBus

    def versao_DSS(self):

        return self.dssObj.Version

if __name__ == "__main__":
    print """Autor: Paulo Radatz \nData: Fevereiro/2018 \nE-mail: paulo.radatz@gmail.com/paulo.radatz@usp.br \n"""

    # Criar um objeto da classe DSS
    objeto = DSS()

    print u"Versão do OpenDSS: " + objeto.versao_DSS() + "\n"