import gui.window


class Glampy(object):
    def __init__(self):
        self.main_window = gui.window.Main()


if __name__ == '__main__':
    # cli.config.Service.start('apache2')
    # print cli.config.Service.status('apache2')
    Glampy()
