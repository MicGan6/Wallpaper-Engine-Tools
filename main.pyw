# -*-Config:UTF-8-*-
# MicGan-RePKG_Python_UI
# | By : MicGan    |
# Import modules
import tkinter as tk
import tkinter.messagebox
import os
import sys
import subprocess
import json
import threading
import tkinter.simpledialog
import winreg
from PIL import Image, ImageTk


# Debug Func
def debug(mode, name, log):
    """
    Print sth. to Console
    Args:
        mode: Debug mode
        name: The name of the output things
        log: The data
    """
    print("[" + mode + "]:" + name + ":" + log)


# Main
class Main:
    def __init__(self):
        # Create Some Vars, they will be use later in the functions
        self.main_frame = None
        self.scrollbar = None
        self.WallPaper_info = None
        self.jsonlist = None
        self.button_start = None
        self.entry_PKGfile_path = None
        self.text_file_path = None
        self.main_canvas = None
        self.PIL_img_Tk_list = []
        self.labels_wallpapers_pic = [] # The labels of the pictures
        self.work_path = os.getcwd()  # Get Work Path
        self.RePKG_path = r".\RePKG.exe"
        self.All_WallPaper_Path = ""
        self.get_wallpaper_path()  #
        self.output_path = self.work_path + r".\output"  # Output File Path
        self.get_filelist()
        self.get_wallpaper_info()
        self.root = tk.Tk()  # Create Main Window
        self.root.geometry("940x732")  # Set Window's Size
        self.root.title("RePKG UI")  # Set Window's title
        self.root.resizable(False, False)
        self.check_file_and_path()  # Check If file exits
        # Load UI
        self.main_ui()
        self.place_labels()

        self.root.mainloop()  # Show the Window

    def __str__(self):
        return self.entry_PKGfile_path.get()

    def main_ui(self):
        """
        Main UI of the application
        """
        self.main_canvas = tk.Canvas(self.main_frame, width=920, height=732)
        self.main_canvas.configure(highlightthickness=0)
        self.main_canvas.pack(fill='both', expand=True)

        self.scrollbar = tk.Scrollbar(
            self.main_canvas, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.main_canvas.yview)


    def place_labels(self):
        """
        Show the preview Image of the Wallpapers
        """
        img_x = 0 # Set the x pos
        img_y = 0 # Set the y pos
        count = 0

        for Wallpaper_info_k, Wallpaper_info_v in self.WallPaper_info.items():
            count += 1

            PIL_img = Image.open(Wallpaper_info_v.get('Wallpaper_preview_file')) # Open the preview pic
            PIL_Tk_img = ImageTk.PhotoImage(PIL_img.resize((100,100))) # Use ImageTk to show the pic
            self.PIL_img_Tk_list.append(PIL_Tk_img)
            Wallpaper_pic = tk.Button(self.main_canvas, image=PIL_Tk_img)  # Create the label
            Wallpaper_pic.place(x=img_x,y=img_y)
            self.labels_wallpapers_pic.append(PIL_Tk_img) # append it to Wallpaper_pic list
            img_x += 100 # Change x Pos
            if count % 9 == 0: # If The Column was full, Change a Column
                img_y += 100
                img_x = 0
    def check_file_and_path(self):
        """
        Check if the output Folder or RePKG.exe exist
        """
        if not os.path.isdir(self.output_path):
            os.mkdir(self.output_path)  # If the folder doesn't exist, Create the path
        if not os.path.isfile(self.RePKG_path):
            tkinter.messagebox.showerror(
                "错误", "RePKG.exe文件不存在,程序结束运行"
            )  # If REPKG.exe doesn't exist, Warn user
            sys.exit()  # Stop Running

    def get_wallpaper_path(self):
        """
        Set WallPaper Path Config
        """
        # Use winreg to get Steam Install Folder
        Steam_Install_Path_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, r"SoftWare\Valve\Steam"
        )
        Steam_Install_Path_Value = winreg.QueryValueEx(
            Steam_Install_Path_key, "SteamPath"
        )
        Steam_Path = Steam_Install_Path_Value[0]
        # replace '\'
        Steam_Path = Steam_Path.replace("/", "\\")
        # Get Wallpaper Engine Workshop Folder
        Wallpaper_path = Steam_Path + r"\steamapps\workshop\content\431960"
        # Add it to config_data
        self.All_WallPaper_Path = Wallpaper_path

    def start(self):
        """
        Start conversion
        """
        PKG_file_path_str = self.__str__()  # Get the file's abs path
        json_file = (
            os.path.dirname(PKG_file_path_str.strip('"')) + r"\project.json"
        )  # Get project.json File Path
        with open(json_file, "r", encoding="utf-8") as file_data:  # Load the json file
            json_data = json.load(file_data)
        Wallpaper_Name = json_data.get("title")  # Get the name of the wallpaper
        # Replace spacial string
        Wallpaper_Name = Wallpaper_Name.replace(" ", "_")
        Wallpaper_Name = Wallpaper_Name.replace(" ", "_")
        Wallpaper_Name = Wallpaper_Name.replace("|", "_")
        Wallpaper_Name = Wallpaper_Name.replace("*", "_")
        Wallpaper_Name = Wallpaper_Name.replace(":", "_")
        Wallpaper_Name = Wallpaper_Name.replace("<", "_")
        Wallpaper_Name = Wallpaper_Name.replace(">", "_")
        final_output_path = (
            self.output_path + "\\" + Wallpaper_Name
        )  # Use a var to storge Output Path(final)
        command = (
            self.RePKG_path
            + " "
            + "extract"
            + " "
            + PKG_file_path_str
            + " "
            + "-o"
            + " "
            + final_output_path
        )  # The command of conversion
        # Use subprocess.popen to run the command
        result = subprocess.Popen(
            command,
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
        output_info_message = (
            "终端输出如下:" + "\r" + str(result.communicate()[0].decode("gbk"))
        )  # Use a Var Storage Output Information

        tkinter.messagebox.showinfo(
            "运行结果", output_info_message
        )  # Use a Window to tell User the output information

    # Use Multi-threaded to make sure that it won't Stop responding
    def start_thread(self):
        """
        Use Muti_thread to start Conversion
        """
        RunThread = threading.Thread(target=self.start)
        RunThread.run()

    def get_filelist(self):
        """
        Get the json file
        """
        Filelist = []  # A list to Storge All the file(abs path) in the workshop path
        self.jsonlist = []  # A list to storge Json Files
        # Search all the files in the workshop path
        for home, dirs, files in os.walk(self.All_WallPaper_Path):
            for filename in files:
                Filelist.append(os.path.join(home, filename))
        # find all the json files
        for filename in Filelist:
            if "project.json" in filename:
                self.jsonlist.append(filename)

    def get_wallpaper_info(self):
        """
        Get info of the wallpaper
        """
        self.WallPaper_info = {}  # Create a dict to storge info of the wallpapers
        # Get the info & the path
        for wallpaper in self.jsonlist:
            # ------------------init--------------- #
            wallpaper_path = os.path.dirname(wallpaper)  # Get the path of Wallpaper
            wallpaper_info_in_if = {}  # Create a dic to storage Info
            # -------------Read config------------- #
            with open(
                wallpaper, "r", encoding="utf-8"
            ) as file_data:  # Load the json file
                json_data = json.load(file_data)
            # -------------Add info to wallpaper_info_in_if-------------- #
            wallpaper_info_in_if["Wallpaper_title"] = json_data.get(
                "title"
            )  # Get the name of the wallpaper
            wallpaper_info_in_if["Wallpaper_contentrating"] = json_data.get(
                "contentrating"
            )  # Get the contentrating of the wallpaper
            wallpaper_info_in_if['Wallpaper_preview_file'] = wallpaper_path + '\\' + json_data.get("preview")
            wallpaper_info_in_if['Wallpaper_type'] = json_data.get("type")
            self.WallPaper_info[
                wallpaper_path
            ] = wallpaper_info_in_if  # Create a Key_Value to Storage the info

        print(self.WallPaper_info)


if __name__ == "__main__":
    Main()  # If Run In Main, Just GO!
else:
    tkinter.messagebox.showerror(
        "错误", "请在主程序中运行"
    )  # If not running in main, Warn the user and stop running