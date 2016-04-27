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

target_ref = 'refs/heads/need_server_2_develop'
target_path = '/web/ttjd_phonegap_www/'
target_password = 'slkdjflkk13123ksdfsldk'


def run_cmd():
  cmd = """cd "%s" && git pull && python auto_release.py""" % target_path
  p = subprocess.Popen(cmd, shell=True)
  p.wait()


@app.route('/', methods=["GET", "POST"])
def main():
  lock_file = 'release.lck'
  if not os.path.exists(lock_file):
    try:
      with open(lock_file, 'w') as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        run_cmd()
    finally:
      os.remove(lock_file)
  return 'ok'


app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ =="__main__":
  lock_file = 'release.lck'
  if not os.path.exists(lock_file):
    with open(lock_file, 'w') as file:
      fcntl.flock(file, fcntl.LOCK_EX)
      run_cmd()
    os.remove(lock_file)
