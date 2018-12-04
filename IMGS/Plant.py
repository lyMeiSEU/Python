import requests
import os, shutil

# 导入requests_toolbelt库使用MultipartEncoder
from requests_toolbelt import MultipartEncoder

url = "http://shibietu.wwei.cn/fileupload.html?op=shibietu_zhiwu"

headers = {
"Content-Type":"multipart/form-data",
"Referer":"http://shibietu.wwei.cn/zhiwu.html",
"Origin":"http://shibietu.wwei.cn",
"Host":"shibietu.wwei.cn",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763",
"Connection":"Keep-Alive"}


if __name__=='__main__':
    work_dir = 'C:\\Users\\83723\\Desktop\\IMGS'
    for parent, dirnames, filenames in os.walk(work_dir,  followlinks=True):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            print('文件名：%s' % filename)
            print('文件完整路径：%s\n' % file_path)
            files = {'file':(filename,open(filename,'rb'),'image/png',{})}
            m=MultipartEncoder(files)
            # 自动生成Content-Type类型和随机码
            headers['Content-Type'] = m.content_type
            # 使用data上传文件
            html = requests.post(url, headers=headers, data=m)
            print(html.json())


