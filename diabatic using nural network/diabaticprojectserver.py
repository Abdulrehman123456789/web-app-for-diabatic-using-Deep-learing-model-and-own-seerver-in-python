import asyncio
import websockets
import pymysql
import base64 
from PIL import Image
import numpy as np  
import random
import requests

class img():
 def imgsave(fname,base64str):
  img=base64str.split(",")
  pic=base64.b64decode(img[1])
  f=open(fname,"wb")
  f.write(pic)
  f.close()  
 








class patient():
  def dietanddoseandvalues(tdata):
   
    sp=tdata.split("$")
    db=pymysql.connect(host="localhost",user="root",passwd="root",db="diabaticproject")
    c=db.cursor()
    c.execute("INSERT INTO patientdiet values (%s,%s,%s,%s,%s,%s,%s)",(sp[0],sp[1],sp[2],sp[4],sp[5],sp[6],sp[7]))
    c.execute("INSERT INTO patientdose values (%s,%s,%s,%s,%s)",(sp[3],sp[4],sp[5],sp[6],sp[7]))
    c.execute("INSERT INTO diabaticvalues values (%s,%s,%s,%s,%s,%s,%s)",(sp[8],sp[9],sp[10],sp[11],sp[5],sp[6],sp[7]))
    db.commit()
    db.close()
    patient.sendtopatientnumber(sp)
    print("diet and saved");
    return("1")
   





  def sendtopatientnumber(sp):
    message="DIET:"+"  protains="+sp[0]+"  carbohydrate="+sp[1]+"  fat="+sp[2]+"      MEDICINE:"+sp[3]+"      reportdate:"+sp[5]+"      givendate:"+sp[4]
    patientphoneno=sp[6]
    print(patientphoneno)

    url = "https://www.fast2sms.com/dev/bulk"
    payload = "sender_id=FSTSMS&message="+message+"&language=english&route=p&numbers="+patientphoneno
    headers = {
    'authorization': "pDtOwdf2nFcREMeAvU9GHVkYaTBSbr1PC8q3i7uQlhLWJzg4xjHc6AZNxEIFUJ0Mog7dKlV4vmP9OQYa",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    
  


  def getpatientdetails(tdata):
   print(tdata)
   ph=tdata.split("&")
   db=pymysql.connect(host="localhost",user="root",passwd="root",db="diabaticproject")
   c=db.cursor()
   c.execute("select p.name,p.phoneno,p.emails,p.typeofpatient FROM patientdetails p where p.phoneno=%s and p.dphoneno=%s",(ph[0],ph[1]))
   result=c.fetchall()
   fulldata=result[0][0]+"$"+str(result[0][1])+"$"+result[0][2]+"$"+result[0][3];
   print(fulldata)
   return(fulldata)






  



  def getpatientdietanddoseandvalues(tdata):
   print(tdata)
   ph=tdata.split("&")
   db=pymysql.connect(host="localhost",user="root",passwd="root",db="diabaticproject")
   c=db.cursor()
   c.execute("select di.protains,di.carbohydrate,di.fat,di.givendate,di.reportdate FROM patientdiet di where di.ptphoneno=%s and di.dtphoneno=%s",(ph[0],ph[1]))
   diet=c.fetchall()
   c.execute("select do.medicine FROM patientdose do where do.ptphoneno=%s and do.dtphoneno=%s",(ph[0],ph[1]))
   dose=c.fetchall()
   c.execute("select val.bfbs,val.afbs,val.bfus,val.afus FROM diabaticvalues val  where val.pphoneno=%s and val.dphoneno=%s",(ph[0],ph[1]))
   values=c.fetchall()
   fulldata="start&"
   i=0;
   for count in diet:
    fulldata=fulldata+str(diet[i][0])+"$"+str(diet[i][1])+"$"+str(diet[i][2])+"$"+str(diet[i][3])+"$"+str(diet[i][4])+"$"+str(dose[i][0])+"$"+str(values[i][0])+"$"+str(values[i][1])+"$"+str(values[i][2])+"$"+str(values[i][3])+"%"
    i=i+1;
   db.commit()
   db.close()
   print(fulldata)
   return(fulldata)


  






  def graphvalues(tdata):
   print(tdata)
   ph=tdata.split("&")
   db=pymysql.connect(host="localhost",user="root",passwd="root",db="diabaticproject")
   c=db.cursor()
   c.execute("select val.bfbs,val.afbs,val.reportdate FROM diabaticvalues val  where val.pphoneno=%s and val.dphoneno=%s",(ph[0],ph[1]))
   values=c.fetchall()
   lengthvalues=len(values)
   if lengthvalues>=5:
    fulldata="start&"
    for i in values:
     datearr=str(i[2]).split("-")
     fulldata=fulldata+str(i[0])+"$"+str(i[1])+"$"+str(datearr[0])+"$"+str(datearr[1])+"$"+str(datearr[2])+"%"
    db.commit()
    db.close()
    print(fulldata)
    return(fulldata)
   else:
    return("insuffecint diabatic values for ploting graph(alest 5 values)")
   
 


  def nuralnetwork(tdata):
   print(tdata)
   ph=tdata.split("&")
   db=pymysql.connect(host="localhost",user="root",passwd="root",db="diabaticproject")
   c=db.cursor()
   c.execute("select val.afbs FROM diabaticvalues val  where val.pphoneno=%s and val.dphoneno=%s",(ph[0],ph[1]))
   values=c.fetchall()
   c.execute("select di.protains,di.carbohydrate,di.fat FROM patientdiet di where di.ptphoneno=%s and di.dtphoneno=%s",(ph[0],ph[1]))
   diet=c.fetchall()
   lengthvalues=len(values)
   print(lengthvalues)
   lengthdiet=len(diet)
   print(lengthdiet)
   print(diet)
   print(values)
   if lengthvalues>=5 and lengthdiet>=4:
    fulldata="start&"
    valuescount=1;
    for i in range(0,lengthdiet-1):
     fulldata=fulldata+str(diet[i][0])+"$"+str(diet[i][1])+"$"+str(diet[i][2])+"$"+str(values[valuescount][0])+"%"
     valuescount=valuescount+1
    db.commit()
    db.close()
    print(fulldata)

    pridictedvalue=patient.prediction(fulldata)
    return(pridictedvalue) 
   
   else:
    return("insuffecint diabatic values and diet values for prediction(alest 5 values)")



  
  
  def prediction(fulldata):
   arr=fulldata.split("&")
   actualdata=arr[1]
   allset=actualdata.split("%")
   set1=allset[0].split("$")
   set2=allset[1].split("$")
   set3=allset[2].split("$")
   set4=allset[3].split("$")
   set1p=int(set1[0])/100
   set1c=int(set1[1])/100
   set1f=int(set1[2])/100
   set1result=int(set1[3])/500
   set2p=int(set2[0])/100
   set2c=int(set2[1])/100
   set2f=int(set2[2])/100
   set2result=int(set2[3])/500
   set3p=int(set3[0])/100
   set3c=int(set3[1])/100
   set3f=int(set3[2])/100
   set3result=int(set3[3])/500
   set4p=int(set4[0])/100
   set4c=int(set4[1])/100
   set4f=int(set4[2])/100
   set4result=int(set4[3])/500

   
   print("training nuralnetwork")

   feature_set = np.array([[set1p,set1c,set1f],[set2p,set2c,set2f],[set3p,set3c,set3f],[set4p,set4c,set4f]])  
   labels = np.array([[set1result,set2result,set3result,set4result]])  
   labels = labels.reshape(4,1)  



   np.random.seed(42)  
   weights = np.random.rand(3,1)  
   bias = np.random.rand(1)  
   lr = 0.05  


   def sigmoid(x):  
    return 1/(1+np.exp(-x))


   def sigmoid_der(x):  
    return sigmoid(x)*(1-sigmoid(x))




   for epoch in range(20000):  
    inputs = feature_set

    # feedforward step1
    XW = np.dot(feature_set, weights) + bias


    #feedforward step2
    z = sigmoid(XW)

    print(z)


    # backpropagation step 1
    error = z - labels

    print(error.sum())

    # backpropagation step 2
    dcost_dpred = error
    dpred_dz = sigmoid_der(z)

    z_delta = dcost_dpred * dpred_dz

    inputs = feature_set.T
    weights -= lr * np.dot(inputs, z_delta)

    



   for num in z_delta:
    bias -= lr * num

   
   print("warginal values")
   print(set1result)
   print(set2result)
   print(set3result)
   print(set4result)

   
   print("predicting lowest super and best diet")
  

   

   predictedsugervalue=0.4  #this assignment is for loop entry
  
   while predictedsugervalue>0.3:

    p=random.randint(1,100)/100
    c=random.randint(1,100)/100
    f=random.randint(1,100)/100
    single_point = np.array([p,c,f])  
    predictedsugervalue = sigmoid(np.dot(single_point, weights) + bias)
    predictedsugervalue=float(predictedsugervalue)
    if predictedsugervalue<0.2:
     predictedsugervalue=0.4  #this assignment is for loop entry
    print(predictedsugervalue)
   

   finalp=p*100
   finalc=c*100
   finalf=f*100
   finalpredictedsugervalue=predictedsugervalue*500

   print("best diet")
   print(finalp)
   print(finalc)
   print(finalf)   
   print("which give a super of")
   print(finalpredictedsugervalue)

   finalvalue=str(finalp)+"$"+str(finalc)+"$"+str(finalf)+"$"+str(finalpredictedsugervalue)
   return(finalvalue)








class owner():
 def doctorsignin(tdata):
  try:
   print(tdata) 
   sp=tdata.split("$")
   db=pymysql.connect(host="localhost",user="root",passwd="root",db="diabaticproject")
   c=db.cursor()
   c.execute("INSERT INTO doctordetails values (%s,%s,%s,%s,%s,%s,%s)",(sp[0],int(sp[1]),sp[2],sp[3],sp[4],sp[5],sp[6]))
   db.commit()
   db.close()
   return(1)
  except:
   return(0)
    


 def login(tdata):
  try:
   sp=tdata.split("$")
   db=pymysql.connect(host="localhost",user="root",passwd="root",db="diabaticproject")
   c=db.cursor()
   c.execute("select d.phoneno,d.password from doctordetails d where d.phoneno=%s",int(sp[0]))
   result=c.fetchall()
   print("userphoneno")
   print(result[0][0]) #don't delete is print statment
   db.commit()
   db.close()
   if result[0][1]==sp[1]:
     return(1)
   else:
     return(2)
  except:
   return(0)
     
 
 

 def savepatient(tdata):
  print(tdata) 
  try:
   sp=tdata.split("$")
   db=pymysql.connect(host="localhost",user="root",passwd="root",db="diabaticproject")
   c=db.cursor()
   c.execute("INSERT INTO patientdetails values (%s,%s,%s,%s,%s)",(sp[0],int(sp[1]),sp[2],sp[3],int(sp[4])))
   db.commit()
   db.close()
   patientdoctorphoneno=str(sp[1])+"@"+str(sp[4])
   return(patientdoctorphoneno)
  except:
   return("0")
  

 



 def getdoctordetails(tdata):
   print(tdata)
   db=pymysql.connect(host="localhost",user="root",passwd="root",db="diabaticproject")
   c=db.cursor()
   c.execute("select d.name,d.phoneno,d.emails,d.workplaceaddress,d.spicilization,d.workplace FROM doctordetails d where d.phoneno=%s",tdata)
   result=c.fetchall()
   fulldata=result[0][0]+"$"+str(result[0][1])+"$"+result[0][2]+"$"+result[0][3]+"$"+str(result[0][4])
   print(fulldata)
   return(fulldata)





 def getdoctorpatients(tdata):
   print(tdata)
   db=pymysql.connect(host="localhost",user="root",passwd="root",db="diabaticproject")
   c=db.cursor()
   c.execute("select p.name,p.phoneno,p.emails,p.typeofpatient FROM patientdetails p where p.dphoneno=%s",tdata)
   result=c.fetchall()
   fulldata="start&"
   for row in result:
    fulldata=fulldata+row[0]+"$"+str(row[1])+"$"+row[2]+"$"+row[3]+"%"

   return(fulldata)
   db.commit()
   db.close()




 
 def verifyphoneno(tdata):
   doctorphone=tdata
   otp=random.randint(1001,9999)
   otp=str(otp)
   otpmsg="DIABATICCARE OPT:"+str(otp)
   url = "https://www.fast2sms.com/dev/bulk"
   payload = "sender_id=FSTSMS&message="+otpmsg+"&language=english&route=p&numbers="+doctorphone
   headers = {
   'authorization': "pDtOwdf2nFcREMeAvU9GHVkYaTBSbr1PC8q3i7uQlhLWJzg4xjHc6AZNxEIFUJ0Mog7dKlV4vmP9OQYa",
   'Content-Type': "application/x-www-form-urlencoded",
   'Cache-Control': "no-cache",
   }
   response = requests.request("POST", url, data=payload, headers=headers)
   responsemessage=response.text
   print(responsemessage)
   arr1=responsemessage.split("message")
   arr2=arr1[1].split('"')
   message=arr2[2]
   if message=="Message sent successfully to NonDND numbers":
    return("0"+"$"+otp)
   elif message=="Mobile Number in DND, Check delivery reports from panel":
    return("1"+"$"+"NO OPT")
   elif message=="Invalid Numbers":
    return("2"+"$"+"NO OPT")
   elif message=="SMS scheduled successfully to NonDND numbers at 9AM (in morning)":
    return("3"+"$"+"NO OPT")
   else:
    return("4"+"$"+"NO OPT")









async def time(websocket, path):
 print(websocket)
 data= await websocket.recv()
 tdata=data.split('%')



 if tdata[0]=="1":
  r=owner.doctorsignin(tdata[1])
  if r==1:
   await websocket.send("1")
   base64str = await websocket.recv()
   arr=tdata[1].split("$")
   ownerph=arr[1]
   imgname="doctorprofile"+ownerph+".jpg"
   img.imgsave(imgname,base64str)
   print("docter profile details saved")
  else:
   await websocket.send("0") 
   print("unable to save the docter profile")    
   



 if tdata[0]=="2":
   patientdoctorphoneno=owner.savepatient(tdata[1])
   if patientdoctorphoneno=="0":
   	print("patient not saved patient already present")
   	await websocket.send("patient already present")
   else:	
    base64str = await websocket.recv()
    imgname="patientprofile"+patientdoctorphoneno+".jpg"
    img.imgsave(imgname,base64str)
    print("patient saved")
    await websocket.send("patient saved")



   


 

 
 if tdata[0]=="5":
   data=owner.getdoctordetails(tdata[1])
   print(data)
   #filename="profile"+"90"+".jpg"
   filename="doctorprofile"+tdata[1]+".jpg"
   print(tdata[1])

   with open(filename, "rb") as image_file:
      baseimg=base64.b64encode(image_file.read())


   baseimg=str(baseimg)
   arrf=baseimg.split("'")
   finalpic="data:image/jpg;base64,"+arrf[1]
   finaldata=data+"&"+finalpic
   await websocket.send(finaldata)







   data=owner.getdoctorpatients(tdata[1])
   print(data)
   await websocket.send(data)
   

   
   arr=data.split("&")
   actualdata=arr[1]
   data1=actualdata.split("%")
   print(data1)
   l=len(data1)
   
   for i in range(l-1):
    data2=data1[i].split("$")
    #filename="camera"+"90"+".jpg"
    filename="patientprofile"+data2[1]+"@"+tdata[1]+".jpg"
    print(tdata[1])#doctorphone
    print(data2[1])#patientphone

    with open(filename, "rb") as image_file:
       baseimg=base64.b64encode(image_file.read())


    baseimg=str(baseimg)
    arrf=baseimg.split("'")
    finalpic="data:image/jpg;base64,"+arrf[1]
   
    await websocket.send(finalpic)  
   await websocket.send("ok") 
   print("sucess")
   
  





 
   
 
 if tdata[0]=="6":
   data=owner.login(tdata[1])
   sdata=str(data)
   print(sdata)
   await websocket.send(sdata) 





 if tdata[0]=="7":
   data=owner.verifyphoneno(tdata[1])
   print("otpsend")
   print(data)
   await websocket.send(data)  












 if tdata[0]=="11":
   result=patient.dietanddoseandvalues(tdata[1])
   await websocket.send(result) 
   
   



 if tdata[0]=="12":
   patientdoctorph=tdata[1].split("&")
   data=patient.getpatientdetails(tdata[1])
   print(data)
   #filename="profile"+"90"+".jpg"
   filename="patientprofile"+patientdoctorph[0]+"@"+patientdoctorph[1]+".jpg"
   print(tdata[1])

   with open(filename, "rb") as image_file:
      baseimg=base64.b64encode(image_file.read())


   baseimg=str(baseimg)
   arrf=baseimg.split("'")
   finalpic="data:image/jpg;base64,"+arrf[1]
   finaldata=data+"&"+finalpic
   await websocket.send(finaldata)


  




   data=patient.getpatientdietanddoseandvalues(tdata[1])
   print(data)
   await websocket.send(data)
   await websocket.send("ok") 
   print("sucess")
   











 if tdata[0]=="13":
   data=patient.graphvalues(tdata[1])
   print(data)
   await websocket.send(data)
   print("graphsend")



 



 if tdata[0]=="14":
   data=patient.nuralnetwork(tdata[1])
   print(data)
   await websocket.send(data)
   print("predictionsend")
















     
print("server is online")
start_server = websockets.serve(time, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

