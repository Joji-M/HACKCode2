from connections import connect_mqtt, connect_internet
from time import sleep
import oled_display

latest_message = ""
def cb(topic,msg):
    global latest_message
    if topic == b"text":
        print(msg.decode())
        latest_message = msg.decode()
        #oled.fill(0)
        #oled.text(msg.decode(),0,0)
        #oled.show()


def main():
    try:
    
        connect_internet("HAcK-Project-WiFi-2",password="UCLA.HAcK.2024.Summer") #ssid (wifi name), pass
        client = connect_mqtt("e692cf2605a24a2d9646410d037217e7.s1.eu.hivemq.cloud", "Joji1", "Bobbuilder1") # url, user, pass
        
        
        client.set_callback(cb)
        client.subscribe("text")
        #client.check_msg()
            #sleep(0.1)
            #temp, hum = humAndTemp()   # ➋  tuple unpacking
            #temp = temp if temp is not None else -1
            #hum  = hum  if hum  is not None else -1
        
        
        while True:
            client.check_msg()
            oled_display.clear_display2()
            
            
            
            
            temp, hum = oled_display.humAndTemp()   # ➋  tuple unpacking
            temp = temp if temp is not None else -1
            hum  = hum  if hum  is not None else -1
            
            lumenV =  oled_display.lumens()
            ultraV = oled_display.ultra()
            '''
            oled_display.display_text2("lumens: " + lumenV, 0, 0)
            oled_display.display_text2("cm: " + ultraV, 0, 10)
            oled_display.display_text2("Hum:" + str(hum), 0,20)
            oled_display.display_text2("Temp:" + str(temp), 0,30)
            '''
            oled_display.wrap_and_display(latest_message)
            oled_display.show_display2()
   
            #print("test")
                
            
          
            
            #hard code thse values to test
            #experimental code, must be output as string
            #client.publish("response", "testing")
            
            client.publish("light",str(lumenV))
            client.publish("humidity", str(hum) )
            client.publish("ultrasonic", str(ultraV))
            client.publish("temp", str(temp))
            sleep(.5)
            '''
            client.publish("light","test light")
            client.publish("humdidity", "test hum" )
            client.publish("ultrasonic", "testUltra")
            client.publish("temp", "test temp")
            '''
            
            
            

            

    except KeyboardInterrupt:
        print('keyboard interrupt')
        
        
if __name__ == "__main__":
    main()