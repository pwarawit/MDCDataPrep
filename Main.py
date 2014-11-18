'''
Created on Nov 18, 2014

@author: InfoMobius
'''

import sys
from PyQt4 import QtGui

class MainWindow(QtGui.QWidget):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        # Initialize main window
        self.resize(250,150)
        self.center()
        self.setWindowTitle("MDC Data Preparation")
        
        # Initialize button
        btn = QtGui.QPushButton('Run', self)
        btn.resize(btn.sizeHint())
        btn.move(50,50)
        
        self.show()
        
    def center(self):
        # Put the MainWindow into the center of screen
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def main():
    app = QtGui.QApplication(sys.argv)
    myMainWindow = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()