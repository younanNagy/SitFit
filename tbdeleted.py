try:                        # In order to be able to import tkinter for
    import tkinter as tk    # either in python 2 or in python 3
except ImportError:
    import Tkinter as tk


def upon_select(widget):
    print("{}'s value is {}.".format(widget['text'], widget.var.get()))


if __name__ == '__main__':
    root = tk.Tk()
    names = {"Chester", "James", "Mike"}
    username_cbs = dict()
    for name in names:
        username_cbs[name] = tk.Checkbutton(root, text=name,
                                                onvalue=True, offvalue=False)
        username_cbs[name].var = tk.BooleanVar()
        username_cbs[name]['variable'] = username_cbs[name].var
        username_cbs[name]['command'] = lambda w=username_cbs[name]: \
                                                                upon_select(w)
        username_cbs[name].pack()
    tk.mainloop()
