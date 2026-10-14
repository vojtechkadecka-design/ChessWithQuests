from Controller.controller import Controller
from View.tkinter_view import TkinterView


def main():
    controller = Controller()
    view = TkinterView(controller)
    view.spustit()


if __name__ == "__main__":
    main()
