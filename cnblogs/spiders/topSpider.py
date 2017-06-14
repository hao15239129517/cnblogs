# -*- coding: utf-8 -*-
import scrapy
from cnblogs.items import CnblogsItem


class TopSpider(scrapy.Spider):
    name = 'top'
    allowed_domains = ['www.cnblogs.com']
    start_urls = ['http://www.cnblogs.com/AllBloggers.aspx']

    def parse(self, response):
        for i in response.xpath("//table[@width='90%']//td"):
            item = CnblogsItem()
            item['top'] = i.xpath(
                "./small[1]/text()").extract()[0].split('.')[-2].strip()
            item['nickName'] = i.xpath("./a[1]//text()").extract()[0].strip()
            item['userName'] = i.xpath(
                "./a[1]/@href").extract()[0].split('/')[-2].strip()
            totalAndScore = i.xpath(
                "./small[2]//text()").extract()[0].lstrip('(').rstrip(')').split(',')
            item['score'] = totalAndScore[2].strip()
#             print(top)
#             print(nickName)
#             print(userName)
#             print(total)
#             print(score)
#             return
            yield scrapy.Request(i.xpath("./a[1]/@href").extract()[0], meta={'page': 1, 'item': item},
                                 callback=self.parse_page)

    def parse_page(self, response):
        #         print(response.meta['nickName'])
        #//a[contains(@id,'TitleUrl')]
        urlArr = response.url.split('default.aspx?')
        if len(urlArr) > 1:
            baseUrl = urlArr[-2]
        else:
            baseUrl = response.url
        list = response.xpath("//a[contains(@id,'TitleUrl')]")
        for i in list:
            item = CnblogsItem()
            item['top'] = int(response.meta['item']['top'])
            item['nickName'] = response.meta['item']['nickName']
            item['userName'] = response.meta['item']['userName']
            item['score'] = int(response.meta['item']['score'])
            item['pageLink'] = response.url
            item['title'] = i.xpath(
                "./text()").extract()[0].replace(u'[置顶]', '').replace('[Top]', '').strip()
            item['articleLink'] = i.xpath("./@href").extract()[0]
            yield scrapy.Request(i.xpath("./@href").extract()[0], meta={'item': item}, callback=self.parse_content)
        if len(list) > 0:
            response.meta['page'] += 1
            yield scrapy.Request(baseUrl + 'default.aspx?page=' + str(response.meta['page']), meta={'page': response.meta['page'], 'item': response.meta['item']}, callback=self.parse_page)

    def parse_content(self, response):
        content = response.xpath("//div[@id='cnblogs_post_body']").extract()
        item = response.meta['item']
        if len(content) == 0:
            item['content'] = u'该文章已加密'
        else:
            item['content'] = content[0]
        yield item
