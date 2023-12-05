from customtkinter import CTkInputDialog, CTk
from frontend.util import centered


@centered
class DIALOG_DatabaseInfo(CTkInputDialog):
    def __init__(self) -> None:
        self.WIDTH, self.HEIGHT = 360, 550
        super().__init__(title="Database information")

    def _create_widgets(self) -> None:
        from frontend.frames import FRAME_ConfigScreen

        self._frame_configscreen = FRAME_ConfigScreen(self)
        self._frame_configscreen.pack(anchor="center", expand=True)

        self.bind("<Return>", self._close_on_return)

    def _close_on_return(self, event) -> None:
        self._frame_configscreen._save_config_command()
        self._ok_event()

    def _on_closing(self):
        super()._on_closing()

        if isinstance(self.master, CTk):
            self.master.destroy()

    def _ok_event(self, event=None):
        self.grab_release()
        self.destroy()

    def get_input(self):
        self.master.wait_window(self)
        return None
