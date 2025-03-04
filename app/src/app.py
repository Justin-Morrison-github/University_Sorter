import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk


class FileMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Mover")

        # Frame for file selection
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.select_button = tk.Button(self.frame, text="Select Files", command=self.load_files)
        self.select_button.pack(side=tk.LEFT, padx=5)

        self.move_button = tk.Button(self.frame, text="Move Selected", command=self.move_selected)
        self.move_button.pack(side=tk.LEFT, padx=5)

        # Table for file list
        self.tree = ttk.Treeview(root, columns=("#1", "#2"), show="headings", selectmode="none")
        self.tree.heading("#1", text="Select")
        self.tree.heading("#2", text="Filename")
        self.tree.column("#1", width=50, anchor=tk.CENTER)
        self.tree.column("#2", width=300)
        self.tree.pack(pady=10)

        self.check_vars = {}

    def load_files(self):
        folder = filedialog.askdirectory()
        if not folder:
            return

        self.tree.delete(*self.tree.get_children())  # Clear existing entries
        self.check_vars.clear()

        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path):
                var = tk.BooleanVar()
                self.check_vars[file_path] = var
                self.tree.insert("", "end", values=("[ ]", file), tags=(file_path,))
                self.tree.tag_bind(file_path, "<ButtonRelease-1>", self.toggle_checkbox)

    # def load_files(self):
    #     folder = filedialog.askdirectory()
    #     if not folder:
    #         return

    #     self.tree.delete(*self.tree.get_children())  # Clear existing entries
    #     self.check_vars.clear()

    #     for file in os.listdir(folder):
    #         file_path = os.path.join(folder, file)
    #         if os.path.isfile(file_path):
    #             var = tk.BooleanVar()
    #             self.check_vars[file_path] = var
    #             self.tree.insert("", "end", values=("[ ]", file), tags=(file_path,))
    #             self.tree.tag_bind(file_path, "<ButtonRelease-1>", self.toggle_checkbox)

    def toggle_checkbox(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            file_path = self.tree.item(item, "tags")[0]
            var = self.check_vars[file_path]
            var.set(not var.get())
            self.tree.item(item, values=("[✓]" if var.get() else "[ ]", self.tree.item(item, "values")[1]))

    def move_selected(self):
        target_folder = filedialog.askdirectory()
        if not target_folder:
            return

        for file_path, var in self.check_vars.items():
            if var.get():
                shutil.move(file_path, os.path.join(target_folder, os.path.basename(file_path)))

        self.load_files()  # Refresh the file list


if __name__ == "__main__":
    root = tk.Tk()
    app = FileMoverApp(root)
    root.mainloop()
