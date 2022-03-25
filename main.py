from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout
import pandas as pd
import pyqtgraph as pg

WIDTH=1200
HEIGHT=1000


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Data Viewer")
        MainWindow.resize(WIDTH, HEIGHT)

        #Create Central Widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        #Create a label Widget
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(240, 50, 321, 121))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setObjectName("label")


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, WIDTH, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionImportCSV= QtWidgets.QAction(MainWindow)
        self.actionImportCSV.setObjectName("actionImportCSV")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionImportCSV)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.actionNew.triggered.connect(lambda: self.clicked("New was clicked"))
        self.actionSave.triggered.connect(lambda: self.clicked("Save was clicked"))
        self.actionCopy.triggered.connect(lambda: self.clicked("Copy was clicked"))
        self.actionPaste.triggered.connect(lambda: self.clicked("Paste was clicked"))
        self.actionExit.triggered.connect(MainWindow.close)
        self.actionImportCSV.triggered.connect(self.getFile)

        # Create a chart widget
        # self.layout = QtWidgets.QVBoxLayout(self)  # create the layout
        # self.pgcustom = CustomPlot()  # class abstract both the classes"
        # self.layout.addWidget(self.pgcustom)
        # self.show()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Data Viewer", "Data Viewer"))
        self.label.setText(_translate("Data Viewer", "TextLabel"))
        self.menuFile.setTitle(_translate("Data Viewer", "File"))
        self.menuEdit.setTitle(_translate("Data Viewer", "Edit"))
        self.actionCopy.setText(_translate("Data Viewer", "Copy"))
        self.actionCopy.setShortcut(_translate("Data Viewer", "Ctrl+C"))
        self.actionPaste.setText(_translate("Data Viewer", "Paste"))
        self.actionPaste.setShortcut(_translate("Data Viewer", "Ctrl+V"))
        self.actionSave.setText(_translate("Data Viewer", "Save"))
        self.actionSave.setShortcut(_translate("Data Viewer", "Ctrl+S"))
        self.actionNew.setText(_translate("Data Viewer", "New"))
        self.actionNew.setShortcut(_translate("Data Viewer", "Ctrl+N"))
        self.actionImportCSV.setText(_translate("Data Viewer", "Import CSV"))
        self.actionImportCSV.setShortcut(_translate("Data Viewer", "Ctrl+I"))
        self.actionExit.setText(_translate("Data Viewer", "Exit"))
        self.actionExit.setShortcut(_translate("Data Viewer", "Ctrl+E"))

    def clicked(self, text):
        self.label.setText(text)
        self.label.adjustSize()

    def getFile(self):
        try:
            self.filename = QFileDialog.getOpenFileName(filter="csv (*.csv)")[0]
            self.readData()
        except Exception as e:
            print(e)
            pass

    def readData(self):
        import os
        self.dataset = {}

        base_name = os.path.basename(self.filename)
        self.Title = os.path.splitext(base_name)[0]


        self.df = pd.read_csv(self.filename, encoding='utf-8').fillna(0)
        self.units = {}
        newcols = []
        for col in self.df:
            name, unit = col.split('(')
            newcols.append(name)
            self.units[name] = unit.strip(')')
        self.df.columns = newcols

        self.Update()  # lets 0th theme be the default : bmh

    def Update(self):
             print("update")
             print(self.df.head())
             print(self.units)
             print(len(self.df.index))


class CustomPlot1(pg.PlotWidget):
    def __init__(self):
        pg.PlotWidget.__init__(self)
        self.x = np.random.normal(size=1000) * 1e-5 #
        self.y = self.x * 750 + 0.005 * np.random.normal(size=1000)
        self.y -= self.y.min() - 1.0
        self.mask = self.x > 1e-15
        self.x = self.x[self.mask]
        self.y = self.y[self.mask]
        self.plot(self.x, self.y, pen='g', symbol='t', symbolPen='g', symbolSize=1)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
