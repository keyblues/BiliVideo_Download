import threading
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter.ttk
from BilibiliVideo import *
import time


class MyGui:
    def __init__(self, init_window_name):
        self.bili = BilibiliVideo()
        self.init_windows_name = init_window_name
        self.init_windows_name.title("BiliVideo v1.6")
        self.init_windows_name.config(bg='#DDDDDD')
        self.init_windows_name.geometry('600x300')
        self.CheckbuttonVar = StringVar(value=0)
        self.stop = StringVar(value='stop')
        self.start = StringVar(value='start')
        self.foldername = StringVar()
        self.bv = StringVar()
        self.cookies = StringVar()
        self.t = threading.Thread(target=self.download)
        root.protocol("WM_DELETE_WINDOW", self.no_closing)

    def get_windows(self):
        Entry(root, textvariable=self.bv, font=("Times", 15, "bold")).place(x=130, y=20, width=340, height=30)  # bv号输入框
        Entry(root, textvariable=self.cookies, font=("Times", 12, "bold")).place(x=130, y=60, width=340,
                                                                                 height=30)  # cookie输入框
        Entry(root, textvariable=self.foldername, font=("Times", 15, "bold")).place(x=130, y=100, width=340,
                                                                                    height=30)  # 目录名输入框
        Entry(root, textvariable=self.start, font=("Times", 15, "bold")).place(x=130, y=140, width=50,
                                                                               height=30)  # 起始输入框
        Entry(root, textvariable=self.stop, font=("Times", 15, "bold")).place(x=200, y=140, width=50,
                                                                              height=30)  # 结束输入框
        Label(root, text='BV号:', bg='#DDDDDD', font=("Times", 15)).place(x=0, y=21, width=99, height=29)
        Label(root, text='Cookie:', bg='#DDDDDD', font=("Times", 15)).place(x=0, y=61, width=99, height=29)
        Label(root, text='保存目录:', bg='#DDDDDD', font=("Times", 15)).place(x=0, y=101, width=99, height=29)
        self.enter = Button(root, text="Enter", font=("Times", 15), bg='#DDDDDD', command=lambda: self.thread())
        self.enter.place(x=501, y=20, width=99, height=70)
        Button(root, text="选择", font=("Times", 15), bg='#DDDDDD', command=self.fold).place(x=501, y=100, width=99,
                                                                                             height=30)
        Checkbutton(root, text="合集", bg='#DDDDDD', font=("Times", 15), activebackground='#DDDDDD', command='',
                    variable=self.CheckbuttonVar).place(x=0, y=141, width=99, height=30)
        self.log = Text(root)
        self.log.place(x=5, y=181, width=590, height=115)
        self.progressbar = tkinter.ttk.Progressbar(root)
        self.progressbar.place(x=285, y=141, width=280, height=30)
        self.progressbar.update()
        self.temp_config()

    def fold(self):
        # 打开目录选择器，并返回目录路径
        file = filedialog.askdirectory()
        self.foldername.set(file)
        self.t = threading.Thread(target=self.download)
        self.log.insert(1.0, f'选择新的目录{file}，Time：{time.strftime("%Y-%m-%d %H:%M:%S")}')
        self.log.insert(1.0, '\n')

    def thread(self):
        # 每点击一次下载就生成一个新的线程
        self.t = threading.Thread(target=self.download)
        self.t.start()

    def download(self):
        global video
        self.code = ''
        self.new_config()
        self.bili.cookie(self.cookies.get())
        self.enter.config(state='disabled')
        if not self.bili.inquire(self.bv.get()):
            messagebox.showinfo("警告！", "BV号不合法或不存在！")
            self.enter.config(state='normal')
            exit()
        if self.CheckbuttonVar.get() == '1':
            for i in range(int(self.start.get()), int(self.stop.get()) + 1):
                try:
                    video = self.bili.bili_requests(str(self.bv.get() + '?p=' + str(i)))
                except:
                    messagebox.showinfo("警告！", "请求失败！")
                    break
                if video == 200:
                    self.bili.write(self.foldername.get(), self.progressbar)
                    filename = self.bili.collectionname(str(self.bv.get()), i)
                    self.bili.rename(filename)
                    self.code = True
                else:
                    self.code = False
                self.logok(self.bv.get() + '?p=' + str(i))
            self.log.insert(1.0, f'视频合集{self.bv.get()}?p={self.start.get()}-{self.stop.get()}下载完成！，'
                                 f'Time：{time.strftime("%Y-%m-%d %H:%M:%S")}\n')

        else:
            try:
                video = self.bili.bili_requests(self.bv.get())
                self.log.insert(1.0, f'开始下载{self.bv.get()}，视频大小：{self.bili.size()}，'
                                     f'Time：{time.strftime("%Y-%m-%d %H:%M:%S")}\n')
            except:
                messagebox.showinfo("警告！", "请求失败！")
            if video == 200:
                self.bili.write(self.foldername.get(), self.progressbar)
                self.code = True
            else:
                self.code = False
            self.logok(self.bv.get())
        self.enter.config(state='normal')

    def no_closing(self):
        # 设置关闭方式的函数
        if self.t.is_alive():
            if messagebox.askokcancel("Quit", "正在下载，你确定要退出吗?"):
                root.destroy()
        else:
            root.destroy()

    def check_ffmpeg(self):
        if not self.bili.ffmpeg():
            messagebox.showinfo("警告！", "检测到你未安装ffmpeg！")

    def logok(self, bv):
        if self.code:
            self.log.insert(1.0, f'视频{bv}下载成功，Time：{time.strftime("%Y-%m-%d %H:%M:%S")}\n')
        elif not self.code:
            self.log.insert(1.0, f'视频{bv}下载失败，Time：{time.strftime("%Y-%m-%d %H:%M:%S")}\n')

    def temp_config(self):
        # 判断是否存在文件如果不存在则创建
        if not os.path.exists('.\\tmp'):
            os.makedirs('.\\tmp')
        if not os.path.exists('.\\tmp\\config.json'):
            return False

        # 读取配置
        with open('.\\tmp\\config.json', 'r') as f:
            self.log.insert(1.0, f'读取历史配置中···，Time：{time.strftime("%Y-%m-%d %H:%M:%S")}\n')
            data = json.load(f)
            if data['bv']:
                self.bv.set(data['bv'])
                self.log.insert(1.0, f'成功读取BV号，Time：{time.strftime("%Y-%m-%d %H:%M:%S")}\n')
            if data['cookie']:
                self.cookies.set(data['cookie'])
                self.log.insert(1.0, f'成功读取cookie值，Time：{time.strftime("%Y-%m-%d %H:%M:%S")}\n')
            if data['folder']:
                self.foldername.set(data['folder'])
                self.log.insert(1.0, f'成功读取保存目录，Time：{time.strftime("%Y-%m-%d %H:%M:%S")}\n')
            self.log.insert(1.0, f'读取已完成，Time：{time.strftime("%Y-%m-%d %H:%M:%S")}\n')

    def new_config(self):
        data = {
            "bv": f"{str(self.bv.get())}",
            "cookie": f"{str(self.cookies.get())}",
            "folder": f"{str(self.foldername.get())}"
        }

        with open('.\\tmp\\config.json', 'w') as f:
            json.dump(data, f)

if __name__ == '__main__':
    root = Tk()
    windows = MyGui(root)
    windows.get_windows()
    windows.check_ffmpeg()
    windows.init_windows_name.mainloop()
