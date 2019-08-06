"""
Created on Fri Apr 19 2019
Description: Derivatives Pricing Calculator

@author: Siping Wang
"""
from tkinter import *
from option import Option


class Base():
    def __init__(self, master):
        self.root = master
        self.root.config()
        self.root.title('Derivatives Pricing Calculator')
        self.root.geometry('400x400')
        Initface(self.root)


class Initface():
    def __init__(self, master):
        self.__author = 'Siping Wang @THU'
        self.master = master
        self.master.config(bg='Aquamarine')
        self.initface = Frame(self.master)
        self.initface.pack(expand=YES, fill=X, anchor=CENTER)
        option_button = Button(self.initface, text='click here to start', command=self.change_to_option)
        option_button.pack()
        author = Label(self.initface, text='by '+self.__author)
        author.pack(side=BOTTOM, fill=X)

    def change_to_option(self):
        self.initface.destroy()
        OptionCalc(self.master)


class OptionCalc():
    def __init__(self, master):
        self.master = master
        self.master.config(bg='blue')
        self.optioncalc = Frame(self.master)
        self.optioncalc.pack(expand=YES, fill=BOTH, anchor=CENTER)
        Label(self.optioncalc, text='Please input relevant parameters, '
                 'then click "Calculate" button.').grid(row=0, column=0, columnspan=3)
        Label(self.optioncalc, text='Click "back" to the main page.').grid(columnspan=3)
        Label(self.optioncalc, text='Option Type').grid(row=2, column=0, sticky=W)

        self.cp = StringVar()
        Radiobutton(self.optioncalc, text='Call', variable=self.cp, value='Call').grid(row=2, column=1)
        Radiobutton(self.optioncalc, text='Put', variable=self.cp, value='Put').grid(row=2, column=2)

        plist = ['Current Price', 'Strike Price', 'Days to Maturity',
                 'Risk-free Rate', 'Volatility', 'Continuous Dividend Rate', 'Monte Carlo Iteration']
        self.elist = []
        r = 3
        for param in plist:
            Label(self.optioncalc, text=param).grid(column=0, sticky=W)
            e = Entry(self.optioncalc)
            e.grid(row=r, column=1, columnspan=2, sticky=W + E)
            self.elist.append(e)
            r += 1

        Button(self.optioncalc, text='Calculate', command=self.calc).grid(row=r, column=1, columnspan=2, sticky=W)
        r += 1

        self.answ = Label(self.optioncalc, text='The result is as follows:')
        self.answ.grid(row=r, columnspan=3)
        r += 1

        self.bs = Label(self.optioncalc)
        self.mc = Label(self.optioncalc)
        self.bs.grid(row=r, columnspan=2, sticky=E)
        self.mc.grid(row=r + 1, columnspan=2, sticky=E)

        Label(self.optioncalc, text='Use Black-Scholes formula: ').grid(row=r, sticky=W)
        Label(self.optioncalc, text='Use Monte Carlo simulation: ').grid(row=r + 1, sticky=W)

        Button(self.optioncalc, text='back', command=self.goBack).grid(row=1, column=1, columnspan=2, sticky=E)

    def calc(self):
        # check if inputs are all numbers
        vlist = []
        for e in self.elist:
            try:
                p = float(e.get())
                vlist.append(p)
            except:
                self.answ.config(text='Invalid Input(s). Please input correct parameter(s)', fg='red')
                e.delete(0, len(e.get()))
                return 0
        # check if all inputs are > 0 (except for the risk-free rate)
        for i in range(6):
            if i != 3 and vlist[i] < 0:
                self.answ.config(text='Invalid Input(s). Please input correct parameter(s)', fg='red')
                self.elist[i].delete(0, len(self.elist[i].get()))
                return 0

        vlist[6] = int(vlist[6])

        obj = Option(self.cp.get(), vlist[0], vlist[1], vlist[2] / 365, vlist[3], vlist[4], vlist[5])
        self.answ.config(text='The result is as follows:', fg='black')
        self.bs.config(text=str("%.8f" % obj.BlackScholesPricing()))
        self.mc.config(text=str("%.8f" % obj.MonteCarloPricing(iteration=vlist[6])))

    def goBack(self):
        self.optioncalc.destroy()
        Initface(self.master)


if __name__ == '__main__':
    root = Tk()
    Base(root)
    root.mainloop()