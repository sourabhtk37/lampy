import gui.window


class Glampy(object):
    def __init__(self):
        self.main_window = gui.window.Main()
        self.main_window.main()

if __name__ == '__main__':
    Glampy()
