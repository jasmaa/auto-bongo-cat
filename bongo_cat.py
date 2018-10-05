from scipy.io import wavfile
import cv2
import moviepy.editor as mpe
import os, sys
import time

def thin(a, interval):
    return [a[i] for i in range(0, len(a), interval)]

def energy(i, l, r):
    return l[i] ** 2 + r[i] ** 2

def avg_energy(l, r):
    s = 0
    for i in range(len(r)):
        s += (l[i] ** 2 + r[i] ** 2) / len(r)
    return s

# read in data
in_name = 'test'
out_name = 'output'

fps = 15
sample_rt, sound = wavfile.read(in_name+'.wav')

img1 = cv2.imread('clean_frame01.png')
img2 = cv2.imread('clean_frame02.png')
h, w, layers = img1.shape

# generate video
video = cv2.VideoWriter(out_name+'.avi', -1, fps, (w,h))
interval = int(sample_rt / fps)

left = thin(sound[:,0], interval)
right = thin(sound[:,1], interval)

cutoff = avg_energy(left, right)

for i in range(len(right)):
    
    if energy(i, left, right) >= cutoff:
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
