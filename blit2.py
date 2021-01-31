import matplotlib.pyplot as plt

fig, axes = plt.subplots(5, 1)

for ax in axes:
    ax.plot([1,2,3], [2,3,4])

def onPress(e):
    print(e)
    if e.xdata:
        for ax in axes:
            xlim = ax.get_xlim()
            diff = (xlim[1] - xlim[0])*0.05
            ax.set_xlim( [xlim[0]+diff, xlim[1]+diff])
            ax.cla()
            ax.draw_artist(ax.get_lines()[0])
            #ax.draw_artist(ax.axis.XTick)
        fig.canvas.blit(fig.bbox)
        #fig.canvas.draw()

fig.canvas.mpl_connect("button_press_event", onPress)

fig.canvas.draw()
bg = fig.canvas.copy_from_bbox(fig.bbox)


plt.show()