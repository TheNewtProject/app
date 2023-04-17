import tkinter as tk
from tkinter import filedialog
import os
import configparser
import subprocess
from tkinter import scrolledtext
import traceback
from contextlib import redirect_stdout
from io import StringIO

config = configparser.ConfigParser()
themecfg = configparser.ConfigParser()

icon_path = os.path.join(os.path.dirname(__file__), "newt.ico")
config_path = os.path.join(os.path.dirname(__file__), "config.ini")

with open(config_path, "r") as f:
    config.read_file(f)

theme_path = os.path.join(os.path.dirname(__file__), "themes")


if not os.path.exists(os.path.join(theme_path, config["theme"]["default-theme"] + ".ini")):
    print(f"Theme {config['theme']['default-theme']} is not in {theme_path} or does not exist! Attempting to use dark theme...")

    if os.path.exists(os.path.join(theme_path, "dark.ini")):
        theme_path = os.path.join(theme_path, "dark.ini")

    else:
        print(f"Theme {os.path.join(theme_path, 'dark.ini')} is not in {theme_path} or does not exist! Attempting to use light theme...")
        if os.path.exists(os.path.join(theme_path, "light.ini")):
            theme_path = os.path.join(theme_path, "light.ini")
        
        else:
            print(f"Theme {os.path.join(theme_path, 'light.ini')} is not in {theme_path} or does not exist! Attempting to use amoled theme...")

            if os.path.exists(os.path.join(theme_path, "amoled.ini")):
                theme_path = os.path.join(theme_path, "amoled.ini")
            else:
                print(f"Theme {os.path.join(theme_path, 'amoled.ini')} is not in {theme_path} or does not exist!")
                print(f"Please install themes in {theme_path} to continue using Newt.")
                exit()

else:
    theme_path = os.path.join(theme_path, config["theme"]["default-theme"] + ".ini")

with open(theme_path, "r") as f:
    themecfg.read_file(f)



class Newt:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Newt")
        self.root.configure(bg=f"{themecfg['root']['background']}")  # set background color
        self.root.option_add("*foreground", f"{themecfg['root']['foreground']}")  # set foreground color
        self.root.iconbitmap(icon_path) # set icon

        # configure text widget
        self.text = tk.Text(self.root, bg=f"{themecfg['text']['background']}", fg=f"{themecfg['text']['foreground']}", insertbackground=f"{themecfg['text']['insert-background']}", wrap=f"{themecfg['text']['wrap']}", font=(f"{themecfg['text']['font-family']}", int(themecfg['text']['font-size'])), tabstyle="wordprocessor")

        self.tab_width = 36
        self.text.configure(tabs=self.tab_width)

        # configure menu bar
        self.menu_bar = tk.Menu(self.root, bg=f"{themecfg['menu-bar']['background']}", fg=f"{themecfg['menu-bar']['foreground']}", activebackground=f"{themecfg['menu-bar']['active-background']}", activeforeground=f"{themecfg['menu-bar']['active-foreground']}")
        self.root.config(menu=self.menu_bar)

        # configure file menu
        self.file_menu = tk.Menu(self.menu_bar, bg=f"{themecfg['file-menu']['background']}", fg=f"{themecfg['file-menu']['foreground']}", activebackground=f"{themecfg['file-menu']['active-background']}", activeforeground=f"{themecfg['file-menu']['active-foreground']}")
        self.file_menu.add_command(label="Open (Ctrl+O)", command=self.open_file)
        self.file_menu.add_command(label="Save As", command=self.save_file_as)
        self.file_menu.add_command(label="Save (Ctrl+S)", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Close Window", command=self.root.destroy)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # configure edit menu
        self.edit_menu = tk.Menu(self.menu_bar, bg=f"{themecfg['edit-menu']['background']}", fg=f"{themecfg['edit-menu']['foreground']}", activebackground=f"{themecfg['edit-menu']['active-background']}", activeforeground=f"{themecfg['edit-menu']['active-foreground']}")
        self.edit_menu.add_command(label="Undo (Ctrl+Z)", command=self.text.edit_undo)
        self.edit_menu.add_command(label="Redo (Ctrl+Y)", command=self.text.edit_redo)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # configure run menu
        """
        self.run_menu = tk.Menu(self.menu_bar, bg=f"{themecfg['run-menu']['background']}", fg=f"{themecfg['run-menu']['foreground']}", activebackground=f"{themecfg['run-menu']['active-background']}", activeforeground=f"{themecfg['run-menu']['active-background']}")
        self.edit_menu.add_command(label="Run (Ctrl+R)", command=self.run_file)
        self.menu_bar.add_cascade(label="Run", menu=self.run_menu)
        """

        self.menu_bar.configure(bg=f"{themecfg['menu-bar']['background']}")

        # configure toolbar
        self.toolbar = tk.Frame(self.root, bg=f"{themecfg['toolbar']['background']}")
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.open_button = tk.Button(self.toolbar, text="Open", command=self.open_file, bg=f"{themecfg['tools']['background']}", fg=f"{themecfg['tools']['foreground']}", activebackground=f"{themecfg['tools']['active-background']}", activeforeground=f"{themecfg['tools']['active-foreground']}")
        self.open_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.save_button = tk.Button(self.toolbar, text="Save", command=self.save_file, bg=f"{themecfg['tools']['background']}", fg=f"{themecfg['tools']['foreground']}", activebackground=f"{themecfg['tools']['active-background']}", activeforeground=f"{themecfg['tools']['active-foreground']}")
        self.save_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.saveas_button = tk.Button(self.toolbar, text="Save As", command=self.save_file_as, bg=f"{themecfg['tools']['background']}", fg=f"{themecfg['tools']['foreground']}", activebackground=f"{themecfg['tools']['active-background']}", activeforeground=f"{themecfg['tools']['active-foreground']}")
        self.saveas_button.pack(side=tk.LEFT, padx=2, pady=2)
        """
        self.run_button = tk.Button(self.toolbar, text="Run", command=self.run_file, bg=f"{themecfg['tools']['background']}", fg=f"{themecfg['tools']['foreground']}", activebackground=f"{themecfg['tools']['active-background']}", activeforeground=f"{themecfg['tools']['active-foreground']}")
        self.run_button.pack(side=tk.LEFT, padx=2, pady=2)
        """
        self.undo_button = tk.Button(self.toolbar, text="Undo", command=self.text.edit_undo, bg=f"{themecfg['tools']['background']}", fg=f"{themecfg['tools']['foreground']}", activebackground=f"{themecfg['tools']['active-background']}", activeforeground=f"{themecfg['tools']['active-foreground']}")
        self.undo_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.redo_button = tk.Button(self.toolbar, text="Redo", command=self.text.edit_redo, bg=f"{themecfg['tools']['background']}", fg=f"{themecfg['tools']['foreground']}", activebackground=f"{themecfg['tools']['active-background']}", activeforeground=f"{themecfg['tools']['active-foreground']}")
        self.redo_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.exit_button = tk.Button(self.toolbar, text="Exit", command=self.root.destroy, bg=f"{themecfg['tools']['background']}", fg=f"{themecfg['tools']['foreground']}", activebackground=f"{themecfg['tools']['active-background']}", activeforeground=f"{themecfg['tools']['active-foreground']}")
        self.exit_button.pack(side=tk.RIGHT, padx=2, pady=2)

        # pack text widget
        self.text.pack(fill=tk.BOTH, expand=1)

        # configure scrollbar
        self.scrollbar = tk.Scrollbar(self.text)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text.yview)

        # status bar
        self.status = tk.Text(self.root, height=1, bg=f"{themecfg['tools']['background']}", fg=f"{themecfg['tools']['foreground']}", insertbackground=f"{themecfg['text']['insert-background']}", wrap=f"{themecfg['text']['wrap']}", font=(f"{themecfg['text']['font-family']}", int(themecfg['text']['font-size'])), tabstyle="wordprocessor", state="disabled")
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        
        # configure keyboard shortcuts
        self.root.bind("<Control-o>", self.open_file)
        self.root.bind("<Control-s>", self.save_file)
        """
        self.root.bind("<Alt-Shift-s>", self.save_file_as)
        """
        self.root.bind("<Control-z>", self.text.edit_undo)
        self.root.bind("<Control-y>", self.text.edit_redo)
        """
        self.root.bind("<Control-r>", self.run_file)
        """

    def open_file(self, event=None):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                self.text.delete("1.0", tk.END)
                self.text.insert("1.0", file.read())
                self.root.title(f"Newt - {file_path}")

    def save_file(self, event=None):
        if self.root.title() == "Newt":
            # If the file hasn't been saved before, open the "Save As" dialog
            self.save_file_as()
        else:
            # Otherwise, save the file to the current path
            file_path = self.root.title().replace("Newt - ", "")
            with open(file_path, "w") as file:
                file.write(self.text.get("1.0", tk.END))

    def save_file_as(self, event=None):
        file_types = [("Text Files", "*.txt"), ("Python Files", "*.py"), ("JavaScript Files", "*.js"), 
            ("HTML Files", "*.html"), ("CSS Files", "*.css"), ("Markdown Files", "*.md"),
            ("YAML Files", "*.yaml"), ("JSON Files", "*.json"), ("XML Files", "*.xml"), 
            ("All Files", "*.*")]
        
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=file_types)

        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text.get("1.0", tk.END))
                self.root.title(f"Newt - {file_path}")

    def run(self):
        self.root.mainloop()

    async def run_async(self):
        self.run()

if __name__ == "__main__":
    Newt().run()
