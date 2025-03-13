from pathlib import Path
import tkinter as tk
from tkinter import ttk
from exceptions import PathException
from university import Packet, SchoolSorter, Folder, Mode
from string_utils import path_from_substring_exclusive, path_from_substring_offset
from colorama import init as colorama_init
from Style import Style
from colorama import Fore
# import customtkinter as ctk
    


class FileMoverApp:
    def __init__(self, window: tk.Tk):

        # Set up sorter and get files
        self.school_sorter = SchoolSorter()

        self.settings = self.school_sorter.settings
        self.all_packets = self.school_sorter.packets_to_be_sent
        self.mode = self.school_sorter.mode

        self.packets_to_send: list[Packet] = []
        self.longest_src_name = self.find_longest_src_file_name()
        self.longest_dst_name = self.find_longest_dst_file_name()

        self.column1_width = 70
        self.column2_width = self.longest_src_name // 5 * 40
        self.column3_width = self.longest_dst_name // 5 * 200

        self.window = window
        self.window.title("File Mover")
        self.window.geometry(f"{sum([self.column1_width, self.column2_width, self.column3_width])}x{550}")

        # Frame for file selection
        self.title_frame = tk.Frame(window)
        self.title_frame.pack(pady=5, fill='x')

        # Settings Button
        self.settings_button = tk.Button(self.title_frame, text="Settings", command=self.open_settings, anchor='w')
        self.settings_button.pack(padx=5, side=tk.LEFT)

        self.title_label = tk.Label(self.title_frame, text="University File Mover",  font=("Arial", 14), anchor="center")
        self.title_label.pack(pady=5)


        # Add user control buttons
        self.button_frame = tk.Frame(window)
        self.button_frame.pack(pady=5, fill='x')

        self.move_selected_button = tk.Button(self.button_frame, text="Move Selected", command=self.move_selected)
        self.move_selected_button.pack(side=tk.RIGHT, padx=5)
        
        # Select All Button
        select_all_button = tk.Button(self.button_frame, text="Select All", command=self.select_all, anchor='w')
        select_all_button.pack(side=tk.LEFT, padx=5)

        selected_option:Mode = tk.StringVar(value=Mode.DEBUG)  # Default value

        # Create Mode Select Radio Buttons
        self.debug_radio = tk.Radiobutton(self.button_frame, text="Debug", variable=selected_option, value=Mode.DEBUG, command=lambda:self.select_mode(selected_option))
        self.send_radio = tk.Radiobutton(self.button_frame, text="Send", variable=selected_option, value=Mode.SEND, command=lambda:self.select_mode(selected_option))
        self.send_mkdir_radio = tk.Radiobutton(self.button_frame, text="Send Mkdir", variable=selected_option, value=Mode.SEND_MKDIR, command=lambda:self.select_mode(selected_option))

        self.debug_radio.pack(side="left", padx=10)
        self.send_radio.pack(side="left", padx=10)
        self.send_mkdir_radio.pack(side="left", padx=10)

        self.text_frame = tk.Frame(window, bg='lightgray')
        self.text_frame.pack(pady=5, fill='x')

        # Left-aligned label
        self.src_folder_label = tk.Label(
            self.text_frame, text=f"Files from {self.school_sorter.settings.src_path}", anchor="w", bg='lightgray')
        self.src_folder_label.pack(side="left", anchor="w", padx=5)

        # Right-aligned label
        self.count_packets_sent_label = tk.Label(
            self.text_frame, text=f"{len(self.packets_to_send)} Files Selected", anchor="e", bg='lightgray')
        self.count_packets_sent_label.pack(side='right', anchor="e", padx=5)

        self.tree_frame = tk.Frame(window)
        self.tree_frame.pack(pady=5, fill='x')

        # Create a vertical scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical")

        # Table for file list
        self.tree = ttk.Treeview(self.tree_frame, columns=("#1", "#2", "#3"), show="headings",
                                 selectmode="none", height=20, yscrollcommand=scrollbar.set)
        self.tree.heading("#1", text="Selected")
        self.tree.heading("#2", text="Filename", anchor="w")
        self.tree.heading("#3", text="Destination", anchor="w")
        self.tree.column("#1", width=self.column1_width, anchor=tk.CENTER, stretch=False)
        self.tree.column("#2", width=self.column2_width, stretch=False)
        self.tree.column("#3", width=self.column3_width, stretch=False)
        self.tree.pack(side="left", fill="both", expand=True, padx=5)

        # Configure the scrollbar to work with the Treeview
        scrollbar.config(command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')

        self.check_vars = {}
        self.all_selected = False
        self.settings_open = False

    def select_mode(self, selected_option: tk.StringVar):
        self.mode = Mode(selected_option.get())
        print(f"Selected Mode: {Fore.MAGENTA}{self.mode.upper()}")


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

        for item, packet in zip(self.tree.get_children(), self.all_packets, strict=True):
            self.tree.item(
                item,
                values=(
                    # "[✓]" if self.tree.item(item, "values")[0] != "[✓]" else "[ ]",
                    "[ ]" if self.all_selected else "[✓]",
                    self.tree.item(item, "values")[1],
                    (">>> " if self.tree.item(item, "values")[
                     0] != "[✓]" else "") + self.tree.item(item, "values")[2].lstrip(">>> ")
                )
            )

            if self.all_selected:
                self.packets_to_send.remove(packet)
            else:
                self.packets_to_send.append(packet)

        self.all_selected = not self.all_selected

        self.update_file_count_text()
        print(self.packets_to_send)

    def find_longest_src_file_name(self):
        longest = 0
        for packet in self.all_packets:
            src: Path = path_from_substring_exclusive(packet.src, Folder.DOWNLOADS)
            if len(str(src)) > longest:
                longest = len(packet.src.name)

        return longest

    def find_longest_dst_file_name(self):
        longest = 0

        for packet in self.all_packets:
            dst: Path = path_from_substring_offset(packet.dst, Folder.UNIVERSITY, 3)

            if len(str(dst)) > longest:
                longest = len(packet.dst.name)

        return longest


    def toggle_checkbox(self, event, packet):
        item = self.tree.identify_row(event.y)
        if item:
            file_path = self.tree.item(item, "tags")[0]

            var = self.check_vars[file_path][0]
            packet = self.check_vars[file_path][1]
            var.set(not var.get())

            unchecked = var.get()
            # unchecked = True if self.tree.item(item, "values")[0] != "[✓]" else False

            val1 = self.tree.item(item, "values")[1]
        
            val2 = (">>> " if unchecked else "") + (
                self.tree.item(item, "values")[2].lstrip(">>> ")
            )

            if unchecked:
                new_values = ("[✓]", val1, val2)  # Set to Checked state
                self.packets_to_send.append(packet)
                    
            else:
                new_values = ("[ ]", val1, val2)  # Set to Unchecked state
                self.packets_to_send.remove(packet)
                # if self.all_selected:
                #     self.all_selected = False


            self.tree.item(item, values=new_values)  # Update the item values
            print(self.packets_to_send)
            self.update_file_count_text()

    def update_file_count_text(self):
        self.count_packets_sent_label.config(text=f"{len(self.packets_to_send)} Files Selected")


    def move_selected(self):
        print(f"{Fore.MAGENTA}{self.mode.upper()} MODE")
        for packet in self.packets_to_send:
            try:
                packet.send(self.mode)
            except PathException as e:
                pass

    def mainloop(self):
        self.display_packets()

    def save_settings(self):
        print("Settings Saved!")  # Perform any cleanup or save settings
        self.close_settings()

    def close_settings(self):
        print("Settings window closed!")  # Perform any cleanup or save settings
        self.settings_open = False
        self.settings_window.destroy()  # Close the settings window

    def open_settings(self):
        if not self.settings_open:
            self.settings_open = True
            self.settings_window = tk.Toplevel(self.window)  # Create a new top-level window
            self.settings_window.title("Settings")
            self.settings_window.geometry("500x250")  # Set size

            tk.Label(self.settings_window, text="Settings", font=("Arial", 14)).pack(pady=10)

            tk.Label(self.settings_window, text=f"Json File").pack()
            self.json_entry = PlaceholderEntry(
                self.settings_window, placeholder=self.settings.json_file).pack(
                pady=5, padx=40, fill="x")
            
            tk.Label(self.settings_window, text=f"Source Folder:").pack()
            self.src_entry = PlaceholderEntry(
                self.settings_window, placeholder=self.settings.src_path).pack(pady=5, padx=40, fill="x")

            tk.Label(self.settings_window, text=f"Destination Folder:").pack()    
            self.dst_entry = PlaceholderEntry(
                self.settings_window, placeholder=self.settings.dst_path).pack(pady=5, padx=40, fill="x")

            tk.Button(self.settings_window, text="Save", command=self.save_settings).pack(pady=10)
            self.settings_window.protocol("WM_DELETE_WINDOW", self.close_settings)


class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="Enter text...", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.default_fg_color = self["fg"]

        # self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

        self._add_placeholder()

    def _add_placeholder(self):
        """Display the placeholder text."""
        self.insert(0, self.placeholder)
        # self["fg"] = self.placeholder_color

    def _on_focus_out(self, event):
        """Restore placeholder if the entry is empty when focus is lost."""
        if not self.get():
            self._add_placeholder()


if __name__ == "__main__":
    colorama_init(autoreset=True)
    window = tk.Tk()
    app = FileMoverApp(window)
    app.mainloop()
    window.mainloop()
    print()
