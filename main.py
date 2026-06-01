import os
import tkinter as tk
from src.controllers import AkinatorController
from src.views import AkinatorView

def main():

    os.environ["TCL_LIBRARY"] = r"C:\Users\MY\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
    os.environ["TK_LIBRARY"] = r"C:\Users\MY\AppData\Local\Programs\Python\Python313\tcl\tk8.6"

    root = tk.Tk()
    controller = AkinatorController()
    view = AkinatorView(root, controller)
    controller.set_view(view)
    root.mainloop()

if __name__ == "__main__":
    main()