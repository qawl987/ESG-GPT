import numpy as np
import matplotlib.pyplot as plt
class mat():
    def __init__(self):
        self.alpha = 1
        self.p = 1.5
    def rmaf(self, x):
        y = self.alpha * x / np.power((0.25 * (1 + np.exp(-x)) + 0.75), self.p)
        return y
    def sigmoid(slef, x):
        return 1 / (1 + np.exp(-x))
    def swish(self, x):
        return x * self.sigmoid(x)
    def derive_swish(self, x):
        return self.swish(x) + self.sigmoid(x) * (1 - self.swish(x))

    def derive_rmaf(self, x):
        y = self.alpha / np.power((0.25 * (1 + np.exp(-x)) + 0.75), self.p) + \
            0.25 * self.p * self.alpha * x * np.exp(-x) / np.power((0.25 * (1 + np.exp(-x)) + 0.75), self.p + 1)
        return y
    def draw(self):
        x = np.linspace(-10, 10, 100)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.spines['left'].set_position('center')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ps = [1, 1.5, 2, 2.5]
        for i in ps:
            self.p = i
            plt.plot(x, self.derive_swish(x), 'r')
        # plot the function
        # xaxis = [-10, 10]
        xaxis = [-3, 3]
        plt.xticks(xaxis)
        # yaxis = [-25, 5]
        yaxis = [-1, 1]
        plt.yticks(yaxis)
        # show the plot
        plt.show()
ob = mat()
ob.draw()