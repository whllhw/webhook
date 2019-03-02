#!/usr/bin/python3
# coding:utf-8
import logging
import subprocess
import time
import threading

from flask import Flask, jsonify, request, send_from_directory
import sys,os

#if 'debug' not in sys.argv:
#    logging.basicConfig(filename='build.log',format="%(asctime)s %(levelname)s  PID[%(process)d] at:%(funcName)s line:%(lineno)d >>> %(message)s", level=logging.INFO)
#else:
#    logging.basicConfig(format="%(asctime)s %(levelname)s  PID[%(process)d] at:%(funcName)s line:%(lineno)d >>> %(message)s", level=logging.DEBUG)

app = Flask(__name__)
@app.route('/webhook/log')
def get_dir():
    Dir = [ (i,os.stat('build-log/'+i).st_mtime) for i in os.listdir('build-log/')]
    Dir = sorted(Dir,key=lambda x:x[1],reverse=True)
    return ''.join(['<li style="text-align: center;"><a href="log/{0}">{0}</a></li>'.format(i[0]) for i in Dir])

@app.route('/webhook/log/<build_time>')
def getlog(build_time):
    return send_from_directory('build-log/',build_time)

@app.route('/webhook/deploy/<git>',methods=['POST'])
def post(git):
    json = request.json
    if not json:
        return jsonify({'error':1,'msg':'not post data'}),400
    if request.headers['X-Coding-Event'] == 'ping':
        return 'pong'
    shell = None
    for i in branch_switch[git]:
        if i['branch'] == json['ref'].split('/')[-1]:
            shell = i['shell']
            break
    if not shell:
        return jsonify({'error':1,'stdout':'not ' + json['ref'].split('/')[-1] + ' branch!ignore'}),400
    key = str(int(time.time()))+'.txt'
    t = threading.Thread(target=pull,args=(shell,json['after'],key))
    t.start()
    return jsonify({'error':0,'stdout':'https://api.smartercollege.cn/webhook/log/'+key}),200
branch_switch = \
{
    'ims':[
        {
            'branch':'master',
            'shell':'../run-ims-master.sh'
        },
        {
            'branch':'server',
            'shell':'../run-ims-server.sh'
        }
    ],
    'mssm':[
        {
            'branch':'master',
            'shell':'../build-mssm-master.sh'
        },
        {
            'branch':'dev',
            'shell':'../build-mssm-dev.sh'
        }
    ]
}

def pull(shell,sha,key):
    try:
        out_bytes = subprocess.check_output([shell+' ' +sha],stderr=subprocess.STDOUT,shell=True).decode()
    except subprocess.CalledProcessError as e:
        out_bytes = e.output.decode()       # Output generated before error
        code      = e.returncode   # Return code
    with open('build-log/'+key,'w') as f:
        f.write(out_bytes)


if __name__=='__main__':
    app.run(port=1080,debug=True)

