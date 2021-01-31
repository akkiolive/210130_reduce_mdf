import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
from asammdf import MDF
import scipy.optimize
import numpy as np
import bisect



class MDFPlots():
	def __init__(self, mdf_filename):
		#load mdf
		self.mdf = MDF(mdf_filename, time_from_zero=False)
		
		#start matplotlib
		self.fig = plt.figure()
		mplstyle.use('fast')

		#add vcursor layor
		self.axes_vcursor = []
		self.line2d_vcursors = []
		self.add_vcursor(visible=False)

		#range
		self.xrange_min = 0
		self.xrange_max = 0
		self.yrange_min = 0
		self.yrange_max = 0

		#load target signals to plot
		self.signals = []
		for num, signal in enumerate(self.mdf):
			self.signals.append(signal)
			if num > 20:
				break

		#make subplot areas
		self.axes = []
		for num, signal in enumerate(self.signals):
			ax = self.fig.add_subplot(len(self.signals), 1, num+1)
			self.axes.append(ax)

		#set plots
		for num, signal in enumerate(self.signals):
			ax = self.axes[num]
			ax.set_title(signal.name, loc="left")
			ax.spines["top"].set_visible(False)
			ax.spines["bottom"].set_visible(False)
			ax.spines["right"].set_visible(False)
			ax.axes.set_xticks([])
			ax.patch.set_alpha(0)
			ax.grid(axis="y", linestyle="--", linewidth=0.6)
			ax.plot(signal.timestamps, signal.samples)
			xrange = ax.set_xlim()
			yrange = ax.set_ylim()
			self.xrange_min = min((self.xrange_min, xrange[0]))
			self.xrange_max = max((self.xrange_max, xrange[1]))
			self.yrange_max = min((self.yrange_max, yrange[0]))
			self.yrange_max = max((self.yrange_max, yrange[1]))
		
		for ax in plt.gcf().get_axes():
			ax.set_xlim(left=self.xrange_min, right=self.xrange_max)

		self.fig.canvas.draw()
		self.background = self.fig.canvas.copy_from_bbox(self.fig.get_clip_box())
		self.ax_vcursor.set_visible(True)

		#connect event
		self.click = False
		self.cids = []
		self.connect()
		
		#show
		plt.subplots_adjust(hspace=1, wspace=0)
		plt.show()




	def add_vcursor(self, lw=0.8, color="orange", visible=True):
		self.ax_vcursor = self.fig.add_subplot(1,1,1)
		self.line2d_vcursor = self.ax_vcursor.axvline(0, lw=lw, color=color)
		self.ax_vcursor.patch.set_alpha(0)
		self.ax_vcursor.spines["top"].set_visible(False)
		self.ax_vcursor.spines["bottom"].set_visible(False)
		self.ax_vcursor.spines["left"].set_visible(False)
		self.ax_vcursor.spines["right"].set_visible(False)
		self.ax_vcursor.axes.set_xticks([])
		self.ax_vcursor.axes.set_yticks([])
		self.ax_vcursor.set_visible(visible)
		self.axes_vcursor.append(self.ax_vcursor)

	def set_vcursor(self, x=None, visible_force=None, visible_switch=False, redraw=True):
		#set x
		if x is not None:
			data = self.line2d_vcursor.get_data()
			x1 = data[0][0]
			y1 = data[1][0]
			x2 = data[0][1]
			y2 = data[1][1]
			x1 = x
			x2 = x1
			self.line2d_vcursor.set_data([[x1, x2], [y1, y2]])
		#set visiblity
		if visible_force is not None:
			self.line2d_vcursor.set_visible(visible_force)
		elif visible_switch:
			self.line2d_vcursor.set_visible(not self.line2d_vcursor.get_visible())
		#apply change
		elif redraw:
			#self.line2d_vcursor.figure.canvas.draw() #too slow...
			self.fig.canvas.restore_region(self.background)
			self.ax_vcursor.draw_artist(self.line2d_vcursor)
			self.fig.canvas.blit(self.ax_vcursor.bbox)

	def update_value_at_vcursor(self, x):
		for num, signal in enumerate(self.signals):
			x = self.line2d_vcursor.get_data()[0][0]
			idx = find_nearest_index_bisection(signal.timestamps, x)
			timestamp = signal.timestamps[idx]
			value = signal.samples[idx]
			ax = self.axes[num]
			ax.set_title(signal.name + "=" + str(value) + " at " + str(timestamp))
			ax.draw_artist(ax)


	def onRelease(self, e):
		self.click = False
		self.ax_vcursor.set_visible(False)
		self.fig.canvas.draw()
		#self.background = self.fig.canvas.copy_from_bbox(self.fig.get_clip_box())
		self.background = self.fig.canvas.copy_from_bbox(self.axes[1].bbox)
		self.ax_vcursor.set_visible(True)
		self.fig.canvas.draw()
		
	def onClick(self, e):
		#debug print
		print(e)
		self.click = True
		#set vcursor
		self.set_vcursor(x=e.xdata)
		#find near sample by vcursor
		if e.xdata and False:
			self.update_value_at_vcursor(e.xdata)
			

	def onMotion(self, e):
		if self.click:
			#vcursor
			self.set_vcursor(x=e.xdata)
			#near sample by vcursor
			if e.xdata and False:
				self.update_value_at_vcursor(e.xdata)

	def onDraw(self, e):
		print(e)

	def connect(self):
		self.cids.append(self.fig.canvas.mpl_connect("button_press_event", self.onClick))
		self.cids.append(self.fig.canvas.mpl_connect("button_release_event", self.onRelease))
		self.cids.append(self.fig.canvas.mpl_connect("motion_notify_event", self.onMotion))
		self.cids.append(self.fig.canvas.mpl_connect("draw_event", self.onDraw))







def find_nearest_index_bisection(data_list, hook_value, eps=0.5):
	idx = bisect.bisect(data_list, hook_value)
	better_idx = None
	if idx >= 0 and idx <= len(data_list) - 1 and data_list[idx] == hook_value:
		return idx
	neis = [float("inf"), float("inf"), float("inf")]
	if idx > 0:
		neis[0] = abs(data_list[idx-1] - hook_value)
	if idx >= 0 and idx <= len(data_list) - 1:
		neis[1] = abs(data_list[idx] - hook_value)
	if idx < len(data_list) - 1:
		neis[2] = abs(data_list[idx+1] - hook_value)
	nearest_idx = idx + neis.index(min(neis)) - 1
	if abs(data_list[nearest_idx] - hook_value) <= eps:
		return nearest_idx
	else:
		return None



MDFPlots("sample.dat")