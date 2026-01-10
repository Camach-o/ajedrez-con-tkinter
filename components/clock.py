import tkinter as tk
from PIL import Image, ImageTk
import components.alert as alert
from components import project_vars as pv

class Clock():
    def __init__(self, container):
        self.container = container
        self.top_button = None
        self.bottom_button = None
        self.img_pause = None

        # Clock attributes
        self._listener_function = None
        self.status = "active"
        self.active_timer = ['bottom', 'top']
        self.minutes = pv.clock_default_minutes
        self.bonus = pv.clock_default_bonus
        self.active_pause = False
        self.kill_timers_swicth = False

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

    def put_clock(self):
        """ Create the clock widgets."""
        # Top Clock
        top_frame = tk.Frame(self.container, bg=pv.DARK_GRAY)
        top_frame.pack(side="top")

        top_clock = tk.Label(top_frame, textvariable=self.top_time)
        top_clock.configure(relief="solid", bg=pv.GRAY)
        top_clock.configure(font=("Arial", 30), fg="white")
        top_clock.grid(row=0, column=0, pady=(0, 20))

        self.top_button = tk.Button(top_frame, width=10, height=12)
        self.top_button.configure(bd=10, state="disabled", relief="sunken")
        self.top_button.configure(background="#A6A6A6", activebackground="#A6A6A6")
        self.top_button.configure(command=self.switch_active_timer)
        self.top_button.grid(row=1, column=0)

        # Pause Button
        center_frame = tk.Frame(self.container, bg=pv.DARK_GRAY, height=80)
        center_frame.pack(fill="both", expand=True)

        self.img_pause = ImageTk.PhotoImage(
            Image.open("assets/panel/pause.png")
        )

        pause_button = tk.Button(center_frame, image=self.img_pause, bd=0)
        pause_button.configure(bg=pv.DARK_GRAY, activebackground=pv.DARK_GRAY)
        pause_button.configure(command=self.pause)
        pause_button.place(relx=0.5, rely=0.5, anchor="center")

        # Bottom Clock
        bottom_frame = tk.Frame(self.container, bg=pv.DARK_GRAY)
        bottom_frame.pack(side="bottom")

        bottom_clock = tk.Label(bottom_frame, textvariable=self.bottom_time)
        bottom_clock.configure(relief="solid", bg=pv.GRAY)
        bottom_clock.configure(font=("Arial", 30), fg="white")
        bottom_clock.grid(row=1, column=0, pady=(20, 0))

        self.bottom_button = tk.Button(bottom_frame, width=10, height=12)
        self.bottom_button.configure(bd=10, state="disabled", relief="raised")
        self.bottom_button.configure(background="#A6A6A6", activebackground="#A6A6A6")
        self.bottom_button.configure(command=self.switch_active_timer)
        self.bottom_button.grid(row=0, column=0)

    def restart(self):
        self.kill_timers()

        # Clock attributes
        self.active_timer = ['bottom', 'top']
        self.minutes = pv.clock_default_minutes
        self.bonus = pv.clock_default_bonus
        self.active_pause = False

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

    def set_time(self, minutes, bonus):
        """ Set the time configuration."""
        self.minutes = minutes
        self.bonus = bonus
        self.top_minute_hand = minutes
        self.bottom_minute_hand = minutes
        for timer in (self.top_time, self.bottom_time):
            self._update_timer(timer, minutes, 0)

    def starts_with_top_timer(self):
        """ Starts the clock with the top timer."""
        self.active_timer.reverse()
        self.top_button.configure(relief="raised")
        self.bottom_button.configure(relief="sunken")

    def suscribe_observer(self, callback):
        """ Subscribe an observer to notify him when the pause button is pressed."""
        self._listener_function = callback

    def pause(self, pause_by="main_player"):
        """ Pause or active the clock."""
        if pv.there_is_an_active_server and not pv.is_there_a_connected_player:
            return

        if not pv.ongoing_game:
            return

        if self.active_timer[0] != "bottom" and pv.partide.game_mode == "stockfish":
            alert.show_info("Advertencia.", "No puedes pausar el reloj si no es tu turno.")
            return

        if pause_by == "main_player" and pv.there_is_an_active_server:
            self._listener_function()

        if self.active_pause: # To pause clock
            self.active_pause = False
            if self.active_timer[0] == "top":
                self._update_top_timer()
            elif self.active_timer[0] == "bottom":
                self._update_bottom_timer()
            pv.dont_touch = False
            alert.show_info(tittle="Reloj reanudado",
                            message="El reloj se ha activado, ya puedes volver a mover.")
        else: # To active clock
            self.kill_timers()
            self.active_pause = True
            pv.dont_touch = True
            alert.show_info(tittle="Reloj detenido",
                            message="Mientras el reloj esté en pausa no se puede mover.")

    def kill_timers(self):
        """ Stop the timer updates."""
        self.kill_timers_swicth = True
        if self.top_timer_id is not None:
            self.container.after_cancel(self.top_timer_id)
        if self.bottom_timer_id is not None:
            self.container.after_cancel(self.bottom_timer_id)
        self.kill_timers_swicth = False

    def switch_active_timer(self):
        """ Change the active timer."""
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

    def _update_timer(self, timer, minutes, seconds):
        """ Update minutes and seconds of the timer that needs to be update

            Args:
                timer (StringVar): is the timer that will needs be update.
                minutes (int): clock's minutes
                seconds (int): clock's seconds
        """

        if len(str(minutes)) < 2:
            minutes = f"0{minutes}"
        if len(str(seconds)) < 2:
            seconds = f"0{seconds}"
        timer.set(f"{minutes}:{seconds}")

    def _update_top_timer(self):
        if self.kill_timers_swicth:
            return
        if not self._time_remaining(self.top_minute_hand, self.top_second_hand):
            self.container.after_cancel(self.top_timer_id)
            pv.dont_touch = True
            alert.show_info(tittle="Partida finalizada.",
                            message="¡HAS GANADO!\nTu oponente se ha quedado sin tiempo.")
            return

        if self.top_second_hand == 0:
            self.top_minute_hand -= 1
            self.top_second_hand = 59
        if self.top_milisecond_hand == 0:
            self.top_second_hand -= 1
            self.top_milisecond_hand = 890
        self.top_milisecond_hand -= 1

        self._update_timer(self.top_time, self.top_minute_hand, self.top_second_hand)
        if not self.kill_timers_swicth:
            self.top_timer_id = self.container.after(1, self._update_top_timer)

    def _update_bottom_timer(self):
        if self.kill_timers_swicth:
            return
        if not self._time_remaining(self.bottom_minute_hand, self.bottom_second_hand):
            self.container.after_cancel(self.bottom_timer_id)
            pv.dont_touch = True
            alert.show_info(tittle="Partida finalizada.",
                            message="has perdido...\nTe has quedado sin tiempo.")
            return

        if self.bottom_second_hand == 0:
            self.bottom_minute_hand -= 1
            self.bottom_second_hand = 59
        if self.bottom_milisecond_hand == 0:
            self.bottom_second_hand -= 1
            self.bottom_milisecond_hand = 890
        self.bottom_milisecond_hand -= 1

        self._update_timer(self.bottom_time, self.bottom_minute_hand, self.bottom_second_hand)
        if not self.kill_timers_swicth:
            self.bottom_timer_id = self.container.after(1, self._update_bottom_timer)

    def _time_remaining(self, minute_hand, second_hand):
        """ Check if there are any minutes and seconds left.

            Return: true or false to indicate if are time remaining.
        """
        if minute_hand == 0 and second_hand == 0:
            return False
        return True
