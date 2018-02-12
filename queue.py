from rq import Queue
from worker import conn

q = Queue(connection=conn)

from utils import aquadvisor

result = q.enqueue(aquadvisor, 'http://heroku.com')
