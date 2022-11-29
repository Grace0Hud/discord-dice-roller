from os.path import isfile
from sqlite3 import connect
from apscheduler.triggers.cron import CronTrigger
DB_PATH = "./data/db/database.db"
BUILD_PATH = "./data/db/build.sql"

#connects the database to the path of where the database file is
cxn = connect(DB_PATH, check_same_thread=False)
#called a database cursor
cur = cxn.cursor()

def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()

    return inner

@with_commit
def build():
    if isfile(BUILD_PATH):
        scriptexec(BUILD_PATH)

#commits to the database before being able to save the changes
def commit():
    cxn.commit()

#add job to the scheduler to commit database every minute
def autosave(sched):
    sched.add_job(commit, CronTrigger(second=0))

def close():
    cxn.close()

#shortcut function for running commands/queries
def field(command, *values):
    cur.execute(command, tuple(values))
    #will return none if querying from a nonexistent table
    fetch = cur.fetchone()
    if(fetch) is not None:
        return fetch[0]

def record(command, *values):
    cur.execute(command, tuple(values))
    return cur.fetchone()
#executes a command and fetches all the data to verify it was added
def records(command, *values):
    cur.execute(command, tuple(values))
    return cur.fetchall()

def column(command, *values):
    cur.execute(command, tuple(values))
    return [item[0] for item in cur.fetchall()]

#the two below are mostly just flavor for calling sqlite3 commands
def execute(command, *values):
    cur.execute(command, tuple(values))

def multiexec(command, valueset):
    cur.executemany(command, valueset)

def scriptexec(path):
	with open(path, "r", encoding="utf-8") as script:
		cur.executescript(script.read())