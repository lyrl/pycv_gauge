import cv2
import numpy as np
print (cv2.__version__)
# Create a VideoCapture object
cap = cv2.VideoCapture(0)
import plotly.graph_objects as go





#width = cap.get(cv2.CAP_PROP_FRAME_WIDTH);
#height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT);

#print (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT)

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH);
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT);

print (width, height)


cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


width = cap.get(cv2.CAP_PROP_FRAME_WIDTH);
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT);

print (width, height)



# Check if camera opened successfully
if (cap.isOpened() == False): 
  print("Unable to read camera feed")
 
# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
 
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('outpy.mkv',cv2.VideoWriter_fourcc('h','2','6','4'), 30, (frame_width,frame_height))
#out = cv2.VideoWriter('outpy.mp4',cv2.VideoWriter_fourcc('m','p','4','v'), 30, (frame_width,frame_height))
#out = cv2.VideoWriter('outpy.mp4',cv2.VideoWriter_fourcc('m','p','4','v'), 30, (frame_width,frame_height))
 
while(True):
  ret, frame = cap.read()
 
  if ret == True: 
     
    # Write the frame into the file 'output.avi'
    out.write(frame)
 
    # Display the resulting frame    
    cv2.imshow('frame',frame)


 
    # Press Q on keyboard to stop recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
 
  # Break the loop
  else:
    break 
 
# When everything done, release the video capture and video write objects
cap.release()
out.release()
 
# Closes all the frames
cv2.destroyAllWindows() 
