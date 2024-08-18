import os
import subprocess
import threading
import time
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import yt_dlp

class Downloader:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.style = ttkb.Style(theme='darkly')
        self.version_of_downloader = "v1.0.1"
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
        self.progressbar = ttkb.Progressbar(self.root, bootstyle=LIGHT)
        self.progressbar.place(x=x_base, y=y_base + 93, width=580, height=24)

        self.download_thread = None

    def on_download_button_click(self):
        if not self.selected_directory_entry.get():
            messagebox.showwarning("Warning!", "Please select e directory to be saved!")
        elif not self.url_entry.get():
            messagebox.showwarning("Warning!", "Please enter a youtube url!")
        elif self.audio_type_combobox.get() == "Audio Type":
            messagebox.showwarning("Warning!", "Please select an audio type!")
        else:
            self.download_thread = threading.Thread(target=self.download_audio, args=(self.download_complete_callback,))
            self.download_thread.start()

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
            self.update_progress_bar(percent)
        elif d['status'] == 'finished':
            self.update_progress_bar(100)

    def update_progress_bar(self, percent):
        self.progressbar['value'] = percent
        self.root.update_idletasks()

    def download_audio(self, callback):
        get_url_to_download = self.url_entry.get()
        path_to_save = self.selected_directory_entry.get()
        ffmpeg_path = self.DIR+"/ffmpeg/bin/"

        if(self.audio_type_combobox.get() == "mp4"):
            ydl_opts = {
                'format': 'best',
                'outtmpl': f'{path_to_save}/%(title)s.%(ext)s',
                'progress_hooks': [self.progress_hook],
            }

        else:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': '%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'ffmpeg_location': ffmpeg_path,
                'outtmpl': f'{path_to_save}/%(title)s.%(ext)s',
                'progress_hooks': [self.progress_hook],
            }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([get_url_to_download])
        except Exception as e:
            print(f"Exception occured: {e}")
            messagebox.showerror("Error!", "Something went wrong. Please check your preferences!")
        finally:
            time.sleep(1)
            if callback:
                self.root.after(0, callback)
            self.update_progress_bar(0)

    def download_complete_callback(self):
        messagebox.showinfo("Download Complete", "The download has been completed successfully!")

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
    # root = tk.Tk()
    root = ttkb.Window()
    app = Downloader(root)
    root.mainloop()

if __name__ == "__main__":
    main()