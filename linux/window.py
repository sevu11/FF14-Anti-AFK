from Xlib import X, display
from ewmh import EWMH

def get_window_titles():
    ewmh = EWMH()
    window_titles = []

    # Get all windows
    root = display.Display().screen().root
    window_ids = root.get_full_property(
        ewmh.display.intern_atom('_NET_CLIENT_LIST'), X.AnyPropertyType
    ).value

    # Iterate over all windows and get their titles
    for window_id in window_ids:
        window = ewmh.display.create_resource_object('window', window_id)
        window_title = window.get_full_property(
            ewmh.display.intern_atom('_NET_WM_NAME'), 0
        ).value
        window_titles.append(window_title)

    return window_titles

# Example usage
if __name__ == '__main__':
    titles = get_window_titles()
    for title in titles:
        print(title)
