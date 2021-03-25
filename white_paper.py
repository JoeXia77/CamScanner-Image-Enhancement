
## environment
import cv2
import numpy as np
import sys


## commend line interaction
## example(call cmd in windows): python white_paper.py yourImageName.jpg outputName.jpg
if(len(sys.argv) != 3) :
    print(sys.argv[0], ": takes 2 arguments. Not ", len(sys.argv)-1)
    print("Expecting arguments: ImageIn ImageOut.")
    print("Example:", sys.argv[0], "fruits.jpg out.png")
    sys.exit()

name_input = sys.argv[1]
name_output = sys.argv[2]


'''
## if don't use cmd, can specify image file path here
name_input = 'handwritten_img.png'
name_output = f'./{name_input}_modified.png'
'''

## read image: img = cv2.imread(name, type)  type could be : IMREAD_COLOR, IMREAD_GRAYSCALE, IMREAD_UNCHANGED
inputImage = cv2.imread(name_input, cv2.IMREAD_COLOR)
## error: image read fail
if(inputImage is None) :
    print(sys.argv[0], ": Failed to read image from: ", name_input)
    sys.exit()

## and show input image
cv2.imshow("input image", inputImage)
## get image shape: r,c,d = img.shape
rows, columns, demensions = inputImage.shape

## convert to LUV, extract L demension
LUVImg = cv2.cvtColor(inputImage,cv2.COLOR_BGR2Luv)
L_demension = LUVImg[:,:,0]


######################### modifying img ##############################
window_size = (rows+columns) // 400
window_size = max(5, window_size)

windows_v = rows // window_size
windows_h = columns // window_size

for i in range(windows_v):
    for j in range(windows_h):
        position_x = i*window_size
        position_y = j*window_size
        window = L_demension[position_x : position_x+window_size,  position_y : position_y+window_size]
        min_bright = np.min(window)
        ave_bright = np.average(window)
        white_color = 255
        if min_bright>50 and ave_bright>200:
            for r in range(position_x,position_x+window_size):
                for c in range(position_y,position_y+window_size):
                    L_demension[r,c] = white_color

## convert LUV back to RGB:
output_img = cv2.cvtColor(LUVImg,cv2.COLOR_Luv2BGR)

## 
cv2.imshow('output image',output_img)


cv2.imwrite(name_output, output_img)


cv2.waitKey(0)
cv2.destroyAllWindows()



