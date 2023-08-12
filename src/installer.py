from calendar import c
import logging
import os
import requests

import yaml

logger = logging.getLogger("CUBEinstaller")

class CUBEinstaller:
    def __init__(self, minecraft_path, cube_path, texture_pack):
        self.minecraft_path = minecraft_path
        self.cube_path = cube_path
        self.texture_pack = texture_pack
        
        # make working directory
        self.workdir = self.cube_path + "\\.cubeinstaller"
        if not os.path.exists(self.workdir):
            os.mkdir(self.workdir)

    def install(self):
        logger.info("fetching files...")

        # TODO: fetch files from github
        filepath = f"assets\\{self.texture_pack}.yml"
        if not os.path.exists(filepath):
            logger.error(f"mod list file for {self.texture_pack} not found!")
            return
    
        with open(filepath, "r") as f:
            self.mod_list = yaml.safe_load(f)
            
            self.install_forge()

            # self.create_launcher_profiles()

            # self.install_mods()

            # self.enable_resource_pack()
    
    def install_forge(self):
        mc_version = self.mod_list["mc-version"] # 1.12.2
        forge_version = self.mod_list["forge-version"] # 1.12.2-14.23.5.2860

        # check if forge is installed
        # dist_path = os.path.join(self.minecraft_path, "versions", f"{mc_version}-forge-{forge_version}")
        # if os.path.exists(dist_path):
        #     logger.info("forge is already installed")
        #     return

        # download forge installer
        version = f"{mc_version}-{forge_version}" # 1.12.2-14.23.5.2860
        filename = f"forge-{version}-installer.jar"
        url = f"https://maven.minecraftforge.net/net/minecraftforge/forge/{version}/{filename}"
        logger.info(f"downloading forge installer...")
        logger.debug(f"url: {url}")
        r = requests.get(url)
        if r.status_code != 200:
            logger.error(f"failed to download forge installer!")
            return
        jar = r.content
        with open(os.path.join(self.workdir, filename), "wb") as f:
            f.write(jar)
        
        # run forge installer
        logger.info("running forge installer...")
        # TODO: run forge installer without gui
