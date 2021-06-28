from controller.controller import *
from repository.repository import *
from ui import *

if __name__ == '__main__':
    repository = Repository()
    controller = Controller(repository)
    ui = UI(controller, repository)
    ui.menu()