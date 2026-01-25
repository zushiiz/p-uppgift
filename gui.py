import tkinter as tk

class GUI():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("main-window")
        window_width = 800
        window_height = 500
        self.root.geometry(f"{window_width}x{window_height}")
        left_frame_width = window_width//3 

        # Terminal 
        self.terminal_frame =  tk.Frame(
            self.root,
            height=window_height,
            width=800,

            bd=1, #Temporary
            relief="solid"

            )
        self.terminal_frame.grid_propagate(False)        
        scrollbar = tk.Scrollbar(self.terminal_frame)
        scrollbar.pack(side="right", fill="y")
        self.terminal_frame.grid(column=1, row=0, rowspan=2)

        # Player actions
        self._actions_frame = tk.Frame(
            self.root,
            height=window_height//3,
            width=left_frame_width,

            bd=1, #Temporary
            relief="solid"
            )
        self._actions_frame.grid(row=1, column=0)
        self._actions_frame.grid_propagate(False)

        self.actions_box = tk.Listbox(self._actions_frame, width=25)

        # Buttons
        self._button_frame = tk.Frame(
            self.root,
            height=window_height//3,
            width=left_frame_width,
            bd=1, #Temporary
            relief="solid"
            )
        self._button_frame.grid(row=2, column=0)
        self._button_frame.grid_propagate(False)

        self.action_button = tk.Button(
            self._button_frame,
            text = "Confirm",
            command=lambda:print(None)
        )
        self.action_button.grid()         

        # Labels
        label_frame = tk.Frame(
            self.root,
            height=window_height//3,
            width=left_frame_width,

            bd=1, # Temp
            relief="solid"
        )
        label_frame.grid(row=0, column=0)
        test_label = tk.Label(label_frame, text="Hello World!") #temporary
        test_label.pack()

        self.display_terminal = tk.Text(
            self.terminal_frame,
            bg="black",
            fg="white",
            yscrollcommand = scrollbar.set
        )
        self.display_terminal.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.display_terminal.yview)

        self.display_terminal.config(state="disabled")

        # Displayed map
        self.gui_map_frame = tk.Frame(self.root)

        # Key-binds
        self.root.bind("<Return>", lambda event: self.action_button.invoke())
        self.root.bind("w", lambda event: self.up.invoke())
        self.root.bind("s", lambda event: self.down.invoke())
        self.root.bind("d", lambda event: self.right.invoke())
        self.root.bind("a", lambda event: self.left.invoke())

    """Terminal Methods - terminal_frame"""
    def write_line(self, msg):
        self.display_terminal.config(state="normal")
        self.display_terminal.insert("end", f"{msg}\n")
        self.display_terminal.see("end")
        self.display_terminal.config(state="disabled")

    def show_terminal(self):
        self.terminal_frame.grid(column=1, row=0, rowspan=2)
    
    def disable_terminal(self):
        self.terminal_frame.grid_forget()

    """Player action methods - actions_frame"""
    def update_listbox(self, contents):
        self.create_actions_box()
        for i in contents:
            self.actions_box.insert(tk.END, str(i))
    
    def clear_action_frame(self):
        for widget in self._actions_frame.winfo_children():
            widget.destroy()          
    
    def create_actions_box(self):
        self.clear_action_frame()
        self.actions_box = tk.Listbox(self._actions_frame, width=25)
        self.actions_box.pack()

    def create_input_field(self):
        self.clear_action_frame()
        self.input_field = tk.Entry(self._actions_frame)
        self.input_field.pack()

    """Map methods - terminal_frame"""
    def show_map(self, map):
        self.gui_map_frame.grid(column=1, row=0, rowspan=2)
        self.refresh_map(map)
    
    def disable_map(self):
        self.gui_map_frame.grid_forget()
    
    def refresh_map(self, map):
        for tile in self.gui_map_frame.winfo_children():
            tile.destroy()
        i = 0
        for col in map.grid:
            j = 0
            for row in col:
                tile = tk.Label(
                    self.gui_map_frame,
                    text="o",
                    height=1,
                    width=2,
                    bd=2,
                    relief="solid",
                    bg = "red"
                    )
                if row == "p":
                    tile.config(text="p", bg = "blue")
                tile.grid(column=i, row=j)
                j += 1
            i += 1        

    def create_dpad(self):
        self.action_button.grid_forget()
        self._dpad_frame = tk.Frame(self._button_frame)
        self._dpad_frame.pack()
        self.up = tk.Button(
            self._dpad_frame,
            text = "↑",
            width=2,
            height=1
            )
        self.down = tk.Button(
            self._dpad_frame,
            text = "↓",
            width=2,
            height=1
            )
        self.left = tk.Button(
            self._dpad_frame,
            text = "←",
            width=2,
            height=1
            )
        self.right = tk.Button(
            self._dpad_frame,
            text = "→",
            width=2,
            height=1
            )
        self.up.grid(row=0, column=1)
        self.left.grid(row=1, column=0)
        self.down.grid(row=1, column=1)
        self.right.grid(row=1, column=2)
    
    def destroy_dpad(self):
        self._dpad_frame.destroy()
        self.action_button.grid()

    """Button methods - button_frame"""
    def create_back_button(self):
        self.back_button = tk.Button(
            self._button_frame,
            text="Back"
        )
        self.back_button.grid()

    def create_yn_buttons(self):
        self.action_button.grid_forget()

        self.yes_button = tk.Button(
            self._button_frame,
            text="Yes"
        )
        self.no_button = tk.Button(
            self._button_frame,
            text="No"
        )
        self.yes_button.grid()
        self.no_button.grid()
    
    def destroy_yn_buttons(self):
        self.yes_button.destroy()
        self.no_button.destroy()