import difflib, logging, subprocess, threading
from typing import Iterator, Callable
from tkinter import messagebox
from customtkinter import (
    CTkFrame,
    CTkTextbox,
    CTkLabel,
    CTkFont,
    END,
    INSERT,
    DISABLED,
    NORMAL,
    NSEW,
    NONE,
    CENTER,
)
from backend.db import Postgres
from backend.configs import CONFIGS


class FRAME_ShowDiff(CTkFrame):
    def __init__(self, master: any):
        super().__init__(master)

        self._create_widgets()

    def _create_widgets(self) -> None:
        self.rowconfigure(1, weight=1)
        self.columnconfigure([1, 2], weight=1)

        self._line_counter_entry = CTkTextbox(
            self,
            state=DISABLED,
            width=45,
            spacing1=2,
            spacing2=4,
            spacing3=2,
            activate_scrollbars=False,
            font=CTkFont(size=14, weight="bold"),
            wrap=NONE,
        )
        self._first_db_entry = CTkTextbox(
            self,
            state=DISABLED,
            spacing1=2,
            spacing2=4,
            spacing3=2,
            font=CTkFont(size=14, weight="bold"),
            wrap=NONE,
        )
        self._second_db_entry = CTkTextbox(
            self,
            state=DISABLED,
            spacing1=2,
            spacing2=4,
            spacing3=2,
            font=CTkFont(size=14, weight="bold"),
            wrap=NONE,
        )

        self._first_db_entry.bind(
            "<Motion>",
            self.__highlight_current_line,
        )
        self._second_db_entry.bind("<Motion>", self.__highlight_current_line)

        self._line_counter_entry.configure(yscrollcommand=self.__sync_entry_y_scroll)
        self._first_db_entry.configure(
            yscrollcommand=self.__sync_entry_y_scroll,
            # xscrollcommand=self.__sync_entry_x_scroll,
        )
        self._second_db_entry.configure(
            yscrollcommand=self.__sync_entry_y_scroll,
            # xscrollcommand=self.__sync_entry_x_scroll,
        )

        self._first_label = CTkLabel(
            self,
            text="DB #1",
            font=CTkFont(
                size=16,
                weight="bold",
            ),
        )
        self._second_label = CTkLabel(
            self,
            text="DB #2",
            font=CTkFont(
                size=16,
                weight="bold",
            ),
        )

        self._first_label.grid(row=0, column=1, pady=(12, 0))
        self._second_label.grid(row=0, column=2, pady=(12, 0))

        self._line_counter_entry.grid(
            row=1, column=0, pady=(4, 12), padx=(8, 2), sticky=NSEW
        )
        self._first_db_entry.grid(
            row=1,
            column=1,
            sticky=NSEW,
            pady=(4, 12),
            padx=(2, 5),
        )
        self._second_db_entry.grid(
            row=1,
            column=2,
            sticky=NSEW,
            pady=(4, 12),
            padx=(5, 8),
        )

    def __highlight_current_line(self, event) -> None:
        """Highlights the line currently under the mouse cursor."""
        if (
            len(self._first_db_entry.get("1.0", END)) > 1
            and len(self._second_db_entry.get("1.0", END)) > 1
        ):
            line_first = self._first_db_entry.index(
                "@{},{} linestart".format(event.x, event.y)
            )
            line_second = self._second_db_entry.index(
                "@{},{} linestart".format(event.x, event.y)
            )

            highlight_line(
                self._line_counter_entry,
                float(line_first),
                fg="#f5f5f5",
                bg="#A9A9A9",
                tag_name="cursor_highlight",
                clear_tag=True,
            )
            highlight_line(
                self._first_db_entry,
                float(line_first),
                fg="#f5f5f5",
                bg="#A9A9A9",
                tag_name="cursor_highlight",
                clear_tag=True,
            )
            highlight_line(
                self._second_db_entry,
                float(line_second),
                fg="#f5f5f5",
                bg="#A9A9A9",
                tag_name="cursor_highlight",
                clear_tag=True,
            )

    def __update_line_numbers(self) -> None:
        # This code was also made with help of chatGPT
        self._line_counter_entry.configure(state=NORMAL)
        self._line_counter_entry.delete("1.0", END)
        num_lines = self._first_db_entry.get("1.0", "end-1c").count("\n") + 1

        self._line_counter_entry.insert(
            "1.0", "\n".join(str(i) for i in range(1, num_lines + 1))
        )
        self._line_counter_entry.tag_add("center", "1.0", END)
        self._line_counter_entry.tag_config("center", justify=CENTER)
        self._line_counter_entry.configure(state=DISABLED)

    def __entry_scroll_y_command(self, *args) -> None:
        """Updates the yview for the text boxes on scroll."""
        self._line_counter_entry.yview(*args)
        self._first_db_entry.yview(*args)
        self._second_db_entry.yview(*args)

    # def __entry_scroll_x_command(self, *args) -> None:
    #     """Updates the xview for the text boxes on scroll"""
    #     self._first_db_entry.xview(*args)
    #     self._second_db_entry.xview(*args)

    # def __sync_entry_x_scroll(self, start_value, end_value) -> None:
    #     """Sync the horizontal scroll bar of both text boxes."""

    #     # sets the position of the scrollbars
    #     self._first_db_entry._x_scrollbar.set(start_value, end_value)
    #     self._second_db_entry._x_scrollbar.set(start_value, end_value)

    #     # sets the scrollbar to move the xview of the text boxes
    #     self._first_db_entry._x_scrollbar.configure(
    #         command=self.__entry_scroll_x_command
    #     )
    #     self._second_db_entry._x_scrollbar.configure(
    #         command=self.__entry_scroll_x_command
    #     )

    def __sync_entry_y_scroll(self, start_value, end_value) -> None:
        """Sync the vertical scroll bar of both text boxes."""
        # found how to sync the scrollbars reading the source code for CTkTextBox in https://github.com/TomSchimansky/CustomTkinter/blob/master/customtkinter/windows/widgets/ctk_textbox.py
        # not ideal to use protected/private atributes, but couldn't find another way

        # sets the position of the scrollbars
        self._line_counter_entry._y_scrollbar.set(start_value, end_value)
        self._first_db_entry._y_scrollbar.set(start_value, end_value)
        self._second_db_entry._y_scrollbar.set(start_value, end_value)

        # sets the scrollbar to move yview of the text boxes
        self._line_counter_entry._y_scrollbar.configure(
            command=self.__entry_scroll_y_command
        )
        self._first_db_entry._y_scrollbar.configure(
            command=self.__entry_scroll_y_command
        )
        self._second_db_entry._y_scrollbar.configure(
            command=self.__entry_scroll_y_command
        )

    def __sync_text_boxes(self):
        """Make both text boxes have the same number of lines."""
        # this function was courtesy of ChatGPT
        # Get the number of lines in each text box
        lines1 = self._first_db_entry.get("1.0", "end-1c").count("\n")
        lines2 = self._second_db_entry.get("1.0", "end-1c").count("\n")

        # Add blank lines to the text box with fewer lines
        if lines1 < lines2:
            self._first_db_entry.insert(END, "\n" * (lines2 - lines1))
        elif lines2 < lines1:
            self._second_db_entry.insert(END, "\n" * (lines1 - lines2))

    def __insert_diff(
        self, diff_tables: Iterator[str], diff_declaration: Iterator[str]
    ) -> None:
        """Draws the diff values to the text boxes."""
        self._first_db_entry.configure(state=NORMAL)
        self._second_db_entry.configure(state=NORMAL)

        self._first_db_entry.delete(1.0, END)
        self._second_db_entry.delete(1.0, END)

        def perform_insert(diff: Iterator[str]):
            for line in diff:
                if line.startswith("@"):
                    continue

                if line.startswith("---"):
                    self._first_db_entry.insert(END, "\n" + line + "\n")
                    continue
                elif line.startswith("+++"):
                    self._second_db_entry.insert(END, "\n" + line + "\n")
                    continue

                line = line.strip("\n")

                if line.startswith("-"):
                    curr_line = self._first_db_entry.index(INSERT).split(".")[0]
                    self._first_db_entry.insert(END, line + "\n")
                    self._second_db_entry.insert(END, "\n")
                    highlight_line(
                        self._first_db_entry, curr_line, fg="#db4f5a", bg="#f2bbbf"
                    )
                elif line.startswith("+"):
                    curr_line = self._second_db_entry.index(INSERT).split(".")[0]
                    self._second_db_entry.insert(END, line + "\n")
                    self._first_db_entry.insert(END, "\n")
                    highlight_line(
                        self._second_db_entry, curr_line, fg="#2fc24c", bg="#b5f5c1"
                    )
                else:
                    self._first_db_entry.insert(END, line + "\n")
                    self._second_db_entry.insert(END, line + "\n")

        self._first_db_entry.insert(END, "~~~~~~~~~ TABLES ~~~~~~~~~\n")
        self._second_db_entry.insert(END, "~~~~~~~~~ TABLES ~~~~~~~~~\n")

        perform_insert(diff_tables)

        self._first_db_entry.insert(END, "\n\n\n~~~~~~~~~ DECLARATION ~~~~~~~~~\n")
        self._second_db_entry.insert(END, "\n\n\n~~~~~~~~~ DECLARATION ~~~~~~~~~\n")

        for diff in diff_declaration:
            perform_insert(diff)

        self.__sync_text_boxes()
        self.__update_line_numbers()
        self._first_db_entry.configure(state=DISABLED)
        self._second_db_entry.configure(state=DISABLED)

    def __show_loading_info(self) -> None:
        self._line_counter_entry.configure(state=NORMAL)
        self._first_db_entry.configure(state=NORMAL)
        self._second_db_entry.configure(state=NORMAL)

        self._line_counter_entry.delete("1.0", END)
        self._first_db_entry.delete("1.0", END)
        self._second_db_entry.delete("1.0", END)

        self._first_db_entry.insert(END, "Loading diff...")
        self._second_db_entry.insert(END, "Loading diff...")

        self._line_counter_entry.configure(state=DISABLED)
        self._first_db_entry.configure(state=DISABLED)
        self._second_db_entry.configure(state=DISABLED)

    def on_do_diff(self) -> None:
        if CONFIGS["RUNNING"]["first_db"] == CONFIGS["RUNNING"]["second_db"]:
            messagebox.showwarning("Warning", "Select different dataases to compare.")
            return

        if threading.active_count() > 1:
            messagebox.showwarning(
                "Keep calm", "Wait for the actual comparison to be finished."
            )
            return

        self.__show_loading_info()

        t = _ExecDiffThread()
        t.setDaemon(True)
        t.set_show_diff_callback(self.__insert_diff)
        t.start()


class _ExecDiffThread(threading.Thread):
    def set_show_diff_callback(self, callback: Callable) -> None:
        self._show_diff_callback = callback

    def __query_database(self):
        tables_query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name"

        with Postgres(
            user=CONFIGS["DATABASE"]["user"],
            database=CONFIGS["RUNNING"]["first_db"],
            password=CONFIGS["DATABASE"]["password"],
            host=CONFIGS["DATABASE"]["host"],
        ) as first_conn:
            first_conn_tables = [data[0] for data in first_conn.query(tables_query)]

        with Postgres(
            user=CONFIGS["DATABASE"]["user"],
            database=CONFIGS["RUNNING"]["second_db"],
            password=CONFIGS["DATABASE"]["password"],
            host=CONFIGS["DATABASE"]["host"],
        ) as second_conn:
            second_conn_tables = [data[0] for data in second_conn.query(tables_query)]

        return (
            first_conn_tables,
            second_conn_tables,
        )

    def __get_table_declarations(self, tables: list[str], database: str) -> dict[str]:
        get_table_declaration = lambda database, table: [
            "pg_dump",
            f"--username={CONFIGS['DATABASE']['user']}",
            f"--host={CONFIGS['DATABASE']['host']}",
            f"--table={table}",
            "--schema-only",
            "--no-privileges",
            "--no-security-labels",
            database,
        ]

        declarations = {}
        for table in tables:
            dump = subprocess.run(
                get_table_declaration(database, table),
                stdout=subprocess.PIPE,
            )

            lines = dump.stdout.decode().splitlines(keepends=True)
            # remove comments, blank lines,  and unnecessary lines
            lines = [
                line
                for line in lines
                if not (
                    line.startswith("--")
                    or line.startswith("SET")
                    or len(line.strip()) < 1
                )
            ]
            # declaration = "".join(lines)

            declarations[table] = lines

        return declarations

    def run(self) -> None:
        try:
            first_conn_tables, second_conn_tables = self.__query_database()
        except Exception as e:
            logging.error(f"Error querying for the avaiable databases. Detail: {e}")
            messagebox.showerror(
                "Postgres error",
                f"Error querying for the avaiable databases. Detail: {e}",
            )
        else:
            table_diff = tuple(
                difflib.unified_diff(
                    first_conn_tables,
                    second_conn_tables,
                    fromfile=CONFIGS["RUNNING"]["first_db"],
                    tofile=CONFIGS["RUNNING"]["second_db"],
                )
            )

            declaration_diff = []

            # get the tables exclusive for each database
            first_conn_only_tables = [
                table.strip("-")
                for table in table_diff
                if not table.startswith("---") and table.startswith("-")
            ]
            second_conn_only_tables = [
                table.strip("+")
                for table in table_diff
                if not table.startswith("+++") and table.startswith("+")
            ]

            # get their SQL declarations
            try:
                first_conn_table_declarations = self.__get_table_declarations(
                    first_conn_only_tables, CONFIGS["RUNNING"]["first_db"]
                )
                second_conn_table_declarations = self.__get_table_declarations(
                    second_conn_only_tables, CONFIGS["RUNNING"]["second_db"]
                )
            except Exception as e:
                logging.error(
                    f"Error getting SQL declaration for the tables. Detail: {e}"
                )
                messagebox.showerror(
                    "Dump error",
                    f"Error getting SQL declaration for the tables. Detail: {e}",
                )
                return

            # diff them against nothing, so you have a diff of their declarations
            for tfirst in first_conn_only_tables:
                diff = tuple(
                    difflib.unified_diff(first_conn_table_declarations[tfirst], [])
                )
                diff = (
                    line
                    for line in diff
                    if not (line.startswith("---") or line.startswith("+++"))
                )
                declaration_diff.append(diff)

            for tsecond in second_conn_only_tables:
                diff = tuple(
                    difflib.unified_diff([], second_conn_table_declarations[tsecond])
                )
                diff = (
                    line
                    for line in diff
                    if not (line.startswith("---") or line.startswith("+++"))
                )
                declaration_diff.append(diff)

            self._show_diff_callback(table_diff, declaration_diff)


def highlight_line(
    textbox: CTkTextbox,
    line: int,
    fg: str | None = None,
    bg: str | None = None,
    tag_name: str = "highlight",
    clear_tag: bool = False,
) -> None:
    if clear_tag:
        textbox.tag_remove(tag_name, "1.0", END)
    textbox.tag_add(tag_name, f"{int(line)}.0", f"{int(line) + 1}.0")
    textbox.tag_config(tag_name, foreground=fg, background=bg)
