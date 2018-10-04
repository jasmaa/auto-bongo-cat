from scipy.io import wavfile
import matplotlib.pyplot as plt
import cv2

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
fps = 10
sample_rt, sound = wavfile.read('test.wav')

img1 = cv2.imread('clean_frame01.png')
img2 = cv2.imread('clean_frame02.png')
h, w, layers = img1.shape

"""
# plot
play_time = np.arange(0, len(s1), 1)
plt.plot(play_time, s1, color='k')
plt.ylabel('Amplitude')
plt.xlabel('Time (ms)')
plt.show()
"""

video = cv2.VideoWriter('test_out.avi', -1, fps, (w,h))
interval = int(sample_rt / fps)

left = thin(sound[:,0], interval)
right = thin(sound[:,1], interval)

# generate video
cutoff = avg_energy(left, right)

for i in range(len(right)):
    if energy(i, left, right) >= cutoff:
        video.write(img2)
    else:
        video.write(img1)

    print(str(int(float(i) / len(right) * 100)) + "%")

video.release()
cv2.destroyAllWindows()
