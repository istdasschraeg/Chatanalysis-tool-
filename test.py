#Hopefully Better UI 

import re
from datetime import date
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QComboBox, QLabel,
    QScrollArea, QGraphicsView,  QFrame, QHBoxLayout
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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

            for person in self.participant_objects:
                person.calculate_message_percentage(self.total_message_count)
                person.calculate_text_message_percentage(self.total_textmessages)
                person.calculate_word_percentage(self.total_words)
                person.calculate_file_percentage(self.total_files)
                person.calculate_sticker_percentage(self.total_stickers)
                person.calculate_audio_percentage(self.total_audios)
                person.calculate_video_percentage(self.total_videos)
                person.calculate_image_percentage(self.total_images)
                person.calculate_edit_percentage(self.total_edits)
                person.calculate_deleted_percentage(self.total_deleted)
                person.calculate_video_call_percentage(self.total_video_calls)
                person.calculate_voice_call_percentage(self.total_voice_calls)
                person.calculate_links_percentage(self.total_links)
                

    def output_file_analyses(self):
            # Final calculations for message and word percentages
            for person in self.participant_objects:
                # Combine all messages as a single text block and calculate word count
                person.text_content = " ".join(person.messages)
                person.word_count = len(person.text_content.split())
                
                # Calculate percentages of total messages and words
                person.word_percentage = person.word_count / len(self.new_total_text_content.split()) #
                person.calculate_words_per_message()

# Define a class to represent each chat participant
class Person:
    def __init__(self, name, gender):
        """Initialize a Person with their name, gender, and message statistics."""
        self.name = name
        self.gender = gender

        # Lists to store timestamps and other message-related information
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

    def calculate_message_percentage(self, message_count_total):
        self.message_percentage = self.message_count / message_count_total if message_count_total > 0 else 0

    def calculate_text_message_percentage(self, text_message_count_total):
        self.text_message_percentage = self.text_message_count / text_message_count_total if text_message_count_total > 0 else 0

    def calculate_word_percentage(self, total_words):
        self.word_percentage = self.word_count / total_words if total_words > 0 else 0

    def calculate_file_percentage(self, total_files):
        self.file_percentage = self.file_count / total_files if total_files > 0 else 0

    def calculate_sticker_percentage(self, total_stickers):
        self.sticker_percentage = self.sticker_count / total_stickers if total_stickers > 0 else 0

    def calculate_audio_percentage(self, total_audios):
        self.audio_percentage = self.audio_count / total_audios if total_audios > 0 else 0

    def calculate_video_percentage(self, total_videos):
        self.video_percentage = self.video_count / total_videos if total_videos > 0 else 0

    def calculate_image_percentage(self, total_images):
        self.image_percentage = self.image_count / total_images if total_images > 0 else 0

    def calculate_edit_percentage(self, total_edits):
        self.edit_percentage = self.edit_count / total_edits if total_edits > 0 else 0

    def calculate_deleted_percentage(self, total_deleted):
        self.deleted_percentage = self.deleted_count / total_deleted if total_deleted > 0 else 0

    def calculate_video_call_percentage(self, total_video_calls):
        self.video_call_percentage = self.video_call_count / total_video_calls if total_video_calls > 0 else 0

    def calculate_voice_call_percentage(self, total_voice_calls):
        self.voice_call_percentage = self.voice_call_count / total_voice_calls if total_voice_calls > 0 else 0

    def calculate_links_percentage(self, total_links):
        self.link_percentage = self.link_count / total_links if total_links > 0 else 0
    
    def calculate_words_per_message(self):
         self.words_per_message= self.word_count/self.message_count if self.message_count > 0 else 0

for file in file_list:
    object_Chatfile_list.append(Chatfile(file))



from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QFrame, QVBoxLayout, QLabel, 
                             QComboBox, QScrollArea, QWidget, QSlider)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ChatAnalysisGUI(QMainWindow):
    def __init__(self, chat_files):
        super().__init__()
        self.chat_files = chat_files
        self.username = ""
        self.active_tab = None
        self.setGeometry(100, 100, 1200, 800)

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background-color: #1e1e1e;")

        self.tab_widget = QTabWidget(self)
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane { border: 0; }
            QTabBar::tab { background: #333333; color: white; padding: 10px; }
            QTabBar::tab:selected { background: #444444; }
        """)

        self.combining_two_files("Ada.txt", "Ada2.txt")
        self.combining_two_files("Christina.txt", "Christina2.txt")
        self.combining_two_files("Daniela.txt", "Daniela2.txt")
        self.find_username()
        self.create_tabs()

    def find_username(self):
        list_names = {}
        list_of_done = []
        name_double = False

        for file in self.chat_files:
            for person in file.participant_objects:
                if person.name in list_of_done:
                    list_names[person.name] += 1
                    name_double = True
                elif not name_double:
                    list_names[person.name] = 1
                    list_of_done.append(person.name)

        self.username = max(list_names, key=list_names.get)
        print("Username detected:", self.username)

    def create_tabs(self):
    # Create the combined statistics tab
        self.combined_tab = QWidget()
        self.tab_widget.addTab(self.combined_tab, "Combined Statistics 📊")
        self.display_combined_statistics(self.combined_tab)  # Call combined statistics once

        # Create individual file tabs
        self.file_tabs = {}
        self.tab_loaded = {}  # Track loaded tabs to avoid reloading

        for file in self.chat_files:
            file_tab = QWidget()
            self.tab_widget.addTab(file_tab, file.name)
            self.file_tabs[file.name] = file_tab
            self.tab_loaded[file.name] = False  # Mark the tab as not yet loaded

        # Connect the tab change event
        self.tab_widget.currentChanged.connect(self.on_tab_change)

    def on_tab_change(self, index):
    # Get the selected tab name
        selected_tab_name = self.tab_widget.tabText(index)

        if selected_tab_name == "Combined Statistics 📊":
            # Show combined statistics content if not already loaded
            if not self.tab_loaded.get("Combined Statistics"):
                self.combined_statistics(self.combined_tab)
                self.tab_loaded["Combined Statistics"] = True
        else:
            # Show file statistics if the tab is not already loaded
            if not self.tab_loaded.get(selected_tab_name, False):
                file = next(file for file in self.chat_files if file.name == selected_tab_name)
                self.file_statistics(self.file_tabs[selected_tab_name], file)
                self.tab_loaded[selected_tab_name] = True

    def clear_tab(self, tab):
        for widget in tab.children():
            widget.deleteLater()

    def create_scrollable_tab(self, parent, chat_file):
        self.clear_tab(parent)

        scroll_area = QScrollArea(parent)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: #1e1e1e;")
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        layout = QVBoxLayout(content_widget)

        self.display_file_statistics(content_widget, chat_file)
        self.display_hourly_statistics(content_widget, chat_file)
        layout.addWidget(scroll_area)

    def display_combined_statistics(self, tab):
        self.clear_tab(tab)
        layout = QVBoxLayout(tab)

        label = QLabel("Combined Statistics")
        label.setStyleSheet("color: white; font-size: 18px; padding: 20px;")
        layout.addWidget(label)

        fig = Figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        ax.set_facecolor("#1e1e1e")

        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

    def display_file_statistics(self, tab, chat_file):
        layout = QVBoxLayout(tab)
        
        for item in ["message", "word", "sticker", "audio", "video", "image", "edit", "link", "deleted"]:
            frame = QFrame()
            frame.setStyleSheet("background-color: #2b2b2b; color: #cccccc;")
            frame_layout = QVBoxLayout(frame)
            layout.addWidget(frame)

            message_count_label = QLabel(f"{chat_file.name} - {item.capitalize()} Statistics")
            message_count_label.setStyleSheet("color: white;")
            frame_layout.addWidget(message_count_label)

            fig = Figure(figsize=(4, 4))
            ax = fig.add_subplot(111)
            ax.set_facecolor("#1e1e1e")
            canvas = FigureCanvas(fig)
            frame_layout.addWidget(canvas)

    def combining_two_files(self, chat_fileAname, chat_fileBname):
        for chat_file in self.chat_files:
            if chat_file.name == chat_fileAname:
                chatfileA = chat_file
                for chat_fileB in self.chat_files:
                    if chat_fileB.name == chat_fileBname:
                        chatfileA.chat_lines.extend(chat_fileB.chat_lines)
                        self.chat_files.remove(chat_fileB)

    def display_hourly_statistics(self, parent, chat_file):
        hourly_stats_frame = QFrame(parent)
        hourly_stats_frame.setStyleSheet("background-color: #1e1e1e; color: #cccccc;")
        layout = QVBoxLayout(hourly_stats_frame)

        participant_selector = QComboBox()
        participant_selector.addItems([p.name for p in chat_file.participant_objects])
        layout.addWidget(participant_selector)

        year_selector = QComboBox()
        year_selector.addItems([str(year) for year in range(2020, 2024)])
        layout.addWidget(year_selector)

        month_selector = QComboBox()
        month_selector.addItems([str(month) for month in range(1, 13)])
        layout.addWidget(month_selector)

        day_slider = QSlider(Qt.Orientation.Horizontal)
        day_slider.setRange(1, 31)
        day_slider.setStyleSheet("QSlider::handle { background-color: #444444; }")
        layout.addWidget(day_slider)

        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.set_facecolor("#1e1e1e")
        self.canvas = FigureCanvas(fig)
        layout.addWidget(self.canvas)


if __name__ == "__main__":
        app = QApplication(sys.argv)
        chat_files = object_Chatfile_list
        window = ChatAnalysisGUI(chat_files)
        window.show()
        sys.exit(app.exec())

"""TO DO LIST:

    exclude names(through min participation ) 
    Sentiment Analyses
    emotions detection?
    include one number statistics in display like: messages per time or words per message
    Time of Day patters

        dictionary with each hour when message 
            one with the count and one with the text(for analysis)

    Month Year inlfux of texts
    Message Batch recognition
    Instagramm extension
    Responds time Analyses (with certain modifable thresholds)
    
    GUI with possiblity of 
        identifying doubles in group chats
        insta whatsapp identification

    Conversation starter (Useres that start a conversation)
    Mentions 
    Emojis?
    Topic Analyser
    personilsed language
    Politness meter

    Interface that can:

        find and acess Folder where txt are
        ask User for which chats to combine 
        ask User to possily combine Insta and whatsapp chats  
        ask User if they want to remove certain names

    
        
        For Instagramm analysis:

            maybe remove reels enterly and just let Omitted stand there
    
    """

