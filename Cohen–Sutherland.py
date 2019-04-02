from tkinter import Tk, Radiobutton, IntVar, Label, Button, Entry, Frame, filedialog
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from scipy.special import comb
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import tkinter
import random
import csv
import gc


class RecLineArea(object):
    # Базовый конструктор
    def __init__(self):
        # Количество точек и список линий
        self.amountLines = 3
        self.lines = []
        self.min = 0
        self.max = 10
        # Задаём координаты прямоугольника и его базовых угловых точек
        self.someX1, self.someY1 = 0, 0
        self.xsize, self.ysize = 3, 4
        self.someX2, self.someY2 = self.someX1 + self.xsize, self.someY1
        self.someX3, self.someY3 = self.someX1 + self.xsize, self.someY1 + self.ysize
        self.someX4, self.someY4 = self.someX1, self.someY1 + self.ysize
        self.recLine1X = np.array([self.someX1, self.someX2])
        self.recLine1Y = np.array([self.someY1, self.someY2])
        self.recLine2X = np.array([self.someX2, self.someX3])
        self.recLine2Y = np.array([self.someY2, self.someY3])
        self.recLine3X = np.array([self.someX3, self.someX4])
        self.recLine3Y = np.array([self.someY3, self.someY4])
        self.recLine4X = np.array([self.someX4, self.someX1])
        self.recLine4Y = np.array([self.someY4, self.someY1])
        # Формируем прямоугольник
        self.recLine1 = np.array([self.recLine1X,self.recLine1Y])
        self.recLine2 = np.array([self.recLine2X,self.recLine2Y])
        self.recLine3 = np.array([self.recLine3X,self.recLine3Y])
        self.recLine4 = np.array([self.recLine4X,self.recLine4Y])
        # Генерируем линии
        xR = np.array([-1, 3])
        yR = np.array([1, 5])
        lineR = np.array([xR,yR])
        self.lines.append(lineR)
        xR = np.array([-1, 5])
        yR = np.array([2, 2])
        lineR = np.array([xR,yR])
        self.lines.append(lineR)
        xR = np.array([1, 4])
        yR = np.array([-1, 0])
        lineR = np.array([xR,yR])
        self.lines.append(lineR)
        # Рисуем линии
        for i in range(self.amountLines):
            lineR = self.lines[i]
            plt.plot(lineR[0], lineR[1], marker = 'o')

    def create_rec(self,someX1,someY1,xsize,ysize):
        self.someX2, self.someY2 = someX1 + xsize, someY1
        self.someX3, self.someY3 = someX1 + xsize, someY1 + ysize
        self.someX4, self.someY4 = someX1, someY1 + ysize

        self.recLine1X = np.array([someX1, self.someX2])
        self.recLine1Y = np.array([someY1, self.someY2])

        self.recLine2X = np.array([self.someX2, self.someX3])
        self.recLine2Y = np.array([self.someY2, self.someY3])

        self.recLine3X = np.array([self.someX3, self.someX4])
        self.recLine3Y = np.array([self.someY3, self.someY4])

        self.recLine4X = np.array([self.someX4, someX1])
        self.recLine4Y = np.array([self.someY4, someY1])

        #rectangle
        self.recLine1 = np.array([self.recLine1X,self.recLine1Y])
        self.recLine2 = np.array([self.recLine2X,self.recLine2Y])
        self.recLine3 = np.array([self.recLine3X,self.recLine3Y])
        self.recLine4 = np.array([self.recLine4X,self.recLine4Y])

    def generate(self):
        self.lines.clear()
        for i in range(self.amountLines):
            xR = np.array([random.uniform(self.min,self.max), random.uniform(self.min,self.max)])
            yR = np.array([random.uniform(self.min,self.max), random.uniform(self.min,self.max)])
            lineR = np.array([xR,yR])
            self.lines.append(lineR)

    # Функция кнопки "Ввести число отрезков"
    def get_amount(self,line_entry,fig,canvas):
        amount = int(line_entry.get())
        self.amountLines = amount
        self.generate()
        self.drawCS(fig,canvas)

    # Функция кнопки "Ввести Xmin"
    def get_amountX(self,line1_entry,fig,canvas):
        amount = int(line1_entry.get())
        self.min = amount

    # Функция кнопки "Ввести Xmax"
    def get_amountY(self,line2_entry,fig,canvas):
        amount = int(line2_entry.get())
        self.max = amount

    def gen_rec(self,width_entry, height_entry, X_entry, Y_entry,fig,canvas):
        width = int(width_entry.get())
        height = int(height_entry.get())
        X = int(X_entry.get())
        Y = int(Y_entry.get())
        self.someX1 = X
        self.someY1 = Y
        self.xsize = width
        self.ysize = height
        self.create_rec(self.someX1,self.someY1,self.xsize,self.ysize)
        self.drawCS(fig,canvas)

    # Рисуем кривую Безье
    def drawCS(self,fig,canvas):
        fig.clf()
        # Сетка 1x1, 2Д - проекция
        ax = fig.add_subplot(111)
        ax.grid(True)
        ax.set_xlabel('X',
              fontsize = 15,    #  размер шрифта
              color = 'red',    #  цвет шрифта
        )

        ax.set_ylabel('Y',
              fontsize = 15,
              color = 'red',
        )
        for i in range(self.amountLines):
            lineR = self.lines[i]
            ax.plot(lineR[0], lineR[1], marker = 'o')
        ax.plot(self.recLine1[0], self.recLine1[1], c = 'black')
        ax.plot(self.recLine2[0], self.recLine2[1], c = 'black')
        ax.plot(self.recLine3[0], self.recLine3[1], c = 'black')
        ax.plot(self.recLine4[0], self.recLine4[1], c = 'black')
        canvas.draw()    

    def cohensutherland(self,xmin, ymax, xmax, ymin, x1, y1, x2, y2):

        INSIDE, LEFT, RIGHT, LOWER, UPPER = 0, 1, 2, 4, 8

        def getclip(xa, ya):
            p = INSIDE  

            if xa < xmin:
                p |= LEFT
            elif xa > xmax:
                p |= RIGHT

            if ya < ymin:
                p |= LOWER  
            elif ya > ymax:
                p |= UPPER  
            return p

        k1 = getclip(x1, y1)
        k2 = getclip(x2, y2)

        while (k1 | k2) != 0: 

            if (k1 & k2) != 0:  
                return None, None, None, None

            # non-trivial case, at least one point outside window
            # this is not a bitwise or, it's the word "or"
            opt = k1 or k2  # take first non-zero point, short circuit logic
            if opt & UPPER:  # these are bitwise ANDS
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            elif opt & LOWER:
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif opt & RIGHT:
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif opt & LEFT:
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin
            else:
                raise RuntimeError('Undefined clipping state')

            if opt == k1:
                x1, y1 = x, y
                k1 = getclip(x1, y1)
            
            elif opt == k2:
                x2, y2 = x, y
                k2 = getclip(x2, y2)
        return x1, y1, x2, y2

    def drawCutCS(self,fig,canvas):
        fig.clf()
        # Сетка 1x1, 2Д - проекция
        ax = fig.add_subplot(111)
        ax.grid(True)
        ax.set_xlabel('X',
              fontsize = 15,    #  размер шрифта
              color = 'red',    #  цвет шрифта
        )

        ax.set_ylabel('Y',
              fontsize = 15,
              color = 'red',
        )
        for i in range(self.amountLines):
            lineR = self.lines[i]
            ax.plot(lineR[0], lineR[1], marker = 'o')
        ax.plot(self.recLine1[0], self.recLine1[1], c = 'black')
        ax.plot(self.recLine2[0], self.recLine2[1], c = 'black')
        ax.plot(self.recLine3[0], self.recLine3[1], c = 'black')
        ax.plot(self.recLine4[0], self.recLine4[1], c = 'black')
        
        for i in range(self.amountLines):
            lineR = self.lines[i]
            pointX = lineR[0]
            pointY = lineR[1]
            x1 = pointX[0]
            y1 = pointY[0]
            x2 = pointX[1]
            y2 = pointY[1]
            cx1,cy1,cx2,cy2 = self.cohensutherland(self.someX1,self.someY3,self.someX2,self.someY2, x1,y1,x2,y2)
            if ((cx1 != None) and (cy1 != None) and (cx2 != None) and (cy2 != None)):
                xR = np.array([cx1, cx2])
                yR = np.array([cy1, cy2])
                lineR = np.array([xR,yR])
                #self.lines[i] = lineR
                self.lines.append(lineR)
                ax.plot(lineR[0], lineR[1], c = 'deeppink', ls = '-', lw = '3', marker = '8')
        canvas.draw()    



# Функция кнопки "Выход"
def quit(root):
    root.quit()     
    root.destroy() 

def main():
    CohenSutherland = RecLineArea()
    # Cоздаём главное окно
    root = Tk()
    # Ширина экрана
    w = root.winfo_screenwidth() 
    # Высота экрана
    h = root.winfo_screenheight() 
    w = w//2 - 300
    h = h//2 - 200
    root.geometry('+{}+{}'.format(w, h))
    
    root.title("Алгоритм Коэна — Сазерленда")
    line_infoLabel = Label(root, text="Введите количество линий: ",font=("Consolas", 10, "bold"))
    line_entry = Entry(root,width=10)
    line12_infoLabel = Label(root, text="Введите диапозон генерации линий по X,Y: ",font=("Consolas", 10, "bold"))
    line1_entry = Entry(root,width=10)
    line1_but = Button(root,text="Ввести", command= lambda: CohenSutherland.get_amountX(line1_entry, fig,canvas))
    line2_entry = Entry(root,width=10)
    line2_but = Button(root,text="Ввести", command= lambda: CohenSutherland.get_amountY(line2_entry, fig,canvas))
    rec12_infoLabel = Label(root, text="Введите ширину сдвига прямоугольника по горизонтали и вертикали: ",font=("Consolas", 10, "bold"))
    width_entry = Entry(root,width=10)
    height_entry = Entry(root,width=10)
    rec34_infoLabel = Label(root, text="Введите X, Y- координату нижней левой точки: ",font=("Consolas", 10, "bold"))
    X_entry = Entry(root,width=10)
    Y_entry = Entry(root,width=10)
    line_but = Button(root,text="Ввести и сгенерировать", command= lambda: CohenSutherland.get_amount(line_entry, fig,canvas))
    rec_but = Button(root,text="Ввести и сгенерировать", command= lambda: CohenSutherland.gen_rec(width_entry, height_entry, X_entry, Y_entry, fig,canvas))
    
    cut_but = Button(root,text="Выделить отрезки внутри", command= lambda: CohenSutherland.drawCutCS(fig,canvas))
    
    line_infoLabel.pack(side=tkinter.TOP)
    line_entry.pack(side=tkinter.TOP)
    line_but.pack(side=tkinter.TOP)

    line12_infoLabel.pack(side=tkinter.TOP)
    line1_entry.pack(side=tkinter.TOP)
    line1_but.pack(side=tkinter.TOP)

    line2_entry.pack(side=tkinter.TOP)
    line2_but.pack(side=tkinter.TOP)
    
    rec12_infoLabel.pack(side=tkinter.TOP)
    width_entry.pack(side=tkinter.TOP)
    height_entry.pack(side=tkinter.TOP)

    # Формиурем фигуру кривой и "холст" + панель
    fig = plt.figure()
    canvas = FigureCanvasTkAgg(fig, master=root)  
    toolbar = NavigationToolbar2Tk(canvas, root)
    
    exButton = tkinter.Button(master=root, text="Выход", command= lambda: quit(root))
    
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    toolbar.pack()
    
    rec34_infoLabel.pack(side=tkinter.LEFT)
    X_entry.pack(side=tkinter.LEFT)
    Y_entry.pack(side=tkinter.LEFT)
    
    
    exButton.pack(side=tkinter.BOTTOM)
    rec_but.pack(side=tkinter.BOTTOM)
    cut_but.pack(side=tkinter.BOTTOM)
    
    

    CohenSutherland.drawCS(fig,canvas)
    # Собираем мусор и обновляем окно
    gc.collect()
    root.update()
    root.mainloop()
    
if __name__ == '__main__':
    main()
