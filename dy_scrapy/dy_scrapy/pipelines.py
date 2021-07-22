# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import DyNoteItem, DyCommentItem
from common.mysqlUtil import MysqlConn


class DyScrapyPipeline:
    def process_item(self, item, spider):
        sql = ""

        if isinstance(item, DyNoteItem):
            pass
        elif isinstance(item, DyCommentItem):
            pass
        print(sql)
        self.do_insert(conn=MysqlConn(), sql=sql)
        return item

    def do_insert(self, conn, sql):
        conn.process_item(sql)
