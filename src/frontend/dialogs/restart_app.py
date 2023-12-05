from customtkinter import CTkInputDialog, CTkLabel, CTkButton, CTk, W, EW
from frontend.util import centered


@centered
class DIALOG_RestartApp(CTkInputDialog):
    def __init__(self) -> None:
        self.WIDTH, self.HEIGHT = 500, 120
        super().__init__()

    def _create_widgets(self):
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        self._label = CTkLabel(
            self,
            text="Application needs to restart to apply the changes. Close?",
        )
        self._label.grid(row=0, column=0, sticky=W, pady=12, padx=8)

        self._ok_button = CTkButton(self, text="Yes", command=self._ok_event, width=120)
        self._ok_button.grid(row=1, column=0, columnspan=1, padx=12, pady=6, sticky=EW)

        self._cancel_button = CTkButton(
            self, text="No", command=self._cancel_event, width=120
        )
        self._cancel_button.grid(
            row=1, column=1, columnspan=1, padx=12, pady=6, sticky=EW
        )

    def _ok_event(self, event=None):
        self.grab_release()
        self.destroy()

        if isinstance(self.master, CTk):
            self.master.destroy()

    def get_input(self):
        self.master.wait_window(self)
