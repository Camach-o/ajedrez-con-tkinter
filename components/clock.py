import tkinter as tk
from PIL import Image, ImageTk
if __name__ != "__main__":
    from components import project_vars as project_vars
else: 
    from components import project_vars as project_vars

""" Changes that I'll to do it
    - Create a unique funtion to do the work that is doing update_top_timer and update_bottom_timer right now
    - Create the pause funtion
    - Terminate the automatic clock type widgets
    - Create the function to change the clock state
    - Create a function to change the clock values
"""

class Clock():
    def __init__(self, container, board_view=1):
        self.container = container
        self.board_view = board_view

        # Clock Atributes
        self.current_timer = None 

        # Top Timer
        self.top_minute_hand = project_vars.clock_time 
        self.top_second_hand = 0
        self.top_milisecond_hand = 1000
        self.top_time = tk.StringVar()
        self.update_timer(self.top_time, self.top_minute_hand, self.top_second_hand)

        # Bottom Timer
        self.bottom_minute_hand = project_vars.clock_time 
        self.bottom_second_hand = 0
        self.bottom_milisecond_hand = 1000
        self.bottom_time = tk.StringVar()
        self.update_timer(self.bottom_time, self.bottom_minute_hand, self.bottom_second_hand)

    def put_clock(self):
        # Top Clock
        top_frame = tk.Frame(self.container, bg=project_vars.OSCURO_FUERTE)
        top_frame.pack(side="top")

        top_clock = tk.Label(top_frame, textvariable=self.top_time)
        top_clock.configure(relief="solid", bg=project_vars.OSCURO_SUAVE)
        top_clock.configure(font=("Arial", 30), fg="white") 
        top_clock.grid(row=0, column=0, pady=(0, 20))

        self.top_button = tk.Button(top_frame, width=10, height=12)
        self.top_button.configure(bd=10, state="disabled", relief="sunken")
        self.top_button.configure(background="#A6A6A6", activebackground="#A6A6A6")
        self.top_button.configure(command=lambda: self.switch_active_timer("top"))
        self.top_button.grid(row=1, column=0)

        self.top_status = tk.Canvas(top_frame, width=92, height=204, relief="solid" , bd=2)
        self.top_status.configure(highlightthickness=0, background=project_vars.OSCURO_FUERTE)

        self.top_status.create_oval(23, 79, 73, 129, outline="black", width=2)
        self.top_circle = self.top_status.create_oval(32, 88, 64, 120, fill="#A6A6A6", outline="#191918")


        # Pause Button
        center_frame = tk.Frame(self.container, bg=project_vars.OSCURO_FUERTE, height=80)
        center_frame.pack(fill="both", expand=True)

        self.img_pause = ImageTk.PhotoImage(
            Image.open("contenido_grafico/imagenes_panel/pause.png")
        )

        pause_button = tk.Button(center_frame, image=self.img_pause, bd=0)
        pause_button.configure(bg=project_vars.OSCURO_FUERTE, activebackground=project_vars.OSCURO_FUERTE)
        pause_button.configure(command=self.pause)
        pause_button.place(relx=0.5, rely=0.5, anchor="center")

        # Bottom Clock
        bottom_frame = tk.Frame(self.container, bg=project_vars.OSCURO_FUERTE)
        bottom_frame.pack(side="bottom")

        bottom_clock = tk.Label(bottom_frame, textvariable=self.bottom_time)
        bottom_clock.configure(relief="solid", bg=project_vars.OSCURO_SUAVE)
        bottom_clock.configure(font=("Arial", 30), fg="white")
        bottom_clock.grid(row=1, column=0, pady=(20, 0))

        self.bottom_button = tk.Button(bottom_frame, width=10, height=12)
        self.bottom_button.configure(bd=10, state="active", relief="raised")
        self.bottom_button.configure(background="#A6A6A6", activebackground="#A6A6A6")
        self.bottom_button.configure(command=lambda: self.switch_active_timer("bottom"))
        self.bottom_button.grid(row=0, column=0)

        self.bottom_status = tk.Canvas(bottom_frame, width=92, height=204, relief="solid", bd=2)
        self.bottom_status.configure(highlightthickness=0, background=project_vars.OSCURO_FUERTE)

        self.bottom_status.create_oval(23, 79, 73, 129, outline="black", width=2)
        self.bottom_circle = self.bottom_status.create_oval(32, 88, 64, 120, fill="green", outline="#191918")

    def restart_clock(self): # Cuando se haga una nueva partida
        self.top_minute_hand = project_vars.clock_time
        self.bottom_minute_hand = project_vars.clock_time
        self.update_timer(self.top_time, self.top_minute_hand, self.top_second_hand)
        self.update_timer(self.bottom_time, self.bottom_minute_hand, self.bottom_second_hand)
    
    def pause(self):
        if self.current_timer is not None:
            self.container.after_cancel(self.current_timer)
        
        # project_vars.board.block_moves()

    # Estas funciones son las que permiten el funcionamiento del reloj

    def update_timer(self, timer, minutes, seconds):
        """ Update the time of the timer that need's to update
        
            Args:
                timer (StringVar): is the timer that will need update
                minutes (int): clock's minutes
                seconds (int): clock's seconds
        """
        
        if len(str(minutes)) < 2:
            minutes = f"0{minutes}"
        if len(str(seconds)) < 2:
            seconds = f"0{seconds}"
        timer.set(f"{minutes}:{seconds}")

    def kill_timers(self):
        if self.current_timer is not None: 
            self.container.after_cancel(self.current_timer)

    def switch_active_timer(self, timer):
        """ Change the active timer.
        
            Args:
                timer (int): Number that indicate the button that called the function.
        """

        self.kill_timers()

        if timer == "top":
            if project_vars.clock_type == 1:
                self.top_button.configure(state="disabled", relief="sunken")
                self.bottom_button.configure(state="active", relief="raised")
            else:
                self.top_status.itemconfig(self.top_circle, fill="#A6A6A6")
                self.bottom_status.itemconfig(self.bottom_circle, fill="green")

            if project_vars.clock_bonus:
                self.top_second_hand += project_vars.clock_bonus
                if self.top_second_hand > 60:
                    self.top_minute_hand += 1
                    self.top_second_hand -= 60
            self.update_timer(self.top_time, self.top_minute_hand, self.top_second_hand)
            self.update_bottom_timer()

        elif timer == "bottom":
            if project_vars.clock_type == 1:
                self.bottom_button.configure(state="disabled", relief="sunken")
                self.top_button.configure(state="active", relief="raised")
            else:
                self.top_status.itemconfig(self.top_circle, fill="green")
                self.bottom_status.itemconfig(self.bottom_circle, fill="#A6A6A6")

            if project_vars.clock_bonus:
                self.bottom_second_hand += project_vars.clock_bonus
                if self.bottom_second_hand > 60:
                    self.bottom_minute_hand += 1
                    self.bottom_second_hand -= 60
            self.update_timer(self.bottom_time, self.bottom_minute_hand, self.bottom_second_hand)
            self.update_top_timer()

    def update_top_timer(self): # Do not touch

        if self.top_second_hand == -1:
            self.top_minute_hand -= 1
            self.top_second_hand = 59

        if self.top_milisecond_hand == 0:
            self.top_second_hand -= 1
            self.top_milisecond_hand = 890

        self.top_milisecond_hand -= 1

        self.update_timer(self.top_time, self.top_minute_hand, self.top_second_hand)
        self.current_timer = self.container.after(1, self.update_top_timer)

    def update_bottom_timer(self): # Do not touch

        if self.bottom_second_hand == 0:
            self.bottom_minute_hand -= 1
            self.bottom_second_hand = 59

        if self.bottom_milisecond_hand == 0:
            self.bottom_second_hand -= 1
            self.bottom_milisecond_hand = 890

        self.bottom_milisecond_hand -= 1

        self.update_timer(self.bottom_time, self.bottom_minute_hand, self.bottom_second_hand)
        self.current_timer = self.container.after(1, self.update_bottom_timer)

    def change_clock_type(self, type):
        if type == 1:
            self.top_status.grid_forget()
            self.bottom_status.grid_forget()

            self.top_button.grid(row=1, column=0)
            self.bottom_button.grid(row=0, column=0) 

        elif type == 2:
            self.top_button.grid_forget()
            self.bottom_button.grid_forget()

            self.top_status.grid(row=1, column=0)
            self.bottom_status.grid(row=0, column=0) 

if __name__ == "__main__":
    ventana = tk.Tk()
    ventana.config(bg=project_vars.OSCURO_FUERTE)
    ventana.geometry("+400+100")
    
    frame_reloj = tk.Frame(ventana)
    frame_reloj.pack(side="left")

    r = Clock(frame_reloj, 1)
    r.put_clock()

    ventana.mainloop()