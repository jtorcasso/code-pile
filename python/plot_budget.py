import matplotlib.pylab as plt

def autolabel(rects, labels):
    for ii,rect in enumerate(rects):
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.02*height, '%s'% (labels[ii]),
                ha='center', va='bottom', fontsize=15)

ax = plt.subplot(111)
rects = ax.bar([0,1,2], [5.2, 8.0, 16.5], align='center',\
	   color=['#ffa319', '#c16622', '#8f3931'], linewidth=0)

ax.set_xticks([0,1,2])
ax.set_xticklabels(['CCDF', 'Head\nStart', 'TANF'], fontsize=25)

ax.tick_params(axis='both', left='off', top='off', \
	           bottom='off', right='off', labelleft='off')

ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['top'].set_visible(False)

labels = ['$5.2B', '$8.0B', '$16.5B']


autolabel(rects, labels)

plt.show()