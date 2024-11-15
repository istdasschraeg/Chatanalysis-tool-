#Hopefully Better UI 

import re
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QComboBox, QLabel,
    QScrollArea, QGraphicsView,  QFrame, QHBoxLayout,  QFileDialog ,QPushButton, QListWidget
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from functools import partial
from PyQt6.QtCharts import QChart, QChartView, QPieSeries
from PyQt6.QtGui import QPainter
#QGraphicsScen

nltk.download('vader_lexicon')

# Initialize the Sentiment Intensity Analyzer
sid = SentimentIntensityAnalyzer()

# Global variables
timestamp_pattern = r"\[\d{2}\.\d{2}\.\d{2}, \d{2}:\d{2}:\d{2}\]"
enable_interface = False
excluded_names = ["\u200eYou", "DummeLeuteDieSchachSpiele","Gossip Girls", "Gott Der Fucking Welt"]
file_list=["DummeLeuteDieSchachSpielen.txt","Nyla.txt","Moritz.txt","Gossip.txt","Ada.txt","Ada2.txt","Carl Erhardt.txt","Caro.txt","Chat 2024.txt","Christina.txt","Christina2.txt",
           "Cosima.txt","Daniela.txt","Daniela2.txt", "Elise HeHe.txt", "Emilia.txt","Emma.txt", "Enz.txt","Fahrradtour.txt","Fiona.txt","Herren.txt","Jule.txt","Juliane.txt",
           "Julius.txt","Liam.txt","Lukas.txt","Mama.txt","Manu.txt","Marcus.txt","Mihn.txt","Mitchel.txt","Q3-Q4.txt","Renate.txt","Sergio.txt","Tay.txt"]
object_Chatfile_list =[]

if enable_interface:
    print("What file should be opend")
    file_list.append(input())




 


# Names of people participating in the chat
participant_names = []

class Chatfile:
    def __init__(self,name):
        self.name=name
        self.chat_lines = []
        self.participant_objects = []
        self.participant_names = []
        self.new_total_text_content=""
        self.total_words=0
        self.total_message_count=0
        self.total_textmessages=0
        self.total_messages=0
        self.total_stickers=0
        self.total_images=0
        self.total_audios=0
        self.total_videos=0
        self.total_files=0
        self.total_voice_calls=0
        self.total_video_calls=0
        self.total_edits=0
        self.total_deleted=0
        self.total_links=0
        self.time_str =""
        self.date_str = ""

        self.count_messages_per_timeframe={}
        self.text_messages_per_timeframe={}
        self.count_messages_per_timeframe_daily={}
        self.text_messages_per_timeframe_daily={}
        self.count_messages_per_timeframe_monthly={}
        self.text_messages_per_timeframe_monthly={}

        self.load_file()
        self.clean_up_file()
        self.extract_participant_names()
        self.create_person_objects()
        self.measure_time()
        self.ANALyse_messages()
        self.analyse_entiere_file()
        self.output_file_analyses()

    def load_file(self):
            with open(self.name, "r", encoding="utf8") as file:
                self.chat_lines = file.readlines()

    def clean_up_file(self):
            # Process lines to clean up and merge
            t = 0

            # Iterate through lines to merge any without a timestamp to the previous line
            while t < len(self.chat_lines) - 1:
                self.chat_lines[t] = self.chat_lines[t].strip()  # Remove extra whitespace
                self.chat_lines[t] = self.chat_lines[t].replace("Ã¼", "ue").replace("â€Ž", "").replace("ä","ae")  # Clean encoding artifacts
    
                # If the next line lacks a timestamp or  contains "omitted," merge it with the current line
                if not re.match(timestamp_pattern, self.chat_lines[t + 1]) and not "omitted" in self.chat_lines[t + 1]:
                    self.chat_lines[t] += " " + self.chat_lines[t + 1]
                    self.chat_lines.pop(t + 1)  # Remove the next line after merging
                else:        
                    t += 1

    def extract_participant_names(self):
            # Extract and store unique names from the chat content
            for line in self.chat_lines:
            # Extract a possible name substring (between index 21 and 35)
                name_segment = line[21:]
                colon_position = name_segment.find(":")
                
                # Check if there's a valid name and extract it
                if colon_position != -1:
                    name = name_segment[:colon_position].strip()
                    
                    # Add the name to participant_names if it's new
                    if name not in self.participant_names and name not in excluded_names:

                        if colon_position > 20:
                            t=0
                            while t < len(self.chat_lines) - 1:
                                self.chat_lines[t] = self.chat_lines[t].replace(name,line[21:40])
                                t+=1 
                            self.participant_names.append(line[21:40])

                        else:
                            self.participant_names.append(name)



            if enable_interface:
                if participant_names.count()>2:
                    print(*participant_names)
                    print("Which of these is the name of the groupchat?")
                    excluded_names.append(input())
                    print("Which of these is your name?")
                    #user_name=input()

                    number_of_replicates=0
                    print("Is any of these names a replication of Another? y/n")
                    if input()=="y":
                        while number_of_replicates==0:
                            print("Which one is the duplicate")
                            to_be_replaced=input()
                            print("Which one is the original")
                            to_be_kept=input()
                            t=0
                            for line in self.chat_lines:
                                self.chat_lines[t]=self.chat_lines[t].replace(to_be_replaced,to_be_kept)
                                t+=1
                            print("Are those all dublicates?")
                            if input()=="y":
                                number_of_replicates+=1


    def create_person_objects(self):
            for participant_name in self.participant_names:
                #print("What gender is ",participant_name,"?(male, female, other)")
                gender = "other"  # Placeholder for user input
                self.participant_objects.append(Person(participant_name, gender))

    def measure_time(self):

            for participant in self.participant_names:
                person_index = 0
                for line in self.chat_lines:
                    # Check for lines starting with "[" indicating a message
                    if line.startswith("["):
                        line = line.replace(participant, "(Person)").replace("Ã¼", "ue").replace("â€Ž", "")
                        
                        # Identify and extract message time details if participant name matches
                        if line[21:29] == participant:
                            self.time_str = line[12:19]
                            self.date_str = line[2:10]
                            
                            # Extract and store individual time components
                            hour = int(line[11:13])
                            minute = int(line[14:16])
                            second = int(line[17:19])
                            day = int(line[1:3])
                            month = int(line[4:6])
                            year = int(line[7:9])

                            #add to the dictionary
                            self.count_messages_per_timeframe[participant][year][month][day][hour] += 1
                            self.text_messages_per_timeframe[participant][year][month][day][hour] +=line 
                            self.text_messages_per_timeframe_daily[participant][year][month][day] +=line 
                            self.count_messages_per_timeframe_daily[participant][year][month][day]+=1
                            self.text_messages_per_timeframe_monthly[participant][year][month]+=line 
                            self.count_messages_per_timeframe_monthly[participant][year][month]+=1

                    person_index += 1
                    line = line.replace("(Person)", participant)

    def analyze_mood_vader(text):
        scores = sid.polarity_scores(text)
        compound_score = scores['compound']
        
        return scores   

    def ANALyse_messages(self):
            # Collect message content for each participant
            message_count_total = 0
            for person_index, participant in enumerate(self.participant_names):
                for line in self.chat_lines:
                    
                    # Identify and store message content if participant's name is found
                    if line.find(participant) >= 0:
                        self.participant_objects[person_index].message_count += 1
                        message_count_total += 1
                        if line.count("image omitted")==1:
                            self.participant_objects[person_index].image_count+=1                        
                        elif line.count("document omitted")==1:  
                            self.participant_objects[person_index].file_count+=1                          
                        elif line.count("audio omitted")==1:  
                            self.participant_objects[person_index].audio_count+=1                           
                        elif line.count("video omitted")==1:  
                            self.participant_objects[person_index].video_count+=1                             
                        elif line.count("sticker omitted")==1:  
                            self.participant_objects[person_index].sticker_count+=1                           
                        elif line.count("This message was deleted")==1:
                            self.participant_objects[person_index].deleted_count+=1                           
                        elif line.count("ideo call")==1:
                            self.participant_objects[person_index].video_call_count+=1                           
                        elif line.count("oice call")==1:
                            self.participant_objects[person_index].voice_call_count+=1    
                        else:
                            message_start = line.find(participant) + len(participant)
                            self.participant_objects[person_index].messages.append(line[message_start:])
                            self.participant_objects[person_index].text_message_count += 1  
                        if line.count ("<This message was edited>")==1:
                            self.participant_objects[person_index].edit_count+=1                       
                        if line.count ("http")>=1:
                            self.participant_objects[person_index].link_count+=1 

    def analyse_entiere_file(self):
            # Creates a String with all the messages 
            self.new_total_text_content= ""
            for person in self.participant_objects:
                self.new_total_text_content+= " ".join(person.messages)  

                self.total_files = sum(person.file_count for person in self.participant_objects)
                self.total_stickers = sum(person.sticker_count for person in self.participant_objects)
                self.total_audios = sum(person.audio_count for person in self.participant_objects)
                self.total_videos = sum(person.video_count for person in self.participant_objects)
                self.total_images = sum(person.image_count for person in self.participant_objects)
                self.total_edits = sum(person.edit_count for person in self.participant_objects)
                self.total_deleted = sum(person.deleted_count for person in self.participant_objects)
                self.total_video_calls = sum(person.video_call_count for person in self.participant_objects)
                self.total_voice_calls = sum(person.voice_call_count for person in self.participant_objects)
                self.total_links = sum(person.link_count for person in self.participant_objects)
                self.total_words = len(self.new_total_text_content.split()) 
                self.total_message_count += person.message_count
                self.total_textmessages += person.text_message_count

    def output_file_analyses(self):
            # Final calculations for message and word percentages
            for person in self.participant_objects:
                # Combine all messages as a single text block and calculate word count
                person.text_content = " ".join(person.messages)
                person.word_count = len(person.text_content.split())              
class Person:
    def __init__(self, name, gender):
        """Initialize a Person with their name, gender, and message statistics."""
        self.name = name
        self.gender = gender

        self.hours = []
        self.minutes = []
        self.seconds = []
        self.days = []
        self.months = []
        self.years = []

        self.message_count = 0
        self.text_message_count=0
        self.file_count = 0
        self.sticker_count = 0
        self.audio_count = 0
        self.video_count = 0
        self.image_count=0
        self.word_count = 0
        self.edit_count= 0
        self.link_count=0
        self.deleted_count=0
        self.video_call_count=0
        self.voice_call_count=0
        self.messages = []
        
        self.text_content = ""
        self.pretty_print_name()

        self.message_percentage = 0
        self.text_message_percentage = 0
        self.file_percentage = 0
        self.sticker_percentage = 0
        self.audio_percentage = 0
        self.video_percentage = 0
        self.image_percentage = 0
        self.word_percentage = 0
        self.edit_percentage = 0
        self.link_percentage = 0
        self.deleted_percentage = 0
        self.video_call_percentage = 0
        self.voice_call_percentage = 0
        self.words_per_message=0

    def pretty_print_name(self):
        print(f"This Person's name is {self.name}.")

for file in file_list:
    object_Chatfile_list.append(Chatfile(file))

from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QHBoxLayout
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt

class FileStatisticsGUI(QWidget):
    def __init__(self, object_Chatfile_list):
        super().__init__()
        self.username=""
        self.minimalpercentage=1
        self.chat_files = object_Chatfile_list
        self.current_timeframe = 'Day'
        self.time_index = 0
        self.setWindowTitle("Whatsapp Analyser")
        self.find_username()
        self.init_ui()       
        
    def init_ui(self):
        self.setGeometry(100, 100, 1200, 900)
        
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

        self.setup_tabs("Pie charts")
        
        # Add sidebar and content layout to the main layout
        main_layout.addLayout(sidebar_layout, 1)  # Sidebar with width ratio
        main_layout.addLayout(content_layout, 4)   # Content with width ratio

        self.setLayout(main_layout)

    def setup_tabs(self, mode):
        # Clear existing tabs before setting up new ones
        self.tab_widget.clear()
        
        if mode =="Pie charts":
        # Combined statistics tab setup
            combined_scroll_area = QScrollArea()
            combined_scroll_area.setWidgetResizable(True)
            
            combined_content = QWidget()
            combined_layout = QVBoxLayout(combined_content)
            
            # Combo box and label for combined statistics display
            combined_combo_box = QComboBox()
            combined_combo_box.addItems(["message", "word", "sticker", "audio", "video", "image", "edit", "link", "deleted"])
            combined_label = QLabel("Selected option will appear here")
            
            combined_layout.addWidget(combined_combo_box)
            combined_layout.addWidget(combined_label)
            
            # Placeholder layout for charts or numbers in combined statistics
            combined_chart_layout = QVBoxLayout()
            combined_layout.addLayout(combined_chart_layout)
            
            # Add combined content to the scroll area and tab widget
            combined_scroll_area.setWidget(combined_content)
            self.tab_widget.addTab(combined_scroll_area, "Combined Statistics")

            # Connect the combo box for "Combined Statistics" tab
            combined_combo_box.currentTextChanged.connect(
                    lambda text: self.show_combined_stats(text, combined_label, combined_chart_layout))
            
        if mode =="Numbers":

            #add combo box for ranking

            file_scroll_area = QScrollArea()
            file_scroll_area.setWidgetResizable(True)
            file_label = QLabel("")
                
            file_content = QWidget()
            file_layout = QVBoxLayout(file_content)                    
            file_layout.addWidget(file_label)
            file_layout = QVBoxLayout()
                    
            file_scroll_area.setWidget(file_content)
            self.tab_widget.addTab(file_scroll_area, f"Combined Statistics")     

            text_data = ""
            items = ["message", "word", "sticker", "audio", "video", "image", "edit", "link", "deleted", "video_call", "voice_call"]
            list_names = []
            dict_counts = {} 

            for chat_file in self.chat_files:
                for person in chat_file.participant_objects:
                    name_double = False
                    
                    for i in list_names:
                        if i == person.name:
                            
                            for item in items:
                                count = getattr(person, f"{item}_count", 0)
                                dict_counts[person.name + "_" + item] = dict_counts.get(person.name + "_" + item, 0) + count
                            name_double = True
                            break
                    
                    if not name_double and person.message_count> 50:
                        for item in items:
                            count = getattr(person, f"{item}_count", 0)
                            dict_counts[person.name + "_" + item] = count
                        list_names.append(person.name)

            for name in list_names:
                text_data += f"{name.capitalize()}:\n\n"
                for item in items:
                    count = dict_counts.get(name + "_" + item, 0)
                    text_data += f"{item.capitalize()} messages: {count}\n"
                
                word_count = dict_counts.get(name + "_word", 0)
                message_count = dict_counts.get(name + "_message", 0)
                if message_count > 0:
                    words_per_message = round(word_count / message_count, 4)
                    text_data += f"Words per Message: {words_per_message}\n"
                
                text_data += "-" * 150 + "\n\n"  

            file_label.setText(text_data)

            
        if mode == "Pie charts":
            for file in self.chat_files:
                # Create a scrollable area for each file tab
                scroll_area = QScrollArea()
                scroll_area.setWidgetResizable(True)
                
                # Create a container widget for each file tab's content
                file_tab_content = QWidget()
                file_tab_layout = QVBoxLayout(file_tab_content)
                
                combo_box = QComboBox()
                combo_box.addItems(["message", "word", "sticker", "audio", "video", "image", "edit", "link", "deleted", "video_call", "voice_call"])
                label = QLabel("Selected option will appear here")
                
                file_tab_layout.addWidget(combo_box)
                file_tab_layout.addWidget(label)
                
                chart_layout = QVBoxLayout()
                file_tab_layout.addLayout(chart_layout)
                
                combo_box.currentTextChanged.connect(lambda text, file=file, label=label, chart_layout=chart_layout: 
                                                    self.display_file_statistics(text, file, label, chart_layout))
                
                # Set the file_tab_content as the widget of the scroll area
                scroll_area.setWidget(file_tab_content)

                self.tab_widget.addTab(scroll_area, f"Statistics for {file.name}")
        if mode == "Numbers":   
            for chat_file in self.chat_files:
                file_scroll_area = QScrollArea()
                file_scroll_area.setWidgetResizable(True)
                file_label = QLabel("")
                    
                file_content = QWidget()
                file_layout = QVBoxLayout(file_content)
                file_layout.addWidget(file_label)
                
                file_layout = QVBoxLayout()
                        
                file_scroll_area.setWidget(file_content)
                self.tab_widget.addTab(file_scroll_area, f"Statistics for {chat_file.name}")     

                file_label.setText(self.display_file_numbers(chat_file)   ) 
            
        if mode == "Over time":
            # Initialize variables needed across "Over time" methods
            self.time_index = 0  # Keeps track of current timeframe position
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
            
            # Layout setup for navigation and chart display
            layout = QVBoxLayout(self)
            navigation_layout = QHBoxLayout()
            navigation_layout.addWidget(self.prev_button)
            navigation_layout.addWidget(self.timeframe_selector)
            navigation_layout.addWidget(self.next_button)
            
            layout.addLayout(navigation_layout)
            layout.addWidget(self.chart_view)
            
            # Initial chart setup
            self.update_chart()

    def update_chart(self):
        # Clear the old chart and create a new one
        chart = QChart()
        self.current_timeframe = self.timeframe_selector.currentText()
        
        # Placeholder data based on selected timeframe
        time_units = ["01", "02", "03", "04", "05", "06", "07"]  # Customize with real data
        
        series = QBarSeries()
        data_set = QBarSet(self.current_timeframe)
        
        # Populate bars with example data; replace with real data
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
        
        
        

    

         
    def change_display_mode(self, item):
        if item:
            mode = item.text()  
            self.setup_tabs(mode)

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
        # Update the label with the selected option
        label.setText(f"Statistics for {text}")
        
        for i in reversed(range(chart_layout.count())):
            widget_to_remove = chart_layout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.deleteLater()
                chart_layout.removeWidget(widget_to_remove)

        # Calculate the total count for the selected statistic
        total_count = sum(int(getattr(person, f"{text}_count", 0) or 0) for person in chat_file.participant_objects)
        if total_count == 0:
            print(f"No data to display for {text}.")
            return  # No data to show for this option

        # Create a new pie chart per item
        series = QPieSeries()
        total=0
        for person in chat_file.participant_objects:
            count = int(getattr(person, f"{text}_count", 0) or 0)
            print (count)
            total +=count
            print (total)
            percentage = (count / total_count) * 100  # Calculate percentage
            if count > 0 and percentage > (10 / len(chat_file.participant_objects)):
                # Append data with formatted label showing absolute value and percentage
                slice = series.append(f"{person.name}: {count} ({percentage:.1f}%)", count)
                slice.setLabelVisible(True)
                
                
        label.setText(f"Statistics for {text}. Total {total}")

        # Create a chart for the series
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(f"{text.capitalize()} Statistics")

        # Create a QChartView to display the chart
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Add the chart view to the chart layout
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


