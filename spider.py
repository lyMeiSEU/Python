# 爬取豆瓣电影上的影评并生成词云

import re,requests,sys,os

class Spider():
    # 登陆的参数
    data = {'source': 'None',
            'redir': 'https://www.douban.com/',
            'form_email': '你的账号',
            'form_password': '你的密码',
            'remember': 'on',
            'login': '登录'}

    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }

    def __init__(self,target,movie_name,root_pattern,sum_pattern,next_pattern,login_url,supple_url=''):
        # supple_url 是对url的修改
        '''构造函数'''
        self.page = 1
        self.num = 0
        self.target = target
        self.supple_url = supple_url
        self.sum_pattern = sum_pattern
        self.next_pattern = next_pattern
        self.captcha_img_pattern = '<img id="captcha_image" src="([\d\D]*?)" alt="captcha" class="captcha_image"/>'
        self.captcha_id_pattern = '<input type="hidden" name="captcha-id" value="([\d\D]*?)"/>'
        self.file_name=movie_name
        self.login_url=login_url
        # 为保存登陆信息，存储对话
        self.session = requests.session()
        self.root_pattern = root_pattern
        f = open(self.file_name+'.txt','w',encoding='utf-8')
        f.write(' '*50+self.file_name+'\n\n')
        f.close()

    def __fetch_content(self,url):
        htmls = self.session.get(url).text
        #print(htmls)
        return htmls

    def __get_key_info(self,htmls):
        '''找出想要的数据'''
        comments=re.findall(self.root_pattern,htmls)
        pages = re.findall(self.next_pattern,htmls)
        return comments,pages

    def __show(self,comments):
        '''存储数据，分析数据'''
        print('第%d页正在下载'%self.page)
        for x in range(len(comments)):
            with open(self.file_name+'.txt','a',encoding='utf-8') as f:
                f.write(comments[x].strip()+'\n')
                self.num +=1
        self.page +=1



    def __fill_captcha__(self):
        try:
            htmls = self.session.get(self.login_url,headers=Spider.headers).text
            # 获取验证码图片和验证码id
            captcha_img=re.findall(self.captcha_img_pattern, htmls)[0]
            captcha_id = re.findall(self.captcha_id_pattern, htmls)[0]
            # 将验证码图片保存到本地文件,以二进制形式写文件
            with open('captcha.jpg', 'wb') as f:
                captcha_img = requests.session().get(captcha_img)
                f.write(captcha_img.content)

            # 等待用户输入验证码
            captcha = input('输入验证码')
            # 将验证码和id放在登陆参数上面
            Spider.data['captcha-solution'] = captcha
            Spider.data['captcha-id'] = captcha_id
        except Exception as e:
            print(e,'不需要输入验证码')

    def __login(self):
        # 登陆网站，用同一个会话信息，这个data就是登陆的参数
        self.session.post(login_url,headers=Spider.headers,data=Spider.data)

    def run(self):
        # 登陆网站
        self.__fill_captcha__()
        self.__login()
        while True:
            htmls = self.__fetch_content(self.target)
            comments,pages=self.__get_key_info(htmls)
            self.__show(comments)
            print('  该页下载完毕')
            if pages:
                self.target = self.supple_url + pages[0]
            else:
                print('所有影评下载完毕')
                print('下载了%d条影评'%self.num)
                break



if __name__ == '__main__':
    movie_name = '大黄蜂 短评'
    root_pattern='<p class="">([\s\S]*?)</p>'
    # 第一页的影评url
    target = 'https://movie.douban.com/subject/26394152/comments?status=P'
    supple_url='https://movie.douban.com/subject/26394152/comments'
    login_url='https://accounts.douban.com/login'
    sum_pattern='<span>看过[\D]([\d]+)[\D]</span>'
    next_pattern='前页<[\D]{2,5}>[\s]+<a href="([\s\S]*?)" data-page="" class="next">后页'
    spider = Spider(target,movie_name,root_pattern,sum_pattern,next_pattern,login_url,supple_url=supple_url)
    spider.run()

    # # 得到每个词的权值后生成词云
    # path = spider.file_name+'.txt'
    # with open(path,encoding='utf-8') as f:
    #     content = f.read()
    # # 停用词表路径，即是过滤
    # #analyse.set_stop_words('jieba.txt')
    # tags = analyse.extract_tags(content,topK=100,withWeight=True)
    # for v,n in tags:
    #     print(v+'\t'+ str(n*100))

