import requests


raspberryIPLocation = "http://localhost:5000/cmd/"
for i in range(0,1000):
    response = requests.get(raspberryIPLocation + "{\"c\":4"+str(i)+"}",timeout=5) 
    print("Sent message and got response:" + str(response) )
