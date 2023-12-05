import atexit, logging
from customtkinter import CTk, CTkTabview, NSEW
from .util import centered
from .frames import FRAME_MainScreen, FRAME_ConfigScreen
from .dialogs import DIALOG_DatabaseInfo
from backend.configs import CONFIGS, save_config


@centered
class App(CTk):
    def __init__(self) -> None:
        super().__init__()

        self.WIDTH, self.HEIGHT = 1280, 720
        self.minsize(800, 600)
        self.title("PGDB Diff")

        if CONFIGS["APP"].getboolean("first_use"):
            DIALOG_DatabaseInfo().get_input()

        try:
            self._create_widgets()
            CONFIGS["APP"]["first_use"] = "false"
            atexit.register(save_config)
        except Exception as e:
            logging.error(f"Could not display widgets. Detail: {e}")
            exit(1)

    def _create_widgets(self) -> None:
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._tabview = CTkTabview(self)
        self._tabview.grid(row=0, column=0, sticky=NSEW, padx=5, pady=(0, 5))

        self._tabview.add("Main")
        self._tabview.add("Configuration")
        self._tabview.set("Main")

        self._frame_mainscreen = FRAME_MainScreen(self._tabview.tab("Main"))
        self._frame_mainscreen.pack(anchor="center", fill="both", expand=True)
        self._frame_config_screen = FRAME_ConfigScreen(
            self._tabview.tab("Configuration")
        )
        self._frame_config_screen.pack(anchor="center", expand=True)

    def run(self) -> None:
        self.mainloop()
