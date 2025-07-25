import pygetwindow as gw
import tkinter as tk
import win32gui
from localstorage import read_local_storage, write_local_storage

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
            
            # Get client area in screen coordinates
            x, y, width, height = get_client_area_rect(hwnd)
            latest_window_rect = (x, y, width, height)

            # Add data in local db
            write_local_storage("window_pos", latest_window_rect, overwrite=True)

            print(f"BlueStacks client area position and size: {latest_window_rect}")
            
            root.geometry(f"{width}x{height}+{x}+{y}")
            canvas.config(width=width, height=height)
            canvas.delete("all")

            # Draw bounding box around client area
            #padding = 5
            padding = 0
            canvas.create_rectangle(
                padding, padding, width - padding, height - padding,
                outline='red', width=3
            )

            # Test code
            # Blue rectangle: 70% width, 30% height anchored to bottom-left
            # Used for detection of card deck

            # Adjusted rect for deck
            DECK_ADJ_WIDTH = 0.7
            DECK_ADJ_HEIGHT = 0.3

            # Get the full client area in screen coordinates
            x, y, width, height = get_client_area_rect(hwnd)

            # Calculate the 70% width and 30% height
            deck_width = int(width * DECK_ADJ_WIDTH)
            deck_height = int(height * DECK_ADJ_HEIGHT)

            # Bottom-left corner: x stays the same, y needs to move *down* from top by (full height - 30%)
            deck_x = x
            deck_y = y + (height - deck_height)

            # Resulting region
            card_deck_pos = (deck_x, deck_y, deck_width, deck_height)

            # Store the region
            write_local_storage("window_pos_card_deck", card_deck_pos, overwrite=True)
            
            screen_x1 = x
            screen_y1 = y + height - int(height * DECK_ADJ_HEIGHT)
            screen_x2 = x + int(width * DECK_ADJ_WIDTH)
            screen_y2 = y + height

            # Convert to canvas coords:
            canvas_x1 = screen_x1 - x  # = 0
            canvas_y1 = screen_y1 - y
            canvas_x2 = screen_x2 - x
            canvas_y2 = screen_y2 - y

            canvas.create_rectangle(
                canvas_x1, canvas_y1, canvas_x2, canvas_y2,
                outline='blue', width=3
            )
            
            # Elixir count area — 30% of remaining width, same 30% height
            ELIXIR_WIDTH_RATIO = (1.0 - DECK_ADJ_WIDTH)  # 30% of remaining 30% width
            elixir_width = int(width * ELIXIR_WIDTH_RATIO)
            elixir_height = deck_height

            elixir_x = deck_x + deck_width  # immediately to the right of deck
            elixir_y = deck_y  # same vertical alignment as deck

            elixir_count_pos = (elixir_x, elixir_y, elixir_width, elixir_height)
            write_local_storage("window_pos_elixir_count", elixir_count_pos, overwrite=True)

            canvas.create_rectangle(
                elixir_x - x, elixir_y - y,
                elixir_x - x + elixir_width, elixir_y - y + elixir_height,
                outline='green', width=3
            )

    else:
        root.geometry("1x1+0+0")
    root.after(2000, _update_overlay)

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
    root.after(6000, clear)  # auto-clear after 6s (3 detection intervals)
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
