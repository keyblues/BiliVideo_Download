import tkinter
import threading
import ctypes
import time
import re
import os

from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

from moviepy.editor import VideoFileClip, AudioFileClip

import requests


class MyGui:
    def __init__(self, init_windows, thread):
        """ 初始化窗口 """
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        self.init_windows = init_windows
        self.init_windows.title('BiliVideo_Download GUI v2.0.3 by keyblue.cn')
        self.init_windows.config(bg='#FFFFFF')
        self.init_windows.geometry("600x365")
        self.init_windows.call('tk', 'scaling', scale_factor / 75)
        self.init_windows.resizable(False, False)
        style = ttk.Style()
        style.configure("Custom.TLabel", background="white", font=("微软雅黑", 12), anchor="center")
        style.configure("Custom.TCheckbutton", background="white", font=("微软雅黑", 12), anchor="center")

        # 文字
        self.label_bvid = ttk.Label(self.init_windows, text='BV号:', style="Custom.TLabel")
        self.label_bvid.place(x=5, y=21, width=120, height=29)
        self.label_cookie = ttk.Label(self.init_windows, text='SESSDATA:', style="Custom.TLabel")
        self.label_cookie.place(x=5, y=61, width=120, height=29)
        self.label_directory = ttk.Label(self.init_windows, text='保存目录:', style="Custom.TLabel")
        self.label_directory.place(x=5, y=101, width=120, height=29)
        self.label_collection = ttk.Label(self.init_windows, text='-', style="Custom.TLabel")
        self.label_collection.place(x=152, y=140, width=16, height=30)
        self.label_quality = ttk.Label(self.init_windows, text='质量:', style="Custom.TLabel")
        self.label_quality.place(x=230, y=140, width=50, height=30)

        # 输入框
        self.input_bvid = ttk.Entry(self.init_windows, font=("微软雅黑", 15))
        self.input_bvid.place(x=130, y=20, width=455, height=30)
        self.input_bvid.bind('<KeyRelease>', thread.set_quality)
        self.input_cookie = ttk.Entry(self.init_windows, font=("微软雅黑", 15))
        self.input_cookie.place(x=130, y=60, width=455, height=30)
        self.input_cookie.bind('<KeyRelease>', thread.set_quality)
        self.input_directory = ttk.Entry(self.init_windows, font=("微软雅黑", 15))
        self.input_directory.place(x=130, y=100, width=340, height=30)

        # 日志
        self.frame_log = tkinter.Frame(self.init_windows, relief=tkinter.SUNKEN)
        self.frame_log.place(x=15, y=220, width=571, height=100)
        self.scroll = tkinter.Scrollbar(self.frame_log)
        self.scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.text_log = tkinter.Text(self.frame_log, borderwidth=0)
        self.text_log.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        self.text_log.configure(font=("微软雅黑", 9), bd=1, relief="solid", yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.text_log.yview)
        self.text_log.insert(tkinter.END, "欢迎! 更多请访问www.keyblue.cn")

        # 按钮
        self.button_directory = ttk.Button(self.init_windows, text="...", command=self.open_directory)
        self.button_directory.place(x=485, y=100, width=101, height=30)
        self.button_info = ttk.Button(self.init_windows, text="info", command=thread.get_info)
        self.button_info.place(x=485, y=140, width=101, height=30)
        self.button_info = ttk.Button(self.init_windows, text="help", command=self.help)
        self.button_info.place(x=370, y=140, width=101, height=30)
        self.button_download = ttk.Button(self.init_windows, text="download", command=thread.main)
        self.button_download.place(x=15, y=180, width=571, height=30)

        # 下拉菜单
        self.combobox_start = ttk.Combobox(self.init_windows, values=[], state="readonly")
        self.combobox_start.place(x=100, y=140, width=50, height=30)
        self.combobox_stop = ttk.Combobox(self.init_windows, values=[], state="readonly")
        self.combobox_stop.place(x=170, y=140, width=50, height=30)
        self.combobox_quality = ttk.Combobox(self.init_windows, values=[], state="readonly")
        self.combobox_quality.place(x=285, y=140, width=70, height=30)
        self.checkbutton_var = tkinter.IntVar()
        self.checkbutton_collection = ttk.Checkbutton(self.init_windows, text="合集", variable=self.checkbutton_var,
                                                      style="Custom.TCheckbutton", command=thread.set_collection)
        self.checkbutton_collection.place(x=30, y=140, width=60, height=30)

        # 进度条
        self.progressbar = ttk.Progressbar(self.init_windows)
        self.progressbar.place(x=15, y=330, width=571, height=20)

    def open_directory(self):
        """ 打开目录选择器，并返回目录路径 """
        file = filedialog.askdirectory()
        self.input_directory.delete(0, tkinter.END)
        self.input_directory.insert(0, file)

    def help(self):
        """ 获取帮助 """
        data = """ 输入正确的BV号会自动获取合集数量和清晰度
        输入正确的b站SESSDATA可提高质量 """
        messagebox.showinfo("help", data)


class Thread:
    def __init__(self):
        self.function = ''

    def main(self, *args):
        t = threading.Thread(target=self.function.main, args=())
        t.daemon = True  # 守护线程，在关闭主程序时也关闭线程
        t.start()

    def get_info(self, *args):
        t = threading.Thread(target=self.function.get_info, args=())
        t.daemon = True  # 守护线程，在关闭主程序时也关闭线程
        t.start()

    def set_quality(self, *args):
        t = threading.Thread(target=self.function.set_quality, args=())
        t.daemon = True  # 守护线程，在关闭主程序时也关闭线程
        t.start()

    def set_collection(self, *args):
        t = threading.Thread(target=self.function.set_collection, args=())
        t.daemon = True  # 守护线程，在关闭主程序时也关闭线程
        t.start()


class Function:
    def __init__(self, mygui, video):
        self.mygui = mygui
        self.video = video
        self.set_cookie()

    def main(self):
        self.set_cookie()
        if self.mygui.checkbutton_var.get():
            start = int(self.mygui.combobox_start.get())
            stop = int(self.mygui.combobox_stop.get())
            if start <= stop:
                self.download_collection(start, stop)
            else:
                messagebox.showinfo("温馨提示", '起始集数不能大于结束集数')
        else:
            self.retry_function(self.download, 5, 1)
            self.enable_all_widgets()

    def retry_function(self, func, max_retries=5, *args):
        """
        重试函数
        :param func: 被重试的函数
        :param max_retries: 最大重试次数
        :param args: 被重试函数的参数
        """
        retries = 0
        self.errer_download = []
        while retries < max_retries:
            try:
                return func(*args)
            except Exception as e:
                self.add_log(f"下载出错, 错误信息: {e}")
                retries += 1
                if retries < max_retries:
                    self.add_log(f"等待10秒后重试, 当前重试次数: {retries}")
                    time.sleep(10)
                else:
                    self.add_log("已达到最大重试次数, 放弃重试")
                    self.errer_download.append(*args)
                    return False
                

    def download(self, pages):
        """ 单集下载 """
        bvid = self.mygui.input_bvid.get()
        directory = self.mygui.input_directory.get()
        quality = self.quality_reverse(self.mygui.combobox_quality.get())

        self.disable_all_widgets()

        if not self.inspect_bvid(bvid):
            messagebox.showinfo("温馨提示", '请输入正确的BV号')
            return 0
        if not self.is_directory_exist(directory):
            messagebox.showinfo("温馨提示", '请提供正确的目录')
            return 0
        if quality == '':
            messagebox.showinfo("温馨提示", '请选择视频质量')
            return 0

        videore, audiore = self.video.get_video(bvid, pages=pages, quality=quality)
        bit = self.get_bit(videore, audiore)
        self.set_progressbar(bit)
        self.add_log(f"BV号: {bvid} 状态: 正在下载, 质量-{self.mygui.combobox_quality.get()}, 大小-{self.size(bit)}")

        filename_temp = self.save(directory, videore, audiore)
        self.add_log(f"BV号: {bvid} 状态: 正在合成, 请耐心等待")

        title = self.get_title(bvid)
        try:
            self.merge_videos(filename_temp, directory + '/' + title)
        except:
            messagebox.showinfo("错误", '合成失败，请重试')
            self.enable_all_widgets()
            return False
        self.add_log(f"BV号: {bvid} 状态: 合成完毕, 请前往视频保存目录查看")

        self.enable_all_widgets()
    
    def download_collection(self, start, stop):
        """ 合集下载 """
        bvid = self.mygui.input_bvid.get()
        directory = self.mygui.input_directory.get()
        directory = str(directory) + '/' + str(self.get_title(bvid))
        if not os.path.exists(directory):
            os.makedirs(directory)
        quality = self.quality_reverse(self.mygui.combobox_quality.get())
        self.disable_all_widgets()
        if not self.inspect_bvid(bvid):
            messagebox.showinfo("温馨提示", '请输入正确的BV号')
            return 0
        if not self.is_directory_exist(directory):
            messagebox.showinfo("温馨提示", '请提供正确的目录')
            return 0
        if quality == '':
            messagebox.showinfo("温馨提示", '请选择视频质量')
            return 0
        
        for pages in range(start, stop+1):
            def download_pages(pages):
                videore, audiore = self.video.get_video(bvid, pages=pages, quality=quality)
                bit = self.get_bit(videore, audiore)
                self.set_progressbar(bit)
                self.add_log(f"BV号: {bvid} 合集: {pages} 状态: 正在下载, 质量 {self.mygui.combobox_quality.get()}, 大小 {self.size(bit)}")
                filename_temp = self.save(directory, videore, audiore)
                self.add_log(f"BV号: {bvid} 合集: {pages} 状态: 正在合成, 请耐心等待")
                title = self.get_title_collection(bvid, pages)
                try:
                    self.merge_videos(filename_temp, directory + '/' + title)
                except:
                    messagebox.showinfo("错误", '合成失败，请重试')
                    return False
                self.add_log(f"BV号: {bvid} 合集: {pages} 状态: 合成完毕, 请前往视频保存目录查看")
                    
            if not self.retry_function(download_pages, 5, pages):
                """ 跳过该视频 """
                continue

        self.enable_all_widgets()
        if bool(self.errer_download):
            self.add_log(f"BV号: {bvid} 状态: 出错合集{self.errer_download}")
        else:
            self.add_log(f"BV号: {bvid} 状态: 合集全部下载完成")

    def merge_videos(self, filename_temp, filename_new):
        """ 合并视频和音频 """
        video = VideoFileClip(f"{filename_temp}.mp4")
        audio = AudioFileClip(f"{filename_temp}.mp3")
        final_video = video.set_audio(audio)
        final_video.write_videofile(f"{filename_new}.mp4", verbose=False, logger=None)
        self.mygui.progressbar['value'] = self.maximum
        self.remove(filename_temp)
    
    def disable_all_widgets(self):
        """ 禁用部分控件 """
        for widget in self.mygui.init_windows.winfo_children():
            if not isinstance(widget, (tkinter.Text, ttk.Progressbar, tkinter.Frame, tkinter.Scrollbar)):
                widget.configure(state='disabled')

    def enable_all_widgets(self):
        """ 启用部分控件 """
        for widget in self.mygui.init_windows.winfo_children():
            if not isinstance(widget, (tkinter.Text, ttk.Progressbar, tkinter.Frame, tkinter.Scrollbar)):
                widget.configure(state='normal')
    
    def remove(self,filename_temp):
        """ 删除临时文件 """
        try:
            os.remove(f"{filename_temp}.mp4")
            os.remove(f"{filename_temp}.mp3")
        except:
            pass
    
    def set_progressbar(self, bit):
        """ 设置进度条 """
        self.maximum = bit + int(bit / 6)
        self.mygui.progressbar['value'] = 0
        self.mygui.progressbar['maximum'] = self.maximum

    def add_log(self, text):
        """ 输出日志 """
        text = f"\nTime:{time.strftime('%H:%M:%S')} {text}"
        self.mygui.text_log.insert(tkinter.END, text)
        self.mygui.text_log.see(tkinter.END)
    
    def get_bit(self, videore, audiore):
        bit = int(videore.headers.get('Content-Length')) + int(audiore.headers.get('Content-Length'))
        return bit

    def size(self, bit):
        """ 字节添加单位 """
        value = int(bit)
        units = ["B", "KB", "MB", "GB", "TB", "PB"]
        size = 1024.0
        for i in range(len(units)):
            if (value / size) < 1:
                return "%.2f%s" % (value, units[i])
            value = value / size

    def is_directory_exist(self, directory):
        """ 检查目录合法性 """
        return os.path.exists(directory)
    
    def title_filterate(slef, title):
        """ 过滤标题特殊字符 """
        return re.sub(r"\/|\,|\:|\*|\?|\<|\>|\\|\&|\[|\]|\.\.|\||\'|\"", "", title)

    def inspect_bvid(self, bvid):
        """ 检查BV号 """
        if bool(re.match(r'^BV[a-zA-Z0-9]{10}$', bvid)):
            if self.video.get_info(bvid):
                return True
            else:
                return False
        else:
            return False

    def set_cookie(self):
        """ 设置cookie """
        cookie = self.mygui.input_cookie.get()
        if cookie:
            self.video.set_cookie(cookie)
        else:
            self.video.set_cookie('cookie')

    def set_quality(self):
        """ 设置质量的值 """
        self.set_cookie()
        bvid = self.mygui.input_bvid.get()
        if self.inspect_bvid(bvid):
            cid = self.video.get_cid(bvid, 1)
            quality_list = list(set(self.video.get_quality(bvid, cid)))
            self.mygui.combobox_quality['values'] = self.quality_set_replace(quality_list)

    def set_collection(self):
        """ 设置合集下拉菜单的值 """
        bvid = self.mygui.input_bvid.get()
        if self.inspect_bvid(bvid):
            data = self.video.get_info(bvid)
            commbobox_list = list(range(1, len(data['data']['pages']) + 1))
            self.mygui.combobox_start['values'] = commbobox_list
            self.mygui.combobox_stop['values'] = commbobox_list
            self.mygui.combobox_start.set(min(commbobox_list))
            self.mygui.combobox_stop.set(max(commbobox_list))

    def quality_set_replace(self, quality_list):
        """ 将质量代号提高可读性 """
        for i in range(len(quality_list)):
            if quality_list[i] == 80:
                quality_list[i] = "1080p"
            elif quality_list[i] == 64:
                quality_list[i] = "720p"
            elif quality_list[i] == 32:
                quality_list[i] = "480p"
            elif quality_list[i] == 16:
                quality_list[i] = "360p"
        return quality_list

    def quality_reverse(self, quality):
        """ 将质量替换成代号 """
        if quality == "1080p":
            quality = 80
        elif quality == "720p":
            quality = 64
        elif quality == "480p":
            quality = 32
        elif quality == "360p":
            quality = 16
        return quality

    def get_info(self):
        """ 获取视频的详细信息 """
        bvid = self.mygui.input_bvid.get()
        if bool(re.match(r'^BV[a-zA-Z0-9]{10}$', bvid)):
            data = self.video.get_info(bvid)
            messagebox.showinfo("JSON数据", data)
        else:
            messagebox.showinfo("温馨提示", '请输入正确的BV号')
    
    def get_title(self, bvid):
        """ 获取视频标题 """
        data = self.video.get_info(bvid)
        title = data['data']['title']
        title = self.title_filterate(title)
        return title
    
    def get_title_collection(self, bvid, pages):
        """ 获取合集标题 """
        data = self.video.get_info(bvid)
        title = data['data']['pages'][pages-1]['part']
        title = 'P' + str(pages) + ' ' + self.title_filterate(title)
        return title

    def save(self, directory, videore, audiore):
        """ 保存视频 """
        filename_temp = directory + '/' + str(time.time())
        with open(f"{filename_temp}.mp3", mode="wb") as f:
            for chunk in audiore.iter_content(chunk_size=4096):
                self.mygui.progressbar['value'] += 4096
                self.mygui.progressbar.update()
                if chunk:
                    f.write(chunk)
        with open(f"{filename_temp}.mp4", mode="wb") as f:
            for chunk in videore.iter_content(chunk_size=4096):
                self.mygui.progressbar['value'] += 4096
                self.mygui.progressbar.update()
                if chunk:
                    f.write(chunk)
        return filename_temp


class Video:
    def __init__(self):
        # 获取视频详细信息的接口
        self.api_info = 'https://api.bilibili.com/x/web-interface/view?bvid={}'
        # 获取视频下载链接的接口
        self.api_url = 'https://api.bilibili.com/x/player/wbi/playurl?bvid={}&cid={}&fnval=4048'
        self.headers = {
            "referer": "https://www.bilibili.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/108.0.0.0 Safari/537.36 "
        }

    def set_cookie(self, cookie):
        """ 设置cookie """
        self.cookies = {"SESSDATA": cookie}

    def get_info(self, bvid):
        """ 获取视频信息 """
        url = self.api_info.format(bvid)
        response = requests.get(url=url, headers=self.headers)
        if response.status_code == 200:
            if response.json()['code'] == 0:
                return response.json()
            else:
                return False
        else:
            return False

    def get_cid(self, bvid, pages):
        """ 获取视频cid """
        url = self.api_info.format(bvid)
        response = requests.get(url=url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 0:
                cid = data['data']['pages'][pages - 1]['cid']
                return cid
            else:
                return False
        else:
            return False

    def get_quality(self, bvid, cid):
        """ 获取视频质量列表 """
        url = self.api_url.format(bvid, cid)
        response = requests.get(url=url, headers=self.headers, cookies=self.cookies)
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 0:
                quality_dict = []
                if len(data['data']) > 3:
                    for i in data['data']['dash']['video']:
                        quality_dict.append(i['id'])
                return quality_dict

    def request_url(self, bvid, cid):
        """ 获取视频和音频的url """
        url = self.api_url.format(bvid, cid)
        response = requests.get(url=url, headers=self.headers, cookies=self.cookies)
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 0:
                return data['data']

    def get_video(self, bvid, pages=1, quality=80):
        """ 视频下载 """
        quality_dict = {}
        data = self.request_url(bvid, self.get_cid(bvid, pages))
        for i in data['dash']['video']:
            quality_dict[i['id']] = i['baseUrl']
        video_url = quality_dict[quality]
        audio_url = data['dash']['audio'][0]['baseUrl']
        self.videore = requests.get(url=video_url, headers=self.headers, cookies=self.cookies, stream=True)
        self.audiore = requests.get(url=audio_url, headers=self.headers, cookies=self.cookies, stream=True)
        return self.videore, self.audiore


if __name__ == '__main__':
    windows = tkinter.Tk()
    video = Video()
    thread = Thread()
    mygui = MyGui(windows, thread)
    function = Function(mygui, video)
    thread.function = function
    mygui.init_windows.mainloop()
