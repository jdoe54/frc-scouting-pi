
import bluetooth
import threading
import json
import requests
import sys
import re

# ***** CONFIG *****
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
data_webhook = 'http://127.0.0.1:4909/new_msg'
deviceCount = 200
# ***** CONFIG *****

sentMessagesCount = 0

## Bluetooth Worker Thread
def bluetoothWorker(idx, port, server_sock):
    global sentMessagesCount
    # Thread 
    
    print("Worker {}: Waiting for connection on RFCOMM channel {}...".format(idx, port))
    
    sys.stdout.flush()
        
    # Attempt Connection
    client_sock, client_info = server_sock.accept()
    print(" - Connected to Device {} ({})".format(idx, client_info[0]))
    sys.stdout.flush()
        
    while True:
        try:             
            # Receive data from 
            receiveDataFromTablets(idx, client_sock, client_info)
        except IOError:
            # Device has stop sending data
            print("Worker {}: Lost Connection on RFCOMM channel {}...".format(idx, port))
            print("Worker {}: Waiting for reconnection on RFCOMM channel {}...".format(idx, port))
            
            with open('Scouting/WorkingFiles/scoutingCSVFile.csv', 'a+') as fil:
                lines = fil.read()
                lines = re.sub(r'.\Z', r'',lines)
                fil.close()
            with open('Scouting/WorkingFiles/pitScoutingCSVFile.csv', 'a+') as fil:
                lines = fil.read()
                lines = re.sub(r'.\Z', r'',lines)
                fil.close()
            sys.stdout.flush()
            
            #if client_sock != None:
                #client_sock, client_info = server_sock.accept()
            break
            
    if client_sock != None:
        client_sock.close()
        server_sock.close()

#
### Recv. New Data from BT Worker Thread

def receiveDataFromTablets(idx, client_sock, client_info):
    global sentMessagesCount
    raw_data = client_sock.recv(1024).decode("utf-8")
    var = json.dumps(raw_data)
    
    #if var.replace()
    print(" - Received {} from Device {} ({})".format(raw_data, idx, client_info[0]))
    sys.stdout.flush()

     #Converts into a string
    sentMessagesCount += 1

    print(var)
    print(var[len(var)-4:])
    
    if var[len(var)-4:]== 'Pit"':
        var = var[:len(var)-4]
    
        with open('Scouting/WorkingFiles/pitScoutingCSVFile.csv', 'a+') as fil: #Opens Pit Scouting file and adds entry to csv file
            if sentMessagesCount == 1:
                fil.write("\n")
                fil.write(var.strip('"'))
                fil.close()
    elif var == '"STOPPER"': 
        with open('Scouting/WorkingFiles/scoutingCSVFile.csv', 'a+') as fil:
            fil.close()
        with open('Scouting/WorkingFiles/pitScoutingCSVFile.csv', 'a+') as fil:
            fil.close()
        sentMessagesCount = 0
        client_sock.close() 
        server_sock.close()
    else:
        
        with open('Scouting/WorkingFiles/scoutingCSVFile.csv', 'a+') as fil: #Opens file and adds entry to csv file
            if sentMessagesCount == 1:
                fil.write("\n")
            #if sentMessagesCount % 20 == 0:            
                fil.write(var.strip('"'))
                #fil.close()
            #else:
                #fil.write(var.strip('"') + ",")
                fil.close()

if __name__ == "__main__":
    print("Starting System...")
    sys.stdout.flush()

    server_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    # Advertise Serial Port Profile
    bluetooth.advertise_service( server_sock, "TGA Bluetooth Server",
                       service_id = uuid,
                       service_classes = [ uuid, bluetooth.SERIAL_PORT_CLASS ],
                       profiles = [ bluetooth.SERIAL_PORT_PROFILE ])


    print("Past Startup")
    sys.stdout.flush()

    threads = []
    for i in range(deviceCount):

        t = threading.Thread(target=bluetoothWorker, args=(i,port, server_sock,))
        threads.append(t)
        t.start()
        

    
    print("Started Threads...")
    
    
    
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
    
