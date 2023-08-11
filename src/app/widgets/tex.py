import customtkinter

class TextureSelectWidget(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
    
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.label = customtkinter.CTkLabel(self, text="Texture pack")
        self.label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")

        self.tex = customtkinter.StringVar(value="cocricot")

        buttons = [
            customtkinter.CTkRadioButton(self, text="cocricot", width=20, variable=self.tex, value="cocricot"),
            customtkinter.CTkRadioButton(self, text="MiniaTuria", width=20, variable=self.tex, value="miniaturia"),
        ]

        for i, button in enumerate(buttons):
            button.grid(row=i, column=0, padx=10, pady=10, sticky="sew")
