import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp
import os
import threading
from PIL import Image, ImageTk

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        download_path.set(directory)

def start_download():
    download_button.config(state=tk.DISABLED)
    threading.Thread(target=download_video).start()

def progress_hook(d):
    if d['status'] == 'downloading':
        if not progress_bar.winfo_viewable():  # Check if progress bar is hidden
            progress_bar.grid()
            progress_label.grid()
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes', 0)
        if total > 0:
            percentage = int(downloaded / total * 100)
            progress_bar['value'] = percentage
            progress_label.config(text=f"Downloading... {percentage}%")
        else:
            progress_bar['value'] = 0
            progress_label.config(text="Starting download...")
    elif d['status'] == 'finished':
        progress_bar['value'] = 100
        progress_label.config(text="Download completed")
        download_button.config(state=tk.NORMAL)
        progress_bar.grid_remove()
        progress_label.grid_remove()

def download_video():
    url = url_entry.get()
    path = download_path.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL")
        download_button.config(state=tk.NORMAL)
        return
    if not path:
        messagebox.showerror("Error", "Please select a download location")
        download_button.config(state=tk.NORMAL)
        return
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook]
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Video downloaded successfully")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        download_button.config(state=tk.NORMAL)
        progress_bar.grid_remove()
        progress_label.grid_remove()

def toggle_mode():
    if dark_mode.get():
        root.config(bg="black")
        url_label.config(bg="black", fg="white")
        location_label.config(bg="black", fg="white")
        progress_label.config(bg="black", fg="white")
        dark_mode_switch.config(bg="black", fg="white", selectcolor="black")
    else:
        root.config(bg="white")
        url_label.config(bg="white", fg="black")
        location_label.config(bg="white", fg="black")
        progress_label.config(bg="white", fg="black")
        dark_mode_switch.config(bg="white", fg="black", selectcolor="white")

# Create the main window
root = tk.Tk()
root.title("YouTube Video Downloader")

# Set the icon for the window
img = Image.open('nihal.png')
icon = ImageTk.PhotoImage(img)
root.iconphoto(True, icon)

# Create and place the widgets
url_label = tk.Label(root, text="YouTube URL:", bg="white")
url_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew", columnspan=2)

location_label = tk.Label(root, text="Download Location:", bg="white")
location_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
download_path = tk.StringVar()
path_entry = tk.Entry(root, textvariable=download_path, width=50)
path_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew", columnspan=2)

browse_button = tk.Button(root, text="Browse", command=browse_directory)
browse_button.grid(row=1, column=3, padx=10, pady=10, sticky="w")

download_button = tk.Button(root, text="Download", command=start_download)
download_button.grid(row=2, column=1, pady=20, sticky="ew", columnspan=2)

# Add a progress bar and label, initially hidden
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=3, column=1, pady=10, sticky="ew", columnspan=2)
progress_bar.grid_remove()

progress_label = tk.Label(root, text="", bg="white")
progress_label.grid(row=4, column=1, columnspan=2)
progress_label.grid_remove()

# Dark mode toggle
dark_mode = tk.BooleanVar()
dark_mode_switch = tk.Checkbutton(root, text="Dark Mode", variable=dark_mode, command=toggle_mode, bg="white")
dark_mode_switch.grid(row=5, column=1, pady=10, sticky="ew", columnspan=2)

# Configure column weights for responsiveness
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)

# Run the application
root.config(bg="white")
root.mainloop()
