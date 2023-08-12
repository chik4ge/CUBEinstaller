import logging
import os

import yaml
import customtkinter

from .widgets import PathWidget, TextureSelectWidget
from installer import CUBEinstaller

class CustomFormatter(logging.Formatter):
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENDA = '\033[95m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    format = "[%(asctime)s] [%(levelname)s]: %(message)s"

    FORMATS = {
        logging.DEBUG: format,
        logging.INFO: GREEN + format + ENDC,
        logging.WARNING: YELLOW + format + ENDC,
        logging.ERROR: RED + format + ENDC,
        logging.CRITICAL: RED + format + ENDC
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

logger = logging.getLogger("CUBEinstaller")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)

class CUBEinstallerApp(customtkinter.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.setup()
    
    def setup(self):
        customtkinter.set_appearance_mode("Light")
        customtkinter.set_default_color_theme("blue")

        self.title("CUBE installer")
        # self.geometry("800x600")
        self.resizable(False, False)
        self.iconbitmap("assets\\icon.ico")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.config_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.config_frame.grid_columnconfigure((0, 1), weight=1)
        self.config_frame.grid(row=0, column=0, sticky="nsew")

        self.pbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.pbar_frame.grid_rowconfigure(0, weight=1)
        self.pbar_frame.grid_columnconfigure((0, 1), weight=1)
        self.pbar_frame.grid(row=3, column=0, sticky="sew")

        self.pbar = customtkinter.CTkProgressBar(self.pbar_frame, corner_radius=10)
        self.pbar.grid(row=1, column=0, padx=(10, 0), pady=10, sticky="nsew")
        self.pbar.set(0)

        self.pbar_label = customtkinter.CTkLabel(self.pbar_frame, text="0%", width=30)
        self.pbar_label.grid(row=1, column=1, padx=(0, 10), pady=10, sticky="nsew")

        self.minecraft_path = PathWidget(self.config_frame, ".minecraft Folder")
        self.minecraft_path.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        default_path = os.path.expandvars("%APPDATA%\\.minecraft")
        if os.path.exists(default_path):
            self.minecraft_path.text.set(default_path)

        self.cube_path = PathWidget(self.config_frame, "CUBE Folder")
        self.cube_path.grid(row=1, column=0, padx=10, columnspan=2, pady=10, sticky="nsew")

        self.texture_select = TextureSelectWidget(self.config_frame)
        self.texture_select.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.button = customtkinter.CTkButton(self.config_frame, text="RUN", command=self.run)
        self.button.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
    
    def run(self):
        tex = self.texture_select.tex.get()
        
        logger.info("Running...")

        minecraft_path = self.minecraft_path.text.get()
        cube_path = self.cube_path.text.get()

        logger.debug(f"Texture pack: {tex}")
        logger.debug(f"Minecraft path: {minecraft_path}")
        logger.debug(f"CUBE path: {cube_path}")

        # check directories exist
        if not os.path.exists(minecraft_path):
            logger.error(f"minecraft directory not found!")
            return

        if not os.path.exists(cube_path):
            logger.error(f"cube directory not found!")
            return

        # import time
        # for i in range(101):
        #     self.pbar.set(i/100)
        #     self.pbar_label.configure(text=f"{i}%")
        #     self.update()
        #     time.sleep(0.01)

        self.installer = CUBEinstaller(minecraft_path, cube_path, tex)
        self.installer.install()

        logger.info("Done!")

    def install(self, files, minecraft_path, cube_path):
        logger.debug("installing files...")
