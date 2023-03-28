import re
import json
import requests
import os


class BilibiliVideo:
    def __init__(self):
        # 添加headers请求头，对Python解释器进行伪装
        # referer 和 User-Agent要改写成字典形式
        self.headers = {
            "referer": "https://www.bilibili.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }

    def cookie(self, cookie):
        # 设置cookie
        self.cookies = {"SESSDATA": cookie}

    def inquire(self,bv):
        # 检查bv号是否合法
        url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + str(bv)
        response = requests.get(url=url)
        code = response.json()
        if code['code'] == 0:
            return True
        else:
            return False

    def bili_requests(self, bv):
        # 设置请求的 URL 和数据
        url = 'https://www.bilibili.com/video/' + bv
        # 用 requests 的 get 方法访问网页
        self.response = requests.get(url=url, headers=self.headers, cookies=self.cookies)
        self.video()
        return self.response.status_code

    def collectionname(self,bv,episode):
        # 获取视频合集标题
        url = 'https://api.bilibili.com/x/web-interface/view?bvid='
        re23 = requests.get(url + bv)
        titlejson = re23.json()
        titlemain = titlejson['data']['title']
        title = titlejson['data']['pages'][episode - 1]['part']
        title = re.sub(r"[\/,:*?<>| ：&]", "", title)
        return title

    def video(self):
        # 提取视频标题
        # 调用 re 的 findall 方法，去response.text中匹配我们要的标题
        # 正则表达式提取的数据返回的是一个列表，用[0]从列表中取值
        self.title = re.findall('<h1 title="(.*?)"', self.response.text)[0]
        # 如果标题里有[\/:*?<>|]特殊字符，直接删除
        self.title = re.sub(r"[\/,:*?<>| ：&]", "", self.title)
        # 提取 playinfo 里的数据
        # 调用 re的 findall 方法，去 response.text 中匹配我们要的数据
        # 正则表达式提取的数据返回的是一个列表，用[0]从列表中取值
        html_data = re.findall(r'<script>window.__playinfo__=(.*?)</script>', self.response.text)[0]

        # html_data是字符串类型，将字符串转换成字典
        json_data = json.loads(html_data)

        video_url = json_data["data"]["dash"]["video"][0]["baseUrl"]
        print("视频画面地址为：", video_url)
        # 提取音频网址
        audio_url = json_data["data"]["dash"]["audio"][0]["baseUrl"]
        print("音频地址为：", audio_url)

        # response.content获取响应体的二进制数据
        self.video_content = requests.get(url=video_url, headers=self.headers, cookies=self.cookies).content
        self.audio_content = requests.get(url=audio_url, headers=self.headers).content
        # print(video_content)

    def write(self,fold):
        folder = os.path.exists('.\\tmp')
        # 判断是否存在文件夹如果不存在则创建为文件夹
        if not folder:
            # os.makedirs 传入一个path路径，生成一个递归的文件夹；如果文件夹存在，就会报错,因此创建文件夹之前，需要使用os.path.exists(path)函数判断文件夹是否存在；
            os.makedirs('.\\tmp')

        # 创建mp4文件，写入二进制数据
        with open('.\\tmp\\' + self.title + ".mp4", mode="wb") as f:
            f.write(self.video_content)
        # 创建mp3文件，写入二进制数据
        with open('.\\tmp\\' + self.title + ".mp3", mode="wb") as f:
            f.write(self.audio_content)

        cmd = f"ffmpeg.exe -i .\\tmp\\{self.title}.mp4 -i .\\tmp\\{self.title}.mp3 -c:v copy -c:a aac -strict experimental -y {fold + '/' + self.title}.mp4"
        os.system(cmd)
        os.remove(f'tmp\\{self.title}.mp3')
        os.remove(f'tmp\\{self.title}.mp4')

    def rename(self,titlenew):
        cmd = f'rename {self.title}.mp4 {titlenew}.mp4'
        os.system(cmd)



if __name__ == '__main__':
    bili = BilibiliVideo()
    bili.cookie('')
    video = bili.bili_requests('BV1pi4y1V7wN')
    bili.write('C:/Users/ljk/Pictures/视频项目')
    #print(video)
    print(bili.inquire('BV1RX4y1U7Py'))
