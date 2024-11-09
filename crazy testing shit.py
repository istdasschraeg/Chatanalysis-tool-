#print("hello world")
import re
enable_interface= False
if True==False:
    print("what file do u want to open?")
    file_name= input()
file_name = "Lena.txt"
file = open (file_name,"r",encoding="utf8")
content=file.readlines ()
inttimehours =[]
inttimeminutes =[]
inttimeseconds =[]
inttimedays=[]
inttimemonths=[]
inttimeyears=[]
distance_to_next_message =0
length = len(content)
previousname ="(Person)"
totalseconds=0

Name1 = "Lena S"
Name2 = "Maxim"
Names_of_people = []

for i in content:
    
    #print("stelle:", i[21:35] )
    colon_position = i[21:35].find(":")
    #print (colon_position)

    if colon_position != -1:
        
        colon_position += 21
        
        #print("Position:",colon_position)
        substring = i[21:colon_position]
        substring= substring.strip()
        #print("Name:",substring)
        #print(i)


        new_name=True
        
        for x in Names_of_people:
            
            if x==substring:
                new_name=False
                #print("lol")

        if new_name==True:
            Names_of_people.append(substring)
            new_name=False


print (Names_of_people)
        

class Person:
    def __init__(self, name,gender):
        self.name = name
        self.gender =gender

        #for monthly/weekley stats
        self.inttimehours =[]
        self.inttimeminutes =[]
        self.inttimeseconds =[]
        self.inttimedays=[]
        self.inttimemonths=[]
        self.inttimeyears=[]
        self.count_document=0
        self.count_pictures=0
        self.count_sticker=0
        self.count_audio=0
        self.count_video=0
        self.count_word=0
        self.count_messages=0
        self.content=[]
        self.word_percent=0
        self.messages_percent=0
        self.content_astext= ""
        


        self.pretty_print_name()
    def pretty_print_name(self):
        print("This Persons name is {}.".format(self.name))

my_list = []
number_of_people =0
for i in Names_of_people:

    print ("What gender is ",i,"?(male, female, other)")
    #gender= input()
    gender ="other"
    my_list.append (Person(i,gender) )
    number_of_people+=1

#print (*my_list)
#print(str(1)+'data')

t=0
i =0  
for x in Names_of_people:
    for i in content:
        
        if i[0:1] == "[":
            i=i.replace(x, "(Person)")
            i=i.replace("Ã¼","ue")
            i=i.replace("â€Ž","") 
            #i=i.replace("[U+200E]","") 

            if i[21:29] == x:
                time =i[12:19]
                #print("time_send:"+time)
                date= i[2:10] 
                #print("date sent:"+ date )

                timehours=int(i[11:13])
                #print ("hours:"+str(timehours))
                #print ("t:"+str(t))
                my_list[t].inttimehours.append(timehours)
                #print (inttimehours)
                #print (inttimehours[t]) 

                timeminutes=i[14:16]
                print(timeminutes)
                print(i)
                #print ("minutes:"+timeminutes)
                my_list[t].inttimeminutes.append( int (timeminutes))
                #print (inttimeminutes)

                timeseconds=i[17:19]
                #print ("seconds:"+timeseconds)
                my_list[t].inttimeseconds.append( int (timeseconds))
                #print (inttimeseconds)

                timedays= int(i[1:3])
                my_list[t].inttimedays.append(timedays)
                #print("days:",timedays)

                timemonths= int(i[4:6])
                my_list[t].inttimemonths.append(timemonths)
                #print("months:", timemonths)

                timeyears= int(i[7:9])
                my_list[t].inttimeyears.append(timeyears)
        #print (i)

        t=t+1
        i=i.replace("(Person)",x)    

    else:
        continue
    


#print("Sekundenanzahl insgesamt: "+str(totalseconds))
#print ("Interval der Nachrichten: "+str(totalseconds/t))

t=0
astext=""

textfromperson1 =False

lol=0
lul=100
file = open (file_name,"r",encoding="utf8")
rest=[]
t=0

timestamp_pattern = r"\[\d{2}\.\d{2}\.\d{2}, \d{2}:\d{2}:\d{2}\]"
       
while t < len(content) - 1:
    content[t] = content[t].strip()
    content[t] = content[t].replace("Ã¼", "ue").replace("â€Ž", "")
    
    if not re.match(timestamp_pattern, content[t + 1]) and content[t+1].find("omitted")>=0:
        
        content[t] += " " + content[t + 1]
        print ("This was removed:",content[t+1] )
        content.pop(t + 1)          
    else:        
        t += 1
t=0

for x in Names_of_people:
    t=0
    for i in content:
        i=i.replace("\u200e", "")
        i=i.replace("Ã¼","ue").replace("â€Ž","").replace("/n","")

        place_name_found=0
        #print (i.find(x))
        #print ("length:",len(x))
        
        if i.find(Names_of_people[0]) >=0:
            place_name_found=i.find(x)+len(x)
            
            my_list[lol].content.append(i[place_name_found:])
            my_list[lol].count_messages+=1
        elif i.find(Names_of_people[1]) >=0:
            place_name_found=i.find(x)+len(x)
            
            my_list[lol].content.append(i[place_name_found:])
            my_list[lol].count_messages+=1
        else:
            rest.append(i)               
        t+=1

    print(my_list[lol].count_messages)
    lol+=1
    
for i in rest:
    print(i)
    t=t


