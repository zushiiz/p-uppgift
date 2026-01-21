import tkinter as tk

class GUI():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("main-window")
        window_width = 800
        window_height = 500
        self.root.geometry(f"{window_width}x{window_height}")
        left_frame_width = window_width//3 

        self.root.bind("<Return>", lambda event: self.action_button.invoke())

        # Terminal 
        terminal_frame =  tk.Frame(
            self.root,
            height=window_height,
            width=800,
            )
        terminal_frame.grid_propagate(False)        
        scrollbar = tk.Scrollbar(terminal_frame)
        scrollbar.pack(side="right", fill="y")
        terminal_frame.grid(column=1, row=0, rowspan=2)

        # Player actions
        self._actions_frame = tk.Frame(
            self.root,
            height=window_height//3,
            width=left_frame_width,
            )
        self._actions_frame.grid(row=1, column=0)
        self._actions_frame.grid_propagate(False)

        self.actions_box = tk.Listbox(self._actions_frame, width=25)

        # Buttons
        self._button_frame = tk.Frame(
            self.root,
            height=window_height//3,
            width=left_frame_width,
            )
        self._button_frame.grid(row=2, column=0)
        self._button_frame.grid_propagate(False)

        self.action_button = tk.Button(
            self._button_frame,
            text = "Confirm",
            command=lambda:print(None)
        )
        self.action_button.pack()         

        # Labels
        label_frame = tk.Frame(
            self.root,
            height=window_height//3,
            width=left_frame_width
        )
        label_frame.grid(row=0, column=0)
        test_label = tk.Label(label_frame, text="Hello World!") #temporary
        test_label.pack()

        self.display_terminal = tk.Text(
            terminal_frame,
            bg="black",
            fg="white",
            yscrollcommand = scrollbar.set
        )
        self.display_terminal.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.display_terminal.yview)

        self.display_terminal.config(state="disabled")
    
    def write_line(self, msg):
        self.display_terminal.config(state="normal")
        self.display_terminal.insert("end", f"{msg}\n")
        self.display_terminal.see("end")
        self.display_terminal.config(state="disabled")

    def update_listbox(self, contents):     
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

    def create_map(self, map):
        print("creating")
        for tile in self.gui_map_frame.winfo_children():
            tile.destroy()
        self.gui_map_frame = tk.Frame(self.root)
        self.gui_map_frame.grid(row=3, column=3)
        i = 0
        for col in map.grid:
            print("col")
            j = 0
            for row in col:
                print("row")
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
    
