import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import youtube_dl

def force_english_paste(event):
    try:
        clipboard_text = root.clipboard_get()
        url_entry.insert(tk.INSERT, clipboard_text)
    except tk.TclError:
        pass
    return "break"

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        download_directory.set(directory)


def download_videos():
    urls = url_entry.get("1.0", tk.END).strip().split("\n")
    download_path = download_directory.get()

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'progress_hooks': [update_progress_bar],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            try:
                ydl.download([url])
            except youtube_dl.utils.DownloadError as e:
                print(f"Error downloading {url}: {e}")
            progress_bar['value'] = 0


def update_progress_bar(progress):
    if progress['status'] == 'downloading':
        downloaded_bytes = progress.get('downloaded_bytes', 0)
        total_bytes = progress.get('total_bytes', 0)

        if total_bytes:
            percentage = downloaded_bytes / total_bytes * 100
            progress_bar['value'] = percentage
            root.update_idletasks()


root = tk.Tk()
root.title("YouTubeD")

download_directory = tk.StringVar()
download_directory.set(os.path.expanduser("~"))

url_label = tk.Label(root, text="Enter YouTube URLs: ", font=("Arial", 12))
url_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

url_entry = tk.Text(root, width=60, height=10, font=("Arial", 12), bg="#D3D3D3", fg="black")
url_entry.grid(row=1, column=0, columnspan=3, pady=10, padx=10)
url_entry.bind("<Control-v>", force_english_paste)


location_label = tk.Label(root, text="Download location:", font=("Arial", 12))
location_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")

location_entry = tk.Entry(root, textvariable=download_directory, state="readonly", bg="#D3D3D3", readonlybackground="#D3D3D3", font=("Arial", 12))
location_entry.grid(row=2, column=1, pady=10, padx=10, sticky="ew")

browse_button = tk.Button(root, text="Browse", command=browse_directory, font=("Arial", 12))
browse_button.grid(row=2, column=2, pady=10, padx=10, sticky="ew")

start_download_button = tk.Button(root, text="Start Download", command=download_videos,font=("Arial", 12))
start_download_button.grid(row=4, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=5, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

root.columnconfigure(1, weight=1)

center_window(root)
root.mainloop()
