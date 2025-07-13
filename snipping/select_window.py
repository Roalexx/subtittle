import ctypes

user32 = ctypes.windll.user32

def get_window_title(hwnd):
    length = user32.GetWindowTextLengthW(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buff, length + 1)
    return buff.value

def list_open_windows():
    EnumWindows = user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(
        ctypes.c_bool, ctypes.c_int, ctypes.c_int
    )

    windows = []

    def foreach_window(hwnd, lParam):
        if user32.IsWindowVisible(hwnd):
            title = get_window_title(hwnd)
            if title:
                windows.append((hwnd, title))
        return True

    EnumWindows(EnumWindowsProc(foreach_window), 0)
    return windows

if __name__ == "__main__":
    open_windows = list_open_windows()
    for hwnd, title in open_windows:
        print(title)
