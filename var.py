from queue import Queue
from collections import deque
import json

senderNoFile = "sender.csv"
recieverNoFile = "reciever.csv"
msgFile = "msg.csv"

with open('config.json') as json_file:
    data = json.load(json_file)

statusQ = Queue()

runStatus = False
pauseStatus = False

config = data['config']
projectId = config[0]['projectId']
apiToken = config[0]['apiToken']
signalwire_space_url = config[0]['signalwire_space_url']
print(projectId, apiToken, signalwire_space_url)

tableRowCount = 10

kind = ["sender", "reciever", "message"]