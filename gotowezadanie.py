from PyQt5.QtWidgets import *
from pyqtgraph import *
import pyqtgraph as pg
import numpy as np
import os
from scipy import signal
from scipy.fft import fft
import pandas as pd


class App(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.title = 'Trzeci program okienkowy'
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 570

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.window = QWidget()  # tworzymy nowy obiekt klasy QWidget
        self.layout = QGridLayout()

        self.radio1 = []
        self.radio1.append(QRadioButton('sine'))
        self.radio1.append(QRadioButton('rectangle'))
        self.radio1.append(QRadioButton('triangle'))
        self.radio1.append(QRadioButton('sawtooth'))
        self.radio1.append(QRadioButton('white noise'))
        # ostatni z przycisków (o indeksie 2 na liście) będzie na starcie programu wybrany

        # tworzymy layout pionowy dla przycisków
        self.layout1 = QVBoxLayout()
        # wszystkie przyciski z listy dodjamey w pętli do layoutu
        for radio in self.radio1:
            self.layout1.addWidget(radio)
            # dodatkowo do każdego z nich podpinamy funkcję wywoływaną w momencie zmiany wartości
            radio.toggled.connect(self.radio1_toggle)

        self.group1 = QGroupBox()
        self.group1.setLayout(self.layout1)
        self.layout1.addStretch(1)
        self.radio1_toggle()

        self.button1 = QPushButton('Zapisz .csv', self)
        self.button1.clicked.connect(self.saveprzebieg)
        self.layout1.addWidget(self.button1)

        self.button4 = QPushButton("Zapisz .wav")
        self.button4.clicked.connect(self.zapiszwav)
        self.layout1.addWidget(self.button4)

        self.radio2 = []
        self.radio2.append(QRadioButton('przebieg czasowy'))
        self.radio2.append(QRadioButton('transformata Fouriera'))

        self.layout2 = QVBoxLayout()
        for radio in self.radio2:
            self.layout2.addWidget(radio)
            radio.toggled.connect(self.radio1_toggle)

        self.button2 = QPushButton('Zapisz .csv', self)
        self.button2.clicked.connect(self.savetransformata)
        self.layout2.addWidget(self.button2)

        self.layout2.addStretch(1)

        self.group2 = QGroupBox()
        self.group2.setLayout(self.layout2)

        self.layout.addWidget(self.group1, 0, 0)
        self.layout.addWidget(self.group2, 1, 0)

        self.setCentralWidget(self.window)

        self.button3 = QPushButton('Wyjdz', self)

        self.button3.clicked.connect(self.exit_program)
        self.layout.addWidget(self.button3, 20, 0)

        self.layout3 = QVBoxLayout()

        self.SpinBox1 = QSpinBox(self)
        etykieta_f = QLabel("Czestotliwosc:", self)
        self.layout3.addWidget(etykieta_f)
        self.layout3.addWidget(self.SpinBox1)
        self.SpinBox1.setMaximum(9999)
        self.SpinBox1.setValue(300)
        self.f = self.SpinBox1.value()
        self.SpinBox1.valueChanged.connect(self.aktualizuje_czestotliwosc)
        self.SpinBox1.valueChanged.connect(self.radio1_toggle)

        self.DoubleSpinBox1 = QDoubleSpinBox(self)
        etykieta_A = QLabel("Amplituda:", self)
        self.layout3.addWidget(etykieta_A)
        self.layout3.addWidget(self.DoubleSpinBox1)
        self.DoubleSpinBox1.setRange(0, 9999)
        self.DoubleSpinBox1.setValue(0.1)
        self.A = self.DoubleSpinBox1.value()
        self.DoubleSpinBox1.valueChanged.connect(self.aktualizuje_amplitude)
        self.DoubleSpinBox1.valueChanged.connect(self.radio1_toggle)

        self.SpinBox2 = QSpinBox(self)
        etykieta_sampling = QLabel("Probkowanie:", self)
        self.layout3.addWidget(etykieta_sampling)
        self.layout3.addWidget(self.SpinBox2)
        self.SpinBox2.setRange(0, 9999)
        self.SpinBox2.setValue(100)
        self.sampling = self.SpinBox2.value()
        self.SpinBox2.valueChanged.connect(self.aktualizuje_probkowanie)
        self.SpinBox2.valueChanged.connect(self.radio1_toggle)

        # czestotliwosc probkowania
        # odczytuje wartość z QSpinBox i przypusije ja do zmiennej wartośc 1
        self.SpinBox3 = QSpinBox(self)
        etykieta_czas = QLabel("Czas:", self)
        self.layout3.addWidget(etykieta_czas)
        self.layout3.addWidget(self.SpinBox3)
        self.SpinBox3.setRange(0, 9999)
        self.SpinBox3.setValue(5)
        self.czas = self.SpinBox3.value()
        self.SpinBox3.valueChanged.connect(self.aktualizuje_czas)
        self.SpinBox3.valueChanged.connect(self.radio1_toggle)

        self.group3 = QGroupBox()
        self.group3.setLayout(self.layout3)
        self.layout.addWidget(self.group3, 0, 1)

        # czas
        # odczytuje wartość z QSpinBox i przypusije ja do zmiennej wartośc 1
        self.N = self.czas*self.sampling
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setRowCount(self.N)
        self.layout.addWidget(self.table, 2, 0, 4, 2)
        self.table.clicked.connect(self.radio1_toggle)
        self.table.setItem(0, 0, QTableWidgetItem("Dziedzina"))
        self.table.setItem(0, 1, QTableWidgetItem("Zbior wartosci"))
        self.table.setItem(1, 0, QTableWidgetItem(" "))
        self.table.setItem(1, 1, QTableWidgetItem(" "))

        self.graph = pg.PlotWidget()
        self.layout.addWidget(self.graph, 0, 2, 0, 2)

        self.window.setLayout(self.layout)

        self.radio1[0].setChecked(True)
        self.radio2[0].setChecked(True)

        self.show()

    def saveprzebieg(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self, "QFileDialog.getOpenFileName()", "", options=options)
        # tworzy słownik klucz-wartość przechowujący dane
        data1 = {"t": self.t, "y": self.data}
        dataframe = pd.DataFrame(data1)  # tworzy pandas dataframe+
        file = open(fileName, 'w')
        file.write(str(dataframe))
        file.close()

    def zapiszwav(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self, "QFileDialog.getOpenFileName()", "", options=options)
        # tworzy słownik klucz-wartość przechowujący dane
        self.audio_data = np.int16(self.data * 2**15)
        data1 = {"t": self.sampling, "y": self.audio_data}
        dataframe = pd.DataFrame(data1)  # tworzy pandas dataframe+
        file = open(fileName, 'w')
        file.write(str(dataframe))
        file.close()

    def savetransformata(self):
        print('Zapisuje wynik działania do pliku')
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self, "QFileDialog.getOpenFileName()", "", options=options)
        # tworzy słownik klucz-wartość przechowujący dane
        data1 = {"t": self.xf, "y": self.yf}
        dataframe = pd.DataFrame(data1)  # tworzy pandas dataframe+
        file = open(fileName, 'w')
        file.write(str(dataframe))
        file.close()

    def aktualizuje_amplitude(self):
        self.A = self.DoubleSpinBox1.value()

    def aktualizuje_czestotliwosc(self):
        self.f = self.SpinBox1.value()

    def aktualizuje_probkowanie(self):
        self.sampling = self.SpinBox2.value()

    def aktualizuje_czas(self):
        self.czas = self.SpinBox3.value()

    def exit_program(self):
        print('Kończy działanie aplikacji')
        os._exit(0)

    def radio1_toggle(self):
        if self.radio1[0].isChecked():
            self.t = np.linspace(0, self.czas, self.sampling*self.czas)
            self.data = self.A * np.sin(2 * np.pi * self.f * self.t)
            self.data1 = {"t": self.t, "y": self.data}
            self.dataframe = pd.DataFrame(
                self.data1)
            for i in range(len(self.t)):
                for j in range(0, 2):
                    self.table.setItem(i, j, QtGui.QTableWidgetItem(
                        str(self.dataframe.values[i][j])))
            self.graph.clear()
            if self.radio2[0].isChecked():
                self.plot = self.graph.plot(self.t, self.data)
            elif self.radio2[1].isChecked():
                N = len(self.t)
                dt = self.t[1] - self.t[0]
                self.xf = np.fft.fftfreq(N, d=dt)[0:N // 2]
                self.yf = 2.0 / N * np.abs(fft(self.data)[0:N // 2])
                self.plot = self.graph.plot(self.xf, self.yf)
        elif self.radio1[1].isChecked():
            self.t = np.linspace(0, self.czas, self.sampling*self.czas)
            self.data1 = {"t": self.t, "y": self.data}
            self.dataframe = pd.DataFrame(
                self.data1)
            for i in range(len(self.t)):
                for j in range(0, 2):
                    self.table.setItem(i, j, QtGui.QTableWidgetItem(
                        str(self.dataframe.values[i][j])))
            self.graph.clear()
            self.data = self.A * \
                signal.square(np.sin(2 * np.pi * self.f * self.t))
            if self.radio2[0].isChecked():
                self.plot = self.graph.plot(self.t, self.data)
            elif self.radio2[1].isChecked():
                N = len(self.t)
                dt = self.t[1] - self.t[0]
                self.xf = np.fft.fftfreq(N, d=dt)[0:N // 2]
                self.yf = 2.0 / N * np.abs(fft(self.data)[0:N // 2])
                self.plot = self.graph.plot(self.xf, self.yf)
        elif self.radio1[3].isChecked():
            self.t = np.linspace(0, self.czas, self.sampling*self.czas)
            self.graph.clear()
            self.data = self.A*signal.sawtooth(2 * np.pi * self.f * self.t)
            self.data1 = {"t": self.t, "y": self.data}
            self.dataframe = pd.DataFrame(
                self.data1)
            for i in range(len(self.t)):
                for j in range(0, 2):
                    self.table.setItem(i, j, QtGui.QTableWidgetItem(
                        str(self.dataframe.values[i][j])))
            if self.radio2[0].isChecked():
                self.plot = self.graph.plot(self.t, self.data)
            elif self.radio2[1].isChecked():
                N = len(self.t)
                dt = self.t[1] - self.t[0]
                self.xf = np.fft.fftfreq(N, d=dt)[0:N // 2]
                self.yf = 2.0 / N * np.abs(fft(self.data)[0:N // 2])
                self.plot = self.graph.plot(self.xf, self.yf)
        elif self.radio1[2].isChecked():
            self.t = np.linspace(0, self.czas, self.sampling*self.czas)
            self.graph.clear()
            self.data = abs(
                self.A*signal.sawtooth(2 * np.pi * self.f * self.t))
            self.data1 = {"t": self.t, "y": self.data}
            self.dataframe = pd.DataFrame(
                self.data1)
            for i in range(len(self.t)):
                for j in range(0, 2):
                    self.table.setItem(i, j, QtGui.QTableWidgetItem(
                        str(self.dataframe.values[i][j])))
            if self.radio2[0].isChecked():
                self.plot = self.graph.plot(self.t, self.data)
            elif self.radio2[1].isChecked():
                N = len(self.t)
                dt = self.t[1] - self.t[0]
                self.xf = np.fft.fftfreq(N, d=dt)[0:N // 2]
                self.yf = 2.0 / N * np.abs(fft(self.data)[0:N // 2])
                self.plot = self.graph.plot(self.xf, self.yf)
        elif self.radio1[4].isChecked():
            self.t = np.linspace(0, self.czas, self.sampling*self.czas)
            self.graph.clear()
            self.data = self.A * (np.random.rand(len(self.t)) - 0.5)
            self.data1 = {"t": self.t, "y": self.data}
            self.dataframe = pd.DataFrame(
                self.data1)
            for i in range(len(self.t)):
                for j in range(0, 2):
                    self.table.setItem(i, j, QtGui.QTableWidgetItem(
                        str(self.dataframe.values[i][j])))
            if self.radio2[0].isChecked():
                self.plot = self.graph.plot(self.t, self.data)
            elif self.radio2[1].isChecked():
                N = len(self.t)
                dt = self.t[1] - self.t[0]
                self.xf = np.fft.fftfreq(N, d=dt)[0:N // 2]
                self.yf = 2.0 / N * np.abs(fft(self.data)[0:N // 2])
                self.plot = self.graph.plot(self.xf, self.yf)


app = QApplication(sys.argv)
ex = App()
app.exec_()
