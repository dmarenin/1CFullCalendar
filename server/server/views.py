from datetime import datetime, date, timedelta
from flask import render_template

from server import app, cache
from server import models
from flask import request

import json
import decimal


HEADERS = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST", "Access-Control-Allow-Headers": "Content-Type"}


@app.route('/')
@app.route('/agenda')
def agenda():
    return render_template('agenda.html')

@app.route('/get_tasks')
def get_tasks(): 
    start_trace = datetime.now()
    
    start = request.args.get('start', '')
    end = request.args.get('end', '')
    
    key_cache = f"""{start}_{end}""" 

    tasks = cache.get(key_cache)
    
    if not tasks is None:
        print(f"""backend time {datetime.now()-start_trace}""")
        return tasks, 200, HEADERS 


    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d") + timedelta(days=1)

    task = models.Task

    res = task.select(task.title, task.start, task.end, task.complete, task.employee, task.description)
        
    res = res.where(task.start >= start)
    res = res.where(task.end <= end)
    #res = res.where(task.employee == '9626D89D6773B96411E909BC417AB947')
    #res = res.where(task.complete == False)

    #.where((task.start>=start) & (task.end<=end))

    list_res = list(res.dicts())

    for x in list_res:
        x['url'] = 'http://google.com/'
        if x['complete'] == True:
            x['color'] = '#257e4a'

    res = json.dumps(list_res, default=json_serial)

    cache.set(key_cache, res)
        
    print(f"""backend time {datetime.now()-start_trace}""")
    print(f"""len tasks {len(list_res)}""")
    
    return res, 200, HEADERS

def json_serial(obj):
    if isinstance(obj, (datetime, date)):
      return obj.isoformat()

    if isinstance(obj, decimal.Decimal):
      return float(obj)

    raise TypeError("Type is not serializable %s" % type(obj))

