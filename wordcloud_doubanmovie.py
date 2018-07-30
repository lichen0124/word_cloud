# 对网页进行访问，python中使用的是urllib库
from urllib import request
resp = request.urlopen('https://movie.douban.com/nowplaying/hangzhou/')
html_data = resp.read().decode('utf-8')
#print(html_data)

from bs4 import BeautifulSoup as bs
soup = bs(html_data, 'html.parser') # 第一个参数为需要提取数据的html，第二个参数是指定解析器。
nowplaying_movie = soup.find_all('div', id='nowplaying') # 使用find_all()读取html标签中的内容。
nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_='list-item')

# data-subject属性里面放了电影的id号码，而在img标签的alt属性里面放了电影的名字，因此我们就通过这两个属性来得到电影的id和名称
nowplaying_list = []
for item in nowplaying_movie_list:
    nowplaying_dict = {}
    nowplaying_dict['id'] = item['data-subject']
    for tag_img_item in item.find_all('img'):
        nowplaying_dict['name'] = tag_img_item['alt']
        nowplaying_list.append(nowplaying_dict)

# 给电影加上序号，并按行显示。
print("Movie list:")
for i in range(len(nowplaying_list)):
    print(i, nowplaying_list[i])

# 选择电影并读取1-20*10条短评
input_number = input('Please enter the sequence number of the movie: ')
number = int(input_number)
comment_div_list = []
for i in range(10):
    requrl = 'https://movie.douban.com/subject/' + nowplaying_list[number]['id'] + '/comments' +'?' +'start={}'.format(i*20) + '&limit=20'
    resp = request.urlopen(requrl)
    html_data = resp.read().decode('utf-8')
    soup = bs(html_data, 'html.parser')
    comment_div_list = comment_div_list + soup.find_all('div', class_='comment')
#print(comment_div_list)

eachCommentList = [];
for item in comment_div_list:
    if item.find_all('span')[-1].string is not None:
        eachCommentList.append(item.find_all('span')[-1].string)
#print(eachCommentList)

# 将列表中的数据放在一个字符串数组中
comments = ''
for k in range(len(eachCommentList)):
    comments = comments + (str(eachCommentList[k])).strip()

######### line 40-63 is another method
from wordcloud import WordCloud
# 对分词文本生成词云
# 生成词云，需要指定支持中文的字体，否则无法生成中文词云
wc = WordCloud(
#设置词云图片背景色，默认黑色
# background_color='white',
#设置词云最大单词数
max_words=200,
#设置词云中字号最大值
max_font_size=80,
#设置词云图片宽、高
width=768,
height=1024,
#设置词云文字字体（美化和解决中文乱码问题）
font_path='simhei.ttf'
).generate(comments)

# 绘图（标准长方形图）
import matplotlib.pyplot as plt
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
#plt.title('Word Cloud of Movie: {}'.format(nowplaying_list[number]['name']))
print('Word Cloud of the Movie <<{}>>:'.format(nowplaying_list[number]['name']))
plt.show()
#wc.to_file('wordcloud_movie.png')
