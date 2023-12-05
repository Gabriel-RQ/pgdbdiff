from tkinter import messagebox
from typing import Literal, Callable
from customtkinter import (
    CTkFrame,
    CTkLabel,
    CTkFont,
    CTkOptionMenu,
    CTkButton,
    DISABLED,
    NORMAL,
    NSEW,
)
from backend.db import Postgres, get_all_database_names
from backend.configs import CONFIGS


class FRAME_SelectDatabase(CTkFrame):
    def __init__(self, master, compare_btn_command: Callable):
        super().__init__(master)

        self._compare_btn_command = compare_btn_command

        self._create_widgets()
        self.__set_database_options()

    def _create_widgets(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure([1, 6], weight=1)

        self._title_label = CTkLabel(
            self, text="DATABASE COMPARER", font=CTkFont(size=18, weight="bold")
        )
        self._title_label.grid(row=0, pady=12)

        self._first_db_label = CTkLabel(
            self,
            text="Select first database:",
            font=CTkFont(size=12, weight="bold"),
        )
        self._second_db_label = CTkLabel(
            self,
            text="Select second database:",
            font=CTkFont(size=12, weight="bold"),
        )

        self._first_db_option = CTkOptionMenu(
            self,
            height=46,
            state=DISABLED,
            values=["No database found"],
            command=lambda _: self.__select_db_command("first"),
        )
        self._second_db_option = CTkOptionMenu(
            self,
            height=46,
            state=DISABLED,
            values=["No database found"],
            command=lambda _: self.__select_db_command("second"),
        )

        self._first_db_label.grid(row=2, sticky=NSEW, pady=8)
        self._first_db_option.grid(row=3, sticky=NSEW, padx=10, pady=(0, 12))

        self._second_db_label.grid(row=4, sticky=NSEW, pady=8)
        self._second_db_option.grid(row=5, sticky=NSEW, padx=10, pady=(0, 12))

        self._compare_btn = CTkButton(
            self, height=46, text="Compare", command=self._compare_btn_command
        )
        self._compare_btn.grid(row=7, sticky=NSEW, padx=12, pady=10)

    def __select_db_command(self, option_menu: Literal["first", "second"]) -> None:
        if option_menu == "first":
            CONFIGS["RUNNING"]["first_db"] = self._first_db_option.get()
        elif option_menu == "second":
            CONFIGS["RUNNING"]["second_db"] = self._second_db_option.get()

    def __set_database_options(self) -> None:
        try:
            with Postgres(
                user=CONFIGS["DATABASE"]["user"],
                host=CONFIGS["DATABASE"]["host"],
                password=CONFIGS["DATABASE"]["password"],
                database=CONFIGS["DATABASE"]["admin_db"],
            ) as conn:
                databases = sorted(
                    db for db in get_all_database_names(conn) if "postgres" not in db
                )

            self._first_db_option.configure(values=databases, state=NORMAL)
            self._second_db_option.configure(values=databases, state=NORMAL)

            self._first_db_option.set(databases[0])
            self._second_db_option.set(databases[0])
            CONFIGS["RUNNING"]["first_db"] = databases[0]
            CONFIGS["RUNNING"]["second_db"] = databases[0]

        except Exception as e:
            self._first_db_option.configure(
                values=["No database found"], state=DISABLED
            )
            self._second_db_option.configure(
                values=["No database found"], state=DISABLED
            )

            messagebox.showerror(
                "Postgres error",
                f"Error searching avaiable databases. Detail: {e}",
            )
