import sys
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi
import pathlib
import sqlite3
from sqlite3 import Error


class Setup(QDialog):
    def __init__(self):
        super(Setup, self).__init__()
        mod_path = pathlib.Path(__file__).parent
        loadUi(mod_path / "setup.ui", self)

##Rutina para el Seteo del foco de los inputs en la posición 0 al hacer click##
        self.indexnameinput.installEventFilter(self)
        self.dailyvalueinput.installEventFilter(self)
        self.indexqueryinput.installEventFilter(self)
        self.indexqueryinput.installEventFilter(self)
        self.ipinput.installEventFilter(self)

# Validar Regex IP
        self.ipinput.textChanged.connect(self.validar_ip)

# Mostrar en tabla
        rowPosition = self.tablaindex.rowCount()
        self.tablaindex.insertRow(rowPosition)
        self.tablaindex.insertRow(rowPosition)
        self.tablaindex.setItem(
            0, 0, QTableWidgetItem("LALALALA"))

        # for i in range(1, 10, 1):
        #     self.tablaindex.insertRow(i)
        #     for j in range(1, 4, 1):
        #         QTableWidgetItem * item = new QTableWidgetItem(QString("(%1,%2)").arg(i).arg(j))
        #         self.tablaindex.setItem(i, j, item)
#  RELLENAR COMBO DE RETENTION EN MESES

        for i in range(1, 18, 1):
            self.retentioncombo.addItem(str(i))
        self.retentioncombo.setStyleSheet("color: white;"
                                          "background-color:rgb(40, 40, 40);")

# HABILITAR BOTON ADD CUANDO LOS CAMPOS ESTAN COMPLETOS
        self.addbutton.setEnabled(False)
        self.indexnameinput.textChanged.connect(self.habilitaboton)
        self.dailyvalueinput.textChanged.connect(self.habilitaboton)
        self.retentioncombo.currentTextChanged.connect(self.habilitaboton)


#  FUNCION VALIDAR REGEX  DE INPUT IP


    def validar_ip(self):
        ip = self.ipinput.text()
        validar = re.fullmatch('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip)
        if validar:
            self.ipinput.setStyleSheet("color: white;"
                                       "background-color:  rgb(40, 40, 40);"
                                       "selection-color: yellow;"
                                       "selection-background-color: blue;"
                                       "border: 1px solid green;")
            return True
        else:
            self.ipinput.setStyleSheet("color: white;"
                                       "background-color:  rgb(40, 40, 40);"
                                       "selection-color: yellow;"
                                       "selection-background-color: blue;"
                                       "border: 1px solid red;")
            return False


# Funcion BOTON ADD CUANDO LOS CAMPOS ESTAN COMPLETOS

    def habilitaboton(self):
        if ((self.indexnameinput.text() != "") and (len(self.dailyvalueinput.text()) > 0) and (self.ipinput.text() != "")
            ):
            self.addbutton.setEnabled(True)

## FUNCION para el Seteo del foco de los inputs en la posición 0 al hacer click##

    def eventFilter(self, source, event):
        if source == self.indexnameinput and event.type() == QtCore.QEvent.MouseButtonPress:
            self.indexnameinput.setFocus(QtCore.Qt.MouseFocusReason)
            self.indexnameinput.setCursorPosition(0)
            return True
        if source == self.dailyvalueinput and event.type() == QtCore.QEvent.MouseButtonPress:
            self.dailyvalueinput.setFocus(QtCore.Qt.MouseFocusReason)
            self.dailyvalueinput.setCursorPosition(0)
            return True
        if source == self.indexqueryinput and event.type() == QtCore.QEvent.MouseButtonPress:
            self.indexqueryinput.setFocus(QtCore.Qt.MouseFocusReason)
            self.indexqueryinput.setCursorPosition(0)
            return True
        if source == self.indexqueryinput and event.type() == QtCore.QEvent.MouseButtonPress:
            self.ipinput.setFocus(QtCore.Qt.MouseFocusReason)
            self.ipinput.setCursorPosition(0)
            return True
        return super().eventFilter(source, event)


##ALE##

# DB - Database creation

def createdb():

    try:

        con = sqlite3.connect('splunkindexdb.db')

        print("Database successfuly created")

    except Error:

        print(Error)

    finally:

        con.close()


createdb()


# DB - Table creation and check

def connection():

    try:

        con = sqlite3.connect('splunkindexdb.db')

        return con

    except Error:

        print(Error)


def createtable(con):

    cursorObj = con.cursor()

    cursorObj.execute("""CREATE TABLE IF NOT EXISTS indexes(
        id INTEGER PRIMARY KEY ASC AUTOINCREMENT UNIQUE,
        ip        VARCHAR (15) NOT NULL,
        name TEXT NOT NULL UNIQUE,
        dailyavg INT NOT NULL,
        retention INT NOT NULL);
        """)

    con.commit()


con = connection()

createtable(con)


# Inserting dummy values as example

def insertdummyregistry(con):

    cursorObj = con.cursor()

    cursorObj.execute(
        "INSERT OR REPLACE INTO indexes (name,ip,dailyavg,retention) VALUES('Openshift','127.000.000.001',2048,15)")

    con.commit()


con = connection()

insertdummyregistry(con)


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM indexes")

    rows = cur.fetchall()

    for row in rows:
        print(row)


select_all_tasks(con)

app = QApplication(sys.argv)
mainwindow = Setup()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1366)
widget.setFixedHeight(768)
widget.show()
app.exec_()
