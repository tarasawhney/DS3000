import pandas as pd

#Part 1 
df_gme = pd.read_csv('gme_data_clean.csv')
df_gme.head()

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

sns.set()

plt.suptitle('Game Stop Stock')

for plot_idx in range(1, 3):
    plt.subplot(1, 2, plot_idx)
    x = df_gme['days since 2020_Feb_03']
    for label in ['Low', 'High']:
        y = df_gme[label]
        plt.plot(x, y, label=label)
    plt.ylabel('price ($)')
    plt.legend()
    plt.xlabel('days since Feb 3 2020')

    if plot_idx == 2:
        # only set y scale on rightward plot
        plt.yscale('log')


plt.gcf().set_size_inches((10, 5))

f_out = 'game_stop.pdf'
with PdfPages(f_out) as pdf:
    pdf.savefig(bbox_inches='tight')    
