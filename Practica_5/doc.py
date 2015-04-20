import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D
#from matplotlib.widgets import Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import Tkinter as Tk
import ttk as T
matplotlib.use('TkAgg')
from polynomial_curve_fitting import polynomial_curve_fitting




class DrawPoints:
    def __init__(self, fig, ax):
        self.fig = fig        
        self.ax = ax
	self.points = None  
	self.N = 0      
	self.patchList = []
        self.exists_touched_circle = False
        self.cid_press = fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release_button = fig.canvas.mpl_connect('button_release_event',
                                                         self.on_release)

    def on_press(self, event):        
        if event.inaxes!=self.ax: return
	
        c = Circle((event.xdata, event.ydata), 0.2, color='b')
        patch=self.ax.add_patch(c)
	self.patchList.append(patch)
        ar = np.array([[event.xdata,event.ydata]])
        if self.points != None:
		self.points = np.concatenate((self.points,ar),axis=0)
 	else:
		self.points = ar
	self.N = self.N + 1
	self.fig.canvas.draw()
        
        
    def on_release(self, event):
        self.exists_touched_circle = False
        return

    def getN(self):
	if self.N == 0:
		return 10	
	else:
		return self.N

    def getPoints(self):
	if self.points != None:
		return self.points
	else:
		x = np.random.randint(-10, 10, size=(10, 2))
		for i in range (1,10):
			c = Circle((x[i,0], x[i,1]), 0.2, color='b')
        		patch=self.ax.add_patch(c)
			self.patchList.append(patch)
		return x

    def clearPoints(self):
	for c in self.patchList:
		c.remove()
	self.patchList = []
	self.points = None
	self.N = 0


class Window:

	def start(self,root,fig,ax):
		self.degree = None
		self.fig = fig
		self.ax = ax
		self.curve = None
		self.control = None
		self.L = 0
		button = Tk.Button(master=root, text='Quit', command=quit)
		button.pack(side=Tk.BOTTOM)

		points = Tk.Label(root, text="Points", font=("Helvetica", 14), bg = 'silver')
		points.place(x=5, y=40)

		method = Tk.Label(root, text="Method", font=("Helvetica", 14), bg = 'silver')
		method.place(x=445, y=40)
	
		#Degree
		label_D = Tk.Label(root, text="Degree", font=("Helvetica", 12), bg = 'silver')
		label_D.place(x=445, y=90)
		self.vD = Tk.StringVar()	
		lD_entry = Tk.Entry(root, textvariable=self.vD, width=3)
		lD_entry.place(x=505, y=90)
		
		#L
		label_L = Tk.Label(root, text="L", font=("Helvetica", 12), bg = 'silver')
		label_L.place(x=564, y=90)
		self.vL = Tk.StringVar()	
		lL_entry = Tk.Entry(root, textvariable=self.vL, width=3)
		lL_entry.place(x=584, y=90)

		bnewt = Tk.Button(master=root, text='Newton', command=self.newton) 
		bnewt.place(x=445, y=140)
		bnewt_lib = Tk.Button(master=root, text='Newton lib', command=self.newtonlib) 
		bnewt_lib.place(x=545, y=140)
	
		bls = Tk.Button(master=root, text='Least sq', command=self.ls) 
		bls.place(x=445, y=190)
		bls_lib = Tk.Button(master=root, text='Least sq lib', command=self.lslib) 
		bls_lib.place(x=545, y=190)
		
		self.vChev = Tk.IntVar()
		bchev = Tk.Checkbutton(master=root, text='Chebyshev', variable=self.vChev, font=("Helvetica", 12), bg = 'silver')
		bchev.place(x=445, y=240)
		bclear = Tk.Button(master=root, text='Clear', command=self.clear) 
		bclear.place(x=445, y=380)
		
		self.draw_points = DrawPoints(fig, ax)
		canvas.mpl_connect('key_press_event', self.draw_points)

	def draw(self, poly, x, color):
		self.clean_up()		
		self.curve = Line2D(poly[:, 0], poly[:, 1])
		self.control= Line2D(x[:, 0], x[:, 1])
		self.curve.set_color(color)
		self.ax.add_line(self.curve)
		self.fig.canvas.draw()

	def clean_up(self):
		if self.curve != None:
		   self.curve.remove()
		   self.curve = None
		
	def newton(self):
		N = self.draw_points.getN() 	
		if self.vChev.get():
			knots = 'chebyshev'
		else:
			knots = np.linspace(0, 1, N)
		x = self.draw_points.getPoints()
		num_points = 200
		poly = polynomial_curve_fitting(x, knots, method='newton',
		                      libraries=False, num_points=num_points)
		self.draw(poly,x,'cyan')
		
	def newtonlib(self):	
		N = self.draw_points.getN() 
		x = self.draw_points.getPoints()
		if self.vChev.get():
			knots = 'chebyshev'
		else:
			knots = np.linspace(0, 1, N)
		num_points = 200
		poly = polynomial_curve_fitting(x, knots, method='newton',
		                      libraries=True, num_points=num_points)	
		self.draw(poly,x,'navy')

	def ls(self):
		self.getD()
		self.getL()
		N = self.draw_points.getN() 
		x = self.draw_points.getPoints()
		if self.vChev.get():
			knots = 'chebyshev'
		else:
			knots = np.linspace(0, 1, N)
		num_points = 200
		
		poly = polynomial_curve_fitting(x, knots, method='least_squares', L=self.L,
                                      libraries=False, num_points=num_points, degree=self.degree)		
		self.draw(poly,x,'r')

	def lslib(self):
		self.getD()
		N = self.draw_points.getN() 
		x = self.draw_points.getPoints()
		if self.vChev.get():
			knots = 'chebyshev'
		else:
			knots = np.linspace(0, 1, N)
		num_points = 200
	
		poly = polynomial_curve_fitting(x, knots, method='least_squares',
                                      libraries=True, num_points=num_points, degree=self.degree)	
		self.draw(poly,x,'crimson')

	def clear(self):
		self.draw_points.clearPoints()
		self.clean_up()
		self.fig.canvas.draw()
	
	def on_key_event(self, event):
	    print('you pressed %s'%event.key)
	    key_press_handler(event, canvas, toolbar)

	def quit(self):
	    root.quit()     # stops mainloop
	    root.destroy()  # this is necessary on Windows to prevent
		            # Fatal Python Error: PyEval_RestoreThread: NULL tstate

	def getN(self, event):
		self.N = self.vN.get()

	def getD(self):
		if self.vD.get() != "":	
			self.degree = int(self.vD.get())
		else:
			self.degree = None

	def getL(self):
		if self.vL.get() != "":	
			self.L = float(self.vL.get())
		else:
			self.L = 0



if __name__ == '__main__':

	root = Tk.Tk()
	fig = plt.figure()
	ax = fig.add_subplot(111, aspect=1) 
	ax.set_xlim(-10, 10)    
	ax.set_ylim(-10, 10)
	plt.subplots_adjust(right=0.65)

	canvas = FigureCanvasTkAgg(fig, master=root)
	canvas.show()
	canvas.get_tk_widget().pack(side=Tk.TOP)

	toolbar = NavigationToolbar2TkAgg( canvas, root )
	toolbar.update()
	canvas._tkcanvas.pack()
	toolbar = Tk.Frame(root)
	toolbar.pack(side=Tk.BOTTOM, fill="x")
	
	window = Window()
	window.start(root,fig,ax)
	

	Tk.mainloop()

