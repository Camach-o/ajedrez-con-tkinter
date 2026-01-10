"""
Here I create an "alert" to show info to user.
Why don't I used messagebox? because messagebox
freezes the mainloop.
"""

import tkinter as tk
import components.project_vars as pv

def show_info(tittle, message):

    alert_window = tk.Toplevel(pv.window)
    alert_window.title(tittle)
    label = tk.Label(alert_window, text=message, padx=20, pady=20)
    label.configure(font=("Calibri Bold", 18), bg=pv.GRAY, fg="white")
    label.pack()

    main_window_geometry = pv.window.winfo_geometry()
    position = main_window_geometry.split("+")
    main_window_x_position = int(position[1])
    main_window_y_position = int(position[2])

    alert_window.update()
    height_alert_window = int(alert_window.winfo_height())
    width_alert_window = int(alert_window.winfo_width())

    x_alert_windows_position = ((main_window_x_position + (pv.width_windows / 2)) - (width_alert_window / 2))
    y_alert_windows_position = ((main_window_y_position + (pv.height_windows / 2)) - (height_alert_window / 2))
    alert_window.geometry(f"+{int(x_alert_windows_position)}+{int(y_alert_windows_position)}")

    alert_window.transient(pv.window)
    alert_window.grab_set()
