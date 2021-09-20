import datetime
import os


def migration_format_now():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')


def migration_format(path):
    return os.path.join(
        os.path.dirname(path),
        f'{migration_format_now()}_{os.path.basename(path)}',
    )
