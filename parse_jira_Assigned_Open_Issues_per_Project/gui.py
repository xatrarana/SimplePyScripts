#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import calendar
import datetime as DT
import math
from pathlib import Path
from typing import List
import sys

from PyQt5.QtWidgets import (
    QApplication, QMessageBox, QMainWindow, QSystemTrayIcon, QTabWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QSplitter, QLabel, QGridLayout,
    QHeaderView
)
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtCore import QEvent, QTimer, Qt
from PyQt5.QtChart import QChart, QLineSeries, QDateTimeAxis, QValueAxis

from common import get_table
from get_assigned_open_issues_per_project import get_assigned_open_issues_per_project
from db import Run

sys.path.append('../qt__pyqt__pyside__pyqode')
from chart_line__show_tooltip_on_series__QtChart import ChartViewToolTips


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, 'Error', text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


CURRENT_DIR = Path(__file__).resolve().parent
WINDOW_TITLE = CURRENT_DIR.name


def get_table_widget(header_labels: list) -> QTableWidget:
    table = QTableWidget()
    table.setAlternatingRowColors(True)
    table.setEditTriggers(QTableWidget.NoEditTriggers)
    table.setSelectionBehavior(QTableWidget.SelectRows)
    table.setSelectionMode(QTableWidget.SingleSelection)
    table.setColumnCount(len(header_labels))
    table.setHorizontalHeaderLabels(header_labels)
    table.horizontalHeader().setStretchLastSection(True)
    return table


class TableWidgetRun(QWidget):
    def __init__(self):
        super().__init__()

        self.table_run = get_table_widget(['DATE', 'TOTAL ISSUES'])
        self.table_run.itemClicked.connect(self._on_table_run_item_clicked)

        self.table_issues = get_table_widget(['PROJECT', 'NUMBER'])
        self.table_run.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_issues.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.table_run)
        splitter.addWidget(self.table_issues)

        main_layout = QVBoxLayout()
        main_layout.addWidget(splitter)

        self.setLayout(main_layout)

    def refresh(self, items: List[Run]):
        # Удаление строк таблицы
        while self.table_run.rowCount():
            self.table_run.removeRow(0)

        for i, run in enumerate(items):
            self.table_run.setRowCount(self.table_run.rowCount() + 1)

            item = QTableWidgetItem(run.date.strftime('%d/%m/%Y'))
            item.setData(Qt.UserRole, run.get_project_by_issue_numbers())
            self.table_run.setItem(i, 0, item)

            item = QTableWidgetItem(str(run.get_total_issues()))
            self.table_run.setItem(i, 1, item)

        self.table_run.setCurrentCell(0, 0)
        self.table_run.setFocus()
        self._on_table_run_item_clicked()

    def _on_table_run_item_clicked(self):
        # Удаление строк таблицы
        while self.table_issues.rowCount():
            self.table_issues.removeRow(0)

        item = self.table_run.item(self.table_run.currentRow(), 0)
        if not item:
            return

        for i, (project_name, number) in enumerate(item.data(Qt.UserRole).items()):
            self.table_issues.setRowCount(self.table_issues.rowCount() + 1)

            self.table_issues.setItem(i, 0, QTableWidgetItem(project_name))
            self.table_issues.setItem(i, 1, QTableWidgetItem(str(number)))


class CurrentAssignedOpenIssues(QWidget):
    def __init__(self):
        super().__init__()

        self.table = get_table_widget(['PROJECT', 'NUMBER'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.pb_refresh = QPushButton('REFRESH')
        self.pb_refresh.clicked.connect(self.refresh)

        self.label_total = QLabel()
        font = self.label_total.font()
        font.setPixelSize(30)
        self.label_total.setFont(font)

        self.label_last_refresh_date = QLabel()

        main_layout = QGridLayout()

        main_layout.addWidget(self.label_total, 0, 0)
        main_layout.addWidget(self.pb_refresh, 0, 1)
        main_layout.addWidget(self.label_last_refresh_date, 0, 2)
        main_layout.addWidget(self.table, 1, 0, 2, 0)

        self.setLayout(main_layout)

        self._update_total_issues('-')

    def _update_total_issues(self, value):
        self.label_total.setText(f'<b>Total issues:</b> {value}')

    def refresh(self):
        items = get_assigned_open_issues_per_project()

        self._update_total_issues(sum(items.values()))

        # Удаление строк таблицы
        while self.table.rowCount():
            self.table.removeRow(0)

        for i, (project_name, number) in enumerate(items.items()):
            self.table.setRowCount(self.table.rowCount() + 1)

            self.table.setItem(i, 0, QTableWidgetItem(project_name))
            self.table.setItem(i, 1, QTableWidgetItem(str(number)))

        self.label_last_refresh_date.setText(
            "Last refresh date: " + DT.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        )


class MyChartViewToolTips(ChartViewToolTips):
    def __init__(self, timestamp_by_run: dict):
        super().__init__()

        self._callout_font_family = 'Courier'
        self.timestamp_by_run = timestamp_by_run

    def show_series_tooltip(self, point, state: bool):
        # value -> pos
        point = self.chart().mapToPosition(point)

        if not self._tooltip:
            self._tooltip = self._add_Callout()

        if state:
            distance = 25

            for series in self.chart().series():
                for p_value in series.pointsVector():
                    p = self.chart().mapToPosition(p_value)

                    current_distance = math.sqrt(
                        (p.x() - point.x()) * (p.x() - point.x())
                        + (p.y() - point.y()) * (p.y() - point.y())
                    )

                    if current_distance < distance:
                        date_value = int(p_value.x())
                        run = self.timestamp_by_run[date_value]
                        text = f"Total issues: {run.get_total_issues()}\n\n" \
                               f"{get_table(run.get_project_by_issue_numbers())}"

                        self._tooltip.setText(text)
                        self._tooltip.setAnchor(p_value)
                        self._tooltip.setZValue(11)
                        self._tooltip.updateGeometry()
                        self._tooltip.show()
        else:
            self._tooltip.hide()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(WINDOW_TITLE)

        file_name = str(CURRENT_DIR / 'favicon.ico')
        icon = QIcon(file_name)
        self.setWindowIcon(icon)

        self.timestamp_by_run = dict()

        self.tray = QSystemTrayIcon(icon)
        self.tray.setToolTip(self.windowTitle())
        self.tray.activated.connect(self._on_tray_activated)
        self.tray.show()

        self.chart_view = MyChartViewToolTips(self.timestamp_by_run)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.table_run = TableWidgetRun()
        self.table_run.layout().setContentsMargins(0, 0, 0, 0)

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.chart_view, 'CHART')
        self.tab_widget.addTab(self.table_run, 'TABLE RUN')
        self.tab_widget.addTab(CurrentAssignedOpenIssues(), 'Current Assigned Open Issues')

        self.pb_refresh = QPushButton('REFRESH')
        self.pb_refresh.clicked.connect(self.refresh)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        main_layout.addWidget(self.pb_refresh)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

    def _fill_chart(self, items: List[Run]):
        series = QLineSeries()
        series.setPointsVisible(True)
        series.setPointLabelsVisible(True)
        series.setPointLabelsFormat("@yPoint")
        series.hovered.connect(self.chart_view.show_series_tooltip)

        self.timestamp_by_run.clear()

        for run in items:
            date_value = calendar.timegm(run.date.timetuple()) * 1000
            total_issues = run.get_total_issues()
            series.append(date_value, total_issues)

            self.timestamp_by_run[date_value] = run

        chart = QChart()
        chart.setTheme(QChart.ChartThemeDark)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.addSeries(series)
        chart.legend().hide()

        # No margin
        chart.layout().setContentsMargins(0, 0, 0, 0)
        chart.setBackgroundRoundness(0)

        axisX = QDateTimeAxis()
        axisX.setFormat("dd/MM/yyyy")
        axisX.setTitleText('Date')
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setLabelFormat('%d')
        axisY.setTitleText('Total issues')
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        self.chart_view.clear_all_tooltips()
        self.chart_view.setChart(chart)

    def refresh(self):
        items = list(Run.select())
        self._fill_chart(items)

        items.reverse()
        self.table_run.refresh(items)

        self.setWindowTitle(
            WINDOW_TITLE + ". Last refresh date: " + DT.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        )

    def _on_tray_activated(self, reason):
        self.setVisible(not self.isVisible())

        if self.isVisible():
            self.showNormal()
            self.activateWindow()

    def changeEvent(self, event: QEvent):
        if event.type() == QEvent.WindowStateChange:
            # Если окно свернули
            if self.isMinimized():
                # Прячем окно с панели задач
                QTimer.singleShot(0, self.hide)


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.resize(1200, 800)
    mw.show()

    mw.refresh()

    app.exec()
