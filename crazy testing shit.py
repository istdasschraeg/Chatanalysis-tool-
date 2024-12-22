class FileStatisticsGUI(QWidget):
    def __init__(self, object_Chatfile_list):
        super().__init__()
        self.username=""
        self.minimalpercentage=1
        self.chat_files = object_Chatfile_list
        self.current_timeframe = 'Day'
        self.time_index = 1

        self.timeframe_year=0
        self.timeframe_month=0
        self.timeframe_day=0
        self.timeframe_hour=0

        self.last_hour =0
        self.last_minute = 0
        self.last_second = 0
        self.last_day = 0
        self.last_month = 0
        self.last_year =0
        
        self.setWindowTitle("Whatsapp Analyser")
        self.find_username()
        
        self.init_ui() 

    def create_pie_chart(self,data_series, title):
        """Creates a QChartView containing a pie chart."""
        chart = QChart()
        chart.addSeries(data_series)
        chart.setTitle(title)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        return chart_view

    def create_tab(self,tab_widget, chart_layout, label_text):
        """Clears the tab layout and updates the label."""
        tab_widget.clear()  # If needed for additional tabs management
        for i in reversed(range(chart_layout.count())):
            widget_to_remove = chart_layout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.deleteLater()
                chart_layout.removeWidget(widget_to_remove)
        return label_text      
        
    def init_ui(self):
        self.setGeometry(700, 100, 1200, 900)
        
        # Main layout for the window
        main_layout = QHBoxLayout(self)
        
        # Sidebar for display mode selection
        sidebar_layout = QVBoxLayout()
        self.display_mode_list = QListWidget()
        self.display_mode_list.addItems(["Pie charts", "Numbers", "Over time"])

        self.display_mode_list.currentItemChanged.connect(self.change_display_mode)
        sidebar_layout.addWidget(self.display_mode_list)
        
        # Main content layout (for current tab widget)
        content_layout = QVBoxLayout()
        self.tab_widget = QTabWidget()
        content_layout.addWidget(self.tab_widget)

        self.display_tabs("Pie charts")
        
        # Add sidebar and content layout to the main layout
        main_layout.addLayout(sidebar_layout, 1)  # Sidebar with width ratio
        main_layout.addLayout(content_layout, 4)   # Content with width ratio

        self.setLayout(main_layout)

    def create_scroll_area_with_layout(self):
        """Creates a scrollable area with a vertical layout and returns both."""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        scroll_area.setWidget(content_widget)
        return scroll_area, layout

    def create_combined_tab(self,tab_widget, items, combo_box_handler):
        """Creates a combined statistics tab with a combo box and chart layout."""
        scroll_area, combined_layout = self.create_scroll_area_with_layout()
        combo_box = QComboBox()
        combo_box.addItems(items)
        label = QLabel("Selected option will appear here")

        combined_layout.addWidget(combo_box)
        combined_layout.addWidget(label)

        chart_layout = QVBoxLayout()
        combined_layout.addLayout(chart_layout)

        # Connect the combo box handler
        combo_box.currentTextChanged.connect(lambda text: combo_box_handler(text, label, chart_layout))
        tab_widget.addTab(scroll_area, "Combined Statistics")

    def create_file_tab(self,tab_widget, chat_file, items, combo_box_handler):
        """Creates a statistics tab for a single file with a combo box and chart layout."""
        scroll_area, file_layout = self.create_scroll_area_with_layout()
        combo_box = QComboBox()
        combo_box.addItems(items)
        label = QLabel("Selected option will appear here")

        file_layout.addWidget(combo_box)
        file_layout.addWidget(label)

        chart_layout = QVBoxLayout()
        file_layout.addLayout(chart_layout)

        # Connect the combo box handler
        combo_box.currentTextChanged.connect(
            lambda text, file=chat_file: combo_box_handler(text, file, label, chart_layout))
        tab_widget.addTab(scroll_area, f"Statistics for {chat_file.name}")

    def create_numbers_tab(self,tab_widget, chat_files, items, numbers_handler):
        """Creates a numbers tab for all chat files."""
        scroll_area, layout = self.create_scroll_area_with_layout()
        label = QLabel("")
        layout.addWidget(label)

        text_data = numbers_handler(chat_files, items)
        label.setText(text_data)

        tab_widget.addTab(scroll_area, "Combined Statistics")

    def create_time_stats_tab(self,tab_widget, chat_file, move_handler, update_handler):
        """Creates a time statistics tab for a single chat file."""
        scroll_area, file_layout = self.create_scroll_area_with_layout()

        # Navigation Buttons
        nav_layout = QHBoxLayout()
        prev_button = QPushButton("←")
        next_button = QPushButton("→")
        timeframe_selector = QComboBox()
        timeframe_selector.addItems(["Day", "Week", "Month", "Year"])

        nav_layout.addWidget(prev_button)
        nav_layout.addWidget(next_button)
        nav_layout.addWidget(timeframe_selector)
        file_layout.addLayout(nav_layout)

        # Chart Display
        chart_view = QChartView()
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        file_layout.addWidget(chart_view)

        # Connect buttons and dropdown
        prev_button.clicked.connect(partial(move_handler, chat_file, -1, chart_view, timeframe_selector))
        next_button.clicked.connect(partial(move_handler, chat_file, 1, chart_view, timeframe_selector))
        timeframe_selector.currentTextChanged.connect(partial(update_handler, chat_file, chart_view, timeframe_selector))

        tab_widget.addTab(scroll_area, f"Time Stats for {chat_file.name}")

    def display_tabs(self, mode):
        """Displays the appropriate tabs based on the selected mode."""
        self.tab_widget.clear()
        items = ["message", "word", "sticker", "audio", "video", "image", "edit", "link", "deleted", "video_call", "voice_call"]

        if mode == "Pie charts":
            # Combined Statistics Tab create_combined_tab
            self.create_combined_tab(self.tab_widget, items, self.show_combined_stats)

            # Individual File Tabs
            for chat_file in self.chat_files:
                self.create_file_tab(self.tab_widget, chat_file, items, self.display_file_statistics)

        elif mode == "Numbers":
            # Combined Statistics
            self.create_numbers_tab(self.tab_widget, self.chat_files, items, self.display_file_numbers)

            # Individual File Tabs
            for chat_file in self.chat_files:
                scroll_area, layout = self.create_scroll_area_with_layout()
                label = QLabel(self.display_file_numbers(chat_file))
                layout.addWidget(label)
                self.tab_widget.addTab(scroll_area, f"Statistics for {chat_file.name}")

        elif mode == "Over time":
            # Time Statistics Tabs
            for chat_file in self.chat_files:
                self.create_time_stats_tab(self.tab_widget, chat_file, self.move_in_time, self.update_chart)

    def move_in_time(self, file, direction, chart_view, timeframe_selector):
            """
            Updates the time index and refreshes the chart when navigating.
            """
            self.time_index += direction
            self.update_chart(file, chart_view, timeframe_selector)

    def update_chart(self, file, chart_view, timeframe_selector):
        """
        Refreshes the chart to display messages over the selected timeframe.
        """
        chart = QChart()
        current_timeframe = timeframe_selector.currentText()

        series = QBarSeries()
        data_set = QBarSet(file.name)
        chart.setTitle(f"Messages Over Time ({current_timeframe})")
        if current_timeframe == "Day":
            chart.setTitle(f"Messages for {self.last_day:02}/{self.last_month:02}/{self.last_year + 2000}")
        elif current_timeframe == "Week":
            chart.setTitle(f"Messages for Week Ending {self.last_day:02}/{self.last_month:02}/{self.last_year + 2000}")
        elif current_timeframe == "Month":
            chart.setTitle(f"Messages for {self.last_month:02}/{self.last_year + 2000}")
        elif current_timeframe == "Year":
            chart.setTitle(f"Messages for {self.last_year + 2000}")

       
        if current_timeframe == "Day":
            data = self.get_timeframe_data(file, "daily", self.time_index)
            
            categories = [f"{i}:00" for i in range(len(data))]
        elif current_timeframe == "Week":
            data = self.get_timeframe_data(file, "weekly", self.time_index)
            categories = [f"Day {i+1}" for i in range(len(data))]
        elif current_timeframe == "Month":
            data = self.get_timeframe_data(file, "monthly", self.time_index)
            categories = [f" {i+1}" for i in range(len(data))]
        elif current_timeframe == "Year":
            data = self.get_timeframe_data(file, "yearly", self.time_index)
            categories = [f"{i+1}" for i in range(len(data))]

        data_set.append(data)
        series.append(data_set)
        chart.addSeries(series)

        # Set up axes
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        # Update chart view
        
        chart_view.setChart(chart)

    def find_last_message(self,file):
        file.clean_up_file()
        self.last_hour = int(file.chat_lines[-1][11:13])
        self.last_minute = int(file.chat_lines[-1][14:16])
        self.last_second = int(file.chat_lines[-1][17:19])
        self.last_day = int(file.chat_lines[-1][1:3])
        self.last_month = int(file.chat_lines[-1][4:6])
        self.last_year = int(file.chat_lines[-1][7:9])
                
    def get_timeframe_data(self, file, timeframe, index):

        if timeframe == "daily":
            list_hours = [0] * 24  
            for hours in range(24):  
                for line in file.chat_lines:
                    
                        hour = int(line[11:13])
                        day = int(line[1:3])
                        month = int(line[4:6])
                        year = int(line[7:9])
                        
                       
                        if day == self.last_day and month == self.last_month and year == self.last_year and hour == hours:
                            list_hours[hours] += 1
            return list_hours

        from datetime import datetime, timedelta
        if timeframe == "weekly":
            list_days = [0] * 7  
            last_date = datetime(self.last_year, self.last_month, self.last_day)
            start_date = last_date - timedelta(days=6)  

            for line in file.chat_lines:
                    day = int(line[1:3])
                    month = int(line[4:6])
                    year = int(line[7:9])                     
                    message_date = datetime(year, month, day)                
                    if start_date <= message_date <= last_date:
                        weekday_index = message_date.weekday()  
                        list_days[weekday_index] += 1

            return list_days


        elif timeframe == "monthly":
            list_month = [0] * 31  
            for line in file.chat_lines:
                
                    day = int(line[1:3])
                    month = int(line[4:6])
                    year = int(line[7:9])
                    
                    # Match with the last month
                    if year == self.last_year and month == self.last_month:
                        if 1 <= day <= 31:
                            list_month[day - 1] += 1 
            return list_month

        elif timeframe == "yearly":
            list_months = [0] * 12  
            for line in file.chat_lines:
                
                    month = int(line[4:6])
                    year = int(line[7:9])
                    
                    # Match with the last year
                    if year == self.last_year:
                        list_months[month - 1] += 1  
            return list_months

    def move_in_time(self, file, direction, chart_view, timeframe_selector):
    
        current_timeframe = timeframe_selector.currentText()

        if current_timeframe == "Day":
            
            self.last_day += direction
            if self.last_day < 1:  
                self.last_month -= 1
                if self.last_month < 1:
                    self.last_month = 12
                    self.last_year -= 1
                self.last_day = self.get_days_in_month(self.last_month, self.last_year)
            elif self.last_day > self.get_days_in_month(self.last_month, self.last_year):  
                self.last_day = 1
                self.last_month += 1
                if self.last_month > 12:
                    self.last_month = 1
                    self.last_year += 1

        elif current_timeframe == "Week":
            
            self.last_day += 7 * direction
            while self.last_day < 1:  
                self.last_month -= 1
                if self.last_month < 1:
                    self.last_month = 12
                    self.last_year -= 1
                self.last_day += self.get_days_in_month(self.last_month, self.last_year)
            while self.last_day > self.get_days_in_month(self.last_month, self.last_year): 
                self.last_day -= self.get_days_in_month(self.last_month, self.last_year)
                self.last_month += 1
                if self.last_month > 12:
                    self.last_month = 1
                    self.last_year += 1

        elif current_timeframe == "Month":
            self.last_month += direction
            if self.last_month < 1:
                self.last_month = 12
                self.last_year -= 1
            elif self.last_month > 12:
                self.last_month = 1
                self.last_year += 1

        elif current_timeframe == "Year":
            self.last_year += direction

        self.update_chart(file, chart_view, timeframe_selector)

    def get_days_in_month(self, month, year):
        """
        Returns the number of days in a given month and year.
        """
        return monthrange(year + 2000, month)[1] 

    def change_display_mode(self, item):
        if item:
            mode = item.text()  
            self.display_tabs(mode)

    def display_file_numbers(self,chat_file):
       
        text_data = ""
        items = ["message", "word", "sticker", "audio", "video", "image", "edit", "link", "deleted", "video_call", "voice_call"]
        
        for person in chat_file.participant_objects:
            text_data+=f"{person.name.capitalize()}: \n\n"
            for item in items: 
                count = getattr(person, f"{item}_count", 0)
                text_data += f"{item.capitalize()} messages: {count} \n"
            text_data+= f"Words per Message: {round(person.word_count/person.message_count, 4)}\n"

            text_data += "-" * 200 + "\n\n"

          
        
        return text_data 

    def display_file_statistics(self, text, chat_file, label, chart_layout):
        """Displays file statistics using a pie chart in a tab layout."""
        # Clear and update the tab
        label_text = f"Statistics for {text}"
        label.setText(self.create_tab(self.tab_widget, chart_layout, label_text))

        # Calculate total count
        total_count = sum(int(getattr(person, f"{text}_count", 0) or 0) for person in chat_file.participant_objects)
        if total_count == 0:
            print(f"No data to display for {text}.")
            return

        # Create the pie series
        series = QPieSeries()
        total = 0
        for person in chat_file.participant_objects:
            count = int(getattr(person, f"{text}_count", 0) or 0)
            total += count
            percentage = (count / total_count) * 100
            if count > 0 and percentage > (10 / len(chat_file.participant_objects)):
                pie_slice = series.append(f"{person.name}: {count} ({percentage:.1f}%)", count)
                pie_slice.setLabelVisible(True)

        # Update the label
        label.setText(f"Statistics for {text}. Total {total}")

        # Create pie chart and add to layout
        chart_view = self.create_pie_chart(series, f"{text.capitalize()} Statistics")
        chart_layout.addWidget(chart_view)
        self.tab_widget.update()

    def combining_two_files(self, chat_fileAname, chat_fileBname):
        for chat_file in self.chat_files:
            if chat_file.name ==chat_fileAname:
                chatfileA= chat_file
                for chat_fileB in self.chat_files:
                    if chat_fileB.name ==chat_fileBname:
                        chatfileA.chat_lines.extend ( chat_fileB.chat_lines)
                        self.chat_files.remove(chat_fileB)

    def show_combined_stats(self,text, label, chart_layout):
        # Update the label with the selected option
        label.setText(f"Combined statistics for {text}")

        # Clear the old chart views from the layout
        for i in reversed(range(chart_layout.count())):
            widget_to_remove = chart_layout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.deleteLater()
                chart_layout.removeWidget(widget_to_remove)

        total_count_with=0
        for file in self.chat_files:
            for person in file.participant_objects:  
                    total_count_with += int(getattr(person, f"{text}_count", 0) or 0) 

        # Calculate the total count for the selected statistics
        total_count=0
        for file in self.chat_files:
            for person in file.participant_objects:
                if not person.name== self.username:
                    total_count += int(getattr(person, f"{text}_count", 0) or 0) 

        label.setText(f"Statistics for {text}. Total: {total_count}. Total including U: {total_count_with}")
        # Create a new pie chart per item
        series = QPieSeries()
        for file in self.chat_files:
            for person in file.participant_objects:
                if not person.name == self.username and len(file.participant_objects)==2:
                    count = int(getattr(person, f"{text}_count", 0) or 0)
                    
                    percentage = (count / total_count) * 100    # Calculate percentage           
                    if count > 0  :  
                        if  percentage > (self.minimalpercentage):
                            # Append data with formatted label showing absolute value and percentage
                            slice = series.append(f"{person.name}: {count} ({percentage:.1f}%)", count)
                            slice.setLabelVisible(True)

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
                    
                else:
                    name_double=False

        self.username = max(list_names, key=list_names.get)
        print("Username detected:", self.username)


        

# Main application launch
app = QApplication(sys.argv)
window = FileStatisticsGUI(object_Chatfile_list)
window.show()
sys.exit(app.exec())

