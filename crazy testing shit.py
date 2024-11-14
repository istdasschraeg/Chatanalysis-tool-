import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QScrollArea, QComboBox, QLabel
from PyQt6.QtCharts import QChart, QChartView, QPieSeries
from PyQt6.QtGui import QPainter

class FileStatisticsGUI(QWidget):
    def __init__(self, object_Chatfile_list):
        super().__init__()
        self.setWindowTitle("Whatsapp Analyser")
        self.chat_files = object_Chatfile_list
        self.init_ui()
        self.username=""
        
    def init_ui(self):
        self.setGeometry(100, 100, 1200, 900)
        layout = QVBoxLayout(self)
        
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        for file in self.chat_files:
            # Create a scrollable area for each file tab
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            
            # Create a container widget for each file tab's content
            file_tab_content = QWidget()
            file_tab_layout = QVBoxLayout(file_tab_content)
            
            # Add combo box and label for displaying options and selected data
            combo_box = QComboBox()
            combo_box.addItems(["message", "word", "sticker", "audio", "video", "image", "edit", "link", "deleted"])
            label = QLabel("Selected option will appear here")
            
            file_tab_layout.addWidget(combo_box)
            file_tab_layout.addWidget(label)
            
            # Placeholder layout for charts
            chart_layout = QVBoxLayout()
            file_tab_layout.addLayout(chart_layout)
            
            # Connect the combo box to the display method with a unique scope for each file
            combo_box.currentTextChanged.connect(lambda text, file=file, label=label, chart_layout=chart_layout: 
                                                 self.display_file_statistics(text, file, label, chart_layout))
            
            # Set the file_tab_content as the widget of the scroll area
            scroll_area.setWidget(file_tab_content)

            self.tab_widget.addTab(scroll_area, f"Statistics for {file.name}")
        
        self.setLayout(layout)

    def display_file_statistics(self, text, chat_file, label, chart_layout):
        # Update the label with the selected option
        label.setText(f"Statistics for {text}")

        # Clear the old chart views from the layout
        for i in reversed(range(chart_layout.count())):
            widget_to_remove = chart_layout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.deleteLater()
                chart_layout.removeWidget(widget_to_remove)

        # Create a new pie chart per item
        series = QPieSeries()
        for person in chat_file.participant_objects:
            count = int(getattr(person, f"{text}_count", 0) or 0)
            if count > 0:
                series.append(person.name, count)

        if not series.slices():
            return  # No data to show for this option
        
        # Create a chart for the series
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(f"{text.capitalize()} Statistics")

        # Create a QChartView to display the chart
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Add the chart view to the chart layout
        chart_layout.addWidget(chart_view)

    def find_username(self):
        """Determine the most active username from chat data."""
        list_names = {}
        list_of_done = []
        name_double = False

        for file in self.chat_files:
            for person in file.participant_objects:
                for i in list_of_done:
                    if i == person.name:
                        list_names[person.name] += 1
                        name_double = True

                if not name_double:
                    list_names[person.name] = 1
                    list_of_done.append(person.name)

        self.username = max(list_names, key=list_names.get)
        print("Username detected:", self.username)

if __name__ == "__main__":
    # Dummy data for testing purposes
    class Participant:
        def __init__(self, name, message_count=0, word_count=0, sticker_count=0):
            self.name = name
            self.message_count = message_count
            self.word_count = word_count
            self.sticker_count = sticker_count

    class ChatFile:
        def __init__(self, name, participants):
            self.name = name
            self.participant_objects = participants

    participants = [Participant("Alice", message_count=100, word_count=200),
                    Participant("Bob", message_count=150, word_count=250)]
    object_Chatfile_list = [ChatFile("Chat 1", participants), ChatFile("Chat 2", participants)]

    app = QApplication(sys.argv)
    window = FileStatisticsGUI(object_Chatfile_list)
    window.resize(1200, 900)
    window.show()
    sys.exit(app.exec())
