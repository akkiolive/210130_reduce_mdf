import matplotlib.pyplot as plt




##Add subplots
#fig
fig = plt.figure()

#ax
ax0 = fig.add_subplot(2,2,1)
ax0.set_xlim([0,100])
ax0.set_ylim([0,1])
vline0 = ax0.axvline(10)
ax1 = fig.add_subplot(2,2,4)
ax1.set_xlim([0,100])
ax1.set_ylim([0,1])
vline = ax1.axvline(10)

#bg
fig.canvas.draw()
bg = fig.canvas.copy_from_bbox(fig.bbox)

#connect
def onMotion(e):
    print("Add_subplot:", e)
    if e.xdata:
        #vline.set_xdata([e.xdata]*2)
        #fig.canvas.draw()
        pass
    
def onPress(e):
    print("pressed")
    global bg, ax1
    fig.canvas.restore_region(bg)
    if e.xdata:
        vline.set_xdata([e.xdata]*2)
        ax1.draw_artist(vline)
    fig.canvas.blit(ax1.bbox)

def onDraw(e):
    print("Add_subplot:", e)


fig.canvas.mpl_connect("motion_notify_event", onMotion)
fig.canvas.mpl_connect("button_press_event", onPress)
fig.canvas.mpl_connect("draw_event", onDraw)




##Subplots
#fig
Fig, axes = plt.subplots(2,2)

#ax
ax = axes[0][0]
ax.set_xlim([0,100])
ax.set_ylim([0,1])
Vline = ax.axvline(20)

#ax2
axes2 = Fig.subplots(1,1)
ax2 = axes2
ax2.set_xlim([0,100])
ax2.set_ylim([0,1])
Vline2 = ax2.axvline(50, color="red")

#connect
def OnMotion(e):
    print("Subplots   :", e)
    if e.xdata:
        Vline.set_xdata([e.xdata]*2)
        Vline2.set_xdata([e.xdata]*2)
        #Fig.canvas.draw()

    
def OnDraw(e):
    print("Subplots   :", e)
    
Fig.canvas.mpl_connect("motion_notify_event", OnMotion)
Fig.canvas.mpl_connect("draw_event", OnDraw)


plt.show()