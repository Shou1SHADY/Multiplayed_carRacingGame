import random
from time import sleep
import socket
import pygame
import atexit
import json
import select
import asyncio
import websockets
import websocket
import sys
import os
import random


class CarRacing:
    def __init__(self):

        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None
        self.clientId=0
        self.y_counter=0
        self.initialize()
                # Create a socket object
        
        #self.client_socket.bind(('localhost', 3030))
        # Define the server address and port
        server_address = ('localhost', 8888)
        file_path = "uuid.txt"
        if os.path.exists(file_path):
    # File exists, read random number from it
            with open(file_path, "r") as file:
                random_number = int(file.read())
        else:
    # File does not exist, generate new random number
            random_number = random.randint(1, 1000000)
    
    # Store random number in the file
            with open(file_path, "w") as file:
                file.write(str(random_number))

        print("Random number:", random_number)
        header = {
            'user-agent': 'Mozilla',
        "uid": str(random_number)
        
}

# Convert the header dictionary to a list of tuples
        header_items = header.items()
        headers = {
            'user-agent': 'Mozilla',

        }
        self.ws = websocket.WebSocket(header=headers)
        self.ws.connect('ws://holly-thundering-limit.glitch.me/', header=header)
        # Connect to the server


        message2 = 'run'
        self.ws.send('run')
        #asyncio.run(self.async_main())
        ####data = self.client_socket.recv(1024)
        ####int_decoded_data=int(data.decode())
        #####print(int_decoded_data)
        # Convert the received data to coordinates
        #coordinates = json.loads(data)
        #print("x value",coordinates['x'])

        atexit.register(self.disconnect_socket)
        
    async def async_main(self):
        loop = asyncio.get_running_loop()
        await asyncio.gather(self.receive_messages(), loop.run_in_executor(None, blocking_function))
    async def receive_messages():
        uri = "ws://localhost:8888"  # Replace with the WebSocket server URI
        async with websockets.connect(uri) as websocket:
         while True:
            message = await websocket.recv()
            print("Received message:", message)
    def disconnect_socket(self):
        print("Disconnecting from the socket...")
        self.ws.close()
    def initialize(self):

        self.crashed = False

        self.carImg = pygame.image.load('.\\img\\car.png')
        self.car_x_coordinate = (self.display_width * 0.45)
        self.car_y_coordinate = (self.display_height * 0.8)
        self.car_width = 49

        # enemy_car
        self.enemy_car_1 = pygame.image.load('.\\img\\enemy_car_1.png')
        self.enemy_car_1_startx = 0#random.randrange(310, 450)
        self.enemy_car_1_starty = 0#-600
        self.enemy_car_1_y_counter = 0
        self.enemy_car_1_speed = 5
        self.enemy_car_1_width = 49
        self.enemy_car_1_height = 100
        self.enemy_car_1_state='run'

        self.enemy_car_2 = pygame.image.load('.\\img\\enemy_car_2.png')
        self.enemy_car_2_startx = 0
        self.enemy_car_2_starty = 0
        self.enemy_car_2_y_counter = 0
        self.enemy_car_2_speed = 5
        self.enemy_car_2_width = 49
        self.enemy_car_2_height = 100
        self.enemy_car_2_state='run'

        # Background
        self.bgImg = pygame.image.load(".\\img\\back_ground.jpg")
        self.bg_x1 = (self.display_width / 2) - (360 / 2)
        self.bg_x2 = (self.display_width / 2) - (360 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3
        self.count = 0
        self.lives=3

    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, car_y_coordinate))

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Car Dodge')
        #self.run_car()

    def run_car(self):
        move_up=False
        move_down=False
        state_json = json.dumps({})
        json_data_3={}
        location_change_flag=False
        enemy_1_change_y=False
        enemy_2_change_y=False
        x=True
        print("hadkhol while x")
        while x:
            if self.ws.recv():
                data = self.ws.recv()
                print('Received:', data)
                if data=="reufsed conection":
                    print ("reufsed conection")
                    self.disconnect_socket()
                    pygame.quit()
                    break
                json_data = json.loads(data)
                print(json_data)
                if (json_data['type']=="run"):
                    self.clientId=json_data['client']
                    self.car_x_coordinate=json_data['x']
                    self.car_y_coordinate=json_data['y']
                    x=False
        print("out of the while x")
        
        # readable, writable, exceptional = select.select([self.client_socket], [], [], 0)
        # if self.client_socket in readable:
        data = self.ws.recv()
        json_data = json.loads(data)
        print("json_data",json_data)
        enemy_1_flag=0
        for i in range(1,4):
            if (i != self.clientId) and enemy_1_flag==0:
                enemy_1_flag=1
                self.enemy_car_1_startx=json_data[i-1]["x"]
                self.enemy_car_1_starty=json_data[i-1]["y"]
            if i != self.clientId and enemy_1_flag==1:
                self.enemy_car_2_startx=json_data[i-1]["x"]
                self.enemy_car_2_starty=json_data[i-1]["y"]
        # if self.clientId==1:
        #     print("json_data",json_data)
        #     print("json_data[1][x]",json_data[1]["x"])
        #     #if json_data[1]["type"]=="crash":
        #     self.enemy_car_1_startx=json_data[1]["x"]
        #     self.enemy_car_1_starty=json_data[1]["y"]
        #     self.enemy_car_2_startx=json_data[2]["x"]
        #     self.enemy_car_2_starty=json_data[2]["y"]
        # elif self.clientId==2:
        #     print("json_data[1]",json_data[1])
        #     self.enemy_car_1_startx=json_data[0]["x"]
        #     self.enemy_car_1_starty=json_data[0]["y"]
        #     self.enemy_car_2_startx=json_data[2]["x"]
        #     self.enemy_car_2_starty=json_data[2]["y"]
        # elif self.clientId==3:
        #     print("json_data[2]",json_data[2])
        #     self.enemy_car_1_startx=json_data[0]["x"]
        #     self.enemy_car_1_starty=json_data[0]["y"]
        #     self.enemy_car_2_startx=json_data[1]["x"]
        #     self.enemy_car_2_starty=json_data[1]["y"]
        self.racing_window()
        while not self.crashed:
            if self.count==5000:
                print("self.y_counter",self.y_counter)
                print("self.enemy_car_1_y_counter",self.enemy_car_1_y_counter)
                print("self.enemy_car_2_y_counter",self.enemy_car_2_y_counter)
                if self.enemy_car_1_state=='crash' and self.enemy_car_2_state=='crash':
                    self.display_message_only("WINNER WOHOOOO")
                elif self.enemy_car_1_state=='crash' and self.enemy_car_2_state!='crash'and self.y_counter<self.enemy_car_2_y_counter:
                    self.display_message_only("WINNER WOHOOOO")
                elif self.enemy_car_1_state!='crash' and self.enemy_car_2_state=='crash'and self.y_counter<self.enemy_car_1_y_counter:
                    self.display_message_only("WINNER WOHOOOO")
                elif self.y_counter<self.enemy_car_1_y_counter and self.y_counter<self.enemy_car_2_y_counter:
                    self.display_message_only("WINNER WOHOOOO")
                else:
                    self.display_message_only("LOSER *_*")
                self.disconnect_socket()
                pygame.quit()
                break
            location_change_flag=False

            enemy_1_change_y=False
            enemy_2_change_y=False
            r, w, e = select.select([self.ws.sock], [], [], 0)
            if self.ws.sock in r:
                print ("mestanni a receive fe line 151")
                data = self.ws.recv()
                print('Received in line 139:', data)
                json_data_2 = json.loads(data)
                if json_data_2["type"]== "ping":
                    pong_json={"type":"pong"}
                    pong_json_send = json.dumps(pong_json)
                    self.ws.send(pong_json_send)  
                else:
                    if self.clientId==1:
                        if json_data_2["type"]=="run":
                            if json_data_2["client"]==2:
                                #ekhteber el y counter hena
                                y_counter_difference=(self.y_counter-json_data_2["y_counter"])
                                if self.enemy_car_1_y_counter!=json_data_2["y_counter"]:
                                    enemy_1_change_y=True
                                self.enemy_car_1_y_counter=json_data_2["y_counter"]
                                if y_counter_difference> -100 and y_counter_difference<380:
                                    self.enemy_car_1_startx=json_data_2["x"]
                                    self.enemy_car_1_starty=self.car_y_coordinate- y_counter_difference # hanghayar hena
                            elif json_data_2["client"]==3:
                                y_counter_difference=(self.y_counter-json_data_2["y_counter"])
                                if self.enemy_car_1_y_counter!=json_data_2["y_counter"]:
                                    enemy_2_change_y=True
                                self.enemy_car_2_y_counter=json_data_2["y_counter"]
                                if y_counter_difference> -100 and y_counter_difference<380:
                                    self.enemy_car_2_startx=json_data_2["x"]
                                    self.enemy_car_2_starty=self.car_y_coordinate- y_counter_difference # hanghayar hena
                        elif json_data_2["type"]=="crash":
                            self.remove_enemy()
                            if json_data_2["client"]==2:
                                self.enemy_car_1_startx=-1000
                                self.enemy_car_1_state='crashed'
                            elif json_data_2["client"]==3:
                                self.enemy_car_2_startx=-1000
                                self.enemy_car_2_state="crashed"
                    elif self.clientId==2:
                        if json_data_2["type"]=="run":
                            if json_data_2["client"]==1:
                                y_counter_difference=(self.y_counter-json_data_2["y_counter"])
                                if self.enemy_car_1_y_counter!=json_data_2["y_counter"]:
                                    enemy_1_change_y=True
                                self.enemy_car_1_y_counter=json_data_2["y_counter"]
                                if y_counter_difference> -100 and y_counter_difference<380:
                                    self.enemy_car_1_startx=json_data_2["x"]
                                    self.enemy_car_1_starty=self.car_y_coordinate- y_counter_difference # hanghayar hena
                            elif json_data_2["client"]==3:
                                y_counter_difference=(self.y_counter-json_data_2["y_counter"])
                                if self.enemy_car_1_y_counter!=json_data_2["y_counter"]:
                                    enemy_2_change_y=True
                                self.enemy_car_2_y_counter=json_data_2["y_counter"]
                                if y_counter_difference> -100 and y_counter_difference<380:
                                    self.enemy_car_2_startx=json_data_2["x"]
                                    self.enemy_car_2_starty=self.car_y_coordinate- y_counter_difference # hanghayar hena
                        elif json_data_2["type"]=="crash":
                            self.remove_enemy()
                            if json_data_2["client"]==1:
                                self.enemy_car_1_startx=-1000
                                self.enemy_car_1_state='crashed'
                            elif json_data_2["client"]==3:
                                self.enemy_car_2_startx=-1000
                                self.enemy_car_2_state="crashed"
                    elif self.clientId==3:
                        if json_data_2["type"]=="run":
                            if json_data_2["client"]==1:
                                y_counter_difference=(self.y_counter-json_data_2["y_counter"])
                                if self.enemy_car_1_y_counter!=json_data_2["y_counter"]:
                                    enemy_1_change_y=True
                                self.enemy_car_1_y_counter=json_data_2["y_counter"]
                                if y_counter_difference> -100 and y_counter_difference<380:
                                    self.enemy_car_1_startx=json_data_2["x"]
                                    self.enemy_car_1_starty=self.car_y_coordinate- y_counter_difference # hanghayar hena
                            elif json_data_2["client"]==2:
                                y_counter_difference=(self.y_counter-json_data_2["y_counter"])
                                if self.enemy_car_1_y_counter!=json_data_2["y_counter"]:
                                    enemy_2_change_y=True
                                self.enemy_car_2_y_counter=json_data_2["y_counter"]
                                if y_counter_difference> -100 and y_counter_difference<380:
                                    self.enemy_car_2_startx=json_data_2["x"]
                                    self.enemy_car_2_starty=self.car_y_coordinate- y_counter_difference # hanghayar hena
                        elif json_data_2["type"]=="crash":
                            self.remove_enemy()
                            if json_data_2["client"]==1:
                                self.enemy_car_1_state='crashed'
                                self.enemy_car_1_startx=-1000
                            elif json_data_2["client"]==2:
                                self.enemy_car_2_state="crashed"
                                self.enemy_car_2_startx=-1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True
                    self.disconnect_socket()
                    #self.gameDisplay.quit()
                    pygame.quit()
                # print(event)

                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_LEFT):
                        self.car_x_coordinate -= 50
                        location_change_flag=True
                        state_json={ "client": self.clientId, "type": 'run', "x": self.car_x_coordinate, "y": self.car_y_coordinate ,"y_counter":self.y_counter}
                        json_data_3 = json.dumps(state_json)
                        self.ws.send(json_data_3)   
                        print ("CAR X COORDINATES: %s" % self.car_x_coordinate)
                    if (event.key == pygame.K_RIGHT):
                        self.car_x_coordinate += 50
                        location_change_flag=True

                        state_json={ "client": self.clientId, "type": 'run', "x": self.car_x_coordinate, "y": self.car_y_coordinate ,"y_counter":self.y_counter}
                        json_data_3 = json.dumps(state_json)
                        self.ws.send(json_data_3)    
                     
                       
                    if (event.key == pygame.K_UP):
                        move_up=True
                        location_change_flag=True
                    if (event.key == pygame.K_DOWN):
                        move_down=True
                        location_change_flag=True
                if (event.type == pygame.KEYUP):
                    if (event.key == pygame.K_UP):
                        move_up=False
                    if (event.key == pygame.K_DOWN):
                        move_down=False
                    print ("x: {x}, y: {y}".format(x=self.car_x_coordinate, y=self.car_y_coordinate))
            difference_1=self.y_counter-self.enemy_car_1_y_counter
            difference_2=self.y_counter-self.enemy_car_2_y_counter
            if move_up and self.car_y_coordinate>0 and self.count % 4 == 0:
                self.y_counter-=4
                #self.car_y_coordinate -=4
                location_change_flag=True
                state_json={ "client": self.clientId, "type": 'run', "x": self.car_x_coordinate, "y": self.car_y_coordinate ,"y_counter":self.y_counter}
                self.enemy_car_1_starty=self.car_y_coordinate- difference_1
                self.enemy_car_2_starty=self.car_y_coordinate- difference_2
                json_data_3 = json.dumps(state_json)
                self.ws.send(json_data_3)
            # if move_down and self.car_y_coordinate<480 and self.count % 4 == 0:
            #     self.y_counter+=4
            #     #self.car_y_coordinate +=4
            #     location_change_flag=True
            #     state_json={ "client": self.clientId, "type": 'run', "x": self.car_x_coordinate, "y": self.car_y_coordinate ,"y_counter":self.y_counter}
            #     json_data_3 = json.dumps(state_json)
            # if move_down and self.car_y_coordinate<450:
            #     self.car_y_coordinate +=1



            self.gameDisplay.fill(self.black)
            self.back_ground_raod()
            # difference_1=self.y_counter-self.enemy_car_1_y_counter
            # difference_2=self.y_counter-self.enemy_car_2_y_counter
            if self.enemy_car_1_state=='run' and difference_1> -100 and difference_1<380:
                #print("i will run enemy 1")
                self.run_enemy_car(self.enemy_car_1,self.enemy_car_1_startx, self.enemy_car_1_starty)
            if self.enemy_car_2_state=='run'  and difference_2> -100 and difference_2<380:
                #print("i will run enemy 2")
                self.run_enemy_car(self.enemy_car_2,self.enemy_car_2_startx, self.enemy_car_2_starty)
            
            ####self.enemy_car_1_starty -= self.enemy_car_1_speed

            #if self.enemy_car_1_starty > self.display_height:
            #    self.enemy_car_1_starty = 0 - self.enemy_car_1_height
            #    self.enemy_car_1_startx = random.randrange(310, 450)

            self.car(self.car_x_coordinate, self.car_y_coordinate)
            #print("el mafroud self.car teshtaghal, be x=",self.car_x_coordinate,"we y:",self.car_y_coordinate)
            self.highscore(self.count,self.lives)
            self.count += 1
            # if (not move_up):
            self.y_counter-=0
            # if enemy_1_change_y==False:
            self.enemy_car_1_y_counter-=0
            # if enemy_2_change_y==False:
            self.enemy_car_2_y_counter-=0
            # if (self.count % 100 == 0):
            #     # self.enemy_car_speed += 1
            #     self.bg_speed += 1
            if (location_change_flag):
                if self.car_y_coordinate <= self.enemy_car_1_starty + self.enemy_car_1_height  and (self.car_y_coordinate >= self.enemy_car_1_starty ):

                    if self.car_x_coordinate >= self.enemy_car_1_startx and self.car_x_coordinate <= self.enemy_car_1_startx + self.enemy_car_1_width or self.car_x_coordinate + self.car_width >= self.enemy_car_1_startx and self.car_x_coordinate + self.car_width <= self.enemy_car_1_startx + self.enemy_car_1_width:
                        print("MUST CRASH               self.car_x_coordinate",self.car_x_coordinate,"self.enemy_car_1_startx",self.enemy_car_1_startx)
                        print("MUST CRASH               self.car_x_coordinate",self.car_x_coordinate,"self.enemy_car_1_startx",self.enemy_car_1_startx)
                        print("self.car_x_coordinate",self.car_x_coordinate,"self.enemy_car_1_startx",self.enemy_car_1_startx)
                        print("mafrud crash 2")
                        self.crashed = True
                        state_json={ "client": self.clientId, "type": 'crash', "x": -1000, "y": self.car_y_coordinate ,"y_counter":self.y_counter}
                        json_data = json.dumps(state_json)
                        self.ws.send(json_data)
                        self.display_message_only("Game Over !!!")
                        self.disconnect_socket()
                        self.gameDisplay.quit()
                        pygame.quit()
                        break
                        # if self.lives<=0:
                            
                        #     self.crashed = True
                        #     state_json={ "client": self.clientId, "type": 'crash', "x": self.car_x_coordinate, "y": self.car_y_coordinate ,"y_counter":self.y_counter}
                        #     json_data = json.dumps(state_json)
                        #     self.ws.send(json_data)
                        #     self.display_message_only("Game Over !!!")
                        #     self.disconnect_socket()
                        #     self.gameDisplay.quit()
                        #     pygame.quit()
                        #     break
                        # if self.lives>0:
                        #     self.lives-=1
                        #     self.y_counter+=5
                        #     state_json={ "client": self.clientId, "type": 'run', "x": self.car_x_coordinate, "y": self.car_y_coordinate ,"y_counter":self.y_counter}
                        #     json_data = json.dumps(state_json)
                        #     self.ws.send(json_data)
                        #     self.display_message_only("you consumed a live")
                if self.car_y_coordinate <= self.enemy_car_2_starty + self.enemy_car_2_height and (self.car_y_coordinate >= self.enemy_car_2_starty ):
                    if self.car_x_coordinate >= self.enemy_car_2_startx and self.car_x_coordinate <= self.enemy_car_2_startx   + self.enemy_car_2_width or self.car_x_coordinate + self.car_width >= self.enemy_car_2_startx and self.car_x_coordinate + self.car_width <= self.enemy_car_2_startx + self.enemy_car_2_width:
                        print("self.car_x_coordinate",self.car_x_coordinate,"self.enemy_car_2_startx",self.enemy_car_2_startx)
                        print("mafrud crash 2")
                        self.crashed = True
                        state_json={ "client": self.clientId, "type": 'crash', "x": -1000, "y": self.car_y_coordinate ,"y_counter":self.y_counter}
                        json_data = json.dumps(state_json)
                        self.ws.send(json_data)
                        self.display_message_only("Game Over !!!")
                        self.disconnect_socket()
                        self.gameDisplay.quit()
                        pygame.quit()
                        break
                    

            if self.car_x_coordinate < 310 or self.car_x_coordinate > 460:
                self.crashed = True
                state_json={ "client": self.clientId, "type": 'crash', "x":-1000, "y": self.car_y_coordinate ,"y_counter":self.y_counter}
                json_data = json.dumps(state_json)
                self.ws.send(json_data)
                self.display_message_only("Game Over !!!")
                self.disconnect_socket()
                self.gameDisplay.quit()
                pygame.quit()
                break


            # if ((not self.crashed )and location_change_flag):
            #     self.ws.send(json_data_3) 
            # r, w, e = select.select([self.ws.sock], [], [], 0)
            # if self.ws.sock in r:
            #     print ("mestanni a receive fe lie 170")
            #     data = self.ws.recv()
            #     print('Received in line 170:', data.decode())
            #print("3addet fe line 173")
            pygame.display.update()
            self.clock.tick(60)

    def display_message(self, msg):
        font = pygame.font.SysFont("comicsansms", 72, True)
        text = font.render(msg, True, (255, 255, 255))
        self.gameDisplay.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))
        self.display_credit()
        pygame.display.update()
        self.clock.tick(60)
        sleep(1)
        #car_racing.initialize()
        #car_racing.racing_window()
    def display_message_only(self, msg):
        font = pygame.font.SysFont("comicsansms", 72, True)
        text = font.render(msg, True, (255, 255, 255))
        self.gameDisplay.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))
        self.display_credit()
        pygame.display.update()
        self.clock.tick(60)
        sleep(2)
        # car_racing.initialize()
        # car_racing.racing_window()
    def back_ground_raod(self):
        self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = -600

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = -600

    def run_enemy_car(self, car,thingx, thingy):
        self.gameDisplay.blit(car, (thingx, thingy))
    def remove_enemy (self):
        self.gameDisplay.fill((0, 0, 0))

    def highscore(self, count,lives):
        font = pygame.font.SysFont("arial", 20)
        text = font.render("Score : " + str(count), True, self.white)
        text2 = font.render("Lives : " + str(lives), True, self.white)
        self.gameDisplay.blit(text, (0, 0))
        #self.gameDisplay.blit(text2, (0, 20))

    def display_credit(self):
        font = pygame.font.SysFont("lucidaconsole", 14)
        text = font.render("Thanks for playing!", True, self.white)
        self.gameDisplay.blit(text, (600, 520))

def execute_game():
    car_racing = CarRacing()
    car_racing.run_car()
# if __name__ == '__main__':
#     car_racing = CarRacing()
#     car_racing.racing_window()

