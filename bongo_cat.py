from scipy.io import wavfile
import numpy as np
import cv2
import moviepy.editor as mpe
import os, sys
import time
import math

def thin(a, interval):
    return [a[i] for i in range(0, len(a), interval)]

def energy(l, r):
    return [math.sqrt(l[i] ** 2 + r[i] ** 2) for i in range(len(r))]

# read in data
in_name = 'test'
out_name = 'output'

fps = 10
sample_rt, sound = wavfile.read(in_name+'.wav')

img1 = cv2.imread('clean_frame01.png')
img2 = cv2.imread('clean_frame02.png')
h, w, layers = img1.shape

# generate video
video = cv2.VideoWriter(out_name+'.avi', -1, fps, (w,h))
interval = int(sample_rt / fps)

left = thin(sound[:,0], interval)
right = thin(sound[:,1], interval)

energy_l = energy(left, right)
c = 0.00257 * np.var(energy_l) + 1.514
cutoff = np.average(energy_l)

for i in range(len(right)):
    
    if energy_l[i] >= cutoff:
        video.write(img2)
    else:
        video.write(img1)

    sys.stdout.write("\rGenerating frames: "+str(int(float(i) / len(right) * 100)) + "%")
    sys.stdout.flush()
    
sys.stdout.write("\n")
sys.stdout.flush()

video.release()
cv2.destroyAllWindows()

# attach audio
clip = mpe.VideoFileClip(out_name+'.avi')
bgm = mpe.AudioFileClip(in_name+'.wav')
fin_clip = clip.set_audio(bgm)
fin_clip.write_videofile(out_name+".mp4")
