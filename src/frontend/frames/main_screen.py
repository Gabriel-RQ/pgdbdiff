from . import FRAME_SelectDatabase, FRAME_ShowDiff
from customtkinter import CTkFrame, CTkFont, NSEW


class FRAME_MainScreen(CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)

        self._create_widgets()

    def _create_widgets(self) -> None:
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self._frame_showdiff = FRAME_ShowDiff(self)
        self._frame_selectdb = FRAME_SelectDatabase(
            self,
            compare_btn_command=self._frame_showdiff.on_do_diff,
        )

        self._frame_selectdb.grid(
            row=0,
            column=0,
            padx=12,
            pady=12,
            ipadx=12,
            ipady=12,
            sticky=NSEW,
        )

        self._frame_showdiff.grid(
            row=0,
            column=1,
            padx=12,
            pady=12,
            sticky=NSEW,
        )
