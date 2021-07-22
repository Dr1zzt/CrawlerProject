# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XhsNoteItem(scrapy.Item):
    """
    小红书笔记
    """
    note_id = scrapy.Field()
    note_title = scrapy.Field()
    author_id = scrapy.Field()
    author_red_id = scrapy.Field()
    search_word = scrapy.Field()
    created_time = scrapy.Field()
    note_page = scrapy.Field()


class XhsCommentItem(scrapy.Item):
    """
    小红书评论
    """
    content = scrapy.Field()
    note_id = scrapy.Field()
    nickname = scrapy.Field()
    user_id = scrapy.Field()
    xhs_id = scrapy.Field()
    comment_time = scrapy.Field()
    created_time = scrapy.Field()
    note_page = scrapy.Field()

