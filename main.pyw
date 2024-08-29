# -*-Config:UTF-8-*-
# MicGan-RePKG_Python_UI
# | By : MicGan    |
# Import modules
import tkinter as tk
import tkinter.messagebox as msg
import os
import sys
import subprocess
import json
import shutil
import winreg

from PIL import Image, ImageTk
try:
    from loguru import logger
except ModuleNotFoundError:
    msg.showwarning('警告', '无法找到第三方库,即将开始尝试自动安装')
    result = subprocess.Popen(
        'pip install -i https://pypi.tuna.tsinghua.edu.cn/simple loguru',
        stdin=None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    if 'Successfully' in result.communicate()[0].decode("gbk"):
        msg.showinfo('提示', '安装完成，请重新启动程序')
    else:
        msg.showerror('错误', '安装失败, 请在cmd中手动输入\npip install -i https://pypi.tuna.tsinghua.edu.cn/simple loguru')
    sys.exit()


# Main
class Main:
    def __init__(self):

        # Create Some Vars, they will be use later in the functions
        self.Wallpaper_pic = None
        self.wallpaper_info_window = None
        self.WallpaperTotal = 0
        self.Canvas_height = 0
        self.main_frame = None
        self.scrollbar = None
        self.WallPaper_info = {}
        self.jsonlist = None
        self.button_start = None
        self.entry_PKGfile_path = None
        self.text_file_path = None
        self.main_canvas = None
        self.PIL_img_Tk_list = []
        self.All_WallPaper_Path = ""
        self.labels_wallpapers_pic = []  # The labels of the pictures
        self.work_path = os.path.dirname(os.path.realpath(sys.argv[0]))  # Get Work Path
        self.RePKG_path = self.work_path + r"\RePKG.exe"  # The path of the RePKG.exe
        self.get_wallpaper_path()  #
        self.output_path = self.work_path + r"\output"  # Output File Path
        self.get_json_filelist()  # Get the all json files
        self.get_wallpaper_info()  # Get the info of the wallpapers
        self.get_canvas_height()  # Sum the height that Canvas window needs
        self.root = tk.Tk()  # Create Main Window
        self.x = int(self.root.winfo_screenwidth() / 2 - 930 / 2)
        self.y = int(self.root.winfo_screenheight() / 2 - 732 / 2)
        # Set Window's Size
        self.root.wm_geometry(f"930x732+{self.x}+{self.y}")
        self.root.wm_title("Wallpaper Engine:壁纸引擎 第三方工具")  # Set Window's title
        self.root.wm_resizable(False, True)
        self.check_file_and_path()  # Check If file exits
        self.main_ui()
        self.top_menu()
        self.root.mainloop()  # Show the Window

    def __str__(self):
        return self.entry_PKGfile_path.get()

    # *----------------------------------- Prepare Func--------------------------------------* #

    def get_canvas_height(self):
        """
        Sum the height that Canvas need
        """
        if self.WallpaperTotal % 9 == 0:
            Wallpapers_col = self.WallpaperTotal // 9
        else:
            Wallpapers_col = self.WallpaperTotal // 9 + 1
        self.Canvas_height = Wallpapers_col * 100
        print(self.Canvas_height)

    def get_json_filelist(self):
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
        self.WallpaperTotal = len(self.jsonlist)

    def get_wallpaper_info(self):
        """
        Get info of the wallpaper
        """
        self.WallPaper_info = [{}]  # Create a dict to storge info of the wallpapers
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
            wallpaper_info_in_if["Wallpaper_preview_file"] = (
                wallpaper_path + "/" + json_data.get("preview")
            )
            wallpaper_info_in_if["Wallpaper_type"] = json_data.get("type")

            self.WallPaper_info[0][
                wallpaper_path
            ] = wallpaper_info_in_if  # Create a Key_Value to Storage the info

        print(self.WallPaper_info)

    def check_file_and_path(self):
        """
        Check if the output Folder or RePKG.exe exist
        """
        if not os.path.isdir(self.output_path):
            # If the folder doesn't exist, Create the path
            os.mkdir(self.output_path)
        if not os.path.isfile(self.RePKG_path):
            msg.showerror(
                "错误", "RePKG.exe文件不存在,程序结束运行"
            )  # If RePKG.exe doesn't exist, Warn user
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

    # *--------------------------------UI Func--------------------------------* #
    def top_menu(self):
        """
        Show the top menu
        """
        main_menu = tk.Menu(self.root)
        son_menu = tk.Menu(main_menu)
        main_menu.add_cascade(label="配置", menu=son_menu)
        son_menu.add_command(label="关于", command=self.about)
        son_menu.add_command(label="退出", command=self.root.quit)
        self.root.configure(menu=main_menu)

    def main_ui(self):
        """
        Show the preview Image of the Wallpapers
        """
        self.main_canvas = tk.Canvas(
            self.main_frame, width=930, height=self.Canvas_height
        )
        self.main_canvas.configure(highlightthickness=0)

        self.scrollbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        logger.info("创建 Scrollbar 完成")
        self.main_canvas.pack(fill="both", expand=True)
        logger.info("创建 Canvas 完成")
        self.main_canvas.configure(
            yscrollcommand=self.scrollbar.set,
            yscrollincrement=10,
            scrollregion=(0, 0, 930, self.Canvas_height),
        )
        self.scrollbar.configure(command=self.main_canvas.yview)
        logger.info("滚动绑定成功")

        img_x = 0
        img_y = 0
        count = 0

        for Wallpaper_info_k, Wallpaper_info_v in self.WallPaper_info[0].items():
            count += 1
            PIL_img = Image.open(Wallpaper_info_v.get("Wallpaper_preview_file"))
            PIL_Tk_img = ImageTk.PhotoImage(PIL_img.resize((100, 100)))
            self.PIL_img_Tk_list.append(PIL_Tk_img)
            self.Wallpaper_pic = tk.Button(
                self.main_canvas,
                image=PIL_Tk_img,
                relief="flat",
                command=lambda wp=Wallpaper_info_k: self.show_wallpaper_info(wp),
            )
            self.main_canvas.create_window(
                (img_x, img_y), window=self.Wallpaper_pic, anchor="nw", tags="button"
            )
            self.labels_wallpapers_pic.append(self.Wallpaper_pic)
            img_x += 100
            if count % 9 == 0:
                img_y += 100
                img_x = 0
            logger.info(f"为 {Wallpaper_info_k} 目录的壁纸创建按钮")

    # *------------------------------------Button Func---------------------------------------* #

    def conversion_pkg(self, *args):
        """
        Args:
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
                self.output_path + "\\" + Wallpaper_Name
            )  # Use a var to storge Output Path(final)
            print(final_output_path)
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
            print(command)
            # Use subprocess.popen to run the command
            result = subprocess.Popen(
                command,
                stdin=None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
            )
            print(result.communicate()[0].decode("gbk"))
            if "Done" in str(result.communicate()[0].decode("gbk")):
                suc += 1
            else:
                fail += 1
        msg.showinfo("提示", f"成功解包 {suc} 个,失败 {fail} 个")

    def copy_mp4(self, *args):

        for MP4_path in args:
            print(MP4_path)
            all_files = os.listdir(MP4_path)
            print(all_files)
            mp4_file = ""
            # Find the mp4 file
            for i in all_files:
                if i.endswith(".mp4"):
                    mp4_file = MP4_path + f"\\{i}"
                    break
            print(mp4_file)
            json_file = (
                os.path.dirname(mp4_file.strip("'")) + r"/project.json"
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
                self.output_path + "\\" + Wallpaper_Name
            )  # Use a var to storge Output Path(final)
            print(final_output_path)
            if not os.path.isdir(final_output_path): # If the output path didn't exist, Create it
                os.mkdir(final_output_path)
            shutil.copy(mp4_file, final_output_path + f"\\{Wallpaper_Name}.mp4")
        msg.showinfo('提示', '解包完成')

    def show_wallpaper_info(self, wallpapername):
        """
        Args:
            wallpapername: The path of the Wallpaper
        Show the info of the wallpaper
        """
        logger.info(f"正在查看 {wallpapername} 目录下的壁纸信息")
        self.wallpaper_info_window = tk.Tk()  # Create a New Window
        x = int(self.root.winfo_x() + self.root.winfo_width() / 2 - 350)
        y = int(self.root.winfo_y() + self.root.winfo_height() / 2 - 350)
        self.wallpaper_info_window.wm_geometry(
            f"700x700+{x}+{y}"
        )  # Set the Size of the window
        self.wallpaper_info_window.wm_resizable(False, False)  # Set Resizeable
        # self.wallpaper_info_window.wm_attributes('-topmost', True)

        Wallpaper_info_data = self.WallPaper_info[0].get(
            wallpapername
        )  # Try to get the info of the wallpaper
        # If the wallpaper can not find, Tell the user
        if not Wallpaper_info_data:
            msg.showerror("错误", "无法找到壁纸信息")
            logger.error(f"无法找到{wallpapername}的壁纸信息")
            return 0
        # Open the image
        PIL_img = Image.open(Wallpaper_info_data.get("Wallpaper_preview_file"))
        PIL_Tk_img = ImageTk.PhotoImage(
            PIL_img.resize((300, 300)), master=self.wallpaper_info_window
        )

        Wallpaper_pic = tk.Label(self.wallpaper_info_window, image=PIL_Tk_img)
        Wallpaper_pic.place(x=205, y=30)
        # Get the title and place it
        Wallpaper_info_title = Wallpaper_info_data.get("Wallpaper_title")
        self.wallpaper_info_window.title(
            f"{Wallpaper_info_title}的详细信息"
        )  # Set the title of the Window
        wallpapertitle_label = tk.Label(
            self.wallpaper_info_window, text=Wallpaper_info_title
        )
        wallpapertitle_label.pack()
        wallpapertitle_label.configure(
            justify=tk.CENTER, anchor=tk.CENTER
        )  # Set Text place
        # Get the type of the wallpaper and place it
        wallpapertype = Wallpaper_info_data.get("Wallpaper_type")
        # Transfer English to Chinese
        if wallpapertype.lower() == "video":
            wallpapertype = "视频"
        elif wallpapertype.lower() == "scene":
            wallpapertype = "场景"
        wallpapertype_label = tk.Label(
            self.wallpaper_info_window, text=f"类型: {wallpapertype}"
        )
        wallpapertype_label.place(x=330, y=390)

        Wallpaper_pic.image = PIL_Tk_img
        # If it is Scene Wallpaper, Show the conversion button
        if wallpapertype == "场景":
            conver_button = tk.Button(
                self.wallpaper_info_window,
                text="开始导出",
                command=lambda: self.conversion_pkg(wallpapername),
            )
            conver_button.place(x=330, y=420)
        elif wallpapertype == "视频":
            copy_button = tk.Button(
                self.wallpaper_info_window,
                text="开始导出",
                command=lambda: self.copy_mp4(wallpapername),
            )
            copy_button.place(x=330, y=420)
        self.wallpaper_info_window.mainloop()  # Show the Window

    @staticmethod
    def about():
        """
            The About Page
        """
        logger.info("查看关于信息")
        msg.showinfo(
            "关于",
            "本程序主要制作者:MicGan\n合作贡献者(排名不分先后):CodeCrafter-TL system-window\n版权声明:壁纸的版权归壁纸制作者所有，本程序仅供学习交流",
        )


if __name__ == "__main__":

    logger.info("程序启动")
    Main()  # If Run In Main, Just GO!

    logger.info("程序退出")
else:
    logger.warning("本程序正在作为第三方模块导入! 请注意相关变量的设置")
