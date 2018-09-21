from simple_salesforce import Salesforce

import os
import glob
import time
import RPi.GPIO as GPIO  
import time  



os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

sf = Salesforce(username='ender.cui@hotmail.com', password='ender123', security_token='dPLoBHTvrNUHY14zcWsfjVzN')
print(sf);


def getTemp():
    channel = 16  
    data = [] 
    j = 0        
      
    GPIO.setmode(GPIO.BCM) 
      
    time.sleep(1)        
      
    GPIO.setup(channel, GPIO.OUT)  
      
    GPIO.output(channel, GPIO.LOW)  
    time.sleep(0.02)  
    GPIO.output(channel, GPIO.HIGH)  
      
    GPIO.setup(channel, GPIO.IN)  
      
    while GPIO.input(channel) == GPIO.LOW:  
        continue  
      
    while GPIO.input(channel) == GPIO.HIGH:  
        continue  
      
    while j < 40:  
        k = 0  
        while GPIO.input(channel) == GPIO.LOW:  
            continue  
          
        while GPIO.input(channel) == GPIO.HIGH:  
            k += 1  
            if k > 100:  
                break  
          
        if k < 8:  
            data.append(0)  
        else:  
            data.append(1)  
      
        j += 1  
      
    #print "Temperature Sensor is working....."  
    #print data
    
    humidity_bit = data[0:8]
    humidity_point_bit = data[8:16]  
    temperature_bit = data[16:24]  
    temperature_point_bit = data[24:32]  
    check_bit = data[32:40]  
      
    humidity = 0  
    humidity_point = 0  
    temperature = 0  
    temperature_point = 0  
    check = 0  
      
    for i in range(8):  
        humidity += humidity_bit[i] * 2 ** (7 - i)               
        humidity_point += humidity_point_bit[i] * 2 ** (7 - i)  
        temperature += temperature_bit[i] * 2 ** (7 - i)  
        temperature_point += temperature_point_bit[i] * 2 ** (7 - i)  
        check += check_bit[i] * 2 ** (7 - i)  
      
    tmp = humidity + humidity_point + temperature + temperature_point     
      
    if check != tmp:                                                             
        temperature = -273
        #print "temperature : ", temperature, ", humidity : " , humidity, " check : ", check, " tmp : ", tmp  


    GPIO.cleanup()                               
    return temperature


while True:
    print "==============================="
    print "Get Temperature"
    temp = getTemp()
    
    if temp > -273:
        data = [{'serial_no__c': '1001','door_open__c': 'false','temperature__c':temp}]
        sf.bulk.Flying_Fridge_Event__e.insert(data)
        print "Send to Salesforce @", time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print "Temperature is: ", temp
        time.sleep(5)
    else:
        print "Sensor is not working. Try again...."
        time.sleep(1)
	