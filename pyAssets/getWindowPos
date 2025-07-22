import pygetwindow as gw
import tkinter as tk
import win32gui
import win32con

root = None
canvas = None
running = False

latest_window_rect = None  # (x, y, width, height) in screen coords of client area

def get_client_area_rect(hwnd):
    # Get client rect (relative to window)
    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    width = right - left
    height = bottom - top

    # Convert client top-left to screen coords
    point = win32gui.ClientToScreen(hwnd, (left, top))
    screen_x, screen_y = point

    return screen_x, screen_y, width, height

def _update_overlay():
    global latest_window_rect
    if not running:
        return
    windows = gw.getWindowsWithTitle('BlueStacks') # window title
    if windows:
        win = windows[0]
        if win.visible:
            hwnd = win._hWnd  # Get window handle for pywin32 calls
            
            # Get client area in screen coordinates (accurate content area)
            x, y, width, height = get_client_area_rect(hwnd)
            latest_window_rect = (x, y, width, height)
            print(f"BlueStacks client area position and size: {latest_window_rect}")
            
            root.geometry(f"{width}x{height}+{x}+{y}")
            canvas.config(width=width, height=height)
            canvas.delete("all")

            # Draw bounding box around client area
            padding = 5
            canvas.create_rectangle(
                padding, padding, width - padding, height - padding,
                outline='red', width=3
            )
    else:
        root.geometry("1x1+0+0")
    root.after(100, _update_overlay)

def draw():
    global root, canvas, running
    if running:
        return
    running = True
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.attributes('-transparentcolor', 'white')
    root.overrideredirect(True)
    root.config(bg='white')

    canvas = tk.Canvas(root, bg='white', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    _update_overlay()
    root.after(10000, clear)  # auto-clear after 10s (adjust as needed)
    root.mainloop()

def clear():
    global root, canvas, running
    if not running:
        return
    running = False
    if root:
        root.destroy()
        root = None
        canvas = None

draw()
