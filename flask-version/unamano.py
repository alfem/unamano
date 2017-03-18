
# UNAMANO
# Remote support

from flask import Flask, request, render_template
import os
import datetime

app = Flask(__name__)

sleep_time=10
base_dir="/home/alfem/mysite/DATA"
sessions={}

@app.route('/')
def index():
    dirs=os.listdir(base_dir)
    current_sessions={}
    for d in dirs:
        with open(base_dir+"/"+d+"/id") as f:
            session_id=f.readline()
        current_sessions[d]=session_id
    return render_template('sessions.html', sessions=current_sessions)

@app.route('/session/<uid>')
def session(uid='NO SESSION UID'):
    commands=os.listdir(base_dir+"/"+uid)
    return render_template('commands.html', uid=uid, commands=commands)

@app.route('/output/<uid>/<cid>')
def output(uid='NO SESSION UID',cid=''):
    logdir=base_dir+"/"+uid
    logfile=logdir+"/"+cid
    with open(logfile,"r") as f:
        output=f.read()
    return render_template('output.html', uid=uid, cid=cid, output=output)

@app.route('/command',methods=['POST'])
def command():
    uid=request.form['uid']
    logdir=base_dir+"/"+uid
    commandfile=logdir+"/command"
    command=request.form['command']

    with open(commandfile,"w") as f:
        f.write(command)
    return render_template('commands.html', uid=uid, commands="")



@app.route('/client', methods=['POST','GET'])
def client():
    hostname=request.headers['hostname']
    pclabel=request.headers['pclabel']
    uid=request.headers['sessionid']

    logdir=base_dir+"/"+uid

    if not os.path.exists(logdir):
        os.makedirs(logdir)
        timestamp=datetime.datetime.now()
        with open(logdir+"/id","w") as f:
             f.write(timestamp.isoformat()+" "+hostname+"-"+pclabel)

    if request.method == 'GET':
        commandfile=logdir+"/command"
        try:
           with open(commandfile,"r") as f:
                command=f.read()
        except:
            command=""
        if uid not in sessions:
            sessions[uid]=0
        return command

    if request.method == 'POST':
        logfile=logdir+"/"+str(sessions[uid])
        file = request.files['output']
        file.save(logfile)

        sessions[uid]+=1
        return "OK"


