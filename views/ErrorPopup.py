import tkinter as tk
from views.View import View

class ErrorPopup(View):
    def __init__(self, error, webService):
        self.error = error
        super().__init__(webService)

    def createFrontend(self):
        window = tk.Toplevel()
        window.title("Error")

        label = tk.Label(window, text=self.error)
        label.pack()

        window.mainloop()