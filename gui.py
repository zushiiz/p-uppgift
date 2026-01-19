import tkinter as tk

class GUI():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("main-window")
        window_width = 800
        window_height = 500
        self.root.geometry(f"{window_width}x{window_height}")

        left_frame_width = window_width/3

        terminal_frame =  tk.Frame(
            self.root,
            height=window_height,
            width=800,
            )
        terminal_frame.pack_propagate(False)        
        scrollbar = tk.Scrollbar(terminal_frame)
        scrollbar.pack(side="right", fill="y")
        terminal_frame.grid(column=1, row=0, rowspan=2)

        self._button_frame = tk.Frame(
            self.root,
            height=window_height/2,
            width=left_frame_width,
            )
        self._button_frame.grid(row=1, column=0)
        self._button_frame.pack_propagate(False)

        label_frame = tk.Frame(
            self.root,
            height=window_height/2,
            width=left_frame_width
        )
        label_frame.grid(row=0, column=0)
        test_label = tk.Label(label_frame, text="Hello World!") #temporary
        test_label.pack()

        self.display_terminal = tk.Text(
            terminal_frame,
            bg="black",
            fg="white",
            yscrollcommand=scrollbar.set
        )
        self.display_terminal.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.display_terminal.yview)

        self.display_terminal.config(state="disabled")
    
    def write_line(self, msg):
        print("printing")
        self.display_terminal.config(state="normal")
        self.display_terminal.insert("end", f"{msg}\n")
        self.display_terminal.see("end")
        self.display_terminal.config(state="disabled")

    def create_buttons(self, buttonIndex):
        newButton = tk.Button(self._button_frame, text=f"Button {buttonIndex}")
        newButton.pack()
        

"""
    root = tk.Tk()
    root.title("main-window")

    # Display terminal
    displayFrame = tk.Frame(root)
    scrollbar = tk.Scrollbar(displayFrame)
    scrollbar.pack(side="right", fill="y")  
    displayFrame.pack(padx=10, pady=10)

    displayTerminal = tk.Text(
        displayFrame,
        height=15,
        width=60,
        bg="black",
        fg="white",
        yscrollcommand=scrollbar.set
    )
    displayTerminal.pack(side="left")
    scrollbar.config(command=displayTerminal.yview)

    displayTerminal.config(state="disabled")

"""