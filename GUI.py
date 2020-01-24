import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
    QTextEdit, QGridLayout, QApplication,QTableWidget,QTableWidgetItem,QPushButton,QHBoxLayout,
    QFileDialog,QErrorMessage,QMessageBox)
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QColor
from pandas import read_excel
from VIKOR import vikor


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # creating EmailBlast widget and setting it as central
        self.body_window = BodyWindows(parent=self)
        self.setCentralWidget(self.body_window)
        # filling up a menu bar
        bar = self.menuBar()
        # File menu
        file_menu = bar.addMenu('File')
        # adding actions to file menu
        open_action = QtWidgets.QAction('Open', self)
        close_action = QtWidgets.QAction('Close', self)
        file_menu.addAction(open_action)
        file_menu.addAction(close_action)
        # Edit menu
        edit_menu = bar.addMenu('Edit')
        # adding actions to edit menu
        undo_action = QtWidgets.QAction('Undo', self)
        redo_action = QtWidgets.QAction('Redo', self)
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)

        # use `connect` method to bind signals to desired behavior
        close_action.triggered.connect(self.close)


class BodyWindows(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # create and set layout to place widgets
        self.ROW_Criteria = 0
        self.tableData = []
        self.excelData = []
        self.propertyWidget = PropertyWidget()
        # self.endButton = EndButton()
        print(self.ROW_Criteria)
        self.initUI()

    def initUI(self):
        
        self.criterion = QLabel('Number of criterion')
        self.criterionEdit = QLineEdit()
        # self.criterionEdit.textChanged.connect(self.sync_lineEdit)
        # authorEdit = QLineEdit()
        # reviewEdit = QTextEdit()

        self.button_OK = QPushButton('Go', self)
        self.button_OK.setToolTip('This is an example button')
        self.button_OK.clicked.connect(self.on_click)

        button_clear = QPushButton('Clear', self)
        button_clear.setToolTip('This is an example button')
        button_clear.clicked.connect(self.on_click_clear)

        self.check_table = QPushButton('Check Table',self)
        self.check_table.setToolTip('This is check table button')
        self.check_table.clicked.connect(self.checkTable)
        self.check_table.setEnabled(False)

        self.upload_file = QPushButton('Upload File', self)
        self.upload_file.setToolTip('This is Upload File')
        self.upload_file.clicked.connect(self.UploadData)
        self.upload_file.setEnabled(False)

        self.start = QPushButton('Run', self)
        self.start.setToolTip('Run It')
        self.start.clicked.connect(self.run)
        self.start.setEnabled(False)

        grid = QGridLayout()
        # grid.setSpacing(10)

        grid.addWidget(self.criterion, 1, 0)
        grid.addWidget(self.criterionEdit, 1, 1)
        grid.addWidget(self.button_OK, 2,0)
        grid.addWidget(button_clear, 2,1)
        grid.setColumnStretch(2,2)
        
        
        grid.addWidget(self.propertyWidget, 3, 0)
        grid.addWidget(self.check_table,3,1)
        grid.addWidget(self.upload_file,4,0)
        grid.addWidget(self.start,4,1)
        
        

        # grid.addWidget(self.endButton, 4, 0)

        # self.tableWidget.setItem(0,0, QTableWidgetItem("Cell (1,1)"))
        # self.tableWidget.setItem(3,1, QTableWidgetItem("Cell (4,2)"))
        # self.tableWidget.move(0,0)
        # grid.addWidget(self.tableWidget,3,1,5,1)
        
        # grid.addWidget(review, 3, 0)
        # grid.addWidget(reviewEdit, 3, 1, 5, 1)
        
        self.setLayout(grid) 
        
        self.setGeometry(300, 500, 300, 300)
        self.setWindowTitle('Review')    
        self.show()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click on_click',self.criterionEdit.text())
        self.button_OK.setEnabled(False)
        self.check_table.setEnabled(True)
        self.upload_file.setEnabled(True)
        self.propertyWidget.display(self.criterionEdit.text())
        self.ROW_Criteria = int(self.criterionEdit.text())

    @pyqtSlot()
    def on_click_clear(self):
        print("on_click_clear")
        self.propertyWidget.clearTable()
        self.criterionEdit.setText('1')
        self.button_OK.setEnabled(True)
        self.check_table.setEnabled(False)
        self.upload_file.setEnabled(False)
    
    def checkTable(self):
        print('checkTable is activate')
        print(self.propertyWidget.tableWidget)
        data = []
        dataNull = []
        model = self.propertyWidget.tableWidget.model()
        for row in range(self.propertyWidget.tableWidget.rowCount()):
            data.append([])
            for column in range(model.columnCount()):
                index = model.index(row, column)
                
                if model.data(index) is None or model.data(index)=='':
                    print('none2')
                    self.propertyWidget.tableWidget.setItem(row, column, QTableWidgetItem())
                    self.propertyWidget.tableWidget.item(row, column).setBackground(QColor(255,144,121))
                    dataNull.append(index)
                else :
                    if model.data(index) in  dataNull : 
                        dataNull.remove(model.data(index))
                    # We suppose data are strings
                    data[row].append(str(model.data(index)))
        #TODO: remove color cell 
        # for nulldata in dataNull  :
        #     if model.data(nulldata) != '' | None:
                
        # self.propertyWidget.tableWidget.setRowCount(0)
        print(data)
        if not  dataNull:
            self.start.setEnabled(True)
            self.tableData = data

    
    def UploadData(self):
        print('I am in UploadData')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Excel Files (*.xlsx)", options=options)
        if files:
            print(files)
            print(files.find('.xlsx'))
            
            if files.find('.xlsx') !=-1 or files.find('.xls') !=-1:

                excel_file = read_excel(files)

                
                if len(excel_file.columns) == self.ROW_Criteria : 
                    
                    
                    self.excelData = excel_file.values
                    print(type(self.excelData))
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Error")
                    msg.setInformativeText('Number of colums not equal with Criterions')
                    msg.setWindowTitle("Error")
                    msg.exec_()

            else: 
                print('eeeeerroor')
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Attach Excel file')
                msg.setWindowTitle("Error")
                msg.exec_()

                
            
    def run(self):
        print('run')
        weights = []
        min_max = [] 
        for row in self.tableData:
            weights.append(float(row[1]))
            if row[2] == 'min' or row[2] == 'max' : 
                min_max.append(row[2])
            else : 
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('in row {} ,column min/max just fill min or max'.format(row))
                msg.setWindowTitle("Error")
                msg.exec_()

        # excel_Data
       
        # weights
        print('123: ',weights,min_max)

        # criteria max/min
        import numpy as np
        vikor(np.asarray(self.excelData),np.asarray(min_max),np.asarray(weights),'y')
        self.ShowResultPage()

    def ShowResultPage(self):
        self.Rpage = ResultPage()
        self.Rpage.show()

class PropertyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
       super(PropertyWidget, self).__init__(parent)        
       HB_lay = QHBoxLayout(self)
       
       self.tableWidget = QTableWidget()
       
       self.tableWidget.setRowCount(0)
       self.tableWidget.setColumnCount(3)
       
       HB_lay.addWidget(self.tableWidget)
       HB_lay.addStretch()

    def display(self, n):
        try:
            print('NNNNNNN',n)
            print('n: ',int(n))
            
            self.tableWidget.setHorizontalHeaderLabels(['Criteria','Weghit','min/max'])
            self.tableWidget.setRowCount(int(n))

        except ValueError:
            
            self.tableWidget.clear()      
            self.tableWidget.setRowCount(0)
    def clearTable(self):
        data = []
        model = self.tableWidget.model()
        for row in range(self.tableWidget.rowCount()):
            data.append([])
            for column in range(model.columnCount()):
                index = model.index(row, column)
                # We suppose data are strings
                data[row].append(str(model.data(index)))
        self.tableWidget.setRowCount(0)
        print(data)
        print('clear Table')

# class EndButton (QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         super(EndButton, self).__init__(parent)        
#         HB_lay = QHBoxLayout(self)

#         button_OK = QPushButton('test11111111111111111111111111', self)
#         button_OK.setToolTip('This is an example button')
#         # self.button_OK.clicked.connect(self.on_click)

#         button_clear = QPushButton('test2', self)
#         button_clear.setToolTip('This is an example button')
#         # button_clear.clicked.connect(self.on_click_clear)


class ResultPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Result Page"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500
        self.initUI()
        

    def initUI(self) : 
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # creating main window
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())