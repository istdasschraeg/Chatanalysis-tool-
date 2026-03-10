#Hopefully Better UI 

import re
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import sys
from PyQt6.QtWidgets import  QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QComboBox, QLabel, QScrollArea, QGraphicsView,  QFrame, QHBoxLayout,  QFileDialog ,QPushButton, QListWidget, QLineEdit, QTextEdit
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from functools import partial
from PyQt6.QtCharts import QChart, QChartView, QPieSeries
from PyQt6.QtGui import QPainter
from datetime import datetime, timedelta
from calendar import monthrange
from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt6.QtGui import QPainter
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
#QGraphicsScen

nltk.download('vader_lexicon')
nltk.download('stopwords')

# Initialize the Sentiment Intensity Analyzer
sid = SentimentIntensityAnalyzer()

# Qt alignment constants (since they may not be available in this PyQt6 installation)
ALIGN_BOTTOM = 0x40
ALIGN_LEFT = 0x1

# Global variables
timestamp_pattern = r"\[\d{2}\.\d{2}\.\d{2}, \d{2}:\d{2}:\d{2}\]"
enable_interface = False
excluded_names = ["\u200eYou","Ihmen.txt", "DummeLeuteDieSchachSpiele","Gossip Girls", "Gott Der Fucking Welt"]
file_list=["DummeLeuteDieSchachSpielen.txt","MONMON.txt","Nyla.txt","Moritz.txt","Gossip.txt","Tay.txt","Madlen.txt","Ada.txt",
           "Ada2.txt","Carl Erhardt.txt","Caro.txt","Chat 2024.txt","Christina.txt","Christina2.txt",
           "Cosima.txt","Daniela.txt","Daniela2.txt", "Elise HeHe.txt", "Emilia.txt","Emma.txt", 
           "Enz.txt","Fahrradtour.txt","Fiona.txt","Herren.txt","Jule.txt","Juliane.txt","Julius.txt",
           "Liam.txt","Lukas.txt","Mama.txt","Manu.txt","Marcus.txt","Mihn.txt","Mitchel.txt","Q3-Q4.txt",
           "Renate.txt","Sergio.txt"]
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
        self.measure_time_per_person()
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
                self.chat_lines[t] = self.chat_lines[t].replace("Ã¼", "ue").replace("â€Ž", "").replace("ä","ae").replace("U+200e","")  # Clean encoding artifacts
    
                # If the next line lacks a timestamp or  contains "omitted," merge it with the current line
                if not re.match(timestamp_pattern, self.chat_lines[t + 1]) and not "omitted" in self.chat_lines[t + 1]:
                    self.chat_lines[t] += " " + self.chat_lines[t + 1]
                    self.chat_lines.pop(t + 1)  # Remove the next line after merging
                else:        
                    t += 1

    def parse_date(self, line):
        try:
            start = line.find('[')
            end = line.find(']', start)
            if start == -1 or end == -1:
                return None
            date_str = line[start+1:end]
            if ', ' in date_str:
                date_part, time_part = date_str.split(', ')
            else:
                # Some formats might have different separator
                return None
            # Handle different date separators
            if '.' in date_part:
                parts = date_part.split('.')
            elif '/' in date_part:
                parts = date_part.split('/')
            else:
                return None
            if len(parts) == 3:
                day, month, year = map(int, parts)
                if year < 100:
                    year += 2000
                hour, minute, second = map(int, time_part.split(':'))
                return day, month, year, hour, minute, second
            else:
                return None
        except:
            return None

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

    def create_person_objects(self):
            for participant_name in self.participant_names:
                #print("What gender is ",participant_name,"?(male, female, other)")
                gender = "other"  # Placeholder for user input
                self.participant_objects.append(Person(participant_name, gender))

    #def measure_time(self):

                #for line in self.chat_lines:
                    # Check for lines starting with "[" indicating a message
                    #if line.startswith("["):
                            #line = line.replace("Ã¼", "ue").replace("â€Ž", "")

                            #self.time_str = line[12:19]
                            #self.date_str = line[2:10]
                             
                            # Extract and store individual time components
                            #hour = int(line[11:13])
                            #minute = int(line[14:16])
                            #second = int(line[17:19])
                            #day = int(line[1:3])
                            #month = int(line[4:6])
                            #year = int(line[7:9])

                            #add to the dictionary
                            #self.count_messages_per_timeframe[year][month][day][hour] += 1
                            #self.text_messages_per_timeframe[year][month][day][hour] +=line 
                            #self.text_messages_per_timeframe_daily[year][month][day] +=line 
                            #self.count_messages_per_timeframe_daily[year][month][day]+=1
                            #self.text_messages_per_timeframe_monthly[year][month]+=line 
                            #self.count_messages_per_timeframe_monthly[year][month]+=1

                            
    def measure_time_per_person(self):

                for line in self.chat_lines:  
                    for participant in self.participant_objects:
                        if line.startswith("["):
                            start = line.find('[')
                            end = line.find(']', start)
                            if start != -1 and end != -1:
                                name_start = end + 2
                                name_end = line.find(':', name_start)
                                if name_end != -1:
                                    name = line[name_start:name_end].strip()
                                    if name == participant.name:
                                        parsed = self.parse_date(line)
                                        if parsed:
                                            day, month, year, hour, minute, second = parsed
                                            participant.hours.append(hour)
                                            # Initialize nested dicts if needed
                                            if year not in self.count_messages_per_timeframe:
                                                self.count_messages_per_timeframe[year] = {}
                                            if month not in self.count_messages_per_timeframe[year]:
                                                self.count_messages_per_timeframe[year][month] = {}
                                            if day not in self.count_messages_per_timeframe[year][month]:
                                                self.count_messages_per_timeframe[year][month][day] = [0] * 24
                                            self.count_messages_per_timeframe[year][month][day][hour] += 1
                                            # Similar for text_messages_per_timeframe
                                            if year not in self.text_messages_per_timeframe:
                                                self.text_messages_per_timeframe[year] = {}
                                            if month not in self.text_messages_per_timeframe[year]:
                                                self.text_messages_per_timeframe[year][month] = {}
                                            if day not in self.text_messages_per_timeframe[year][month]:
                                                self.text_messages_per_timeframe[year][month][day] = {}
                                            if hour not in self.text_messages_per_timeframe[year][month][day]:
                                                self.text_messages_per_timeframe[year][month][day][hour] = ""
                                            self.text_messages_per_timeframe[year][month][day][hour] += line
                                            # And so on for the others
                                            if year not in self.text_messages_per_timeframe_daily:
                                                self.text_messages_per_timeframe_daily[year] = {}
                                            if month not in self.text_messages_per_timeframe_daily[year]:
                                                self.text_messages_per_timeframe_daily[year][month] = {}
                                            if day not in self.text_messages_per_timeframe_daily[year][month]:
                                                self.text_messages_per_timeframe_daily[year][month][day] = ""
                                            self.text_messages_per_timeframe_daily[year][month][day] += line
                                            if year not in self.count_messages_per_timeframe_daily:
                                                self.count_messages_per_timeframe_daily[year] = {}
                                            if month not in self.count_messages_per_timeframe_daily[year]:
                                                self.count_messages_per_timeframe_daily[year][month] = {}
                                            if day not in self.count_messages_per_timeframe_daily[year][month]:
                                                self.count_messages_per_timeframe_daily[year][month][day] = 0
                                            self.count_messages_per_timeframe_daily[year][month][day] += 1
                                            if year not in self.text_messages_per_timeframe_monthly:
                                                self.text_messages_per_timeframe_monthly[year] = {}
                                            if month not in self.text_messages_per_timeframe_monthly[year]:
                                                self.text_messages_per_timeframe_monthly[year][month] = ""
                                            self.text_messages_per_timeframe_monthly[year][month] += line
                                            if year not in self.count_messages_per_timeframe_monthly:
                                                self.count_messages_per_timeframe_monthly[year] = {}
                                            if month not in self.count_messages_per_timeframe_monthly[year]:
                                                self.count_messages_per_timeframe_monthly[year][month] = 0
                                            self.count_messages_per_timeframe_monthly[year][month] += 1  

                            # Replace for anonymization
                            line = line.replace(participant.name, "(Person)").replace("Ã¼", "ue").replace("â€Ž", "")  

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

    def get_hourly_counts(self):
        counts = [0] * 24
        for h in self.hours:
            counts[h] += 1
        return counts

    def pretty_print_name(self):
        print(f"This Person's name is {self.name}.")

for file in file_list:
    object_Chatfile_list.append(Chatfile(file))


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
        
    def parse_date(self, line):
        try:
            start = line.find('[')
            end = line.find(']', start)
            if start == -1 or end == -1:
                return None
            date_str = line[start+1:end]
            date_part, time_part = date_str.split(', ')
            day, month, year = map(int, date_part.split('.'))
            year += 000
            hour, minute, second = map(int, time_part.split(':'))
            return day, month, year, hour, minute, second
        except:
            return None
        
    def init_ui(self):
        self.setGeometry(700, 100, 1200, 900)
        
        # Main layout for the window
        main_layout = QHBoxLayout(self)
        
        # Sidebar for display mode selection
        sidebar_layout = QVBoxLayout()
        self.display_mode_list = QListWidget()
        self.display_mode_list.addItems(["Pie charts", "Numbers", "Over time", "Phrase Finder", "Top Phrases", "Time Patterns"])

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
            for file in self.chat_files:
                self.find_last_message(file)
                self.find_last_message
                # Create a tab for each file
                scroll_area = QScrollArea()
                scroll_area.setWidgetResizable(True)

                file_tab_content = QWidget()
                file_tab_layout = QVBoxLayout(file_tab_content)

                # Navigation Buttons
                nav_layout = QHBoxLayout()
                prev_button = QPushButton("←")
                next_button = QPushButton("→")
                nav_layout.addWidget(prev_button)
                nav_layout.addWidget(next_button)

                # Timeframe Dropdown
                timeframe_selector = QComboBox()
                timeframe_selector.addItems(["Day", "Week", "Month", "Year"])
                nav_layout.addWidget(timeframe_selector)

                # Data Type Dropdown
                data_type_selector = QComboBox()
                data_type_selector.addItems(["Message Count", "Sentiment Score"])
                nav_layout.addWidget(data_type_selector)

                # Add navigation layout
                file_tab_layout.addLayout(nav_layout)

                # Chart Display
                chart_view = QChartView()
                chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
                file_tab_layout.addWidget(chart_view)

                # Set up connections
                prev_button.clicked.connect(partial(self.move_in_time, file, -1, chart_view, timeframe_selector, data_type_selector))
                next_button.clicked.connect(partial(self.move_in_time, file, 1, chart_view, timeframe_selector, data_type_selector))
                timeframe_selector.currentTextChanged.connect(
                    partial(self.update_chart, file, chart_view, timeframe_selector, data_type_selector))
                data_type_selector.currentTextChanged.connect(
                    partial(self.update_chart, file, chart_view, timeframe_selector, data_type_selector))

                # Add tab content to scroll area
                scroll_area.setWidget(file_tab_content)
                self.tab_widget.addTab(scroll_area, f"Time Stats for {file.name}")

        if mode == "Phrase Finder":
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            content = QWidget()
            layout = QVBoxLayout(content)
            
            file_combo = QComboBox()
            file_combo.addItems([f.name for f in self.chat_files])
            layout.addWidget(QLabel("Select Chat File:"))
            layout.addWidget(file_combo)
            
            phrase_input = QLineEdit()
            phrase_input.setPlaceholderText("Enter phrase to search")
            layout.addWidget(QLabel("Phrase:"))
            layout.addWidget(phrase_input)
            
            search_button = QPushButton("Search")
            layout.addWidget(search_button)
            
            results_text = QTextEdit()
            results_text.setReadOnly(True)
            layout.addWidget(QLabel("Results:"))
            layout.addWidget(results_text)
            
            search_button.clicked.connect(lambda: self.search_phrase(file_combo.currentText(), phrase_input.text(), results_text))
            
            scroll_area.setWidget(content)
            self.tab_widget.addTab(scroll_area, "Phrase Finder")

        if mode == "Top Phrases":
            for file in self.chat_files:
                scroll_area = QScrollArea()
                scroll_area.setWidgetResizable(True)
                content = QWidget()
                layout = QVBoxLayout(content)
                
                text_edit = QTextEdit()
                text_edit.setReadOnly(True)
                text = f"Top Phrases for {file.name}\n\n"
                
                for person in file.participant_objects:
                    if person.messages and len(person.messages) > 10:
                        text += f"{person.name}:\n"
                        top_phrases = self.get_top_phrases(person.messages, n=20)
                        if top_phrases:
                            for phrase, count in top_phrases:
                                text += f"  '{phrase}': {count} times\n"
                        else:
                            text += "  No significant phrases found.\n"
                        text += "\n"
                
                text_edit.setText(text)
                layout.addWidget(text_edit)
                
                scroll_area.setWidget(content)
                self.tab_widget.addTab(scroll_area, f"Top Phrases for {file.name}")

        if mode == "Time Patterns":
            for file in self.chat_files:
                scroll_area = QScrollArea()
                scroll_area.setWidgetResizable(True)
                content = QWidget()
                layout = QVBoxLayout(content)
                
                for person in file.participant_objects:
                    if person.message_count > 10:
                        chart = QChart()
                        series = QBarSeries()
                        bar_set = QBarSet(person.name)
                        
                        hourly_counts = person.get_hourly_counts()
                        for count in hourly_counts:
                            bar_set.append(count)
                        
                        series.append(bar_set)
                        chart.addSeries(series)
                        
                        axis_x = QBarCategoryAxis()
                        axis_x.append([f"{h}:00" for h in range(24)])
                        chart.addAxis(axis_x, Qt.AlignmentFlag(ALIGN_BOTTOM))
                        series.attachAxis(axis_x)
                        
                        axis_y = QValueAxis()
                        axis_y.setTitleText("Messages")
                        chart.addAxis(axis_y, Qt.AlignmentFlag(ALIGN_LEFT))
                        series.attachAxis(axis_y)
                        
                        chart.setTitle(f"{person.name} - Hourly Activity")
                        
                        chart_view = QChartView(chart)
                        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
                        layout.addWidget(chart_view)
                
                scroll_area.setWidget(content)
                self.tab_widget.addTab(scroll_area, f"Time Patterns for {file.name}")

    def move_in_time(self, file, direction, chart_view, timeframe_selector):
            """
            Updates the time index and refreshes the chart when navigating.
            """
            self.time_index += direction
            self.update_chart(file, chart_view, timeframe_selector)

    def update_chart(self, file, chart_view, timeframe_selector, data_type_selector):
        """
        Refreshes the chart to display messages over the selected timeframe.
        """
        chart = QChart()
        current_timeframe = timeframe_selector.currentText()
        current_data_type = data_type_selector.currentText()

        series = QBarSeries()
        data_set = QBarSet(file.name)
        chart.setTitle(f"{current_data_type} Over Time ({current_timeframe})")
        if current_timeframe == "Day":
            chart.setTitle(f"{current_data_type} for {self.last_day:02}/{self.last_month:02}/{self.last_year + 2000}")
        elif current_timeframe == "Week":
            chart.setTitle(f"{current_data_type} for Week Ending {self.last_day:02}/{self.last_month:02}/{self.last_year + 2000}")
        elif current_timeframe == "Month":
            chart.setTitle(f"{current_data_type} for {self.last_month:02}/{self.last_year + 2000}")
        elif current_timeframe == "Year":
            chart.setTitle(f"{current_data_type} for {self.last_year + 2000}")

       
        if current_timeframe == "Day":
            if current_data_type == "Message Count":
                data = self.get_timeframe_data(file, "daily", self.time_index)
            else:
                data = self.get_sentiment_data(file, "daily", self.time_index)
            categories = [f"{i}:00" for i in range(len(data))]
        elif current_timeframe == "Week":
            if current_data_type == "Message Count":
                data = self.get_timeframe_data(file, "weekly", self.time_index)
            else:
                data = self.get_sentiment_data(file, "weekly", self.time_index)
            categories = [f"Day {i+1}" for i in range(len(data))]
        elif current_timeframe == "Month":
            if current_data_type == "Message Count":
                data = self.get_timeframe_data(file, "monthly", self.time_index)
            else:
                data = self.get_sentiment_data(file, "monthly", self.time_index)
            categories = [f" {i+1}" for i in range(len(data))]
        elif current_timeframe == "Year":
            if current_data_type == "Message Count":
                data = self.get_timeframe_data(file, "yearly", self.time_index)
            else:
                data = self.get_sentiment_data(file, "yearly", self.time_index)
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
        if current_data_type == "Sentiment Score":
            axis_y.setTitleText("Sentiment Score")
        else:
            axis_y.setTitleText("Message Count")
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        # Update chart view
        
        chart_view.setChart(chart)

    def get_timeframe_data(self, file, timeframe, time_index):
        # Placeholder implementation
        if timeframe == "daily":
            year = self.last_year + 2000
            month = self.last_month
            day = self.last_day
            return file.count_messages_per_timeframe.get(year, {}).get(month, {}).get(day, [0] * 24)
        # Add other timeframes as needed
        return []

    def get_sentiment_data(self, file, timeframe, time_index):
        if timeframe == "daily":
            year = self.last_year + 2000
            month = self.last_month
            day = self.last_day
            hourly_sentiments = [[] for _ in range(24)]
            for hour in range(24):
                messages = file.text_messages_per_timeframe.get(year, {}).get(month, {}).get(day, {}).get(hour, "")
                if messages:
                    # Split messages and compute sentiment
                    msg_list = messages.split('\n')
                    for msg in msg_list:
                        if msg.strip():
                            scores = sid.polarity_scores(msg)
                            hourly_sentiments[hour].append(scores['compound'])
            # Compute average per hour
            data = []
            for hour in range(24):
                if hourly_sentiments[hour]:
                    avg = sum(hourly_sentiments[hour]) / len(hourly_sentiments[hour])
                    data.append(avg)
                else:
                    data.append(0)
            return data
        return []

    def find_last_message(self,file):
        file.clean_up_file()
        parsed = self.parse_date(file.chat_lines[-1])
        if parsed:
            self.last_day, self.last_month, self.last_year, self.last_hour, self.last_minute, self.last_second = parsed
                


    def get_timeframe_data(self, file, timeframe, index):

        if timeframe == "daily":
            list_hours = [0] * 24  
            for hours in range(24):  
                for line in file.chat_lines:
                    parsed = self.parse_date(line)
                    if parsed:
                        day, month, year, hour, minute, second = parsed
                        if day == self.last_day and month == self.last_month and year == self.last_year and hour == hours:
                            list_hours[hours] += 1
            return list_hours

        from datetime import datetime, timedelta
        if timeframe == "weekly":
            list_days = [0] * 7  
            last_date = datetime(self.last_year, self.last_month, self.last_day)
            start_date = last_date - timedelta(days=6)  

            for line in file.chat_lines:
                parsed = self.parse_date(line)
                if parsed:
                    day, month, year, hour, minute, second = parsed
                    message_date = datetime(year, month, day)                
                    if start_date <= message_date <= last_date:
                        weekday_index = message_date.weekday()  
                        list_days[weekday_index] += 1

            return list_days


        elif timeframe == "monthly":
            list_month = [0] * 31  
            for line in file.chat_lines:
                parsed = self.parse_date(line)
                if parsed:
                    day, month, year, hour, minute, second = parsed
                    # Match with the last month
                    if year == self.last_year and month == self.last_month:
                        if 1 <= day <= 31:
                            list_month[day - 1] += 1 
            return list_month

        elif timeframe == "yearly":
            list_months = [0] * 12  
            for line in file.chat_lines:
                parsed = self.parse_date(line)
                if parsed:
                    day, month, year, hour, minute, second = parsed
                    # Match with the last year
                    if year == self.last_year:
                        list_months[month - 1] += 1  
            return list_months

    def move_in_time(self, file, direction, chart_view, timeframe_selector, data_type_selector):
    
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

        self.update_chart(file, chart_view, timeframe_selector, data_type_selector)


    def get_days_in_month(self, month, year):
        """
        Returns the number of days in a given month and year.
        """
        return monthrange(year + 2000, month)[1] 

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
        
        label.setText(f"Statistics for {text}")
        
        for i in reversed(range(chart_layout.count())):
            widget_to_remove = chart_layout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.deleteLater()
                chart_layout.removeWidget(widget_to_remove)

        
        total_count = sum(int(getattr(person, f"{text}_count", 0) or 0) for person in chat_file.participant_objects)
        if total_count == 0:
            print(f"No data to display for {text}.")
            return 

        
        series = QPieSeries()
        total=0
        for person in chat_file.participant_objects:
            count = int(getattr(person, f"{text}_count", 0) or 0)
            print (count)
            total +=count
            print (total)
            percentage = (count / total_count) * 100  
            person.messages
            if count > 0 and percentage > (10 / len(chat_file.participant_objects)):
                
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

    def get_top_phrases(self, messages, n=20, ngram_range=(2,4)):
        # Deduplicate messages to prevent repeated messages from dominating
        clean_messages = list(set([msg.strip().lstrip(':').strip() for msg in messages if msg.strip()]))
        
        # List of phrases/words to exclude (common WhatsApp system messages)
        excluded_terms = [
            'omitted', 'deleted this message', 'you deleted', 'changed', 'gif', 'image', 'video', 'audio',
            'youtube', 'spotify', 'instagram', 'facebook', 'twitter', 'tiktok', 'whatsapp', 'telegram',
            'com', 'org', 'net', 'de', 'eu', 'uk', 'us', 'ca', 'au', 'jp', 'cn', 'ru', 'br', 'mx', 'ar',
            'location', 'contact', 'document', 'sticker', 'emoji', 'reaction', 'poll', 'vote'
        ]
        
        phrase_counts = {}
        for msg in clean_messages:
            if not msg:
                continue
            text = msg.lower()
            vectorizer = CountVectorizer(ngram_range=ngram_range, stop_words=nltk.corpus.stopwords.words('german'), min_df=1)
            try:
                X = vectorizer.fit_transform([text])
                feature_names = vectorizer.get_feature_names_out()
                counts = X.toarray()[0]
                unique_phrases_in_msg = set()
                for i, count in enumerate(counts):
                    if count > 0:
                        phrase = feature_names[i]
                        # Filter out phrases with URLs or numbers
                        if not ('http' in phrase or 'www' in phrase or any(char.isdigit() for char in phrase)):
                            # Filter out repetitive phrases (same word repeated)
                            words = phrase.split()
                            if len(words) == len(set(words)):  # no duplicates
                                # Filter out common WhatsApp/system phrases
                                if not any(term in phrase for term in excluded_terms):
                                    unique_phrases_in_msg.add(phrase)
                # Increment count for each unique phrase in this message
                for phrase in unique_phrases_in_msg:
                    if phrase in phrase_counts:
                        phrase_counts[phrase] += 1
                    else:
                        phrase_counts[phrase] = 1
            except Exception as e:
                print(f"Error processing message: {e}")
                continue
        
        # Sort phrases by count descending
        sorted_phrases = sorted(phrase_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_phrases[:n]

    
        

# Main application launch
app = QApplication(sys.argv)
window = FileStatisticsGUI(object_Chatfile_list)
window.show()
sys.exit(app.exec())


