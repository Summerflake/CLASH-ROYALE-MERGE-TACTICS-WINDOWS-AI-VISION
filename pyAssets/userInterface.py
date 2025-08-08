import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import subprocess
import platform
import re
import urllib.request
import socket

# --- Configurations ---
author = "Summerflake"
version = "1.0"
identified_window = "Bluestacks Player 1"
image_path = "C:/path/to/save/image.png"
ping_url = "https://supercell.com/en/games/clashroyale/"

# --- Global variables ---
running = True

# Create main window
root = tk.Tk()
root.title("Summerflake-CRMT-v1")
root.geometry("350x400")
root.overrideredirect(True)  # Remove window frame

# Dragging support
offset_x = 0
offset_y = 0

def start_move(event):
    global offset_x, offset_y
    offset_x = event.x
    offset_y = event.y

def stop_move(event):
    global offset_x, offset_y
    offset_x = 0
    offset_y = 0

def do_move(event):
    x = root.winfo_pointerx() - offset_x
    y = root.winfo_pointery() - offset_y
    root.geometry(f"+{x}+{y}")

# Header frame
header = tk.Frame(root, bg="#444444", height=25)
header.pack(fill=tk.X)
header_label = tk.Label(header, text="Summerflake-CRMT-v1", fg="white", bg="#444444")
header_label.pack(side=tk.LEFT, padx=5)

header.bind("<ButtonPress-1>", start_move)
header.bind("<ButtonRelease-1>", stop_move)
header.bind("<B1-Motion>", do_move)
header_label.bind("<ButtonPress-1>", start_move)
header_label.bind("<ButtonRelease-1>", stop_move)
header_label.bind("<B1-Motion>", do_move)

# Close button
def close():
    global running
    running = False
    root.destroy()

close_btn = tk.Button(header, text="X", command=close, bg="#880000", fg="white", bd=0, padx=5)
close_btn.pack(side=tk.RIGHT)

# Info frame
info_frame = tk.Frame(root)
info_frame.pack(pady=10, padx=10, fill=tk.X)

tk.Label(info_frame, text=f"Author: {author}").pack(anchor="w")
tk.Label(info_frame, text=f"Version Number: {version}").pack(anchor="w")
tk.Label(info_frame, text=f"Identified Window: {identified_window}").pack(anchor="w")
tk.Label(info_frame, text=f"Image Analysis Path: {image_path}").pack(anchor="w")

# Ping label
ping_var = tk.StringVar(value="Ping: calculating...")
ping_label = tk.Label(info_frame, textvariable=ping_var, font=("Arial", 10, "bold"))
ping_label.pack(anchor="w", pady=(10, 0))

# Output area
output_area = scrolledtext.ScrolledText(root, height=10, state='disabled', wrap=tk.WORD)
output_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# hqsWrite function to append text to output area with auto scroll
def hqsWrite(text):
    output_area.config(state='normal')
    output_area.insert(tk.END, text + "\n")
    output_area.see(tk.END)
    output_area.config(state='disabled')

# Ping utilities
def ping_ip(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", ip]
    try:
        output = subprocess.check_output(command, universal_newlines=True, stderr=subprocess.STDOUT)
        if platform.system().lower() == "windows":
            match = re.search(r"Average = (\d+)ms", output)
            if match:
                return int(match.group(1))
        else:
            match = re.search(r"time=(\d+\.\d+) ms", output)
            if match:
                return int(float(match.group(1)))
    except Exception:
        return None

def ping_website(url):
    try:
        hostname = urllib.request.urlparse(url).netloc
        ip = socket.gethostbyname(hostname)
        return ping_ip(ip)
    except Exception:
        return None

def update_ping_label(display, color):
    ping_var.set(display)
    ping_label.config(fg=color)

# Thread that continuously pings and updates the label
def ping_loop():
    while running:
        ping_ms = ping_website(ping_url)
        if ping_ms is None:
            display = "Ping: unreachable"
            color = "red"
        else:
            display = f"Ping: {ping_ms} ms"
            if ping_ms < 100:
                color = "green"
            elif ping_ms < 200:
                color = "#b5a800"
            else:
                color = "red"

        root.after(0, update_ping_label, display, color)
        time.sleep(1)

# Example usage of hqsWrite every 5 seconds
def example_output():
    count = 0
    while running:
        time.sleep(1)
        count += 1
        root.after(0, hqsWrite, f"Example output line {count}")

# Start background threads
threading.Thread(target=ping_loop, daemon=True).start()
threading.Thread(target=example_output, daemon=True).start()

root.mainloop()
running = False
