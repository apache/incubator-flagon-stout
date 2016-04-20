import subprocess
import os

SM_QUESTION_NAME='MOT'
SM_EXPERIMENT_NAME='2015_public_xdataonline'

SM_LOCK_FILE = './op_tasks/SM_LOCK'
SM_SCRIPT_NAME = 'surveyMongoUpdate.sh'
SM_SCRIPT_PATH = './op_tasks/'
SM_PID = None

def sm_request_update(question, experiment):
    global SM_PID

    subprocess.call(['touch', SM_LOCK_FILE])
   
    if not check_pid(SM_PID):
        print 'Spawning new SurveyMongo Update ... ', SM_SCRIPT_PATH+SM_SCRIPT_NAME
        SM_PID = subprocess.Popen([SM_SCRIPT_PATH+SM_SCRIPT_NAME, question, experiment]).pid

    print 'SureveyMongo updating on PID ', SM_PID

#check if a pid is running on the system
def check_pid(pid):
    if pid == None:
        return False

    try:
        os.kill(pid,0)
    except OSError:
        return False
    else:
        return True
