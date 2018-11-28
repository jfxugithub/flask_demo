from __future__ import absolute_import
import os
from flask_migrate import MigrateCommand
from flask_script import Manager

from app import create_app

app = create_app(os.getenv('FLASK_CONF') or 'default')

manage = Manager(app=app)
manage.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manage.run()