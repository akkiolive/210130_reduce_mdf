from asammdf import MDF
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
from matplotlib.widgets import Button

mdf = MDF("sample.dat")
signals = []
height_ratios = []
for num, signal in enumerate(mdf):
    if num > 20:
        break
    signals.append(signal)
    if signal.name == "service":
        height_ratios.append(2)
    else:
        height_ratios.append(1)
colors = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf"
]

subcolors = [
    "#aec7e8",
    "#ffbb78",
    "#98df8a",
    "#c5b0d5",
    "#c49c94",
    "#f7b6d2",
    "#c7c7c7",
    "#dbdb8d",
    "#9edae5"
]
color_index = 0
def get_color(colros=colors, proceed=True):
    global color_index
    color = colors[color_index]
    
    if proceed:
        color_index += 1
        if color_index >= len(colors):
            color_index = 0

    return color


class btn:
    def clicked(self, event):
        print("clicked")
        print(event)

#plt.ion()
fig, axes = plt.subplots(len(signals), 2, gridspec_kw={'height_ratios': height_ratios,'width_ratios': [1,10]}, sharex="col")
mplstyle.use('fast')

lines = []

iniBGs = []
for ax in axes:
    bg_left = fig.canvas.copy_from_bbox(ax[0].get_tightbbox(fig.canvas.get_renderer()))
    bg_right = fig.canvas.copy_from_bbox(ax[1].get_tightbbox(fig.canvas.get_renderer()))
    iniBGs.append([bg_left, bg_right])

print(axes[0][1].bbox)
print(axes[0][1].dataLim)
print(axes[0][1].viewLim)
print(axes[0][1].get_tightbbox(fig.canvas.get_renderer()))


for num, signal in enumerate(signals):
    ##get color
    color = get_color(colors, proceed=False)
    subcolor = get_color(subcolors, proceed=True)
    ##set grid
    axes[num][1].grid(b=True, which="major", color=subcolor, linestyle="dashed", alpha=0.2)
    axes[num][1].grid(b=True, which="minor", color=subcolor, linestyle="dashdot", alpha=0.2)
    ##plot
    lines_ = axes[num][1].plot(signal.timestamps, signal.samples, label=signal.name, linewidth=0.5, color=color)
    lines.append(lines_[0])
    xlim = axes[num][1].get_xlim()
    ylim = axes[num][1].get_ylim()
    ##set ticks color, fontsize
    axes[num][1].tick_params(axis="y", labelsize=6, labelcolor=color, color=subcolor)
    ##set xaxis not visible
    if num != len(signals) - 1:
        axes[num][1].tick_params(axis="x", labelsize=0, length=0, bottom=False)
        plt.setp(axes[num][1].get_xticklabels(), visible=False)
    ##set ylabel color
    axes[num][1].yaxis.label.set_color(color)
    ##set border visible
    axes[num][1].spines["top"].set_visible(False)
    axes[num][1].spines["right"].set_visible(False)
    axes[num][1].spines["bottom"].set_visible(False)
    axes[num][1].spines["left"].set_visible(True)
    ##set right border color
    axes[num][1].spines["left"].set_color(color)
    axes[num][1].patch.set_visible(False)
    
    '''
    axes[num][0].text(
        xlim[0] + (xlim[1]-xlim[0])*0.01,
        ylim[1],
        signal.name, size=6, horizontalalignment="left", verticalalignment="top", color=color,
        bbox=dict(boxstyle="round",
                   ec=(0.5, 0.5, 0.5),
                   fc=(1, 1, 1),
                   ),
       wrap = True 
    )

    '''
    axes[num][0].set_zorder(10)
    axes[num][0].patch.set_visible(False)
    axes[num][0].grid(False)
    axes[num][0].set_xticks([])
    axes[num][0].set_yticks([])
    axes[num][0].set_xlim([0,1])
    axes[num][0].set_ylim([0,1])
    axes[num][0].tick_params(labelsize=0)
    axes[num][0].yaxis.label.set_color(color)
    axes[num][0].spines["top"].set_visible(False)
    axes[num][0].spines["right"].set_visible(False)
    axes[num][0].spines["bottom"].set_visible(False)
    axes[num][0].spines["left"].set_visible(False)
    axes[num][0].text(
        0.95,
        1,
        signal.name, size=8, horizontalalignment="right", verticalalignment="top", color=color,
        bbox=dict(boxstyle="round",
                   ec=(0., 0., 0.),
                   fc=(1, 1, 1),
                   alpha=0.2
                   ),
       wrap = True 
    )

#Last row
num = len(signals) - 1
axes[num][1].spines["bottom"].set_visible(True)
axes[num][1].yaxis.label.set_color(color)
axes[num][1].xaxis.label.set_visible(True)
axes[num][1].tick_params(axis="x", labelsize=6, color="#000000")

print(axes[num][1].lines[0].get_xydata())    

if False:
    def hoge(e):
        print(e)
    buttons = []
    for num, signal in enumerate(signals):
        ax = axes[num][0]
        buttons.append(Button(ax, signal.name))
        buttons[num].on_clicked(hoge)

axes_for_vcursor = fig.subplots(1,2, gridspec_kw={"width_ratios":[1,10]})
ax_vcursor = axes_for_vcursor[1]
axes_for_vcursor[0].set_visible(False)
ax_vcursor.set_xlim(xlim)
ax_vcursor.set_ylim([0, 1])
ax_vcursor.set_zorder(20)
ax_vcursor.patch.set_visible(False)
ax_vcursor.grid(False)
ax_vcursor.set_xticks([])
ax_vcursor.set_yticks([])
ax_vcursor.tick_params(labelsize=0)
#ax_vcursor.spines["top"].set_visible(False)
#ax_vcursor.spines["right"].set_visible(False)
ax_vcursor.spines["bottom"].set_visible(False)
ax_vcursor.spines["left"].set_visible(False)
ax_vcursor.tick_params(axis="x", labelsize=0, length=0, bottom=False)
plt.setp(ax_vcursor.get_xticklabels(), visible=False)
line_vcursor = ax_vcursor.axvline(300, linewidth=2, color="red")


bg = fig.canvas.copy_from_bbox(fig.bbox)
pressed = False
key_pressed = {"control":False,
    "alt":False,
    "shift":False,
    "right":False,
    "left":False,
    "up":False,
    "down":False}
def motion(e):
    global bg, pressed
    print(e)
    if e.xdata:
        if pressed:
            line_vcursor.set_data([e.xdata]*2, [0, 1])
        if e.button == 2:
            zoom_cur = e.xdata
    #fig.canvas.restore_region(bg)
    #ax_vcursor.draw_artist(line_vcursor)
    #fig.canvas.blit(ax_vcursor.bbox)
    #fig.canvas.flush_events()

        

def press(e):
    print(e)
    global bg, line_vcursor, pressed
    pressed = True
    
    if e.xdata:
        if e.button == 2:
            zoom_start = e.xdata

def release(e):
    global bg, pressed
    pressed = False

def resize(e):
    print(e)
    for n, ax in enumerate(axes):
        bb = ax[1].get_lines()[0].clipbox
        ax[1].get_lines()[0].set_visible(False)
        print("line:", ax[1].get_lines()[0].clipbox)
        print("ax:", ax[1].get_tightbbox(fig.canvas.get_renderer()))
        iniBGs[n][1] = fig.canvas.copy_from_bbox(ax[1].get_tightbbox(fig.canvas.get_renderer()))
        ax[1].get_lines()[0].set_visible(True)
        
    fig.canvas.draw()
    bg = fig.canvas.copy_from_bbox(fig.bbox)

def draw(e):
    print(e)
    #bg = fig.canvas.copy_from_bbox(fig.bbox)

def scroll(e):
    print(e)
    global xlim, bg, axes, fig
    diff = (xlim[1] - xlim[0])*0.1
    if e.button == "up":
        if key_pressed["control"]:
            axes[-1][1].set_xlim( [xlim[0]+diff, xlim[1]-diff] )
            xlim = axes[-1][1].get_xlim()
            for n, axe in enumerate(axes):
                line = axe[1].get_lines()[0]
                fig.canvas.restore_region(iniBGs[n][1])
                axe[1].draw_artist(line)
            fig.canvas.blit(fig.bbox)
        else:
            axes[-1][1].set_xlim( [xlim[0]-diff, xlim[1]-diff] )
            xlim = axes[-1][1].get_xlim()
            fig.canvas.draw()
            bg = fig.canvas.copy_from_bbox(fig.bbox)
    elif e.button == "down":
        if key_pressed["control"]:
            axes[-1][1].set_xlim( [xlim[0]-diff, xlim[1]+diff] )
            xlim = axes[-1][1].get_xlim()
            #fig.canvas.draw()
            fig.canvas.blit(fig.bbox)
            bg = fig.canvas.copy_from_bbox(fig.bbox)
        else:
            axes[-1][1].set_xlim( [xlim[0]+diff, xlim[1]+diff] )
            xlim = axes[-1][1].get_xlim()
            fig.canvas.draw()
            bg = fig.canvas.copy_from_bbox(fig.bbox)

def key_press(e):
    global key_pressed
    print("key_press:", "key =", e.key, ",x =", e.x, ",y =", e.y, ",xdata =", e.xdata, ",ydata =", e.ydata, "inaxes =", e.inaxes)
    for key in e.key.split("+"):
        key_pressed[key] = True
    

def key_release(e):
    global key_pressed
    print("key_release:", "key =", e.key, ",x =", e.x, ",y =", e.y, ",xdata =", e.xdata, ",ydata =", e.ydata, "inaxes =", e.inaxes)
    key_pressed[e.key] = False


fig.canvas.mpl_connect("motion_notify_event", motion)
fig.canvas.mpl_connect("button_press_event", press)
fig.canvas.mpl_connect("button_release_event", release)
fig.canvas.mpl_connect("resize_event", resize)
fig.canvas.mpl_connect("draw_event", draw)
fig.canvas.mpl_connect("scroll_event", scroll)
fig.canvas.mpl_connect("key_press_event", key_press)
fig.canvas.mpl_connect("key_release_event", key_release)

#plt.show(block=False)
#plt.subplots_adjust(wspace=0, hspace=0)
plt.subplots_adjust(wspace=0.05, hspace=0)
#plt.show()

for n, ax in enumerate(axes):
    print(ax[1].get_tightbbox(fig.canvas.get_renderer()))
    iniBGs[n][1] = fig.canvas.copy_from_bbox(ax[1].get_tightbbox(fig.canvas.get_renderer()))

ax_vcursor.set_visible(False)
fig.canvas.draw()
bg = fig.canvas.copy_from_bbox(fig.bbox)
ax_vcursor.set_visible(True)

bb = axes[0][1].get_lines()[0].clipbox

plt.show()


input()