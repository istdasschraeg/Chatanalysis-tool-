file_name = "Lena.txt"
file = open (file_name,"r",encoding="utf8")
content=file.readlines ()
astext=""

lul=100

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




lol=0
lul=100
file = open (file_name,"r",encoding="utf8")
rest=[]


for i in content:
    for y in range(len(my_list)):
        if i.find(my_list[y].name) >=1:
            i=i.replace(my_list[y].name,"Pers."+str(y+100))
        #print(i)
        print ("Pers."+str(lul))
        print ("lol:",i)


        
    
    
    

print (*content)

