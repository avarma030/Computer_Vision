import cv2 
import face_recognition
import pickle
name=input("Enter name of the person: --> ")
ref_id=input("Enter referral ID: --> ")

try:
	f=open("ref_name.pkl","rb")

	ref_dictt=pickle.load(f)
	f.close()
except:
	ref_dictt={}
ref_dictt[ref_id]=name


f=open("ref_name.pkl","wb")
pickle.dump(ref_dictt,f)
f.close()

try:
	f=open("ref_capture.pkl","rb")

	capture_dictt=pickle.load(f)
	f.close()
except:
	capture_dictt={}


for i in range(5):
	key = cv2. waitKey(1)
	webcam = cv2.VideoCapture(0)
	while True:
	     
		check, frame = webcam.read()
		cv2.imshow("Capturing Data", frame)
		small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
		rgb_small_frame = small_frame[:, :, ::-1]
		
		key = cv2.waitKey(1)

		if key == ord('c') : 
			face_locations = face_recognition.face_locations(rgb_small_frame)
			if face_locations != []:
				face_encoding = face_recognition.face_encodings(frame)[0]
				if ref_id in capture_dictt:
					capture_dictt[ref_id]+=[face_encoding]
				else:
					capture_dictt[ref_id]=[face_encoding]
				webcam.release()
				cv2.waitKey(1)
				cv2.destroyAllWindows()     
				break
		elif key == ord('q'):
			print("Turning off webcam")
			webcam.release()
			print("Webcam has been turned off")
			print("--END--")
			cv2.destroyAllWindows()
			break
f=open("ref_capture.pkl","wb")
pickle.dump(capture_dictt,f)
f.close()