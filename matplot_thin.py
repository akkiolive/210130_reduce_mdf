from asammdf import MDF
import matplotlib.pyplot as plt
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

plt.ion()
fig, axes = plt.subplots(len(signals), 2, gridspec_kw={'height_ratios': height_ratios,'width_ratios': [1,10]})

for num, signal in enumerate(signals):
    ##get color
    color = get_color(colors, proceed=False)
    subcolor = get_color(subcolors, proceed=True)
    ##set grid
    axes[num][1].grid(b=True, which="major", color=subcolor, linestyle="dashed", alpha=0.2)
    axes[num][1].grid(b=True, which="minor", color=subcolor, linestyle="dashdot", alpha=0.2)
    ##plot
    axes[num][1].plot(signal.timestamps, signal.samples, label=signal.name, linewidth=0.5, color=color)
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

ax = fig.subplots(1,2, gridspec_kw={"width_ratios":[1,10]})
ax[0].set_visible(False)
ax[1].set_xlim(xlim)
ax[1].set_ylim([0, 1])
ax[1].set_zorder(-10)
ax[1].patch.set_visible(False)
ax[1].grid(False)
ax[1].set_xticks([])
ax[1].set_yticks([])
ax[1].tick_params(labelsize=0)
ax[1].spines["top"].set_visible(False)
ax[1].spines["right"].set_visible(False)
ax[1].spines["bottom"].set_visible(False)
ax[1].spines["left"].set_visible(False)
ax[1].tick_params(axis="x", labelsize=0, length=0, bottom=False)
plt.setp(ax[1].get_xticklabels(), visible=False)
lines = ax[1].plot([300, 300], [0, 1], linewidth=2, color="red")
line = lines[0]

def motion(e):
    print(e)
    if e.xdata:
        line.set_data([e.xdata]*2, [0, 1])
        if e.button == 2:
            zoom_cur = e.xdata
        

def press(e):
    print(e)
    if e.xdata:
        if e.button == 2:
            zoom_start = e.xdata
fig.canvas.mpl_connect("motion_notify_event", motion)
fig.canvas.mpl_connect("button_press_event", press)

#plt.show(block=False)
#plt.subplots_adjust(wspace=0, hspace=0)
plt.subplots_adjust(wspace=0.05, hspace=0)
#plt.show()
fig.canvas.draw()

input()