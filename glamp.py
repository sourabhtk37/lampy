import gui.window


class Glamp:
    def __init__(self):
        self.main_window = gui.window.Main()
        self.main_window.main()


app = Glamp()
