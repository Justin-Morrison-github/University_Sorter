from pathlib import Path
import tkinter as tk
from tkinter import ttk
from university import Packet, SchoolSorter, Folder, Mode
from string_utils import path_from_substring_exclusive, path_from_substring_offset
from colorama import init as colorama_init


def show_selection():
    pass


class FileMoverApp:
    def __init__(self, window: tk.Tk):

        # Set up sorter and get files
        self.school_sorter = SchoolSorter()
        self.all_packets = self.school_sorter.packets_to_be_sent
        self.packets_to_send: list[Packet] = []

        self.window = window
        self.window.title("File Mover")
        self.window.geometry("1000x500")

        # Frame for file selection
        self.frame = tk.Frame(window)
        self.frame.pack(pady=5)

        x = tk.IntVar(value=0)

        radio_mode_select = tk.Checkbutton(window, text="Send Enabled", variable=x, command=self.toggle_mode)
        radio_mode_select.pack()

        self.move_button = tk.Button(self.frame, text="Move Selected", command=self.move_selected)
        self.move_button.pack(side=tk.LEFT, padx=5)

        # Select All Button
        select_all_button = tk.Button(self.frame, text="Select All", command=self.select_all)
        select_all_button.pack(side=tk.RIGHT, pady=5)

        self.text_frame = tk.Frame(window, bg='lightgray')
        self.text_frame.pack(pady=5, fill='x')

        self.tree_frame = tk.Frame(window)
        self.tree_frame.pack(pady=5, fill='x')

        # Left-aligned label
        self.src_folder_label = tk.Label(
            self.text_frame, text=f"Files from {self.school_sorter.settings.src_path}", anchor="w", bg='lightgray')
        self.src_folder_label.pack(side="left", anchor="w", padx=5)

        # Right-aligned label
        self.count_packets_sent_label = tk.Label(
            self.text_frame, text=f"{len(self.packets_to_send)} Files Selected", anchor="e", bg='lightgray')
        self.count_packets_sent_label.pack(side='right', anchor="e", padx=5)

        # Create a vertical scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical")

        # Table for file list
        self.tree = ttk.Treeview(self.tree_frame, columns=("#1", "#2", "#3"), show="headings",
                                 selectmode="none", height=20, yscrollcommand=scrollbar.set)
        self.tree.heading("#1", text="Selected")
        self.tree.heading("#2", text="Filename", anchor="w")
        self.tree.heading("#3", text="Destination", anchor="w")
        self.tree.column("#1", width=80, anchor=tk.CENTER, stretch=False)
        self.tree.column("#2", width=200, stretch=True)
        self.tree.column("#3", width=300, stretch=True)
        # self.tree.pack(pady=5)
        self.tree.pack(side="left", fill="both", expand=True, padx=5)

        # Configure the scrollbar to work with the Treeview
        scrollbar.config(command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')

        self.check_vars = {}

        self.all_selected = False

    def display_packets(self):
        self.tree.delete(*self.tree.get_children())  # Clear existing entries
        self.check_vars.clear()

        for packet in self.all_packets:
            src: Path = path_from_substring_exclusive(packet.src, Folder.DOWNLOADS)
            dst: Path = path_from_substring_offset(packet.dst, Folder.UNIVERSITY, 3)
            var = tk.BooleanVar()
            # self.check_vars[packet.src.name] = var
            self.check_vars[packet.src.name] = (var, packet)
            self.tree.insert("", "end", values=("[ ]", src, dst), tags=(packet.src.name,))

            # self.tree.tag_bind(packet.src.name, "<ButtonRelease-1>", self.toggle_checkbox)
            self.tree.tag_bind(packet.src.name, "<ButtonRelease-1>", lambda event: self.toggle_checkbox(event, packet))

    def select_all(self):
        for item in self.tree.get_children():
            self.tree.item(
                item, 
                values=(
                    "[✓]" if self.tree.item(item, "values")[0] != "[✓]" else "[ ]",
                    self.tree.item(item, "values")[1], 
                    ("*" if self.tree.item(item, "values")[0] != "[✓]" else "") + self.tree.item(item, "values")[2].strip("*")
                )
            )

        for packet in self.all_packets:
            if self.all_selected:
                self.packets_to_send.remove(packet)
            else:
                self.packets_to_send.append(packet)

        self.all_selected = not self.all_selected

        self.count_packets_sent_label.config(text=f"{len(self.packets_to_send)} Files Selected")
        print(self.packets_to_send)

    def toggle_mode(self):
        if self.school_sorter.mode == Mode.DEBUG:
            self.school_sorter.mode = Mode.SEND
        elif self.school_sorter.mode == Mode.SEND:
            self.school_sorter.mode = Mode.DEBUG
        print(self.school_sorter.mode)

    

    def toggle_checkbox(self, event, packet):
        item = self.tree.identify_row(event.y)
        if item:
            file_path = self.tree.item(item, "tags")[0]

            var = self.check_vars[file_path][0]
            packet = self.check_vars[file_path][1]
            var.set(not var.get())

            if var.get():
                new_values = ("[✓]", self.tree.item(item, "values")[1], ("*" if self.tree.item(item, "values")
                              [0] != "[✓]" else "") + self.tree.item(item, "values")[2].strip("*")) # Checked state
                self.packets_to_send.append(packet)

            else:
                new_values = ("[ ]", self.tree.item(item, "values")[1],
                              ("*" if self.tree.item(item, "values")[0] != "[✓]" else "") + self.tree.item(item, "values")[2].strip("*"))  # Unchecked state
                self.packets_to_send.remove(packet)

            self.tree.item(item, values=new_values)  # Update the item values
            self.count_packets_sent_label.config(text=f"{len(self.packets_to_send)} Files Selected")
            print(self.packets_to_send)

    def move_selected(self):
        for packet in self.packets_to_send:
            packet.send(self.school_sorter.mode)

    def mainloop(self):
        self.display_packets()


if __name__ == "__main__":
    colorama_init(autoreset=True)
    window = tk.Tk()
    app = FileMoverApp(window)
    app.mainloop()
    window.mainloop()
    print()
