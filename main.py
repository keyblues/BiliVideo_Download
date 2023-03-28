import threading
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import BilibiliVideo
from BilibiliVideo import *


class MyGui:
    def __init__(self, init_window_name):
        self.init_windows_name = init_window_name
        self.init_windows_name.title("BiliVideo v1.0")
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
        Label(root, text='BV号:', font=("Times", 15)).place(x=0, y=21, width=99, height=29)
        Label(root, text='Cookie:', font=("Times", 15)).place(x=0, y=61, width=99, height=29)
        Label(root, text='保存目录:', font=("Times", 15)).place(x=0, y=101, width=99, height=29)
        self.enter = Button(root, text="Enter", font=("Times", 15), bg='#EEEEEE',command=lambda: self.thread())
        self.enter.place(x=501, y=20, width=99, height=70)
        Button(root, text="选择", font=("Times", 15), bg='#EEEEEE', command=self.fold).place(x=501, y=100, width=99,
                                                                                           height=30)
        Checkbutton(root, text="合集", font=("Times", 15), activebackground='#DDDDDD', command='',
                    variable=self.CheckbuttonVar).place(x=0, y=141, width=99, height=30)

    def fold(self):
        # 打开目录选择器，并返回目录路径
        file = filedialog.askdirectory()
        self.foldername.set(file)
        self.t = threading.Thread(target=self.download)

    def thread(self):
        # 每点击一次下载就生成一个新的线程
        self.t = threading.Thread(target=self.download)
        self.t.start()

    def download(self):
        global video
        bili = BilibiliVideo()
        bili.cookie(self.cookies.get())
        self.enter.config(state='disabled')
        if not bili.inquire(self.bv.get()):
            messagebox.showinfo("警告！", "BV号不合法或不存在！")
            self.enter.config(state='normal')
            exit()
        if self.CheckbuttonVar.get() == '1':
            messagebox.showinfo("警告！", "将要下载合集视频，请确认参数是否正确！")
            for i in range(int(self.start.get()), int(self.stop.get()) + 1):
                try:
                    video = bili.bili_requests(str(self.bv.get() + '/p=' + str(i)))
                except:
                    messagebox.showinfo("警告！", "请求失败！")
                if video == 200:
                    bili.write(self.foldername.get())
                    filename = bili.collectionname(self.bv, i)
                    bili.rename(filename)
                    messagebox.showinfo("提示！", f"p{i}下载成功！")
                else:
                    messagebox.showinfo("提示！", f"p{i}下载失败！")
        else:
            try:
                video = bili.bili_requests(self.bv.get())
            except:
                messagebox.showinfo("警告！", "请求失败！")
            if video == 200:
                bili.write(self.foldername.get())
                messagebox.showinfo("提示！", f"{self.bv.get()}下载成功！")
            else:
                messagebox.showinfo("提示！", f"{self.bv.get()}下载失败！")
        self.enter.config(state='normal')

    def no_closing(self):
        # 设置关闭方式的函数
        if self.t.is_alive():
            if messagebox.askokcancel("Quit", "正在下载，你确定要退出吗?"):
                root.destroy()
        else:
            root.destroy()


if __name__ == '__main__':
    root = Tk()
    windows = MyGui(root)
    windows.get_windows()
    windows.init_windows_name.mainloop()