import tkinter as tk
from PIL import Image, ImageTk
from components import project_vars as pv

class Clock():
    def __init__(self, container, board_view=1):
        self.container = container
        self.board_view = board_view

        # Clock Atributes
        self._listener = [] 
        self.status = "active"
        self.active_timer = ['bottom', 'top']
        self.minutes = pv.clock_default_minutes
        self.bonus = pv.clock_default_bonus

        # Top Timer
        self.top_minute_hand = self.minutes
        self.top_second_hand = 0
        self.top_milisecond_hand = 1000
        self.top_time = tk.StringVar()
        self._update_timer(self.top_time, self.top_minute_hand, self.top_second_hand)
        self.top_timer_id = None

        # Bottom Timer
        self.bottom_minute_hand = self.minutes
        self.bottom_second_hand = 0
        self.bottom_milisecond_hand = 1000
        self.bottom_time = tk.StringVar()
        self._update_timer(self.bottom_time, self.bottom_minute_hand, self.bottom_second_hand)
        self.bottom_timer_id = None

    # Inicializa los widgets
    def put_clock(self):
        # Top Clock
        top_frame = tk.Frame(self.container, bg=pv.OSCURO_FUERTE)
        top_frame.pack(side="top")

        top_clock = tk.Label(top_frame, textvariable=self.top_time)
        top_clock.configure(relief="solid", bg=pv.OSCURO_SUAVE)
        top_clock.configure(font=("Arial", 30), fg="white") 
        top_clock.grid(row=0, column=0, pady=(0, 20))

        self.top_button = tk.Button(top_frame, width=10, height=12)
        self.top_button.configure(bd=10, state="disabled", relief="sunken")
        self.top_button.configure(background="#A6A6A6", activebackground="#A6A6A6")
        self.top_button.configure(command=self.switch_active_timer)
        self.top_button.grid(row=1, column=0)

        # Pause Button
        center_frame = tk.Frame(self.container, bg=pv.OSCURO_FUERTE, height=80)
        center_frame.pack(fill="both", expand=True)

        self.img_pause = ImageTk.PhotoImage(
            Image.open("assets/panel/pause.png")
        )

        pause_button = tk.Button(center_frame, image=self.img_pause, bd=0)
        pause_button.configure(bg=pv.OSCURO_FUERTE, activebackground=pv.OSCURO_FUERTE)
        pause_button.configure(command=self.pause)
        pause_button.place(relx=0.5, rely=0.5, anchor="center")

        # Bottom Clock
        bottom_frame = tk.Frame(self.container, bg=pv.OSCURO_FUERTE)
        bottom_frame.pack(side="bottom")

        bottom_clock = tk.Label(bottom_frame, textvariable=self.bottom_time)
        bottom_clock.configure(relief="solid", bg=pv.OSCURO_SUAVE)
        bottom_clock.configure(font=("Arial", 30), fg="white")
        bottom_clock.grid(row=1, column=0, pady=(20, 0))

        self.bottom_button = tk.Button(bottom_frame, width=10, height=12)
        self.bottom_button.configure(bd=10, state="disabled", relief="raised")
        self.bottom_button.configure(background="#A6A6A6", activebackground="#A6A6A6")
        self.bottom_button.configure(command=self.switch_active_timer)
        self.bottom_button.grid(row=0, column=0)

    # Reinicia valores
    def restart(self): # Cuando se haga una nueva partida
        # Clock Atributes
        self.kill_timers()

        # Clock Atributes
        self.active_timer = ['bottom', 'top']
        self.minutes = pv.clock_default_minutes
        self.bonus = pv.clock_default_bonus

        # Top Timer
        self.top_minute_hand = self.minutes 
        self.top_second_hand = 0
        self.top_milisecond_hand = 1000
        self._update_timer(self.top_time, self.top_minute_hand, self.top_second_hand)
        self.top_timer_id = None

        # Bottom Timer
        self.bottom_minute_hand = self.minutes 
        self.bottom_second_hand = 0
        self.bottom_milisecond_hand = 1000
        self._update_timer(self.bottom_time, self.bottom_minute_hand, self.bottom_second_hand)
        self.bottom_timer_id = None

        self.bottom_button.configure(relief="raised")
        self.top_button.configure(relief="sunken")

    # Hacer que la partida empiece con el reloj superior (por si toca jugar con negras)
    def start_with_top_timer(self):
        self.active_timer.reverse()
        self.top_button.configure(relief="raised")
        self.bottom_button.configure(relief="sunken")

    # Agrega a un observador
    def suscribe_a_watcher(self, callback):
        self._listener = callback

    # Actualiza el tiempo de los relojes
    def update_clock_timers(self, minutes, bonus):
        self.minutes = minutes
        self.bonus = bonus
        self.top_minute_hand = minutes
        self.bottom_minute_hand = minutes
        for timer in (self.top_time, self.bottom_time):
            self._update_timer(timer, minutes, 0)

    # Detiene al reloj
    def kill_timers(self):
        if self.top_timer_id is not None:
            self.container.after_cancel(self.top_timer_id)

        if self.bottom_timer_id is not None:
            self.container.after_cancel(self.bottom_timer_id)

    # Pausa el reloj
    def pause(self):
        self._listener()

    # Actualiza el tiempo del reloj
    def _update_timer(self, timer, minutes, seconds):
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

    # Revisar el tiempo que queda en el reloj #######################################
    def _time_remaining(self, minute_hand, second_hand):
        if minute_hand == 0 and second_hand == 0:
            self._listener('finish_time')
            return False
        return True
       
    # Actualiza el reloj superior
    def _update_top_timer(self): # Do not touch
        # print("primera: ", self.minutes)

        if not self._time_remaining(self.top_minute_hand, self.top_second_hand):
            self.container.after_cancel(self.top_timer_id)
            return

        if self.top_second_hand == -1:
            self.top_minute_hand -= 1
            self.top_second_hand = 59
        if self.top_milisecond_hand == 0:
            self.top_second_hand -= 1
            self.top_milisecond_hand = 890
        self.top_milisecond_hand -= 1

        self._update_timer(self.top_time, self.top_minute_hand, self.top_second_hand)
        self.top_timer_id = self.container.after(1, self._update_top_timer)
        # print("segunda: ", self.minutes)

    # Actualiza el reloj inferior
    def _update_bottom_timer(self): # Do not touch

        if not self._time_remaining(self.bottom_minute_hand, self.bottom_second_hand):
            self.container.after_cancel(self.bottom_timer_id)
            return

        if self.bottom_second_hand == 0:
            self.bottom_minute_hand -= 1
            self.bottom_second_hand = 59
        if self.bottom_milisecond_hand == 0:
            self.bottom_second_hand -= 1
            self.bottom_milisecond_hand = 890
        self.bottom_milisecond_hand -= 1

        self._update_timer(self.bottom_time, self.bottom_minute_hand, self.bottom_second_hand)
        self.bottom_timer_id = self.container.after(1, self._update_bottom_timer)

    # Intercambia el reloj activo
    def switch_active_timer(self): # Puede revisarse los tiempos
        """ Change the active timer.
        
            Args:
                timer (str): Indicate the button that called the function.
        """

        if self.status == "desactive":
            return

        self.kill_timers()

        if self.active_timer[0] == "top":
            self.top_button.configure(relief="sunken")
            self.bottom_button.configure(relief="raised")
            if self.bonus:
                self.top_second_hand += self.bonus
                if self.top_second_hand > 60:
                    self.top_minute_hand += 1
                    self.top_second_hand -= 60
            self._update_timer(self.top_time, self.top_minute_hand, self.top_second_hand)
            self._update_bottom_timer()

        elif self.active_timer[0] == "bottom":
            self.bottom_button.configure(relief="sunken")
            self.top_button.configure(relief="raised")
            if self.bonus:
                self.bottom_second_hand += self.bonus
                if self.bottom_second_hand > 60:
                    self.bottom_minute_hand += 1
                    self.bottom_second_hand -= 60
            self._update_timer(self.bottom_time, self.bottom_minute_hand, self.bottom_second_hand)
            self._update_top_timer()

        self.active_timer.reverse()
