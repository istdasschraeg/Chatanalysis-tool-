for i in content:
    
    letter= 21
    print ("special super number pls go up:",i[21:letter].count(":"))
    while variable >=0:
        
        print ("special super number pls go up:",i[21:letter].count("]"))
        if i[21:letter].count("]")==1:
            variable= variable-1
            print ("Special super nice :",i)
        else:
            letter = letter +1

            for i in content:
    
    variable =0
    
    

    while variable== 0:
        letter= 22
        
        if   i[21:letter].count(":")>0:
            print ("special super number pls go up:",i[21:letter].count(":"))
            my_objects[0]=i[21:letter-1]
            print( i[21:letter-1])
            number_of_people= number_of_people+1
            print (*my_objects)
            variable = variable+1
            print ("this is the variable", variable )
        else: 
            letter = letter +1
            
            print("works??",print(i))



            for x in Names_of_people:


    for i in content:
        
        if i[0:1] == "[":
            i=i.replace(x, "(Person)")
            i=i.replace("Ã¼","ue")
            i=i.replace("â€Ž","") 

            if i[21:29] == x:
                time =i[12:19]

                if i[21:29] != previousname:

                    diffrencehours=inttimehours[t]-inttimehours[t-1]
                    #print(diffrencehours) 
                    diffrenceminutes=inttimeminutes[t]-inttimeminutes[t-1]
                    #print(diffrenceminutes) 
                    diffrenceseconds=inttimeseconds[t]-inttimeseconds[t-1]
                    #print(diffrenceseconds) 
                    diffrencedays= inttimedays[t]-inttimedays[t-1]
                    #print(diffrencedays) 
                    diffrencemonths=inttimemonths[t]-inttimemonths[t-1]
                    #print(diffrencemonths) 
                    diffrenceyears=inttimeyears[t]-inttimeyears[t-1]
                    #print(diffrenceyears) 

                    zwischenseconds= float(diffrencehours*3600) + float(diffrenceminutes*60) +float(diffrenceseconds) +float(diffrencedays*86400) +float(diffrencemonths*24*3600*30)+float(diffrenceyears*31536000)
                    #print("sekunden zwischen Nachrichten: "+str(zwischenseconds))
                    totalseconds=totalseconds+zwischenseconds
                previousname= i[21:29]



                for x in Names_of_people:
    for i in content:
        
        if i[0:1] == "[":
            i=i.replace(x, "(Person)")
            i=i.replace("Ã¼","ue")
            i=i.replace("â€Ž","") 

            if i[21:29] == x:
                time =i[12:19]
        #print("time_send:"+time)
        date= i[2:10] 
        #print("date sent:"+ date )

        timehours=int(i[11:13])
        #print ("hours:"+str(timehours))
        #print ("t:"+str(t))
        inttimehours.append(timehours)
        #print (inttimehours)
        #print (inttimehours[t]) 

        timeminutes=i[14:16]
        #print ("minutes:"+timeminutes)
        inttimeminutes.append( int (timeminutes))
        #print (inttimeminutes)

        timeseconds=i[17:19]
        #print ("seconds:"+timeseconds)
        inttimeseconds.append( int (timeseconds))
        #print (inttimeseconds)

        timedays= int(i[1:3])
        inttimedays.append(timedays)
        #print("days:",timedays)

        timemonths= int(i[4:6])
        inttimemonths.append(timemonths)
        #print("months:", timemonths)

        timeyears= int(i[7:9])
        inttimeyears.append(timeyears)

        if i[21:29] != previousname:

            diffrencehours=inttimehours[t]-inttimehours[t-1]
            #print(diffrencehours) 
            diffrenceminutes=inttimeminutes[t]-inttimeminutes[t-1]
            #print(diffrenceminutes) 
            diffrenceseconds=inttimeseconds[t]-inttimeseconds[t-1]
            #print(diffrenceseconds) 
            diffrencedays= inttimedays[t]-inttimedays[t-1]
            #print(diffrencedays) 
            diffrencemonths=inttimemonths[t]-inttimemonths[t-1]
            #print(diffrencemonths) 
            diffrenceyears=inttimeyears[t]-inttimeyears[t-1]
            #print(diffrenceyears) 

            zwischenseconds= float(diffrencehours*3600) + float(diffrenceminutes*60) +float(diffrenceseconds) +float(diffrencedays*86400) +float(diffrencemonths*24*3600*30)+float(diffrenceyears*31536000)
            #print("sekunden zwischen Nachrichten: "+str(zwischenseconds))
            totalseconds=totalseconds+zwischenseconds
        previousname= i[21:29]