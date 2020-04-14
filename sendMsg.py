from signalwire.rest import Client as signalwire_client
import var
from random import randint
from time import sleep
from threading import Thread

# def send():
#     client = signalwire_client(var.projectId, var.apiToken, signalwire_space_url = var.signalwire_space_url)

#     message = client.messages.create(
#                               from_='+14195586216',
#                               body='Hello World!',
#                               to='+13177213016'
#                           )

#     print(message.sid)

class sendMsg():
    def __init__(self):
        self.client = signalwire_client(var.projectId, var.apiToken, signalwire_space_url = var.signalwire_space_url)
    
    def send(self, fromNO, body, toNO):
        # fromNO = fromNO.replace(" ","").replace("-","").replace("(","").replace(")","")
        # toNO = toNO.replace(" ","").replace("-","").replace("(","").replace(")","")
        # while True:
        #     if " " in fromNO or " " in toNO:
        #         fromNO = fromNO.replace(" ","")
        #         toNO = toNO.replace(" ","")
        #         toNO = toNO.replace("\xa","")
        #     else:
        #         break
        fromNO = "+"+fromNO
        toNO = "+"+toNO
        print(fromNO, toNO, body)
        message = self.client.messages.create(
                              from_=fromNO,
                              body=body,
                              to=toNO
                          )
        # print(message)
        print(message.sid)

def main(data, timeDuration, messageLimit):
    print(data, timeDuration, messageLimit)
    sender = list()
    reciever = list()
    body = list()
    for count in range(len(data)):
        if data[count][0] != "":
            sender.append(data[count][0])
        if data[count][1] != "":
            reciever.append(data[count][1])
        if data[count][2] != "":
            body.append(data[count][2])

    senderLen = len(sender)
    recieverLen = len(reciever)
    bodyLen = len(body)
    send = sendMsg()
    for count in range(len(reciever)):
        try:
            senderIndex = randint(0,senderLen-1)
            senderT = sender[senderIndex]
            recieverIndex = randint(0, bodyLen-1)
            bodyT = body[recieverIndex]
            # send.send(senderT, bodyT, reciever[count])
            Thread(target=send.send, daemon=True, args=[senderT, bodyT, reciever[count], ]).start()
            var.statusQ.put("Send - "+ senderT + " Reciever - "+ reciever[count])
            sleep((timeDuration*60)/messageLimit)
            if var.pauseStatus == True:
                var.statusQ.put("Paused...")
                while var.pauseStatus != False:
                    sleep(1)
        except Exception as e:
            print(e)
            print(senderT, bodyT)
            print(senderIndex, recieverIndex)
    var.runStatus = False
    var.statusQ.put("Finished")
