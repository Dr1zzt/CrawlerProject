# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DyNoteItem(scrapy.Item):
    author_nickname = scrapy.Field()
    aweme_id = scrapy.Field()
    desc = scrapy.Field()
    author_uid = scrapy.Field()
    author_unique_id = scrapy.Field()
    author_short_id = scrapy.Field()
    author_gender = scrapy.Field()
    author_signature = scrapy.Field()
    note_page = scrapy.Field()


class DyCommentItem(scrapy.Item):
    note_id = scrapy.Field()
    comment = scrapy.Field()
    aweme_id = scrapy.Field()
    create_time = scrapy.Field()
    uid = scrapy.Field()
    short_id = scrapy.Field()
    nickname = scrapy.Field()
    gender = scrapy.Field()
    signature = scrapy.Field()
    unique_id = scrapy.Field()
