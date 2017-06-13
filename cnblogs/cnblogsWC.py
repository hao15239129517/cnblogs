# coding=utf-8
import sys
import jieba
from wordcloud import WordCloud
import pymongo
import threading
from Queue import Queue
import datetime
import os
reload(sys)
sys.setdefaultencoding('utf-8')


class MyThread(threading.Thread):

    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self):
        apply(self.func, self.args)
# 获取内容 线程


def getTitle(queue, table):
    for j in range(1, 3001):
        #         start = datetime.datetime.now()
        list = table.find({'top': j}, {'title': 1, 'top': 1, 'nickName': 1})
        if list.count() == 0:
            continue
        txt = ''
        for i in list:
            txt += str(i['title']) + '\n'
            name = i['nickName']
            top = i['top']
        txt = ' '.join(jieba.cut(txt))
        queue.put((txt, name, top), 1)
#         print((datetime.datetime.now() - start).seconds)


def getImg(queue, word):
    for i in range(1, 3001):
        #         start = datetime.datetime.now()
        get = queue.get(1)
        word.generate(get[0])
        name = get[1].replace('<', '').replace('>', '').replace('/', '').replace('\\', '').replace(
            '|', '').replace(':', '').replace('"', '').replace('*', '').replace('?', '')
        word.to_file(
            'wordcloudimgs/' + str(get[2]) + '-' + str(name).decode('utf-8') + '.jpg')
        print(str(get[1]).decode('utf-8') + '\t生成成功')
#         print((datetime.datetime.now() - start).seconds)


def main():
    client = pymongo.MongoClient(host='127.0.0.1', port=27017)
    dbName = client['cnblogs']
    table = dbName['articles']
    wc = WordCloud(
        font_path='msyh.ttc', background_color='#ccc', width=600, height=600)
    if not os.path.exists('wordcloudimgs'):
        os.mkdir('wordcloudimgs')
    threads = []
    queue = Queue()
    titleThread = MyThread(getTitle, (queue, table))
    imgThread = MyThread(getImg, (queue, wc))
    threads.append(imgThread)
    threads.append(titleThread)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
