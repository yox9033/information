from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from info import create_app, db
from info import models

"""入口程序"""

app = create_app("develop")

# 把app交由manager管理
manager = Manager(app)
# 添加数据库迁移框架
migrate = Migrate(app, db)
# 添加迁移数据库框架脚本
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
