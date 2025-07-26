import time
from datetime import datetime

def get_formatted_epoch_time(type):
    # Get current epoch time
    epoch_time = int(time.time())
    
    # Convert epoch time to datetime object
    dt = datetime.fromtimestamp(epoch_time)
    
    # Format the date as dd-mm-yyyy
    date_str = dt.strftime('%d-%m-%Y')
    
    # Combine date and epoch in the specified format
    formatted_str = f"{type}-{date_str}-{epoch_time}"
    
    return formatted_str

# Example usage
print(get_formatted_epoch_time("screen"))
print(get_formatted_epoch_time("deck"))
print(get_formatted_epoch_time("elixir"))
from screenshot import screenshot
file_prefix = get_formatted_epoch_time("deck") + ".png"
print(file_prefix)
# screenshot("window_pos_card_deck", file_prefix)