from gui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox
import sys
import os
import var
import csv
from time import sleep
from threading import Thread
import sendMsg

global app
class MyGui(Ui_MainWindow, QtWidgets.QWidget):
    def __init__(self, mainWindow):
        Ui_MainWindow.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(mainWindow)


class myMainClass():
    def __init__(self):
        GUI.pushButton_start.clicked.connect(self.start)
        GUI.pushButton_pause.clicked.connect(self.pause)
        GUI.pushButton_stop.clicked.connect(self.stop)

        GUI.pushButton_uSendingNumber.clicked.connect(self.uSendingNumber)
        GUI.pushButton_uRecieverNumber.clicked.connect(self.uRecieverNumber)
        GUI.pushButton_uMessageBody.clicked.connect(self.uMessageBody)
        
        

        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.monitor)
        # self.timer.start(1000)
        Thread(target=updateStatus, daemon=True).start()
    def start(self):
        
        if var.pauseStatus == True:
            var.pauseStatus = False
            var.runStatus = True
        else:
            GUI.pushButton_start.setDisabled(True)
            data = read_data()
            var.runStatus = True
            Thread(target=sendMsg.main, daemon=True, args=[data, int(GUI.lineEdit_timeDuration.text()), int(GUI.lineEdit_messageLimit.text())]).start()
        

    def pause(self):
        GUI.pushButton_start.setDisabled(False)
        var.runStatus = False
        var.pauseStatus = True
        pass

    def stop(self):
        sys.exit()
        pass

    def fileNamePicker(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getOpenFileName(None,"Select file", "","CSV Files (*.csv)", options=options)
        return filePath

    def uSendingNumber(self):
        print("Upload Sending Number")
        senderNoFile = self.fileNamePicker()
        if senderNoFile:
            var.senderNoFile = senderNoFile
            print(senderNoFile)
            GUI.lineEdit_SendingNumber.setText(senderNoFile)
            Thread(target=tablePopulation, args=[senderNoFile, "sender"], daemon=True).start()
        else:
            pass

    def uRecieverNumber(self):
        print("Upload Reciever Number")
        recieverNoFile = self.fileNamePicker()
        if recieverNoFile:
            var.recieverNoFile = recieverNoFile
            print(recieverNoFile)
            GUI.lineEdit_recieverNumber.setText(recieverNoFile)
            Thread(target=tablePopulation, args=[recieverNoFile, "reciever"], daemon=True).start()
        else:
            pass

    def uMessageBody(self):
        print("Upload Sending Number")
        msgFile = self.fileNamePicker()
        if msgFile:
            var.msgFile = msgFile
            print(msgFile)
            GUI.lineEdit_messageBody.setText(msgFile)
            Thread(target=tablePopulation, args=[msgFile, "message"], daemon=True).start()
        else:
            pass

def updateStatus():

    while True:
        while not var.statusQ.empty():
            GUI.label_status.setText(var.statusQ.get())
        sleep(1)

def read_data():
    data = list()

    for count in range(0, var.tableRowCount):
        colD = ["","",""]
        try:
            colD[0] = GUI.tableWidget_data.item(count, 0).text()
        except:
            pass
        try:
            colD[1] = GUI.tableWidget_data.item(count, 1).text()
        except:
            pass
        try:
            colD[2] = GUI.tableWidget_data.item(count, 2).text()
        except:
            pass
        data.append([colD[0], colD[1], colD[2]])
    return data

def tablePopulation(filePath, kind):
    print("Populating Table - ", filePath, kind)
    try:      
        with open(filePath) as f:
            data = csv.reader(f, delimiter=',')
            data = list(data)

        lenData = len(data)-1
        print("Data length- ", lenData)

        if lenData > var.tableRowCount:
            GUI.tableWidget_data.setRowCount(lenData)
            var.tableRowCount = lenData

        kind = var.kind.index(kind)

        for count in range(lenData):
            GUI.tableWidget_data.setItem(count,kind, QTableWidgetItem(str(data[count+1][0])))

    except Exception as e:
        print(e)
    pass


if __name__ == '__main__':

    global app
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    # keyboard = Controller()
    try:
        def resource_path(relative_path):
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
            return os.path.join(os.path.abspath("."), relative_path)

        p = resource_path('favicon.ico')
        mainWindow.setWindowIcon(QtGui.QIcon(p))
    except Exception as e:
        print(e)

    mainWindow.setWindowFlags(mainWindow.windowFlags() |
                          QtCore.Qt.WindowMinimizeButtonHint |
                          QtCore.Qt.WindowSystemMenuHint)
    mainWindow.setWindowFlags(mainWindow.windowFlags() |
                          QtCore.Qt.WindowSystemMenuHint |
                          QtCore.Qt.WindowMinMaxButtonsHint)

    GUI = MyGui(mainWindow)
    mainWindow.show()

    myMC = myMainClass()

    app.exec_()
    print("Exit")
    sys.exit()