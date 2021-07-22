# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

from itemadapter import ItemAdapter
from .items import XhsNoteItem, XhsCommentItem
from .common import mysqlUtil


class XhsScrapyPipeline:
    def process_item(self, item, spider):
        conn = mysqlUtil.MysqlConn()
        sql = ""
        if isinstance(item, XhsCommentItem):
            pass
        elif isinstance(item, XhsNoteItem):
            pass
        print(sql)
        self.do_insert(conn=conn, sql=sql)
        return item

    def do_insert(self, conn, sql):
        conn.process_item(sql)
