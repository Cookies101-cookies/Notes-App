import tkinter as tk
from tkinter import filedialog, messagebox


class NotesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Notes App")
        self.geometry("500x400")

        # Text area with undo/redo
        self.text_area = tk.Text(self, wrap="word", undo=True)
        self.text_area.pack(expand=True, fill="both")

        # Status bar
        self.status = tk.Label(self, text="New Note", anchor="w")
        self.status.pack(side="bottom", fill="x")

        # Menu bar
        self.menu_bar = tk.Menu(self)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_note, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.open_note, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.save_note, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As", command=self.save_note_as)
        self.file_menu.add_command(label="Exit", command=self.on_closing)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Undo", command=self.text_area.edit_undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo", command=self.text_area.edit_redo, accelerator="Ctrl+Y")
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        self.config(menu=self.menu_bar)

        # Track current file
        self.current_file = None

        # Keyboard shortcuts
        self.bind("<Control-n>", lambda event: self.new_note())
        self.bind("<Control-o>", lambda event: self.open_note())
        self.bind("<Control-s>", lambda event: self.save_note())
        self.bind("<Control-z>", lambda event: self.text_area.edit_undo())
        self.bind("<Control-y>", lambda event: self.text_area.edit_redo())

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    # --- File operations ---
    def new_note(self):
        if self.confirm_unsaved_changes():
            self.text_area.delete(1.0, tk.END)
            self.current_file = None
            self.status.config(text="New Note")
            self.text_area.edit_modified(False)

    def open_note(self):
        if not self.confirm_unsaved_changes():
            return
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())
            self.current_file = file_path
            self.status.config(text=f"Opened: {file_path}")
            self.text_area.edit_modified(False)

    def save_note(self):
        if self.current_file:
            with open(self.current_file, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.status.config(text=f"Saved: {self.current_file}")
            self.text_area.edit_modified(False)
        else:
            self.save_note_as()

    def save_note_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text Files", "*.txt")]
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.current_file = file_path
            self.status.config(text=f"Saved: {file_path}")
            self.text_area.edit_modified(False)

    # --- Closing handling ---
    def on_closing(self):
        if self.confirm_unsaved_changes():
            self.destroy()

    def confirm_unsaved_changes(self):
        if self.text_area.edit_modified():
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before continuing?"
            )
            if response:  # Yes, save
                self.save_note()
                return True
            elif response is False:  # No, discard
                return True
            else:  # Cancel
                return False
        return True


if __name__ == "__main__":
    app = NotesApp()
    app.mainloop()
