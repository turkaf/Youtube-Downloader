import os
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import filedialog
from PIL import Image, ImageTk
import ttkbootstrap as ttkb
from pytube import YouTube


class Downloader:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.style = ttkb.Style(theme='darkly')
        self.version_of_downloader = "v1.0.0"
        self.DIR = os.getcwd()
        
        self.configure_panel()
        self.create_widgets()

    def configure_panel(self):
        self.root.geometry("800x230")
        self.root.title("AFTube Downloader " + self.version_of_downloader)
        self.root.iconbitmap(self.DIR + '/images/icon.ico')
        self.root.resizable(False, False)

        # Image section
        image1 = Image.open(self.DIR+"/images/logo.png")
        test = ImageTk.PhotoImage(image1)
        self.label1 = ttk.Label(image=test)
        self.label1.image = test
        self.label1.place(x=290, y=3)

        # Create line to seperate logo from widgets
        self.canvas = tk.Canvas(self.root, width=800, height=15, bg="black", highlightthickness=0)
        self.canvas.place(x=0, y=43)
        self.canvas.create_line(25, 15, 775, 15, fill='white', width=2)

        # Version info at the bottom
        bottom_version_label = ttk.Label(self.root, text=self.version_of_downloader + " created by A.F.T")
        bottom_version_label.place(relx=0.5, rely=0.99, anchor='s')  

        # Configure widgets
        self.style.configure('TLabel', font=('Helvetica', 10, 'bold'), foreground='white')
        self.style.configure('TButton', font=('Helvetica', 10, 'bold'), foreground='white')

    def create_widgets(self, x_base = 60, y_base = 80):
        # Select directory to save to label
        self.select_directory_label = ttk.Label(self.root, text="Select Directory:")
        self.select_directory_label.place(x=x_base, y=y_base)

        # Select directory to save to entry
        self.selected_directory_entry = ttk.Entry(self.root, state="readonly")
        self.selected_directory_entry.place(x=x_base + 120, y=y_base, width=460)

        # Select directory button
        self.select_directory_button = ttk.Button(self.root, text="Select", style='primary.Outline.TButton', command=self.on_select_directory_button_click)
        self.select_directory_button.place(x=x_base + 592, y=y_base)
        self.select_directory_button.config(width=9)

        # Enter url label
        self.select_url_label = ttk.Label(self.root, text="Url:")
        self.select_url_label.place(x=x_base, y=y_base + 50)

        # URL entry wdiget
        self.url_entry = ttk.Entry(self.root)
        self.url_entry.place(x=x_base + 120, y=y_base + 50, width=460)

        # Audio type combobox
        self.audio_types = ["mp3", "mp4"]
        self.audio_type_combobox = ttk.Combobox(self.root, values=self.audio_types, state="readonly")
        self.audio_type_combobox.set("Audio Type")
        self.audio_type_combobox.place(x=x_base + 592, y=y_base + 50, width=88)

        # Download button
        self.download_button = ttk.Button(self.root, text="Download", style='primary.Outline.TButton', command=self.on_download_button_click)
        self.download_button.place(x=x_base + 592, y=y_base + 90)

        # Progressbar
        self.progressbar = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.progressbar.place(x=x_base, y=y_base + 90, width=580, height=25)

        print(self.download_button.winfo_reqwidth())

    def on_download_button_click(self):
        pass

    def on_select_directory_button_click(self):
        folder_selected = filedialog.askdirectory()

        if folder_selected:
            self.selected_directory_entry.config(state="normal")
            self.selected_directory_entry.delete(0, tk.END)
            self.selected_directory_entry.insert(0, folder_selected)
            self.selected_directory_entry.config(state="readonly")
        else:
            print("Not found")
            self.selected_directory_entry.config(state="normal")
            self.selected_directory_entry.delete(0, tk.END)
            self.selected_directory_entry.config(state="readonly")

def main():
    root = tk.Tk()
    app = Downloader(root)
    root.mainloop()

if __name__ == "__main__":
    main()