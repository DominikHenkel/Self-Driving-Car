import cv2
import numpy as np

class Entity(object):

    x=0
    y=0
    w=0
    h=0
    id=0
    obj="not defined"

    def __init__(self, x, y, w, h, id, obj):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.id = id
        self.obj = obj

class Map(object):

    entities = []
    image_shape = 400
    act_car_x = 150
    act_car_y = 240
    total_id = 0

    #def __init__(self):

    def compute2DMap(self):
        image = np.zeros((self.image_shape, self.image_shape, 3), np.uint8)
        for i in range(6):
            cv2.line(image, (0,(i+1)*200), (image.shape[1],(i+1)*200),(255,255,0), 3)
        if(len(self.entities)>0):
            cv2.rectangle(image, (self.act_car_x - 50, self.act_car_y - 50), (self.act_car_x + 50, self.act_car_y + 50), (255, 255, 255), 2)
        for i in range(len(self.entities)):
            cv2.rectangle(image, (self.entities[i].x - 50, self.entities[i].y - 50), (self.entities[i].x + 50, self.entities[i].y + 50), (0, 255, 0), 2)
            cv2.putText(image, self.entities[i].obj+str(self.entities[i].id),(self.entities[i].x-50,self.entities[i].y-55), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
        self.total_id = self.detect_act_car()
        cv2.imshow('Image', image)
        self.entities.clear()

    def add_entity(self,x,y,w,h,id,obj, image_shape):
        if(obj == "car"):
            x_scaled = int(x*(self.image_shape/ image_shape))
            y_scaled = int(y*(self.image_shape/ image_shape))
            self.entities.append(Entity(x_scaled,y_scaled,w,h,id,obj))

    def detect_act_car(self):
        min = 100000
        id = 0
        for i in range(len(self.entities)):
            tmp_min = abs(self.act_car_x-self.entities[i].x)+abs(self.act_car_y-self.entities[i].y)
            if(tmp_min < min):
                min = tmp_min
                id = self.entities[i].id
        return id

    def getTotalId(self):
        return self.total_id
