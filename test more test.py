from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QHBoxLayout
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt

class TimeframeBarGraph(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.current_timeframe = 'Day'
        self.time_index = 0

        # Layout and chart initialization
        layout = QVBoxLayout(self)
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Dropdown for timeframe selection
        self.timeframe_selector = QComboBox()
        self.timeframe_selector.addItems(["Day", "Week", "Month", "Year"])
        self.timeframe_selector.currentTextChanged.connect(self.update_chart)
        
        # Navigation buttons
        self.prev_button = QPushButton("←")
        self.next_button = QPushButton("→")
        self.prev_button.clicked.connect(self.move_back)
        self.next_button.clicked.connect(self.move_forward)
        
        # Horizontal layout for buttons and selector
        navigation_layout = QHBoxLayout()
        navigation_layout.addWidget(self.prev_button)
        navigation_layout.addWidget(self.timeframe_selector)
        navigation_layout.addWidget(self.next_button)

        layout.addLayout(navigation_layout)
        layout.addWidget(self.chart_view)

        self.update_chart()

    def update_chart(self):
        # Clear the old chart and create a new one
        chart = QChart()
        self.current_timeframe = self.timeframe_selector.currentText()
        
        # Placeholder data based on selected timeframe
        time_units = ["01", "02", "03", "04", "05", "06", "07"]  # Customize with real data
        
        series = QBarSeries()
        data_set = QBarSet(self.current_timeframe)
        
        # Populate bars with example data; replace with your real data
        if self.current_timeframe == "Day":
            data_set.append([5, 3, 8, 6, 7, 2, 1])
        elif self.current_timeframe == "Week":
            data_set.append([35, 40, 50, 20, 30, 25, 45])
        elif self.current_timeframe == "Month":
            data_set.append([100, 120, 80, 150, 90, 110, 130])
        elif self.current_timeframe == "Year":
            data_set.append([1200, 1350, 1300, 1400, 1250, 1280, 1380])
        
        series.append(data_set)
        chart.addSeries(series)
        
        # Create axis and categories
        axis_x = QBarCategoryAxis()
        axis_x.append(time_units)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        chart.setTitle(f"Metrics over Time ({self.current_timeframe})")
        self.chart_view.setChart(chart)

    def move_forward(self):
        # Shift timeframe forward and update chart
        self.time_index += 1
        self.update_chart()

    def move_back(self):
        # Shift timeframe backward and update chart
        self.time_index = max(0, self.time_index - 1)
        self.update_chart()


app = QApplication([])
window = TimeframeBarGraph()
window.show()
app.exec()
