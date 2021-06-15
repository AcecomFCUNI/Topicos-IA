import pickle
import os
import cv2
import numpy as np
from skimage.feature import hog
from skimage import feature
# Importamos el modelo entrenado
import matplotlib.pyplot as plt


with open("Model_Trained.pickle", "rb") as file:
    model = pickle.load(file)


# Realizamos las predicciones de la carpeta Testing

Testing = [f"./Testing/{img}" for img in os.listdir("./Testing") ]

for img in Testing:
    imagen = cv2.imread(img)
    gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5)) 
    otsu  = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations = 4)
    otsu  = cv2.morphologyEx(otsu, cv2.MORPH_OPEN, kernel, iterations = 4)

    # ROI
    contours, _ = cv2.findContours(otsu, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    centro_leaf = [cv2.moments(j) for j in contours]

    centroXY = [(int(M["m10"] / M["m00"]), int(M["m01"]/M["m00"])) for M in centro_leaf]
    
    x, y = centroXY[0]

    t = 0
    v_t =True 

    b = 0
    v_b =True 

    l = 0
    v_l =True 

    r = 0
    v_r =True 
    
    for i in range(w//2):
        if y + i < h and y - i > 0:
            if otsu[y+i][x] == 0 and v_t:
                t = i
                v_t = False 
        
            if otsu[y-i][x] == 0 and v_b:
                b = i
                v_b = False 
        if x + i < w and x - i > 0 :

            if otsu[y][x-i] == 0 and v_l:
                l = i
                v_l = False 

            if otsu[y][x+i] == 0 and v_r:
                r = i
                v_r = False 
    t = y + t
    b = y - b

    r = r + x
    l = x - l

    blue, green, red = cv2.split(imagen)

    # Agregando border alrededor de la hoja
    
    t += 150 # px
    b -= 150
    r += 150
    l -= 150

    cut_otsu = otsu[b:t, l:r]
    blue = blue[b:t, l:r]
    red = red[b:t, l:r]
    green = green[b:t, l:r]

    BGR = cv2.merge([blue, green, red])

    # Aplicamos la binarización en la imagen original cortada
    cut_image = cv2.bitwise_or(BGR, BGR, mask=cut_otsu)
    plt.imshow(cut_image)
    plt.show()

    HSV = cv2.cvtColor(cut_image, cv2.COLOR_BGR2HSV)
    h, s, _ = cv2.split(HSV)

    descrip_1 = [h.mean(), s.mean()]

    resize_img = cv2.resize(cut_image, (64, 128), interpolation = cv2.INTER_CUBIC)

    descrip_2,_ = hog(resize_img, orientations = 9, pixels_per_cell=(8,8), cells_per_block=(2,2), visualize = True, multichannel = True)

    descrip_2 = list(descrip_2.reshape(-1))

    resize_img_gray = cv2.cvtColor(resize_img, cv2.COLOR_BGR2GRAY)

    descrip_3 = feature.local_binary_pattern(resize_img_gray, 24, 8, method="uniform")

    hist, _ = np.histogram(descrip_3.ravel(), bins = np.arange(0, 24 + 3),range=(0, 24+ 2))
    hist = hist.astype("float")
    hist /= hist.sum()
    
    descrip_3_pro = list(hist.reshape(-1))

    features = np.array(descrip_1 + descrip_2 + descrip_3_pro)
    features = np.reshape(features, (1, -1))
    
    predict = model.predict(features)

    print(f"{img} -> model predictivo : ", predict)



