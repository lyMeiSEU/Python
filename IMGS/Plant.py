import requests
import os, shutil
import json
import jsonpath

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
    work_dir = input('输入图片所在的文件夹名称\n')
    print('遍历整个文件夹\n')
    for parent, dirnames, filenames in os.walk(work_dir,  followlinks=True):
        for filename in filenames:
            fr=open('result.txt','a',encoding='utf-8')
            file_path = os.path.join(parent, filename)
            fr.write('文件名：%s\n' % filename)
            print('文件名：%s' % filename)
            #print('文件完整路径：%s\n' % file_path)
            files = {'file':(filename,open(file_path,'rb'),'image/png',{})}
            m=MultipartEncoder(files)
            # 自动生成Content-Type类型和随机码
            headers['Content-Type'] = m.content_type
            print(m.content_type)
            # 使用data上传文件
            html = requests.post(url, headers=headers, data=m)
            fw =open('data.json','w',encoding='utf-8')
            json.dump(html.json(),fw,ensure_ascii=False,indent=4)#字典转成json,字典转换成字符串

            data=json.loads(json.dumps(html.json()))
            
            fr.write("植物名 可能性\n")
            print("植物名 可能性")
            for v in data['data']['result']:
                print("%s;%s"%(v['name'],v['score']))
                fr.write("%s;%s\n"%(v['name'],v['score']))
            fr.write("\n")
            
            print("\n")
            #print(html.json())