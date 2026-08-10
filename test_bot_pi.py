import cv2
import os
import asyncio
import time
import face_recognition

from ultralytics import YOLO
from telegram import Bot
from dotenv import load_dotenv


load_dotenv() #loads env file, finds and reads them

viu_image = face_recognition.load_image_file("viusan.jpg")#getting image of myself
print(viu_image.shape, viu_image.dtype)
viu_encoding = face_recognition.face_encodings(viu_image)#getting the encoding

#get the token and chat from enviornment file i have
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

#function to actually send the image to telegram bot 
async def send_message(image_path):
    bot = Bot(token=TOKEN)
    #we get encoding of the face that was scanned by the camera
    scanned_face = face_recognition.load_image_file(image_path)
    scanned_encoding = face_recognition.face_encodings(scanned_face)

    caption_text = "Alert: Unknown person detected"#default alert

    #face encodings will return a list where index 0 is the face, and if there are no faces that were detected
    #then we would be looking into an empty list which causes errors here, so we create a if statement
    if len(scanned_encoding) > 0:
        match = face_recognition.compare_faces(viu_encoding, scanned_encoding[0])
        if match[0]:#match returns [true/false] so we have to enter the list and check
            caption_text = "Alert: Viusan detected"
        else: 
            caption_text = "Alert: Unknown person detected"
    else:
        pass

    with open(image_path, "rb") as photo:
        await bot.send_photo(
            chat_id=CHAT_ID,
            photo=photo,
            caption=caption_text
        )

#YOLO model that we are going to use
model = YOLO("yolov8n.pt")

#initialize the primary webcam
capture = cv2.VideoCapture(0)

#check if the camera opened correctly
if not capture.isOpened():
    print("Error: Webcam couldnt open.")
    exit()

#we are going to need to use the python time module, so we dont send an image every single time we detect a person
#becasue then we would be sending an image 20 times per second which is useless
last_time_cooldown = time.time()

while True:
    #capture the frame
    ret, frame = capture.read()

    #if we got a frame, we display it
    if ret:
        result = model(frame)
        cv2.imshow('Webcam feed', result[0].plot())

        #this part takes tensors and translates them into integers.
        #the integers represent what is being shown, and if it is a person the value returned is 0
        #with that info we can see if we have detected a person or not
        for box in result[0].boxes: 
            #if we have detected a person we first check if last sent image is over 20 seconds (to avoid spam)
            if(int(box.cls) == 0):
                time_cooldown = time.time()
                if(time_cooldown - last_time_cooldown > 20):
                    last_time_cooldown = time_cooldown #we reset the last sent image to the current time
                    cv2.imwrite("alert.jpg", frame) #saves current frame to file called alert.jpg
                    #asyncio.run pauses the whole webcam loop while it waits for the telegram upload to finish, since our code is regular non-async and can only do one thing at a time
                    asyncio.run(send_message("alert.jpg")) 


    #press q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#release capture and close windows
capture.release()
cv2.destroyAllWindows()       