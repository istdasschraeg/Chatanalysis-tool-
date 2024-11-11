import re

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
    file_list.apppend(input())


 


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
                            self.participant_objects[person_index].hours.append(hour)
                            
                            minute = int(line[14:16])
                            self.participant_objects[person_index].minutes.append(minute)

                            second = int(line[17:19])
                            self.participant_objects[person_index].seconds.append(second)

                            day = int(line[1:3])
                            self.participant_objects[person_index].days.append(day)

                            month = int(line[4:6])
                            self.participant_objects[person_index].months.append(month)

                            year = int(line[7:9])
                            self.participant_objects[person_index].years.append(year)

                    person_index += 1
                    line = line.replace("(Person)", participant)
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
                person.message_percentage = person.message_count / self.total_message_count
                person.word_percentage = person.word_count / len(self.new_total_text_content.split()) #
                person.calculate_words_per_message()
                
                # Print statistics for each participant
                #print(f"{person.name} has sent {person.message_count} messages, accounting for {round(person.message_percentage * 100,2)}% of all messages.")
                #print(f"{person.name} has sent {person.text_message_count} textmessages, accounting for {round(person.text_message_percentage * 100,2)}% of all textmessages.")
                #print(f"{person.name} has written {person.word_count} words, accounting for {round(person.word_percentage * 100,2)}% of all words.")
                #print(f"{person.name} has sent {person.file_count} files, accounting for {round(person.file_percentage * 100,2)}% of all files.")
                #print(f"{person.name} has sent {person.link_count} links, accounting for {round(person.link_percentage * 100,2)}% of all links.")
                #print(f"{person.name} has sent {person.sticker_count} stickers, accounting for {round(person.sticker_percentage * 100,2)}% of all stickers.")
                #print(f"{person.name} has sent {person.audio_count} audios, accounting for {round(person.audio_percentage * 100,2)}% of all audios.")
                #print(f"{person.name} has sent {person.video_count} videos, accounting for {round(person.video_percentage * 100,2)}% of all videos.")
                #print(f"{person.name} has sent {person.image_count} images, accounting for {round(person.image_percentage * 100,2)}% of all images.")
                #print(f"{person.name} has edited {person.edit_count} messages, accounting for {round(person.edit_percentage * 100,2)}% of all edits.")
                #print(f"{person.name} has deleted {person.deleted_count} messages, accounting for {round(person.deleted_percentage * 100,2)}% of all deleted messages.")
                #print(f"{person.name} has made {person.video_call_count} video calls, accounting for {round(person.video_call_percentage * 100,2)}% of all video calls.")
                #print(f"{person.name} has made {person.voice_call_count} voice calls, accounting for {round(person.voice_call_percentage * 100,2)}% of all voice calls.")
                #print(f"{person.name} writes an aveage of {round(person.words_per_message,2)} words per message")


    #Work:
    

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


# Final output of total message and word statistic
#print("Total message count:", message_count_total)
#print("Total word count:", len(new_total_text_content.split()))
#print("Average words per message:", len(new_total_text_content.split()) / message_count_total)


for file in file_list:
    object_Chatfile_list.append(Chatfile(file))


import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ChatAnalysisGUI:
    def __init__(self, root, chat_files):
        self.root = root
        self.chat_files = chat_files
        self.username = ""
        self.active_tab = None  # Track the currently active tab

        # Fullscreen, borderless
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#1e1e1e")  # Dark, modern background

        # Styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#1e1e1e", foreground="#ffffff", font=("Helvetica", 12, "bold"))
        style.configure("TNotebook.Tab", background="#333333", foreground="#ffffff", padding=(15, 10), relief="flat")
        style.map("TNotebook.Tab", background=[("selected", "#444444")])

        style.configure("TFrame", background="#1e1e1e")
        style.configure("TLabelFrame", background="#2b2b2b", foreground="#ffffff", relief="flat", padding=20)
        style.configure("TLabelFrame.Label", background="#1e1e1e", foreground="#ffffff", font=("Helvetica", 14, "bold"))
        style.configure("TLabel", background="#2b2b2b", foreground="#cccccc", font=("Helvetica", 12))

        # Custom scrollbar style
        style.configure("Vertical.TScrollbar", background="#444444", troughcolor="#1e1e1e", gripcount=0)

        # Set up main window layout
        self.find_username()
        self.create_tabs()

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

    def create_tabs(self):
        """Create notebook tabs dynamically with content rendering only when active."""
        self.tab_control = ttk.Notebook(self.root)
        self.tab_control.pack(expand=True, fill="both", padx=20, pady=20)

        # Combined statistics tab
        self.combined_tab = ttk.Frame(self.tab_control, style="TFrame")
        self.tab_control.add(self.combined_tab, text="Combined Statistics 📊")

        # Individual file tabs with deferred rendering
        self.file_tabs = {}
        for file in self.chat_files:
            file_tab = ttk.Frame(self.tab_control, style="TFrame")
            self.tab_control.add(file_tab, text=file.name)
            self.file_tabs[file.name] = file_tab

        # Add a callback for tab switching
        self.tab_control.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def on_tab_change(self, event):
        """Handle tab switching, render content for active tab, and clear inactive tabs."""
        selected_tab_index = self.tab_control.index("current")
        selected_tab = self.tab_control.nametowidget(self.tab_control.tabs()[selected_tab_index])

        # Clear content of the previously active tab
        if self.active_tab and self.active_tab != selected_tab:
            self.clear_tab(self.active_tab)

        # Render content for the newly selected tab
        if selected_tab == self.combined_tab:
            self.display_combined_statistics(self.combined_tab)
        else:
            for file_name, tab in self.file_tabs.items():
                if tab == selected_tab:
                    self.create_scrollable_tab(tab, next(file for file in self.chat_files if file.name == file_name))
                    break

        # Update active tab reference
        self.active_tab = selected_tab

    def clear_tab(self, tab):
        """Clear all widgets in a given tab."""
        for widget in tab.winfo_children():
            widget.destroy()

    def create_scrollable_tab(self, parent, chat_file):
        """Create a scrollable tab for individual file statistics."""
        self.clear_tab(parent)  # Ensure the tab is clean before populating

        # Scrollable canvas
        canvas = tk.Canvas(parent, bg="#1e1e1e", highlightthickness=0)
        scrollable_frame = ttk.Frame(canvas, style="TFrame")

        scrollbar_y = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview, style="Vertical.TScrollbar")
        canvas.configure(yscrollcommand=scrollbar_y.set)

        # Pack canvas and scrollbar
        scrollbar_y.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Create a centered window for the scrollable frame
        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

        # Configure scrollable frame update
        def update_canvas(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas_width = canvas.winfo_width()
            frame_width = scrollable_frame.winfo_reqwidth()
            x_offset = max((canvas_width - frame_width) // 2, 0)  # Calculate horizontal centering
            canvas.itemconfigure(window_id, x=x_offset)

        scrollable_frame.bind("<Configure>", update_canvas)
        canvas.bind("<Configure>", lambda event: update_canvas(None))

        # Display file-specific statistics
        self.display_file_statistics(scrollable_frame, chat_file)



    def display_combined_statistics(self, tab):
        """Display combined statistics for all chat files in a scrollable tab."""
        self.clear_tab(tab)

        # Create a scrollable canvas
        canvas = tk.Canvas(tab, bg="#1e1e1e", highlightthickness=0)
        scrollable_frame = ttk.Frame(canvas, style="TFrame")

        scrollbar_y = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview, style="Vertical.TScrollbar")
        canvas.configure(yscrollcommand=scrollbar_y.set)

        # Pack canvas and scrollbar
        scrollbar_y.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Create a window in the canvas for the scrollable frame
        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

        # Configure scrollable frame resizing
        def update_canvas(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas_width = canvas.winfo_width()
            frame_width = scrollable_frame.winfo_reqwidth()
            x_offset = max((canvas_width - frame_width) // 2, 0)
            canvas.itemconfigure(window_id, x=x_offset)

        scrollable_frame.bind("<Configure>", update_canvas)
        canvas.bind("<Configure>", lambda event: update_canvas(None))

        # Centering the combined statistics content
        frame = ttk.LabelFrame(scrollable_frame, text="Combined Statistics", style="TLabelframe", padding=(50, 20))
        frame.pack(pady=50, padx=50, anchor="center")

        # Preparing combined statistics text content
        all_files_messages_by_person_dictionary = {}
        list_names = []

        for file in self.chat_files:
            for person in file.participant_objects:
                if person.name != self.username:
                    name_double = False
                    for i in list_names:
                        if i == person.name:
                            all_files_messages_by_person_dictionary[person.name] += person.message_count
                            name_double = True
                            break
                    if not name_double:
                        all_files_messages_by_person_dictionary[person.name] = person.message_count
                        list_names.append(person.name)

        

        # Filter out participants with <10% of messages divided by the total number of people
        total_messages = sum(all_files_messages_by_person_dictionary.values())
        number_of_people = len(all_files_messages_by_person_dictionary)
        threshold = (0.7 / number_of_people) * total_messages
        filtered_statistics = {name: count for name, count in all_files_messages_by_person_dictionary.items() if count >= threshold}

        # Display statistics as text
        displayed_stats = "\n".join(
            f"Text messages from {name}: {count}"
            for name, count in all_files_messages_by_person_dictionary.items()
            
        )

        displayed_stats += f"\n Total Number of Messages:{total_messages}"
 
        label = ttk.Label(
            frame,
            text=displayed_stats,
            style="TLabel",
            padding=(20, 10),
            font=("Helvetica", 14),
            justify="center"
        )
        label.pack(pady=(0, 20))

        # Pie chart visualization
        fig, ax = plt.subplots(figsize=(15, 15))
        ax.pie(
            filtered_statistics.values(),
            labels=filtered_statistics.keys(),
            autopct='%1.1f%%',
            colors=["#66b3ff", "#99ff99", "#ffcc99", "#ff6666"],
            startangle=140
        )
        ax.set_title("Combined Message Distribution", color="#ffffff", fontsize=12)

        canvas_chart = FigureCanvasTkAgg(fig, master=frame)
        canvas_chart.get_tk_widget().pack(pady=20)
        pass

    def display_file_statistics(self, tab, chat_file):
        """Display individual file statistics."""
        self.clear_tab(tab)  # Ensure the tab is clean before populating

        # List of message types to cycle through
        cycle_list = ["file", "sticker", "audio", "video", "image", "edit", "link", "deleted", "video_call", "voice_call", "text_message", "message"]

        for item in cycle_list:
            # Create a labeled frame for each message type
            frame = ttk.LabelFrame(tab, text=f"{chat_file.name} - {item.capitalize()} Statistics", style="TLabelframe")
            frame.pack(pady=50, padx=50, anchor="center")

            # Dictionary to hold message counts by person for the current message type
            message_dictionary = {
                person.name: int(getattr(person, f"{item}_count", 0) or 0)  # Default to 0 if attribute doesn't exist
                for person in chat_file.participant_objects
            }

            # Display the total number of messages for the current type
            total_count = sum(message_dictionary.values())
            displayed_stats = f"Total number of {item} messages: {total_count}\n"
            displayed_stats += "\n".join(
                f"{item.capitalize()} messages from {person.name}: {message_dictionary[person.name]}"
                for person in chat_file.participant_objects
            )

            # Label for the displayed stats
            label = ttk.Label(frame, text=displayed_stats, style="TLabel", padding=(10, 10))
            label.pack()

            # Generate a pie chart for the current message type if data exists
            if total_count > 0:
                fig, ax = plt.subplots(figsize=(5, 5))
                ax.pie(
                    message_dictionary.values(),
                    labels=message_dictionary.keys(), 
                    autopct='%1.1f%%',
                    colors=["#66b3ff", "#ff9999", "#99ff99", "#ffcc99", "#ff6666"],
                    startangle=140
                )
                ax.set_title(f"{chat_file.name}'s {item.capitalize()} Breakdown", color="#ffffff", fontsize=12)
                canvas = FigureCanvasTkAgg(fig, master=frame)
                canvas.get_tk_widget().pack(pady=20)
            else:
                no_data_label = ttk.Label(frame, text="No data to display for this category.", style="TLabel", padding=(10, 10))
                no_data_label.pack()

    pass



if __name__ == "__main__":
    root = tk.Tk()
    chat_files = object_Chatfile_list  # Use the list of Chatfile objects
    app = ChatAnalysisGUI(root, chat_files)
    root.mainloop()



#known bugs:
# too long names
# two files for one person
# group and solo chat diffrence
# minimal percentag points 

"""TO DO LIST:

    exclude names
    Sentiment Analyses
    emotions detection?
    Time of Day patters
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
    
    
    
    
    
    
    
    
    
    
    
    
    """
