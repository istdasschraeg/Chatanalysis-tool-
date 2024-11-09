import re

# Global variables
timestamp_pattern = r"\[\d{2}\.\d{2}\.\d{2}, \d{2}:\d{2}:\d{2}\]"
enable_interface = False
file_name = "DummeLeuteDieSchachSpielen.txt"
excluded_names = ["\u200eYou", "DummeLeuteDieSchachSpiele","Ur Mum", "Maxim Helmer","Gott Der Fucking Welt"]
user_name="Maxim"
file_list=[]

if enable_interface:
    print("What file should be opend")
    file_name= input()
    print("If it is a groupchat what name does it have?")
    excluded_names.append(input())
    print("What is Ur name")



 


# Names of people participating in the chat
participant_names = []

#TO DO ADD INPUT FOR THIS ALSO ADD YOU TO ONE USER

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
                self.chat_lines[t] = self.chat_lines[t].replace("Ã¼", "ue").replace("â€Ž", "")  # Clean encoding artifacts
    
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
                print(f"{person.name} has sent {person.message_count} messages, accounting for {round(person.message_percentage * 100,2)}% of all messages.")
                print(f"{person.name} has sent {person.text_message_count} textmessages, accounting for {round(person.text_message_percentage * 100,2)}% of all textmessages.")
                print(f"{person.name} has written {person.word_count} words, accounting for {round(person.word_percentage * 100,2)}% of all words.")
                print(f"{person.name} has sent {person.file_count} files, accounting for {round(person.file_percentage * 100,2)}% of all files.")
                print(f"{person.name} has sent {person.link_count} links, accounting for {round(person.link_percentage * 100,2)}% of all links.")
                print(f"{person.name} has sent {person.sticker_count} stickers, accounting for {round(person.sticker_percentage * 100,2)}% of all stickers.")
                print(f"{person.name} has sent {person.audio_count} audios, accounting for {round(person.audio_percentage * 100,2)}% of all audios.")
                print(f"{person.name} has sent {person.video_count} videos, accounting for {round(person.video_percentage * 100,2)}% of all videos.")
                print(f"{person.name} has sent {person.image_count} images, accounting for {round(person.image_percentage * 100,2)}% of all images.")
                print(f"{person.name} has edited {person.edit_count} messages, accounting for {round(person.edit_percentage * 100,2)}% of all edits.")
                print(f"{person.name} has deleted {person.deleted_count} messages, accounting for {round(person.deleted_percentage * 100,2)}% of all deleted messages.")
                print(f"{person.name} has made {person.video_call_count} video calls, accounting for {round(person.video_call_percentage * 100,2)}% of all video calls.")
                print(f"{person.name} has made {person.voice_call_count} voice calls, accounting for {round(person.voice_call_percentage * 100,2)}% of all voice calls.")
                print(f"{person.name} writes an aveage of {round(person.words_per_message,2)} words per message")


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
        """Prints the name of the Person."""
        print(f"This Person's name is {self.name}.")

    def calculate_message_percentage(self, message_count_total):
        """Calculates and updates the percentage of total messages sent by this person."""
        self.message_percentage = self.message_count / message_count_total if message_count_total > 0 else 0

    def calculate_text_message_percentage(self, text_message_count_total):
        """Calculates and updates the percentage of total messages sent by this person."""
        self.text_message_percentage = self.text_message_count / text_message_count_total if text_message_count_total > 0 else 0

    def calculate_word_percentage(self, total_words):
        """Calculates and updates the percentage of total words written by this person."""
        self.word_percentage = self.word_count / total_words if total_words > 0 else 0

    def calculate_file_percentage(self, total_files):
        """Calculates and updates the percentage of total files sent by this person."""
        self.file_percentage = self.file_count / total_files if total_files > 0 else 0

    def calculate_sticker_percentage(self, total_stickers):
        """Calculates and updates the percentage of total stickers sent by this person."""
        self.sticker_percentage = self.sticker_count / total_stickers if total_stickers > 0 else 0

    def calculate_audio_percentage(self, total_audios):
        """Calculates and updates the percentage of total audios sent by this person."""
        self.audio_percentage = self.audio_count / total_audios if total_audios > 0 else 0

    def calculate_video_percentage(self, total_videos):
        """Calculates and updates the percentage of total videos sent by this person."""
        self.video_percentage = self.video_count / total_videos if total_videos > 0 else 0

    def calculate_image_percentage(self, total_images):
        """Calculates and updates the percentage of total images sent by this person."""
        self.image_percentage = self.image_count / total_images if total_images > 0 else 0

    def calculate_edit_percentage(self, total_edits):
        """Calculates and updates the percentage of total edits by this person."""
        self.edit_percentage = self.edit_count / total_edits if total_edits > 0 else 0

    def calculate_deleted_percentage(self, total_deleted):
        """Calculates and updates the percentage of total deleted messages by this person."""
        self.deleted_percentage = self.deleted_count / total_deleted if total_deleted > 0 else 0

    def calculate_video_call_percentage(self, total_video_calls):
        """Calculates and updates the percentage of total video calls by this person."""
        self.video_call_percentage = self.video_call_count / total_video_calls if total_video_calls > 0 else 0

    def calculate_voice_call_percentage(self, total_voice_calls):
        """Calculates and updates the percentage of total voice calls by this person."""
        self.voice_call_percentage = self.voice_call_count / total_voice_calls if total_voice_calls > 0 else 0

    def calculate_links_percentage(self, total_links):
        """Calculates and updates the percentage of total voice calls by this person."""
        self.link_percentage = self.link_count / total_links if total_links > 0 else 0
    
    def calculate_words_per_message(self):
         self.words_per_message= self.word_count/self.message_count if self.message_count > 0 else 0


# Final output of total message and word statistic
#print("Total message count:", message_count_total)
#print("Total word count:", len(new_total_text_content.split()))
#print("Average words per message:", len(new_total_text_content.split()) / message_count_total)




f1= Chatfile(file_name)
