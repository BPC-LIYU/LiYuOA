import json
import os
import subprocess
import fcntl
from flask import Flask, request
import time
from werkzeug.contrib.fixers import ProxyFix
from multiprocessing import Process
import thread

app = Flask(__name__)

def run_cmd(target_path, in_cmd):
    cmd = """cd "%s" && %s>>./log""" % (target_path, in_cmd)
    p = subprocess.Popen(cmd, shell=True)
    p.wait()


@app.route('/', methods=["GET", "POST"])
def main():
    lock_file = 'release.lck'
    if not os.path.exists(lock_file):
        try:
            with open(lock_file, 'w') as file:
                fcntl.flock(file, fcntl.LOCK_EX)
                run_cmd('/web/LiYuOA', 'git pull')
                run_cmd('/web/LiYuOA', 'python manage.py syncdb')
                run_cmd('/web/LiYuOA', 'python manage.py sync_appinfo_and_role')
                run_cmd('/web/LiYuOA', 'python manage.py sync_api_document')
                run_cmd('/web/LiYuOA', '/etc/init.d/apache2 restart')
        finally:
            os.remove(lock_file)
    return 'ok'


app.wsgi_app = ProxyFix(app.wsgi_app)

#
# if __name__ == "__main__":
#     lock_file = 'release.lck'
#     if not os.path.exists(lock_file):
#         with open(lock_file, 'w') as file:
#             fcntl.flock(file, fcntl.LOCK_EX)
#             run_cmd('/web/LiYuOA', 'git pull')
#             run_cmd('/web/LiYuOA', 'python manage.py syncdb')
#             run_cmd('/web/LiYuOA', 'python manage.py sync_appinfo_and_role')
#             run_cmd('/web/LiYuOA', 'python manage.py sync_api_document')
#         os.remove(lock_file)
