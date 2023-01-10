from matplotlib.figure import Figure
from tkinter import filedialog as fd
from functools import partial
from pandastable import Table
from tkinter import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

from app.helper.prediction import predictDirection


def select_file():
    filetypes = (
        ('text files', '*.csv'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    print(filename)
    run = Button(master=frame1,
                 command=partial(RunModel, filename),
                 bg='#5a7ee8', fg='white',
                 text="Execute file")
    run.pack(side=LEFT, padx=10, pady=0)


def RunModel(filename):
    df, accuracy, verses_df = predictDirection(filename)

    acc = Label(frame2, text="Accuracy Of Model: {} %".format(accuracy))
    acc.pack(side=LEFT, padx=10, pady=0)
    plotPrediction(verses_df)
    DataTable(df)


def plotPrediction(df):
    f = Figure(figsize=(10, 4), dpi=100)
    ax = f.add_subplot(121)
    ax2 = f.add_subplot(122)
    ax.plot(df['Actual'].to_list())
    ax2.plot(df['Predicted'].to_list(), 'r:')

    ax.set_title('Actual')
    ax.set_ylabel('Close Price')

    ax2.set_title('Predicted')
    ax2.set_ylabel('Close Price')

    canvas = FigureCanvasTkAgg(f,
                               master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    toolbar = NavigationToolbar2Tk(canvas,
                                   window)
    toolbar.update()
    canvas.get_tk_widget().pack()


def DataTable(df):
    pt = Table(frame3, dataframe=df,
               showtoolbar=True, showstatusbar=True)
    pt.show()


# the main Tkinter window
window = Tk()
window.title("Stock Market (Price & Direction Predictor) App")

# dimensions of the main window
window.geometry("1000x820+400+50")

# button that displays the plot

frame1 = Frame(window)
frame1.pack(fill=X)
lbl1 = Label(frame1, text="Choose csv file: ", width=15)
lbl1.pack(side=LEFT, padx=0, pady=0)
open_button = Button(
    frame1,
    text='Choose a File',
    bg='#5a7ee8', fg='white',
    command=select_file
)
open_button.pack(side=LEFT, padx=5, pady=5)

frame2 = Frame(window)
frame2.pack(fill=X)

frame3 = Frame(window)
frame3.pack(fill=X)
# run the gui
window.mainloop()
