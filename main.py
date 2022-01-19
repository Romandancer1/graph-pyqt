from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QListWidget, QMessageBox, QColorDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap

import sys
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class GraphWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1280, 1080)
        self.move(250, 0)
        self.title = 'Graph-mfo'
        # Колонки исходного датафрейма для пандаса
        self.nodes_list_first_column = ""
        self.nodes_list_second_column = ""
        self.edges_in_list_column = ""
        self.edges_out_list_column = ""
        self.special_list_column = ""
        # по умолчанию ставим на списание
        self.nodes_first_clicked = ""
        # self.transaction_type = "Списание"
        self.sum_limit = ""
        # self.mfo_count = 0
        # Цвета узлов по умолчанию
        self.nodes_first_color = "#7582fb"
        self.nodes_second_color = "#00BFFF"
        self.special_nodes_color = "#080cff"
        # Тип связи по умолчанию
        self.edge_type = 'Все'

        # Датафрейм
        self.df = pd.DataFrame()
        # Все ребра
        self.all_edges_df = pd.DataFrame()
        # Разделитель по умолчанию.
        self.sep = ","
        # Контейнер обертка для блоков
        self._main = QtWidgets.QWidget(self)
        self.horizontal_container = QtWidgets.QHBoxLayout(self._main)

        # Делим окно на два - левая и правая часть
        self.vertical_container_left = QtWidgets.QVBoxLayout(self)
        self.vertical_container_right = QtWidgets.QVBoxLayout(self)
        self.horizontal_container.addLayout(self.vertical_container_left)
        self.horizontal_container.addLayout(self.vertical_container_right)

        # Контейнер для списков выбора полей из датафрейма
        self.horizontal_container_lists = QtWidgets.QHBoxLayout(self)

        # Контейнер для выбора поля 1 узла
        self.vertical_container_nodes_first = QtWidgets.QVBoxLayout(self)
        # Лейбл для листа с узлами 1
        self.nodes_list_first_label = QtWidgets.QLabel(self)
        self.nodes_list_first_label.setFixedSize(100, 40)
        # Лист для выбора поля для узла 1
        self.nodes_list_first_widget = QtWidgets.QListWidget(self)
        self.nodes_list_first_widget.setFixedSize(100, 150)
        self.vertical_container_nodes_first.addWidget(self.nodes_list_first_label)
        self.vertical_container_nodes_first.addWidget(self.nodes_list_first_widget)

        # Контейнер для выбора поля 2 узла
        self.vertical_container_nodes_second = QtWidgets.QVBoxLayout(self)
        # Лейбл для листа с узлами 2
        self.nodes_list_second_label = QtWidgets.QLabel(self)
        self.nodes_list_second_label.setFixedSize(100, 40)
        # Лист для выбора поля с узлами 2
        self.nodes_list_second_widget = QListWidget(self)
        self.nodes_list_second_widget.setFixedSize(100, 150)

        self.vertical_container_nodes_second.addWidget(self.nodes_list_second_label)
        self.vertical_container_nodes_second.addWidget(self.nodes_list_second_widget)

        # Контейнер для выбора поля входящих ребер
        self.vertical_container_edges_in = QtWidgets.QVBoxLayout(self)
        # Лейбл для листа с ребрами
        self.edges_in_list_label = QtWidgets.QLabel(self)
        self.edges_in_list_label.setFixedSize(100, 35)

        # Лист для выбора поля с ребрами
        self.edges_in_list_widget = QListWidget(self)
        self.edges_in_list_widget.setFixedSize(100, 150)

        self.vertical_container_edges_in.addWidget(self.edges_in_list_label)
        self.vertical_container_edges_in.addWidget(self.edges_in_list_widget)

        # Контейнер для выбора поля исходящих ребер
        self.vertical_container_edges_out = QtWidgets.QVBoxLayout(self)
        # Лейбл для листа с ребрами
        self.edges_out_list_label = QtWidgets.QLabel(self)
        self.edges_out_list_label.setFixedSize(100, 35)

        # Лист для выбора поля с ребрами
        self.edges_out_list_widget = QListWidget(self)
        self.edges_out_list_widget.setFixedSize(100, 150)

        self.vertical_container_edges_out.addWidget(self.edges_out_list_label)
        self.vertical_container_edges_out.addWidget(self.edges_out_list_widget)

        # Контейнер для выбора спец признак
        self.vertical_container_special_features = QtWidgets.QVBoxLayout(self)
        # Лейбл для листа со сцец празнаками
        self.special_features_list_label = QtWidgets.QLabel(self)
        self.special_features_list_label.setFixedSize(100, 35)

        # Лист для выбора поля с ребрами
        self.special_features_list_widget = QListWidget(self)
        self.special_features_list_widget.setFixedSize(100, 150)

        self.vertical_container_special_features.addWidget(self.special_features_list_label)
        self.vertical_container_special_features.addWidget(self.special_features_list_widget)

        # Добавляем контейнеры для списков
        self.horizontal_container_lists.addLayout(self.vertical_container_nodes_first)
        self.horizontal_container_lists.addLayout(self.vertical_container_nodes_second)
        self.horizontal_container_lists.addLayout(self.vertical_container_edges_in)
        self.horizontal_container_lists.addLayout(self.vertical_container_edges_out)
        self.horizontal_container_lists.addLayout(self.vertical_container_special_features)
        # self.horizontal_container_lists.addStretch()

        self.horizontal_container_df_options = QtWidgets.QHBoxLayout(self)

        # Контейнер для выбора разделителя
        self.horizontal_container_separator = QtWidgets.QHBoxLayout(self)
        self.separator_label = QtWidgets.QLabel(self)
        self.separator_label.setFixedSize(120, 35)
        self.separator_text = QtWidgets.QLineEdit(self)
        self.separator_text.setFixedSize(30, 20)
        self.horizontal_container_separator.addWidget(self.separator_label)
        self.horizontal_container_separator.addWidget(self.separator_text)

        # Выбор цвета для узла 1
        self.horizontal_container_color_nodes_first = QtWidgets.QHBoxLayout(self)
        self.color_picker_nodes_first_label = QtWidgets.QLabel(self)
        self.color_picker_nodes_first_label.setFixedSize(65, 35)
        self.color_picker_nodes_first = QtWidgets.QPushButton(self.nodes_first_color, self)
        self.color_picker_nodes_first.setFixedSize(100, 30)

        self.horizontal_container_color_nodes_first.addWidget(self.color_picker_nodes_first_label)
        self.horizontal_container_color_nodes_first.addWidget(self.color_picker_nodes_first)

        # Выбор цвета для узла 2
        self.horizontal_container_color_nodes_second = QtWidgets.QHBoxLayout(self)
        self.color_picker_nodes_second_label = QtWidgets.QLabel(self)
        self.color_picker_nodes_second_label.setFixedSize(65, 35)
        self.color_picker_nodes_second = QtWidgets.QPushButton(self.nodes_second_color, self)
        self.color_picker_nodes_second.setFixedSize(100, 30)

        self.horizontal_container_color_nodes_second.addWidget(self.color_picker_nodes_second_label)
        self.horizontal_container_color_nodes_second.addWidget(self.color_picker_nodes_second)

        self.horizontal_container_df_options.addLayout(self.horizontal_container_separator)
        self.horizontal_container_df_options.addLayout(self.horizontal_container_color_nodes_first)
        self.horizontal_container_df_options.addLayout(self.horizontal_container_color_nodes_second)

        # Добавляем в контейнер сепаратора
        self.vertical_container_left.addLayout(self.horizontal_container_df_options)

        # Кнопка загрузки файла
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        # self.pushButton.setFixedSize(150, 50)
        self.pushButton.move(150, 10)
        self.vertical_container_left.addWidget(self.pushButton)

        # Кнопка для построения графа
        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setObjectName("pushButton_3")

        self.vertical_container_left.addLayout(self.horizontal_container_lists)
        self.vertical_container_left.addWidget(self.pushButton_3)

        # Контейнер для выбора узла
        self.horizontal_container_lists_second = QtWidgets.QHBoxLayout(self)

        # Контейнер для выбора узла для отсмотра
        self.vertical_container_get_node = QtWidgets.QVBoxLayout(self)
        # Контейнер для выбора типа узлов
        self.vertical_container_edge_type = QtWidgets.QVBoxLayout(self)
        # Контейнер для ввода суммы
        self.vertical_container_sum_input = QtWidgets.QVBoxLayout(self)
        # Контейнер для индикации найденных узлов
        self.vertical_container_edges_found = QtWidgets.QVBoxLayout(self)

        # Добавляем контейнер для разделителя
        self.horizontal_container_separator.addWidget(self.separator_label)
        self.horizontal_container_separator.addWidget(self.separator_text)

        # Третий ряд контейнеров
        self.horizontal_container_lists_second.addLayout(self.vertical_container_get_node)
        self.horizontal_container_lists_second.addLayout(self.vertical_container_edge_type)
        self.horizontal_container_lists_second.addLayout(self.vertical_container_sum_input)
        self.horizontal_container_lists_second.addLayout(self.vertical_container_edges_found)

        # Лист для выбора узла
        self.get_node_list_widget = QListWidget(self)
        self.get_node_list_widget.setFixedSize(150, 150)
        # Лейбл для листа с сотрудниками
        self.get_node_list_label = QtWidgets.QLabel(self)
        self.get_node_list_label.setFixedSize(190, 50)
        self.vertical_container_get_node.addWidget(self.get_node_list_label)
        self.vertical_container_get_node.addWidget(self.get_node_list_widget)

        # Лейбл для выбора типа ребра
        self.edge_type_label = QtWidgets.QLabel(self)
        self.edge_type_label.setFixedSize(150, 50)
        # Лист для выбора типа ребра
        self.edge_type_list = QtWidgets.QListWidget(self)
        self.edge_type_list.setFixedSize(150, 150)
        self.vertical_container_edge_type.addWidget(self.edge_type_label)
        self.vertical_container_edge_type.addWidget(self.edge_type_list)

        # Фильтр по количеству узлов
        self.sum_limit_value_label = QtWidgets.QLabel(self)
        self.sum_limit_value_label.setFixedSize(100, 50)
        self.sum_limit_value = QtWidgets.QLineEdit(self)
        self.sum_limit_value.setFixedSize(100, 20)
        self.sum_limit_value.setText("0")
        sum_validator = QtGui.QIntValidator()
        sum_validator.setRange(0, 1000000)
        self.sum_limit_value.setValidator(sum_validator)
        self.vertical_container_sum_input.addWidget(self.sum_limit_value_label)
        self.vertical_container_sum_input.addWidget(self.sum_limit_value)

        # Количество уникальных связей
        self.uniq_edges_found_label = QtWidgets.QLabel(self)
        self.uniq_edges_found_label.setFixedSize(100, 50)
        self.uniq_edges_found_text = QtWidgets.QLineEdit(self)
        self.uniq_edges_found_text.setFixedSize(100, 20)
        self.uniq_edges_found_text.setReadOnly(True)
        self.vertical_container_sum_input.addWidget(self.uniq_edges_found_label)
        self.vertical_container_sum_input.addWidget(self.uniq_edges_found_text)
        # self.vertical_container_sum_input.addStretch()

        # Сумма связей
        self.edges_sum_label = QtWidgets.QLabel(self)
        self.edges_sum_label.setFixedSize(100, 50)
        self.edges_sum_text = QtWidgets.QLineEdit(self)
        self.edges_sum_text.setFixedSize(100, 20)
        self.edges_sum_text.setReadOnly(True)
        self.vertical_container_edges_found.addWidget(self.edges_sum_label)
        self.vertical_container_edges_found.addWidget(self.edges_sum_text)
        # self.vertical_container_edges_found.addStretch()

        # ДОБАВЛЯЕМ ВСЕ В КОНТЕЙНЕР_2
        self.vertical_container_left.addLayout(self.horizontal_container_lists_second)

        # Кнопка для построения графа
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setObjectName("pushButton_2")

        self.vertical_container_left.addWidget(self.pushButton_2)
        self.vertical_container_left.addStretch()

        # Инициируем основной виджет
        self._main.setFocus()
        self.setCentralWidget(self._main)
        # Добавляем блок для отрисовки графа
        self.fig = plt.figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.fig)
        self.canvas.draw()
        self.vertical_container_right.addWidget(self.canvas)

        self.retranslateUi()

    def retranslateUi(self):
        """
        Функция навешивает обработчики на кнопки и списки
        Function sets texts and clicks on lists and buttons
        :return:
        """
        _translate = QtCore.QCoreApplication.translate
        self.nodes_list_first_label.setText(_translate("MainWindow", "Выберите поле,\nсодержащее \n узлы(1)"))
        self.nodes_list_second_label.setText(
            _translate("MainWindow", "Выберите поле,\nсодержащее \n узлы(2)"))
        self.edges_in_list_label.setText(
            _translate("MainWindow", "Выберите поле, \n для ребра 1"))
        self.edges_out_list_label.setText(
            _translate("MainWindow", "Выберите поле, \n для ребра 2"))
        self.special_features_list_label.setText(_translate("MainWindow", "Выберите столбец \n с спец признаками \n ("
                                                                          "необязательно)"))

        self.separator_label.setText(_translate("MainWindow", "Разделитель текста \n (по умолчанию ,)"))

        self.pushButton.setText(_translate("MainWindow", "Загрузить \n файл"))
        self.pushButton_2.setText(_translate("MainWindow", "Построить \n граф по узлу"))
        self.pushButton_3.setText(_translate("MainWindows", "Построить общий граф"))
        self.get_node_list_label.setText(
            _translate("MainWindow",
                       "Выберите узел, по которому \n нужно построить граф "
                       "\n (можно выбрать после выбора \n поля с узлами)"))
        self.edge_type_label.setText(
            _translate("MainWindow",
                       "Выберите тип \n связи"))
        self.uniq_edges_found_label.setText(
            _translate("MainWindow", "Количество \n уникальных \n связей"))
        self.sum_limit_value_label.setText(
            _translate("MainWindow", "Введите сумму \n нижней границы \n связей"))
        self.edges_sum_label.setText(
            _translate("MainWindow", "Cумма по связям"))

        self.edge_type_list.addItems(['Все', 'Исходящие', 'Входящие'])
        self.color_picker_nodes_first_label.setText(_translate("MainWindow", "Цвет узла 1"))
        self.color_picker_nodes_second_label.setText(_translate("MainWindow", "Цвет узла 2"))
        self.pushButton.clicked.connect(self.pushButton_handler)
        self.pushButton_2.clicked.connect(self.draw_single_graph)
        self.pushButton_3.clicked.connect(self.draw_summary_graph)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.color_picker_nodes_first.clicked.connect(self.open_color_dialog_first)
        self.color_picker_nodes_second.clicked.connect(self.open_color_dialog_second)

        # self.pushButton_3.clicked.connect(self.draw_summary_graph)
        # self.transaction_status_list.addItems(['Списание', 'Зачисление'])

        # self.transaction_status_list.itemClicked.connect(self.get_transaction_status)
        self.nodes_list_first_widget.itemClicked.connect(self.get_uniq_first_node)
        self.nodes_list_second_widget.itemClicked.connect(self.get_second_node_column)
        self.edges_in_list_widget.itemClicked.connect(self.get_edge_in_column)
        self.edges_out_list_widget.itemClicked.connect(self.get_edge_out_column)
        self.special_features_list_widget.itemClicked.connect(self.get_special_node_column)
        self.get_node_list_widget.itemClicked.connect(self.get_special_node)
        self.edge_type_list.itemClicked.connect(self.set_edge_type)
        self.setWindowTitle(_translate("Graph-program", "Graph-program"))

    def open_color_dialog_first(self):
        """
        Function shows open-color dialog and sets value for first nodes
        :return:
        """
        color = QColorDialog.getColor()
        self.nodes_first_color = color.name()
        self.color_picker_nodes_first.setText(self.nodes_first_color)

    def open_color_dialog_second(self):
        """
        Function shows open-color dialog and sets value for second nodes
        :return:
        """
        color = QColorDialog.getColor()
        self.nodes_second_color = color.name()
        self.color_picker_nodes_second.setText(self.nodes_second_color)

    def pushButton_handler(self):
        """
        Функция активирует загрузку файлаиз из трея
        Method activates file upload from PC
        :return:
        """
        self.load_data_box()

    def get_uniq_first_node(self, item):
        """
        Функция берет уникальные значения из выбранного столбца с первыми узлами и записывает в новый список
        Function gets uniq values from column name with nodes and writes it to new list (QLISTWIDGET)
        :param item: column name from qlistwidget
        :return:
        """
        self.get_node_list_widget.clear()
        try:
            self.get_node_list_widget.addItems(self.df[item.text()].unique().tolist())
            self.nodes_list_first_column = item.text()
        except TypeError as ex:
            # Если в выбранном столбце дерьмовые данные, бросаем exception
            msg = QMessageBox()
            msg.setText("Неверный тип данных в столбце, необходима строка или число. Выберите другой столбец")
            msg.exec_()

    def get_second_node_column(self, item):
        """
        Set second node column from df
        :param item: chosen item from qlistwidget
        :return:
        """
        self.nodes_list_second_column = item.text()

    def get_edge_in_column(self, item):
        """
        Set edge column from df
        :param item: chosen item from qlistwidget
        :return:
        """
        # self.df = self.df.dropna(subset=[item.text()])
        self.edges_in_list_column = item.text()

    def get_edge_out_column(self, item):
        """
        Set edge column from df
        :param item: chosen item from qlistwidget
        :return:
        """
        # self.df = self.df.dropna(subset=[item.text()])
        self.edges_out_list_column = item.text()
        self.pushButton_3.setEnabled(True)

    def get_special_node_column(self, item):
        """
        Get special node to visualize
        :param item: clicked item from qlistwidget
        :return:
        """
        self.special_list_column = item.text()


    def get_special_node(self, item):
        """
        Get special node to create single graph for it
        :param item: QLISTWIDGET CLICKED ITEM
        :return:
        """
        self.nodes_first_clicked = item.text()
        self.pushButton_2.setEnabled(True)

    def set_edge_type(self, item):
        """
        Set which type of edges should be visualized
        :param item: Clicked item from QLISTWIDGET
        :return:
        """
        self.edge_type = item.text()

    def load_data_box(self):
        """
       Загрузка транзакций через модальное окно и создание датафрейма по столбцам
       If there is no file - throw Exceptions, and pass
       :return:
       """
        is_dataframe_loaded = False
        filename = QFileDialog.getOpenFileName()
        try:
            file = DataFile(filename[0], sep=self.sep)
            dataframe_columns = file.pandas_df.columns.tolist()
            is_dataframe_loaded = True
        # В любом случае бросаем exception, если не выбран файл
        except UnboundLocalError as ex:
            msg = QMessageBox()
            msg.setText("Вы не выбрали файл с данными, " + str(ex))
            msg.exec_()
        except TypeError as ex:
            msg = QMessageBox()
            msg.setText("Вы не выбрали файл с данными, " + str(ex))
            msg.exec_()

        # Если флаг сработал инициируем колонки и датафрейм
        if is_dataframe_loaded:
            self.nodes_list_second_widget.clear()
            self.nodes_list_second_widget.clear()
            self.edges_in_list_widget.clear()
            self.edges_out_list_widget.clear()
            self.special_features_list_widget.clear()
            self.nodes_list_first_widget.addItems(dataframe_columns)
            self.nodes_list_second_widget.addItems(dataframe_columns)
            self.edges_in_list_widget.addItems(dataframe_columns)
            self.edges_out_list_widget.addItems(dataframe_columns)
            self.special_features_list_widget.addItems(dataframe_columns)
            self.df = file.pandas_df

    def prepare_graph_df(self, data_frame):
        """
        # Формируем датафрейм с необходимыми стобцами и дф, в которых ребра и связи не пустые
        Параметр filtered nodes идет из узлов, если есть ограничение по количеству связей, убираем из дфа ненужные нам.
        """
        graph_df_full = data_frame.loc[
            (data_frame[self.nodes_list_first_column].notnull()) &
            (data_frame[self.nodes_list_second_column].notnull())]

        if self.edge_type == 'Исходящие':
            graph_df_full[self.edges_out_list_column] = None
        elif self.edge_type == 'Входящие':
            graph_df_full[self.edges_in_list_column] = None

        try:
            # Берем те, у кого есть все связи
            graph_df_all_edges = graph_df_full.loc[(graph_df_full[self.edges_in_list_column].notnull()) &
                                                   (graph_df_full[self.edges_out_list_column].notnull())]

            # Только входящая связь
            graph_df_in = graph_df_full.loc[(graph_df_full[self.edges_in_list_column].notnull()) &
                                            (graph_df_full[self.edges_out_list_column].isnull())]

            # Только выходящая связь
            graph_df_out = graph_df_full.loc[(graph_df_full[self.edges_in_list_column].isnull()) &
                                             (graph_df_full[self.edges_out_list_column].notnull())]

            del graph_df_full
            return graph_df_all_edges, graph_df_in, graph_df_out
        except Exception as ex:
            # Если в выбранном столбце дерьмовые данные, бросаем exception
            msg = QMessageBox()
            msg.setText("Вы не выбрали один из столбцов, " + str(ex))
            msg.exec_()

    def get_all_nodes(self, graph_df_full, graph_df_in, graph_df_out, filtered_nodes):
        """
        Method takes 3 df with nodes and returns arrays with values and colors for it
        :param filtered_nodes: Filtered nodes
        :param graph_df_full: graph, that has both in and out operations
        :param graph_df_in: graph, that has only in operations
        :param graph_df_out: graph, that has only out operations
        :return: Array
        """
        nodes_array = []
        nodes_color = []
        summary_df = pd.concat([graph_df_in, graph_df_out])
        summary_df = pd.concat([summary_df, graph_df_full])
        first_nodes_df = pd.DataFrame(columns=['NODES', 'COLOR'])
        second_nodes_df = pd.DataFrame(columns=['NODES', 'COLOR'])
        first_nodes_df['NODES'] = summary_df[self.nodes_list_first_column]
        first_nodes_df = first_nodes_df.assign(COLOR=self.nodes_first_color)
        first_nodes_df = first_nodes_df.drop_duplicates(subset=['NODES'])
        # Если выбрали колонку
        # где есть спецпризнак у первого спецзла, присваиваем новые цвета у него.
        if len(self.special_list_column) > 0:
            first_nodes_df = self.set_special_color(first_nodes_df)
        second_nodes_df['NODES'] = summary_df[self.nodes_list_second_column]
        second_nodes_df = second_nodes_df.assign(COLOR=self.nodes_second_color)
        second_nodes_df = second_nodes_df.drop_duplicates(subset=['NODES'])
        summary_nodes = pd.concat([first_nodes_df, second_nodes_df])
        summary_nodes = summary_nodes.drop_duplicates(subset=['NODES'])
        if len(filtered_nodes) != 0:
            summary_nodes = summary_nodes.loc[summary_nodes['NODES'].isin(filtered_nodes)]
        # Добавляем узлы
        nodes_array.extend(summary_nodes['NODES'].tolist())
        nodes_color.extend(summary_nodes['COLOR'].tolist())
        return nodes_array, nodes_color

    def get_all_edges(self, graph_df_full, graph_df_in, graph_df_out):
        """
        Function counts edges and weights for graph
        :return: prepared edges array
        """
        edges_in = pd.DataFrame()
        edges_out = pd.DataFrame()
        edges_full = pd.DataFrame()
        if graph_df_in.size > 0:
            edges_in = graph_df_in[
                [self.nodes_list_first_column, self.nodes_list_second_column, self.edges_in_list_column]]
            edges_in.columns = ['OUT', 'IN', 'VALUE']
        if graph_df_out.size > 0:
            edges_out = graph_df_out[
                [self.nodes_list_second_column, self.nodes_list_first_column, self.edges_out_list_column]]
            edges_out.columns = ['OUT', 'IN', 'VALUE']
        if graph_df_full.size > 0:
            edges_full_first = graph_df_full[[self.nodes_list_first_column,
                                              self.nodes_list_second_column, self.edges_in_list_column]]
            edges_full_second = graph_df_full[[self.nodes_list_second_column,
                                               self.nodes_list_first_column, self.edges_out_list_column]]
            edges_full_first.columns = ['OUT', 'IN', 'VALUE']
            edges_full_second.columns = ['OUT', 'IN', 'VALUE']
            edges_full = pd.concat([edges_full_first, edges_full_second])
            del edges_full_first, edges_full_second

        edges_full = pd.concat([edges_full, edges_in])
        edges_full = pd.concat([edges_full, edges_out])

        # Удаляем лишние дфы
        del edges_out, edges_in

        # Убираем дубликаты и считаем веса / суммы / количество
        edges_full = edges_full.groupby(by=['OUT', 'IN']).agg(VALUE=('VALUE', 'sum'), MAX_COUNT=('VALUE', 'count'))
        edges_full = edges_full.reset_index()
        # Фильтруем по количеству связей
        edges_full = edges_full.loc[edges_full['MAX_COUNT'] > int(self.sum_limit_value.text())]
        # Выбираем отфильтрованные узлы
        filtered_nodes = (edges_full['OUT'].append(edges_full['IN'])).unique()
        # Cчитаем веса
        edges_full['WEIGHT'] = edges_full['VALUE'].apply(lambda x: (x / edges_full['VALUE'].sum()) *
                                                                   self.count_weight_coeff(len(edges_full['OUT'])))
        # Количество уникальных связей
        self.uniq_edges_found_text.setText(str(len(edges_full['OUT'])))
        self.edges_sum_text.setText(str(edges_full['VALUE'].sum()))
        return edges_full[['OUT', 'IN', 'WEIGHT']].to_numpy(), filtered_nodes

    def count_weight_coeff(self, nodes_list_length):
        """
        Count weights according to count, to get good visualization
        :return:
        """
        if nodes_list_length > 0 &  nodes_list_length <= 50:
            return 10
        elif nodes_list_length > 50 & nodes_list_length <= 500:
            return 100
        elif nodes_list_length > 500:
            return 1000

    def set_special_color(self, first_nodes_df):
        """
        Set special color for nodes, that is has not nullable column
        :return:
        """
        # Выбираем из дфа те, у кого есть признакми
        special_color_nodes = self.df.loc[(self.df[self.nodes_list_first_column].notnull())
                                          & (self.df[self.special_list_column].notnull())]
        # Выкрашиваем их в отдельный цвет и возвращаем дф
        first_nodes_df.at[first_nodes_df['NODES'].
                          isin(special_color_nodes[self.nodes_list_first_column].unique().tolist()),
                          'COLOR'] = self.special_nodes_color
        return first_nodes_df

    def draw_summary_graph(self):
        self.fig = plt.cla()
        graph = nx.DiGraph()
        # Готовим данные для графа (узлы)
        graph_df_full, graph_df_in, graph_df_out = self.prepare_graph_df(self.df)
        edges, filtered_nodes = self.get_all_edges(graph_df_full, graph_df_in, graph_df_out)
        for edge in edges:
            graph.add_edge(edge[0], edge[1], colour=20, weight=edge[2])

        edges = graph.edges()
        weights = [graph[u][v]['weight'] for u, v in edges]

        # Получаем ребра
        # Получаем узлы и цвета для них
        nodes_list, nodes_color = self.get_all_nodes(graph_df_full, graph_df_in, graph_df_out, filtered_nodes)

        # Добавляем узлы
        graph.add_nodes_from(nodes_list)
        # Добавляем ребра и веса
        nx.draw(graph, node_color=nodes_color, width=weights)
        self.fig = plt.figure(1, figsize=(3, 3))
        self.canvas.draw()

    def draw_single_graph(self):
        self.fig = plt.cla()
        graph = nx.DiGraph()
        special_nodes_df = self.df.loc[self.df[self.nodes_list_first_column] == self.nodes_first_clicked]
        graph_df_full, graph_df_in, graph_df_out = self.prepare_graph_df(special_nodes_df)
        edges, filtered_nodes = self.get_all_edges(graph_df_full, graph_df_in, graph_df_out)
        for edge in edges:
            graph.add_edge(edge[0], edge[1], colour=20, weight=edge[2])

        edges = graph.edges()
        weights = [graph[u][v]['weight'] for u, v in edges]

        nodes_list, nodes_color = self.get_all_nodes(graph_df_full, graph_df_in, graph_df_out, filtered_nodes)

        graph.add_nodes_from(nodes_list)

        nx.draw(graph, node_color=nodes_color, width=weights, with_labels=True)
        self.fig = plt.figure(1, figsize=(3, 3))
        self.canvas.draw()


class DataFile:
    def __init__(self,
                 pandas_df: (pd.DataFrame, str),
                 sep,
                 nrows=None,
                 encoding=None
                 ):

        self.pandas_df = pandas_df

        if self.pandas_df is not None:
            if type(pandas_df) == str:
                if pandas_df.split('.')[-1] == 'csv':
                    self.pandas_df = pd.read_csv(pandas_df, sep=sep, encoding=encoding, nrows=nrows)
                elif pandas_df.split('.')[-1] in ['xlsx', 'xls']:
                    self.pandas_df = pd.read_excel(pandas_df, nrows=nrows)
                elif pandas_df.split('.')[-1] == 'txt':
                    self.pandas_df = pd.read_table(pandas_df, sep=sep, encoding=encoding, nrows=nrows)
                else:
                    raise TypeError(f'Only "csv", "xls(x)" and "txt" file formats are supported, '
                                    f'but given file path ends with "{pandas_df.split(".")[-1]}"')
        else:
            raise TypeError(f'pd.DataFrame or str types are expected, but got: {type(pandas_df)}')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = GraphWindow()
    window.show()
    app.exec_()
