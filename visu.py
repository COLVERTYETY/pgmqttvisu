import pygame as pg
import numpy as np
import paho.mqtt.client as mqtt
import time

def generate(largeur,longueur):
    matrix = np.random.rand(largeur,longueur)
    return matrix

def printer(matrix):
    for row in matrix:
        print(row)

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK Returned code=",rc)
    else:
        print("Bad connection Returned code=",rc)

def on_message_(client, userdata, message):
    print(message.payload)

def drawmat(matrix,screen):
    (screenw,screenh) = screen.get_size()
    (length,depth) = matrix.shape
    cellw = float(screenw/length)
    cellh = float(screenh/depth)
    colorc = (0,128,128)#mix res
    for x in range(length):
        for y in range(depth):
            #calc color from val of cell
            colorc = (int(matrix[x][y]*255),0,int((1.0-matrix[x][y])*255))
            pg.draw.rect(screen,colorc,pg.Rect(int(cellw*x),int(cellh*y),int(cellw),int(cellh)))
 
width = 8
height = 8

matrix = generate(width,height)
# printer(matrix)
swidth = 800
sheight = 800
pg.init()
screen = pg.display.set_mode((swidth, sheight))
drawmat(matrix,screen)
pg.display.flip()
done = False
print("start mqtt")
client = mqtt.Client("tester", True, None)
client.on_connect = on_connect
client.on_message = on_message_
print("pls connect")
while client.is_connected!=True:
    client.connect("stasnicolas.org", 1883,60)
    print("attempting")
    time.sleep(2)
print("pls sub")
client.subscribe("test",qos=1)
while not done:
        for event in pg.event.get():
                if event.type == pg.QUIT:
                        done = True
        drawmat(matrix,screen)
        pg.display.flip()