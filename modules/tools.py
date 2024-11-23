from loguru import logger
import subprocess
import json
import os
import sys
import tkinter.messagebox as msg

class ButtonCommand:
    def ConversionPKG(self, output_path, repkg_path, *args):
        """
        Args:
            output_path:The path to output
            repkg_path:The path of RePKG.exe
            *args:The Wallpapers need to conversion
        Start conversion

        """
        logger.info("进入解包函数")
        suc = 0
        fail = 0
        for PKG_file_path_str in args:
            PKG_file_path_str = PKG_file_path_str + r"\scene.pkg"
            print(PKG_file_path_str)
            json_file = (
                os.path.dirname(PKG_file_path_str.strip('"')) + r"/project.json"
            )  # Get project.json File Path
            with open(
                json_file, "r", encoding="utf-8"
            ) as file_data:  # Load the json file
                json_data = json.load(file_data)
            # Get the name of the wallpaper
            Wallpaper_Name = json_data.get("title")
            # Replace spacial string
            Wallpaper_Name = Wallpaper_Name.replace(" ", "_")
            Wallpaper_Name = Wallpaper_Name.replace(" ", "_")
            Wallpaper_Name = Wallpaper_Name.replace("|", "_")
            Wallpaper_Name = Wallpaper_Name.replace("*", "_")
            Wallpaper_Name = Wallpaper_Name.replace(":", "_")
            Wallpaper_Name = Wallpaper_Name.replace("<", "_")
            Wallpaper_Name = Wallpaper_Name.replace(">", "_")
            final_output_path = (
                output_path + "\\" + Wallpaper_Name
            )  # Use a var to storge Output Path(final)
            print(final_output_path)
            command = (
                repkg_path
                + " "
                + "extract"
                + " "
                + PKG_file_path_str
                + " "
                + "-o"
                + " "
                + final_output_path
            )  # The command of conversion
            print(command)
            # Use subprocess.popen to run the command
            result = subprocess.Popen(
                command,
                stdin=None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
            )
            logger.info(result)
            print(result.communicate()[0].decode("gbk"))
            if "Done" in str(result.communicate()[0].decode("gbk")):
                suc += 1
            else:
                fail += 1
        msg.showinfo("提示", f"成功解包 {suc} 个,失败 {fail} 个")