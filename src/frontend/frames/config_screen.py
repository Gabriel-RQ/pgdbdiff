from customtkinter import (
    CTkFrame,
    CTkLabel,
    CTkEntry,
    CTkFont,
    CTkButton,
    CTkInputDialog,
    NSEW,
    W,
    END,
)
from frontend.dialogs import DIALOG_RestartApp
from backend.configs import CONFIGS, save_config


class FRAME_ConfigScreen(CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)

        self._create_widgets()
        self._fill_entries()

    def _create_widgets(self) -> None:
        entry_label_font = CTkFont(size=14, weight="bold")
        entry_label_pady = (12, 6)
        entry_width = 240
        entry_height = 36
        widget_padx = 20

        # database user
        self._db_user_label = CTkLabel(
            self, text="Database user:", font=entry_label_font
        )
        self._db_user_label.grid(
            row=0, column=0, sticky=W, pady=entry_label_pady, padx=widget_padx
        )

        self._db_user_entry = CTkEntry(self, width=entry_width, height=entry_height)
        self._db_user_entry.grid(row=1, column=0, sticky=NSEW, padx=widget_padx)

        # database host
        self._db_host_label = CTkLabel(
            self, text="Database host:", font=entry_label_font
        )
        self._db_host_label.grid(
            row=2, column=0, sticky=W, pady=entry_label_pady, padx=widget_padx
        )

        self._db_host_entry = CTkEntry(self, width=entry_width, height=entry_height)
        self._db_host_entry.grid(row=3, column=0, sticky=NSEW, padx=widget_padx)

        # database password
        self._db_password_label = CTkLabel(
            self, text="Database password:", font=entry_label_font
        )
        self._db_password_label.grid(
            row=4, column=0, sticky=W, pady=entry_label_pady, padx=widget_padx
        )

        self._db_password_entry = CTkEntry(
            self, width=entry_width, height=entry_height, show="*"
        )
        self._db_password_entry.grid(row=5, column=0, sticky=NSEW, padx=widget_padx)

        # database admin db
        self._db_admindb_label = CTkLabel(
            self, text="Administrative database:", font=entry_label_font
        )
        self._db_admindb_label.grid(
            row=6, column=0, sticky=W, pady=entry_label_pady, padx=widget_padx
        )

        self._db_admindb_entry = CTkEntry(self, width=entry_width, height=entry_height)
        self._db_admindb_entry.grid(row=7, column=0, sticky=NSEW, padx=widget_padx)

        # save button
        self._save_button = CTkButton(
            self,
            text="Save",
            width=entry_width - 15,
            height=48,
            font=entry_label_font,
            command=self._save_config_command,
        )
        self._save_button.grid(row=8, column=0, pady=26)

    def _fill_entries(self) -> None:
        self._db_user_entry.insert(END, CONFIGS["DATABASE"]["user"])
        self._db_host_entry.insert(END, CONFIGS["DATABASE"]["host"])
        self._db_password_entry.insert(END, CONFIGS["DATABASE"]["password"])
        self._db_admindb_entry.insert(END, CONFIGS["DATABASE"]["admin_db"])

    def _save_config_command(self) -> None:
        CONFIGS["DATABASE"]["user"] = self._db_user_entry.get()
        CONFIGS["DATABASE"]["host"] = self._db_host_entry.get()
        CONFIGS["DATABASE"]["password"] = self._db_password_entry.get()
        CONFIGS["DATABASE"]["admin_db"] = self._db_admindb_entry.get()

        save_config()

        if isinstance(self.master, CTkInputDialog):
            # once again, not ideal to access a protected atribute, but it's easier this way
            self.master._ok_event()
        else:
            DIALOG_RestartApp().get_input()
