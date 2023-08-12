import customtkinter
import os

class PathWidget(customtkinter.CTkFrame):
    def __init__(self, master, label, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(self, text=label)
        self.label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")

        self.text = customtkinter.StringVar(value="select a folder... ->")

        self.path = customtkinter.CTkEntry(self, state="readonly", textvariable=self.text)
        self.path.grid(row=1, column=0, padx=10, pady=10, sticky="sew")
        
        self.browse_button = customtkinter.CTkButton(self, text="...", width=20, command=self.browse)
        self.browse_button.grid(row=1, column=1, padx=(0, 10), pady=10, sticky="se")
    
    def browse(self):
        default_path = os.path.expandvars("%APPDATA%\\.minecraft")
        self.text.set(customtkinter.filedialog.askdirectory(initialdir=default_path))
