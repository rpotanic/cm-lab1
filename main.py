import sys
import math
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
import untitled
import RK_methods as rk
import pickle


class MainWindow(QtWidgets.QMainWindow, untitled.Ui_MainWindow):
    def __init__(self):
        global ax
        super().__init__()
        self.setupUi(self)

        # инициализация фигуры и тулбара для графика
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # обработка нажатия кнопок
        self.button_go.clicked.connect(self.AddPlot)
        self.button_clear.clicked.connect(self.ClearPlot)
        # self.tabs.activated.connect(self.LoadTab)

        # установка графика
        self.verticalLayout_2.addWidget(self.toolbar)
        self.verticalLayout_2.addWidget(self.canvas)
        ax = self.figure.add_subplot(111)

    # def LoadTab(self):
    #     if (self.tabs.currentText()[0]) == 'm':
    #         table = self.load_obj("mtable_" + self.tabs.currentText())
    #         info = self.load_obj("minfo_" + self.tabs.currentText())
    #         self.tableWidget.setRowCount(0)
    #         self.tableWidget.setRowCount(len(table['X']))
    #         self.tableWidget.verticalHeader().hide()
    #         if self.tableWidget.columnCount() == 13:
    #             self.tableWidget.removeColumn(12)
    #             self.tableWidget.removeColumn(11)
    #         for i in range(len(table['X'])):
    #             if i == 0:
    #                 self.tableWidget.setItem(i, 0, QTableWidgetItem(str(i)))
    #                 self.tableWidget.setItem(i, 1, QTableWidgetItem(str(table['H'][i])))
    #                 self.tableWidget.setItem(i, 2, QTableWidgetItem(str(table['X'][i])))
    #                 self.tableWidget.setItem(i, 3, QTableWidgetItem(str(table['Y'][i])))
    #             else:
    #                 self.tableWidget.setItem(i, 0, QTableWidgetItem(str(i)))
    #                 self.tableWidget.setItem(i, 1, QTableWidgetItem(str(table['H'][i])))
    #                 self.tableWidget.setItem(i, 2, QTableWidgetItem(str(table['X'][i])))
    #                 self.tableWidget.setItem(i, 3, QTableWidgetItem(str(table['Y'][i])))
    #                 self.tableWidget.setItem(i, 4, QTableWidgetItem(str(table['W'][i])))
    #                 self.tableWidget.setItem(i, 5, QTableWidgetItem(str(table['W-V'][i])))
    #                 self.tableWidget.setItem(i, 6, QTableWidgetItem(str(table['S'][i])))
    #                 self.tableWidget.setItem(i, 7, QTableWidgetItem(str(table['local'][i]+table['Y'][i])))
    #                 self.tableWidget.setItem(i, 8, QTableWidgetItem(str(table['W'][i])))
    #                 self.tableWidget.setItem(i, 9, QTableWidgetItem(str(table['deg_count'][i])))
    #                 self.tableWidget.setItem(i, 10, QTableWidgetItem(str(table['inc_count'][i])))
    #                 header = self.tableWidget.horizontalHeader()
    #                 for i in range(0, 11, 1):
    #                     header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
    #         self.label_8.setText("Задача №9 основная, вариант №3, метод = РК* (4 порядка)")
    #         self.label_7.setText(
    #             "x0 = " + str(table['X'][0]) + ", y0 = " + str(table['Y'][0]) + ", T = " + str(info['x1']) + ", h0 = " + str(table['H'][0]) + ", ε = " + str(info['eps']) + ", ε гр = " + str(info['eps_bord']))
    #         self.label_9.setText(
    #             "Nmax = " + str(info['n']) + ", ε min = " + str(info['eps'] / 32) + ", n = " + str(info['n'] - 1) + ", b-xn = " + str(info['x1'] - table['X'][info['n'] - 1]))
    #         self.label_10.setText("max|S| = " + str(info['max err est']) + " при х = " + str(info['X on max err est']))
    #         self.label_20.setText("min|S| = " + str(info['min err est']) + " при х = " + str(info['X on min err est']))
    #         self.label_11.setText("ум. шага = " + str(info['deg']) + ", ув. шага = " + str(info['inc']))
    #         self.label_12.setText(
    #             "max h = " + str(max(table['H'])) + " при х = " + str(table['X'][table['H'].index(max(table['H'])) + 1]))
    #         if table['H'].index(min(table['H'])) == (info['n'] - 1):
    #             self.label_21.setText(
    #                 "min h = " + str(min(table['H'])) + " при х = " + str(table['X'][table['H'].index(min(table['H']))]))
    #         else:
    #             self.label_21.setText("min h = " + str(min(table['H'])) + " при х = " + str(
    #                 table['X'][table['H'].index(min(table['H'])) + 1]))
    #         self.label_13.setText("")
    #     else:
    #         table = self.load_obj("ttable_" + self.tabs.currentText())
    #         info = self.load_obj("tinfo_" + self.tabs.currentText())
    #         Y_ch=[]
    #         for i in range(len(table['X'])):
    #             Y_ch.append(self.check(table['X'][i], table['X'][0], table['Y'][0], info['a'], info['b'], info['c']))
    #         glob = [0] * (len(table['Y']))
    #         for i in range(len(table['Y'])):
    #             glob[i] = abs(Y_ch[i] - table['Y'][i])
    #         self.tableWidget.setRowCount(0)
    #         self.tableWidget.setRowCount(len(table['X']))
    #         self.tableWidget.verticalHeader().hide()
    #         if self.tableWidget.columnCount() == 11:
    #             self.tableWidget.insertColumn(11)
    #             self.tableWidget.insertColumn(12)
    #         self.tableWidget.setHorizontalHeaderItem(11, QTableWidgetItem("V(i)"))
    #         self.tableWidget.setHorizontalHeaderItem(12, QTableWidgetItem("V(i) - u(i)"))
    #         for i in range(len(table['X'])):
    #             if i == 0:
    #                 self.tableWidget.setItem(i, 0, QTableWidgetItem(str(i)))
    #                 self.tableWidget.setItem(i, 1, QTableWidgetItem(str(table['H'][0])))
    #                 self.tableWidget.setItem(i, 2, QTableWidgetItem(str(table['X'][i])))
    #                 self.tableWidget.setItem(i, 3, QTableWidgetItem(str(table['Y'][i])))
    #                 self.tableWidget.setItem(i, 11, QTableWidgetItem(str(Y_ch[i])))
    #             else:
    #                 self.tableWidget.setItem(i, 0, QTableWidgetItem(str(i)))
    #                 self.tableWidget.setItem(i, 1, QTableWidgetItem(str(table['H'][i])))
    #                 self.tableWidget.setItem(i, 2, QTableWidgetItem(str(table['X'][i])))
    #                 self.tableWidget.setItem(i, 3, QTableWidgetItem(str(table['Y'][i])))
    #                 self.tableWidget.setItem(i, 4, QTableWidgetItem(str(table['W'][i])))
    #                 self.tableWidget.setItem(i, 5, QTableWidgetItem(str(table['W-V'][i])))
    #                 self.tableWidget.setItem(i, 6, QTableWidgetItem(str(table['S'][i])))
    #                 self.tableWidget.setItem(i, 7, QTableWidgetItem(str(table['local'][i] + table['Y'][i])))
    #                 self.tableWidget.setItem(i, 8, QTableWidgetItem(str(table['W'][i])))
    #                 self.tableWidget.setItem(i, 9, QTableWidgetItem(str(table['deg_count'][i])))
    #                 self.tableWidget.setItem(i, 10, QTableWidgetItem(str(table['inc_count'][i])))
    #                 self.tableWidget.setItem(i, 11, QTableWidgetItem(str(Y_ch[i])))
    #                 self.tableWidget.setItem(i, 12, QTableWidgetItem(str(abs(Y_ch[i] - table['Y'][i]))))
    #                 header = self.tableWidget.horizontalHeader()
    #                 for i in range(0, 13, 1):
    #                     header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
    #         self.label_8.setText("Задача №9 тестовая, вариант №3, метод = РК* (4 порядка)")
    #         self.label_7.setText(
    #             "x0 = " + str(table['X'][0]) + ", y0 = " + str(table['Y'][0]) + ", T = " + str(info['x1']) + ", h0 = " + str(table['H'][0]) + ", ε = " + str(
    #                 info['eps']) + ", ε гр = " + str(info['eps_bord']))
    #         self.label_9.setText(
    #             "Nmax = " + str(info['n']) + ", ε min = " + str(info['eps'] / 32) + ", n = " + str(info['n'] - 1) + ", b-xn = " + str(
    #                 info['x1'] - table['X'][info['n'] - 1]))
    #         self.label_10.setText("min|S| = " + str(info['min err est']) + " при х = " + str(info['X on min err est']))
    #         self.label_20.setText("max|S| = " + str(info['max err est']) + " при х = " + str(info['X on max err est']))
    #         self.label_11.setText("ум. шага = " + str(info['deg']) + ", ув. шага = " + str(info['inc']))
    #         self.label_12.setText("max h = " + str(max(table['H'])) + " при х = " + str(
    #             table['X'][table['H'].index(max(table['H'])) + 1]))
    #         if table['H'].index(min(table['H'])) == (info['n'] - 1):
    #             self.label_21.setText("min h = " + str(min(table['H'])) + " при х = " + str(
    #                 table['X'][table['H'].index(min(table['H']))]))
    #         else:
    #             self.label_21.setText("min h = " + str(min(table['H'])) + " при х = " + str(
    #                 table['X'][table['H'].index(min(table['H'])) + 1]))
    #         self.label_13.setText(
    #             "max|ui-vi| = " + str(max(glob)) + " при х = " + str(table['X'][glob.index(max(glob))]))

    def ClearPlot(self): # функция очистки графика
        global ax
        ax.clear()
        plot = plt.xlabel(r'$x$')
        plot = plt.ylabel(r'$u$')
        plot = plt.title('График')
        plot = plt.grid(True)
        self.canvas.draw()
        self.tableWidget.setRowCount(0)
        # self.tabs.clear()

    def AddPlot(self): # функция добавления графика
        global ax
        Y_ch = []  # Значение y для тестовой задачи

        plot = plt.xlabel(r'$x$')
        plot = plt.ylabel(r'$u$')
        plot = plt.title('График')
        plot = plt.grid(True)

        # получение флагов увеличения/уменьшения
        if self.check_not_inc.isChecked():
            check_not_inc = 0
        else:
            check_not_inc = 1

        if self.check_not_deg.isChecked():
            check_not_deg = 0
        else:
            check_not_deg = 1

        # получение параметров диффура
        param_a = np.float64(self.param_a.text())  # a1
        param_b = np.float64(self.param_b.text())  # a2
        param_c = np.float64(self.param_c.text())  # m

        # получение начальных услови
        x0 = np.float64(self.start_value_x.text())
        y0 = np.float64(self.start_value_y.text())

        # получение начального шага
        h = np.float64(self.start_step.text())

        # получение точности выхода за границу
        eps_bord = np.float64(self.eps_border.text())

        # получение контроля локальной погрешности
        eps = np.float64(self.control_error.text())

        # получение макс. числа шагов
        n = np.int(self.max_step.text())

        # получение конечного значения отрезка Х
        x1 = np.float64(self.finish_value.text())

        table, info = rk.rk4_v2(self.f, x0, y0, x1, h, n, param_a, param_b, param_c, eps_bord, check_not_inc, check_not_deg, eps)

        for i in range(len(table['X'])):
            Y_ch.append(self.check(table['X'][i], x0, y0, param_a, param_b, param_c))

        glob = [0] * (len(table['Y']))

        for i in range(len(table['Y'])):
            glob[i] = abs(Y_ch[i] - table['Y'][i])

        if self.GetItem() == "Основная":
            ax.plot(table['X'], table['Y'], '*-', label='a1=' + str(param_a) + ', a2=' + str(param_b) + ', m=' + str(param_c) + ', x0=' + str(x0) + ', y0 = ' + str(y0) + ", осн.")
            ax.legend()
            # self.tabs.addItem("m_a=" + str(param_a) + "b=" + str(param_b) + "c=" + str(param_c) + "x0=" + str(x0) + "y0=" + str(y0) + "eps=" + str(eps) + "eps_bord=" + str(eps_bord) + "h=" + str(h) + "n=" + str(n))
            # self.save_obj(table, "mtable_m_a=" + str(param_a) + "b=" + str(param_b) + "c=" + str(param_c) + "x0=" + str(x0) + "y0=" + str(y0) + "eps=" + str(eps) + "eps_bord=" + str(eps_bord) + "h=" + str(h) + "n=" + str(n))
            # self.save_obj(info, "minfo_m_a=" + str(param_a) + "b=" + str(param_b) + "c=" + str(param_c) + "x0=" + str(x0) + "y0=" + str(y0) + "eps=" + str(eps) + "eps_bord=" + str(eps_bord) + "h=" + str(h) + "n=" + str(n))
            self.tableWidget.setRowCount(0)
            self.tableWidget.setRowCount(len(table['X']))
            self.tableWidget.verticalHeader().hide()
            if self.tableWidget.columnCount() == 13:
                self.tableWidget.removeColumn(12)
                self.tableWidget.removeColumn(11)
            for i in range(len(table['X'])):
                if i == 0:
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(str(i)))
                    self.tableWidget.setItem(i, 1, QTableWidgetItem(str(h)))
                    self.tableWidget.setItem(i, 2, QTableWidgetItem(str(table['X'][i])))
                    self.tableWidget.setItem(i, 3, QTableWidgetItem(str(table['Y'][i])))
                else:
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(str(i)))
                    self.tableWidget.setItem(i, 1, QTableWidgetItem(str(table['H'][i])))
                    self.tableWidget.setItem(i, 2, QTableWidgetItem(str(table['X'][i])))
                    self.tableWidget.setItem(i, 3, QTableWidgetItem(str(table['Y'][i])))
                    self.tableWidget.setItem(i, 4, QTableWidgetItem(str(table['W'][i])))
                    self.tableWidget.setItem(i, 5, QTableWidgetItem(str(table['W-V'][i])))
                    self.tableWidget.setItem(i, 6, QTableWidgetItem(str(table['S'][i])))
                    self.tableWidget.setItem(i, 7, QTableWidgetItem(str(table['local'][i] + table['Y'][i])))
                    self.tableWidget.setItem(i, 8, QTableWidgetItem(str(table['W'][i])))
                    self.tableWidget.setItem(i, 9, QTableWidgetItem(str(table['deg_count'][i])))
                    self.tableWidget.setItem(i, 10, QTableWidgetItem(str(table['inc_count'][i])))
                    header = self.tableWidget.horizontalHeader()
                    for i in range(0, 11, 1):
                        header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
            self.label_8.setText("Задача №9 основная, вариант №3, метод = РК* (4 порядка)")
            self.label_7.setText("x0 = " + str(x0) + ", u0 = " + str(y0) + ", T = " + str(x1) + ", h0 = " + str(h) + ", ε = " + str(eps) + ", ε гр = " + str(eps_bord))
            self.label_9.setText("Nmax = " + str(n) + ", ε min(ниж. грн. контроля погрешности) = " + str(eps/32) + ", n = " + str(info['n']-1) + ", b-xn = " + str(x1-table['X'][info['n']-1]))
            self.label_10.setText("max|S| = " + str(info['max err est']) + " при х = " + str(info['X on max err est']))
            self.label_20.setText("min|S| = " + str(info['min err est']) + " при х = " + str(info['X on min err est']))
            self.label_11.setText("ум. шага = " + str(info['deg']) + ", ув. шага = " + str(info['inc']))
            self.label_12.setText("max h = " + str(max(table['H'])) + " при х = " + str(table['X'][table['H'].index(max(table['H']))+1]))
            if table['H'].index(min(table['H'])) == (info['n']-1):
                self.label_21.setText("min h = " + str(min(table['H'])) + " при х = " + str(table['X'][table['H'].index(min(table['H']))]))
            else:
                self.label_21.setText("min h = " + str(min(table['H'])) + " при х = " + str(table['X'][table['H'].index(min(table['H']))+1]))
            self.label_13.setText("")
        else:
            self.ClearPlot
            xx = np.arange(x0, x1, 0.001)
            yy = [0]*(len(xx))
            for i in range(len(xx)):
                yy[i] = rk.check(xx[i], x0, y0, param_a, param_b, param_c)
            ax.plot(xx, yy, '--', label='a1=' + str(param_a) + ', a2=' + str(param_b) + ', m=' + str(param_c) + ', x0=' + str(x0) + ', y0 = ' + str(y0) + ", тест.")
            ax.plot(table['X'], table['Y'], '*-', label='a1=' + str(param_a) + ', a2=' + str(param_b) + ', m=' + str(param_c) + ', x0=' + str(x0) + ', y0 = ' + str(y0) + ", осн.")
            ax.legend()
            # self.tabs.addItem(
            #     "t_a=" + str(param_a) + "b=" + str(param_b) + "c=" + str(param_c) + "x0=" + str(x0) + "y0=" + str(y0) + "eps=" + str(
            #         eps) + "eps_bord=" + str(eps_bord) + "h=" + str(h) + "n=" + str(n))
            # self.save_obj(table, "ttable_t_a=" + str(param_a) + "b=" + str(param_b) + "c=" + str(param_c) + "x0=" + str(x0) + "y0=" + str(
            #     y0) + "eps=" + str(eps) + "eps_bord=" + str(eps_bord) + "h=" + str(h) + "n=" + str(n))
            # self.save_obj(info, "tinfo_t_a=" + str(param_a) + "b=" + str(param_b) + "c=" + str(param_c) + "x0=" + str(x0) + "y0=" + str(
            #     y0) + "eps=" + str(eps) + "eps_bord=" + str(eps_bord) + "h=" + str(h) + "n=" + str(n))
            self.tableWidget.setRowCount(0)
            self.tableWidget.setRowCount(len(table['X']))
            self.tableWidget.verticalHeader().hide()
            if self.tableWidget.columnCount() == 11:
                self.tableWidget.insertColumn(11)
                self.tableWidget.insertColumn(12)
            self.tableWidget.setHorizontalHeaderItem(11, QTableWidgetItem("V(i)"))
            self.tableWidget.setHorizontalHeaderItem(12, QTableWidgetItem("V(i) - u(i)"))
            for i in range(len(table['X'])):
                if i == 0:
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(str(i)))
                    self.tableWidget.setItem(i, 1, QTableWidgetItem(str(h)))
                    self.tableWidget.setItem(i, 2, QTableWidgetItem(str(table['X'][i])))
                    self.tableWidget.setItem(i, 3, QTableWidgetItem(str(table['Y'][i])))
                    self.tableWidget.setItem(i, 11, QTableWidgetItem(str(Y_ch[i])))
                else:
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(str(i+1)))
                    self.tableWidget.setItem(i, 1, QTableWidgetItem(str(table['H'][i])))
                    self.tableWidget.setItem(i, 2, QTableWidgetItem(str(table['X'][i])))
                    self.tableWidget.setItem(i, 3, QTableWidgetItem(str(table['Y'][i])))
                    self.tableWidget.setItem(i, 4, QTableWidgetItem(str(table['W'][i])))
                    self.tableWidget.setItem(i, 5, QTableWidgetItem(str(table['W-V'][i])))
                    self.tableWidget.setItem(i, 6, QTableWidgetItem(str(table['S'][i])))
                    self.tableWidget.setItem(i, 7, QTableWidgetItem(str(table['local'][i] + table['Y'][i])))
                    self.tableWidget.setItem(i, 8, QTableWidgetItem(str(table['W'][i])))
                    self.tableWidget.setItem(i, 9, QTableWidgetItem(str(table['deg_count'][i])))
                    self.tableWidget.setItem(i, 10, QTableWidgetItem(str(table['inc_count'][i])))
                    self.tableWidget.setItem(i, 11, QTableWidgetItem(str(Y_ch[i])))
                    self.tableWidget.setItem(i, 12, QTableWidgetItem(str(abs(Y_ch[i] - table['Y'][i]))))
                    header = self.tableWidget.horizontalHeader()
                    for i in range(0, 13, 1):
                        header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
            self.label_8.setText("Задача №9 тестовая, вариант №3, метод = РК* (4 порядка)")
            self.label_7.setText(
                "x0 = " + str(x0) + ", y0 = " + str(y0) + ", T = " + str(x1) + ", h0 = " + str(h) + ", ε = " + str(
                    eps) + ", ε гр = " + str(eps_bord))
            self.label_9.setText(
                "Nmax = " + str(n) + ", ε min(ниж. грн. контроля погрешности) = " + str(eps / 32) + ", n = " + str(info['n'] - 1) + ", b-xn = " + str(
                    x1 - table['X'][info['n'] - 1]))
            self.label_10.setText("max|S| = " + str(info['max err est']) + " при х = " + str(info['X on max err est']))
            self.label_20.setText("min|S| = " + str(info['min err est']) + " при х = " + str(info['X on min err est']))
            self.label_11.setText("ум. шага = " + str(info['deg']) + ", ув. шага = " + str(info['inc']))
            self.label_12.setText("max h = " + str(max(table['H'])) + " при х = " + str(
                table['X'][table['H'].index(max(table['H'])) + 1]))
            if table['H'].index(min(table['H'])) == (info['n'] - 1):
                self.label_21.setText("min h = " + str(min(table['H'])) + " при х = " + str(
                    table['X'][table['H'].index(min(table['H']))]))
            else:
                self.label_21.setText("min h = " + str(min(table['H'])) + " при х = " + str(
                    table['X'][table['H'].index(min(table['H'])) + 1]))
            self.label_13.setText("max|ui-vi| = " + str(max(glob)) + " при х = " + str(table['X'][glob.index(max(glob))]))
        self.canvas.draw()

    def GetItem(self): # функция получения информации из ComboBox
        item = self.comboBox.currentText()
        return item

    # def GetTab(self): # функция получения информации из tabs
    #     item = self.tabs.currentText()
    #     return item

    def f(self, x, y, param_a, param_b, param_c):  # Правая часть диффура
        return -(param_a * y + y * y * param_b)/param_c

    def check(self, x, x0, y0, param_a, param_b, param_c):  # Точное решение
        c = math.log(math.exp(param_a * x0 / param_c) * y0 / (y0 * param_b + param_a)) / param_a
        res = -param_a * math.exp(param_a * c)/(param_b * math.exp(param_a * c) - math.exp(param_a * x / param_c))
        return res

    # def save_obj(self, obj, name):
    #     with open('obj/' + name + '.pkl', 'wb') as f:
    #         pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    #
    # def load_obj(self, name):
    #     with open('obj/' + name + '.pkl', 'rb') as f:
    #         return pickle.load(f)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = MainWindow()
    main.show()

    sys.exit(app.exec_())