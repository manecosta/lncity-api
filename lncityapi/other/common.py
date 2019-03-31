
from peewee import MySQLDatabase
from conf import conf


lncity_db = MySQLDatabase(
    conf.get('MYSQL_DB'),
    host=conf.get('MYSQL_HOST'),
    port=int(conf.get('MYSQL_PORT')),
    user=conf.get('MYSQL_USER'),
    passwd=conf.get('MYSQL_PASS'),
    charset='utf8mb4'
)
