import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set()

x = np.linspace(-0, 10, 35)
func_dict = {'sinusoid': 3 * np.sin(2 / 3 * x),
             'polynomial': (x-3) * (x - 2) * (x - 8) / 10 ,
             'abs value': np.minimum(np.abs(x - 3), np.abs(x- 8))}

color_dict = {'sinusoid': 'r',
              'polynomial': 'b',
              'abs value': 'g'}

width_dict = {'sinusoid': 4,
              'polynomial': 2,
              'abs value': 3}

style_dict = {'sinusoid': ':',
              'polynomial': '-',
              'abs value': '--'}

for label, y in func_dict.items():
    plt.plot(x, y, label=label, 
             color=color_dict[label],
             linewidth=width_dict[label],
             linestyle=style_dict[label])
plt.legend()
plt.xlabel('x')
plt.ylabel('f(x)')
