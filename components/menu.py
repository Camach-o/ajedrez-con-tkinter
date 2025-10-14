if __name__ == "__main__":
    import tkinter as tk
    from tkinter import messagebox
    import project_vars as project_vars 
else:
    import tkinter as tk
    from tkinter import messagebox
    import components.project_vars as project_vars

class GameMenu(): # Falta por hacer
    def __init__(self):
        pass

class DifficultyMenu(): # Falta por hacer
    def __init__(self):
        pass

class ClockMenu(): # Falta por terminar
    def __init__(self, frame):
        self.frame = frame

        # Clock status
        self.status_label = tk.Label(self.frame, bg=project_vars.OSCURO_SUAVE)
        self.status_label.configure(text="Estado del Reloj", font=("Calibri Bold", 18), fg="white")

        self.selected_status = tk.IntVar()
        self.selected_status.set(project_vars.clock_status)

        self.active_option = tk.Radiobutton(self.frame, text="Activo", variable=self.selected_status, value=1)
        self.active_option.configure(bg=project_vars.OSCURO_SUAVE, activebackground=project_vars.OSCURO_SUAVE)      
        self.active_option.configure(fg="white", font=("Calibri Bold", 14), activeforeground="white")
        self.active_option.configure(selectcolor=project_vars.OSCURO_SUAVE)

        self.disable_option = tk.Radiobutton(self.frame, text="Desactivado", variable=self.selected_status, value=2)
        self.disable_option.configure(bg=project_vars.OSCURO_SUAVE, activebackground=project_vars.OSCURO_SUAVE)      
        self.disable_option.configure(fg="white", font=("Calibri Bold", 14), activeforeground="white")
        self.disable_option.configure(selectcolor=project_vars.OSCURO_SUAVE)

        # Clock type
        self.type_label = tk.Label(self.frame, bg=project_vars.OSCURO_SUAVE)
        self.type_label.configure(text="Tipo de Reloj", font=("Calibri Bold", 18), fg="white")
        
        self.selected_type = tk.IntVar()
        self.selected_type.set(project_vars.clock_type)

        self.manual_option = tk.Radiobutton(self.frame, text="Manual", variable=self.selected_type, value=1)
        self.manual_option.configure(bg=project_vars.OSCURO_SUAVE, activebackground=project_vars.OSCURO_SUAVE)      
        self.manual_option.configure(fg="white", font=("Calibri Bold", 14), activeforeground="white")
        self.manual_option.configure(selectcolor=project_vars.OSCURO_SUAVE)

        self.automatic_option = tk.Radiobutton(self.frame, text="Automatico", variable=self.selected_type, value=2)
        self.automatic_option.configure(bg=project_vars.OSCURO_SUAVE, activebackground=project_vars.OSCURO_SUAVE)      
        self.automatic_option.configure(fg="white", font=("Calibri Bold", 14), activeforeground="white")
        self.automatic_option.configure(selectcolor=project_vars.OSCURO_SUAVE)
        
        # Time and Increment section
        def show_listbox(listbox, entry):
            if listbox.winfo_manager():
                hide_listbox(listbox)
            else:
                listbox.place(x=entry.winfo_x()-2, y=entry.winfo_y() + entry.winfo_height())

        def hide_listbox(listbox):
            listbox.selection_clear(0, tk.END)
            listbox.place_forget()

        def select_option(listbox, entry):
            try:
                selection = listbox.get(listbox.curselection())
                entry.delete(0, tk.END)
                entry.insert(0, selection)
                hide_listbox(listbox)
            except:
                pass # When the cursor is in a listbox and we select some of the other listbox generate a error
            
        def validate_entry(text):
            return text == "" or (text.isdigit() and len(text) <= 2)
        vcmd = (self.frame.register(validate_entry), "%P")

        # Time
        self.time_label = tk.Label(self.frame, bg=project_vars.OSCURO_SUAVE)
        self.time_label.configure(text="Tiempo", font=("Calibri Bold", 14), fg="white")

        self.time_entry = tk.Entry(self.frame, width=20, cursor="arrow", bg="#A6A6A6", relief="raised", bd=1)
        self.time_entry.configure(validate="key", validatecommand=vcmd)
        self.time_entry.insert(0, project_vars.clock_time)
        self.time_entry.pack_propagate(False)
        
        time_list = tk.Listbox(self.frame, width=20, height=3, bg="#A6A6A6", relief="raised", bd=2, highlightthickness=0)
        time_list.bind("<<ListboxSelect>>", lambda _:select_option(time_list, self.time_entry))
        preset_time = ["1", "3", "5", "10", "15"]
        for minute in preset_time:
            time_list.insert(tk.END, minute)

        self.show_time_menu = tk.Button(self.time_entry, text="v")
        self.show_time_menu.configure(command=lambda:show_listbox(time_list, self.time_entry))
        self.show_time_menu.pack(side="right")

        # Increment
        self.bonus_label = tk.Label(self.frame, bg=project_vars.OSCURO_SUAVE)
        self.bonus_label.configure(text="Bonus", font=("Calibri Bold", 14), fg="white")

        self.bonus_entry = tk.Entry(self.frame, width=20, cursor="arrow", bg="#A6A6A6", relief="raised", bd=1)
        self.bonus_entry.configure(validate="key", validatecommand=vcmd)
        self.bonus_entry.insert(0, project_vars.clock_bonus)
        self.bonus_entry.pack_propagate(False)

        bonus_list = tk.Listbox(self.frame, width=20, height=3, bg="#A6A6A6", relief="raised", bd=2, highlightthickness=0)
        bonus_list.bind("<<ListboxSelect>>", lambda _:select_option(bonus_list, self.bonus_entry))
        preset_bonus = ["1", "2", "3", "5", "10"]
        for bonus in preset_bonus:
            bonus_list.insert(tk.END, bonus)

        self.show_bonus_menu = tk.Button(self.bonus_entry, text="v")
        self.show_bonus_menu.configure(command=lambda:show_listbox(bonus_list, self.bonus_entry))
        self.show_bonus_menu.pack(side="right")

    def save(self):

        if project_vars.clock_status != self.selected_status.get():
            if self.selected_status.get() == 1:
                project_vars.clock_frame.grid(row=1, column=0, padx=6, pady=8)
            elif self.selected_status.get() == 2:
                project_vars.clock_frame.grid_forget()
            project_vars.clock_status = self.selected_status.get()

        if project_vars.clock_type != self.selected_type.get():
            project_vars.clock_type = self.selected_type.get()
            project_vars.clock.change_clock_type(self.selected_type.get())

        project_vars.clock_time = int(self.time_entry.get())
        project_vars.clock_bonus = int(self.bonus_entry.get())

        project_vars.clock.restart_clock()

        return True

    def show(self):
        self.status_label.place(relx=0.12, rely=0.08)
        self.active_option.place(relx=0.07, rely=0.3)
        self.disable_option.place(relx=0.25, rely=0.3)
        self.type_label.place(relx=0.6, rely=0.08)
        self.manual_option.place(relx=0.52, rely=0.3)
        self.automatic_option.place(relx=0.72, rely=0.3)
        self.time_label.place(relx=0.1, rely=0.56)
        self.time_entry.place(relx=0.23, rely=0.58)
        self.bonus_label.place(relx=0.57, rely=0.56)
        self.bonus_entry.place(relx=0.68, rely=0.58)

    def hide(self):
        self.status_label.place_forget()
        self.active_option.place_forget()
        self.disable_option.place_forget()
        self.type_label.place_forget()
        self.type_label.place_forget()
        self.manual_option.place_forget()
        self.automatic_option.place_forget()
        self.time_label.place_forget()
        self.time_entry.place_forget()
        self.bonus_label.place_forget()
        self.bonus_entry.place_forget()
        self.frame.focus_set()

class MatchMenu(): # Falta por hacer
    def __init__(self):
        pass

class StyleMenu(): # Falta por terminar
    def __init__(self, frame):
        self.frame = frame

        # White squares
        self.white_label = tk.Label(self.frame, text="Casillas Blancas", fg="white")
        self.white_label.configure(font=("Calibri Bold", 18), bg=project_vars.OSCURO_SUAVE)
        self.white_entry = tk.Entry(self.frame, width=12, bg="#A6A6A6")
        self.white_entry.configure(font=("Calibri Bold", 12), fg="white", relief="raised", bd=2)
        self.white_entry.insert(0, project_vars.white_theme.upper())
        
        # Black squares
        self.black_label = tk.Label(self.frame, text="Casillas Negras", fg="white")
        self.black_label.configure(font=("Calibri Bold", 18), bg=project_vars.OSCURO_SUAVE)
        self.black_entry = tk.Entry(self.frame, width=12, bg="#A6A6A6")
        self.black_entry.configure(font=("Calibri Bold", 12), fg="black", relief="raised", bd=2)
        self.black_entry.insert(0, project_vars.black_theme.upper())

        # Color display
        self.check_color = tk.Button(self.frame, width=10, text="<PROBAR>", font=("Calibri Bold", 10))
        self.check_color.configure(bg="#A6A6A6", command=self._update_color)
        self.color_view = tk.Frame(self.frame, bd=3, relief="solid")
        self.square_list = []
        for row in range(2):
            for column in range(2):
                square = tk.Frame(self.color_view, width=70, height=70)
                square.grid(column=column, row=row)
                self.square_list.append(square)
        self._update_color()

    def _update_color(self):
        try:
            if self.white_entry.get() == self.black_entry.get():
                raise Exception
            color = [self.white_entry.get(), self.black_entry.get()]
            for loop, square in enumerate(self.square_list):
                square.configure(bg=color[0])
                if loop == 1:
                    continue
                else: 
                    color.reverse()
        except:
            messagebox.showerror("HUBO UN ERROR", "La configuración seleccionada no puede ser aplicada.")
            return False
        else:
            return True

    def save(self):
        if self._update_color():
            project_vars.white_theme = self.white_entry.get().upper()
            project_vars.black_theme = self.black_entry.get().upper()
            project_vars.board.set_theme(project_vars.white_theme, project_vars.black_theme)
            return True
        return False

    def show(self):
        self.white_label.place(x=50, rely=0.22)
        self.white_entry.place(relx=0.42, rely=0.25)
        self.black_label.place(x=50, rely=0.52)
        self.black_entry.place(relx=0.42, rely=0.54)
        self.color_view.place(relx=0.80, rely=0.42, anchor="center")
        self.check_color.place(relx=0.44, rely=0.78)

    def hide(self):
        self.white_entry.delete(0, tk.END)
        self.white_entry.insert(0, project_vars.white_theme)
        self.black_entry.delete(0, tk.END)
        self.black_entry.insert(0, project_vars.black_theme)
        self.frame.focus_set()
        self.white_label.place_forget()
        self.white_entry.place_forget()
        self.black_label.place_forget()
        self.black_entry.place_forget()
        self.color_view.place_forget()
        self.check_color.place_forget()

class CreditsMenu(): # Falta por hacer
    def __init__(self):
        pass

class Menu(tk.Frame):
    def __init__(self, root, **kwargs):
        self.root = root
        self.active_menu = None

        #   Set configure of the frame
        super().__init__(root, width=600, height=250, relief="solid", **kwargs)
        self.configure(bd="2", bg=project_vars.OSCURO_SUAVE) # , highlightthickness=0
        self.propagate(False)
        self.menu_place = None 

        #   Create the save/cancel buttons of the menu
        self.save_button = tk.Button(self.root, width=10, text="Guardar", bg="#A6A6A6")
        self.save_button.configure(font=project_vars.FUENTE_BOTONES_MENU, activebackground="#A6A6A6")
        self.save_button.configure(command=self.save_configuration)
        self.cancel_button = tk.Button(self.root, width=10, text="Cancelar", bg="#A6A6A6")
        self.cancel_button.configure(font=project_vars.FUENTE_BOTONES_MENU, activebackground="#A6A6A6")
        self.cancel_button.configure(command=self.hide_menu)

        #   Inicializate options

        self.game_menu = None # GameMenu(self)
        self.difficulty_menu = None # DifficultyMenu(self)
        self.clock_menu = ClockMenu(self)
        self.match_menu = None # MatchMenu(self)
        self.style_menu = StyleMenu(self)
        self.credits_menu = None # CreditsMenu(self)

    def _get_menu_place(self): # No tocar
        """ Returns the coordinates where the menu will be placed."""

        self.root.update()
        height_root = self.root.winfo_height()
        width_root = self.root.winfo_width()
        height_menu = int(self.configure().get("height")[-1])
        width_menu = int(self.configure().get("width")[-1])

        y_menu = (height_root / 2 - (height_root * 10 / 100)) - height_menu / 2
        x_menu = (width_root / 2) - width_menu / 2
        y_button = (y_menu+4 + height_menu) - 20 # The button's heigth it's 40
        x_save = x_menu+147
        x_cancel = x_menu+347

        self.menu_place = {"menu": {"x": x_menu, "y": y_menu},
                           "save": {"x": x_save, "y": y_button},
                           "cancel": {"x": x_cancel, "y": y_button}}

    def show_menu(self, option): # No tocar
        """ Displays the menu and widgets for the selected option.
        
        - option (event): Widget that called the function.
        """

        option_called = option.widget.configure().get("text")[-1]
        if option_called in project_vars.menu_options:
            # if option_called == "Partida":
            #     self.active_menu = self.game_menu
            # elif option_called == "Dificultad":
            #     self.active_menu = self.difficulty_menu
            if option_called == "Reloj":
                self.active_menu = self.clock_menu
            # elif option_called == "Emparejamiento":
            #     self.active_menu = self.match_menu
            elif option_called == "Estilo":
                self.active_menu = self.style_menu
            # elif option_called == "Créditos":
            #     self.active_menu = self.credits_menu
            else:
                return

        if not self.menu_place:
            self._get_menu_place()

        if project_vars.ongoing_game and (option_called == "Dificultad" or option_called == "Reloj" or option_called == "Emparejamiento"):
            messagebox.showwarning("FINALIZA LA PARTIDA", "Mientras haya una partida en juego no se pueden realizar nuevos ajustes.")
        else:
            self.place(x=self.menu_place["menu"]["x"], y=self.menu_place["menu"]["y"])
            self.save_button.place(x=self.menu_place["save"]["x"], y=self.menu_place["save"]["y"])
            self.cancel_button.place(x=self.menu_place["cancel"]["x"], y=self.menu_place["cancel"]["y"])
            self.active_menu.show()

    def save_configuration(self):
        """ Save the new settings for the selected option and update the game."""

        if self.active_menu:
            if self.active_menu.save():
                self.hide_menu()

    def hide_menu(self):
        self.active_menu.hide()
        self.active_menu = None
        self.save_button.place_forget()
        self.cancel_button.place_forget()
        self.place_forget() 


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")

    mymenu = Menu(root)
    mymenu.pack()

    clock = ClockMenu(mymenu)
    clock.show()

    
    def fofo(event):
        print(root.focus_displayof())

    root.bind("<Button-2>", mymenu.show_menu)
    # root.bind("<Button-1>", lambda _:clock.hide_listbox())
    # root.bind("<Button-1>", fofo)


    root.mainloop()