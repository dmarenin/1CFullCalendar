from datetime import datetime, date, timedelta
from flask import render_template, request

from server import app, cache, models

import json
import decimal
import peewee


HEADERS = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST", "Access-Control-Allow-Headers": "Content-Type"}


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/index2')
def index2():
    return render_template('index2.html')

@app.route('/index3')
def index3():
    return render_template('index3.html')

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
    employee = models.Employee

    res = task.select(task.title, task.start, task.end, task.complete, task.employee, task.description, employee.title.alias('empl_title')).join(employee, join_type=peewee.JOIN.LEFT_OUTER, on=(task.employee == employee.link))
        
    res = res.where(task.start >= start)
    res = res.where(task.end <= end)
    #res = res.where(task.employee == '9626D89D6773B96411E909BC417AB947')
    #res = res.where(task.complete == False)

    list_res = list(res.dicts())

    for x in list_res:
        x['description'] += f"""<BR> {x['empl_title']} </BR>"""
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

