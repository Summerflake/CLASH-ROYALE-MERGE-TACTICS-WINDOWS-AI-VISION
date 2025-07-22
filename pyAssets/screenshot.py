# cords used for screenshot and draw red rect is two sets of data so cannot use same set of cords to complete the tasks
import ctypes
from PIL import ImageGrab
import time
import os

def get_scaling_factor():
    user32 = ctypes.windll.user32
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        pass
    dpi_x = user32.GetDpiForSystem()
    return dpi_x / 96

def screenshotLocation(x, y, width, height, save_path):
    scale = get_scaling_factor()
    x_physical = int(x * scale)
    y_physical = int(y * scale)
    width_physical = int(width * scale)
    height_physical = int(height * scale)

    time.sleep(0.1)
    bbox = (x_physical, y_physical, x_physical + width_physical, y_physical + height_physical)
    img = ImageGrab.grab(bbox)
    img.save(save_path)
    print(f"Screenshot saved to: {save_path}")

# Example:
x, y, width, height = 647, 181, 598, 351

desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
save_path = os.path.join(desktop, 'screenshot3.png')
print(save_path)
screenshotLocation(x, y, width, height, save_path)
