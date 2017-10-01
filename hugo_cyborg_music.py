import json
import glob
import numpy as np
import matplotlib.pylab as plt
import subprocess
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks_cwt, argrelmax, argrelmin
import cv2
import mido
from mido import Message

DIR = 'hugo/*pose.json'
sigma = 3.
width = 10
port_id = 6

files = glob.glob(DIR)
files.sort()

RWrist_x_coord = np.zeros(len(files))
RWrist_y_coord = np.zeros(len(files))

LWrist_x_coord = np.zeros(len(files))
LWrist_y_coord = np.zeros(len(files))

for i,filename in enumerate(files):
	pose = json.load(open(filename))
	body_parts = np.array(pose['people'][0]['body_parts'])
	x_neck = body_parts[1 * 3]
	y_neck = body_parts[1*3+1]
	RWrist_x_coord[i] = body_parts[4 * 3]-x_neck
	RWrist_y_coord[i] = body_parts[4 * 3 + 1]-y_neck

	LWrist_x_coord[i] = body_parts[7 * 3]-x_neck
	LWrist_y_coord[i] = body_parts[7 * 3 + 1]-y_neck



f, ax = plt.subplots(2, 3)
RWrist_x_coord = gaussian_filter1d(RWrist_x_coord, sigma=1.)
RWrist_y_coord = gaussian_filter1d(RWrist_y_coord, sigma=1.)
LWrist_x_coord = gaussian_filter1d(LWrist_x_coord, sigma=1.)
LWrist_y_coord = gaussian_filter1d(LWrist_y_coord, sigma=1.)

R_gradient = np.gradient(RWrist_y_coord)
R_curvature = np.gradient(R_gradient)

L_gradient = np.gradient(LWrist_y_coord)
L_curvature = np.gradient(L_gradient)

RWrist_peaks = np.asarray(argrelmin(R_curvature, order=15))
LWrist_peaks = np.asarray(argrelmin(L_curvature, order=15))


ax[0, 0].plot(np.arange(len(files)), RWrist_x_coord)
ax[0, 1].plot(np.arange(len(files)), RWrist_y_coord)
ax[0, 1].scatter(RWrist_peaks, RWrist_y_coord[RWrist_peaks])
ax[0, 0].scatter(RWrist_peaks, RWrist_x_coord[np.clip(RWrist_peaks,0,len(files)-1)])
ax[0, 2].plot(np.arange(len(files)), R_curvature)
ax[0, 2].scatter(RWrist_peaks, R_curvature[RWrist_peaks])


ax[1, 0].plot(np.arange(len(files)), LWrist_x_coord)
ax[1, 1].plot(np.arange(len(files)), LWrist_y_coord)
ax[1, 1].scatter(LWrist_peaks, LWrist_y_coord[LWrist_peaks])
ax[1, 0].scatter(LWrist_peaks, LWrist_x_coord[np.clip(LWrist_peaks,0,len(files)-1)])
ax[1, 2].plot(np.arange(len(files)), L_curvature)
ax[1, 2].scatter(LWrist_peaks, L_curvature[LWrist_peaks])

#plt.show()
cap = cv2.VideoCapture('hugo/result.avi')
list_ports = mido.get_output_names()
outport = mido.open_output(list_ports[port_id])

R_note = 0
L_note = 0
while True:
	cap = cv2.VideoCapture('hugo/result.avi')
	for i in range(len(files)):
		r,frame = cap.read()
		if i in RWrist_peaks and R_curvature[i] < -5.:
			cv2.circle(frame, (int(RWrist_x_coord[i]+x_neck), int(RWrist_y_coord[i]+y_neck)), 10, (0,0,255), -1)
			outport.send(Message('note_off', note=R_note))
			if RWrist_x_coord[i] > -125 :
				R_note = 36
			elif RWrist_x_coord[i] < -225:
				R_note = 40
			else:
				R_note = 44
			outport.send(Message('note_on', note=R_note))
		if i in LWrist_peaks and L_curvature[i] < -5.:
			cv2.circle(frame, (int(LWrist_x_coord[i]+x_neck), int(LWrist_y_coord[i]+y_neck)), 10, (0,0,255), -1)
			outport.send(Message('note_off', note=L_note))
			if LWrist_x_coord[i] > 175 :
				L_note = 48
			elif LWrist_x_coord[i] < 75:
				L_note = 52
			else:
				L_note = 56
			outport.send(Message('note_on', note=L_note))
		cv2.imshow('frame', frame)
		cv2.waitKey(25)
	outport.send(Message('note_off', note=L_note))
	outport.send(Message('note_off', note=R_note))
