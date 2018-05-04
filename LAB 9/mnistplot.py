import numpy as np
from matplotlib import pyplot as plt
import sys
with open(sys.argv[1], 'r') as f:
    fig = plt.figure()
    for index in range(10):
        plt.subplot(5,5, index+1)
        mean = [255*i//1 for i in list(map(float, f.readline().split(',')))]
        pixels = np.array(mean, dtype='uint8')
        pixels = pixels.reshape((28, 28))
        plt.axis('off')
        plt.title('{}-th Mean'.format(index+1))
        plt.imshow(pixels, cmap='gray')
    plt.show()