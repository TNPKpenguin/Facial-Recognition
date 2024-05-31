import cv2 
import numpy as np 
import os
import pandas as pd 
import openpyxl

class get_data():
    def __init__(self):
        self.imgs_path = "friends_face\\"
        self.name_path = "data\\name_data.csv"
        self.excel_path = 'data\\data2.xlsx'
        self.images = []

    def getImage(self):
        for i in os.listdir(self.imgs_path):
            img_path = os.path.join(self.imgs_path, i)
            img = cv2.imread(img_path)
            img = self.profile(img)
            self.images.append(img)
        return np.array(self.images)
    
    def getDataName(self):
        data = pd.read_csv(self.name_path)
        return np.array(data)
    
    def profile(self, img):
        img = cv2.resize(img, (300, 300))
        h, w = img.shape[:2]
        h2, w2 = h // 2, w // 2
        radius = min(h2, w2)
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(mask, (w2, h2), radius, 255, -1)
        green_background = np.full((h, w, 3), (0, 255, 0), dtype=np.uint8)

        masked_img = cv2.bitwise_and(img, img, mask=mask)
        inverse_mask = cv2.bitwise_not(mask)
        masked_background = cv2.bitwise_and(green_background, green_background, mask=inverse_mask)
        result = cv2.add(masked_img, masked_background)
        
        return result[:, :, ::-1]

    def getNameList(self):
        workbook = openpyxl.load_workbook(self.excel_path)
        return np.array(sorted(workbook.sheetnames))