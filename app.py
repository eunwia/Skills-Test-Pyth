'''
    UC ICT Congress Registration System
    Run: python app.py
    First time only: python setup_db.py
'''
import sys
sys.path.insert(0,'db/')
from db.dbhelper import *
from flask import Flask, render_template, request, redirect
from datetime import date
import random

app = Flask(__name__)
TABLE = 'registration'

# ---------- Menu ----------
@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/go')
def go():
    page = request.args.get('page')
    return redirect('/' + page)

# ---------- Registration ----------
@app.route('/register')
def register():
    students = getall(TABLE)
    return render_template('register.html', students=students, edit=None)

@app.route('/register/add', methods=['POST'])
def register_add():
    old_studnum = request.form.get('old_studnum')
    data = {
        'studnum': request.form['studnum'],
        'studcam': request.form['studcam'],
        'studFname': request.form['studFname'],
        'studLname': request.form['studLname'],
        'amountPaid': request.form['amountPaid'],
    }
    if old_studnum:
        updaterecord(
        TABLE, 
        studnum=old_studnum, 
        studcam=data['studcam'],
        studFname=data['studFname'], 
        studLname=data['studLname'],                 
        amountPaid=data['amountPaid'])
    else:
        data['attended'] = 'No'
        addrecord(TABLE, **data)
    return redirect('/register')

@app.route('/register/edit/<studnum>')
def register_edit(studnum):
    students = getall(TABLE)
    edit = getrecord(TABLE, studnum=studnum)[0]
    return render_template('register.html', students=students, edit=edit)

@app.route('/register/delete/<studnum>')
def register_delete(studnum):
    deleterecord(TABLE, studnum=studnum)
    return redirect('/register')

# ---------- Attendance ----------
@app.route('/attendance')
def attendance():
    students = getall(TABLE)
    return render_template('attendance.html', students=students, msg=None)

@app.route('/attendance/check', methods=['POST'])
def attendance_check():
    studnum = request.form['studnum']
    found = getrecord(TABLE, studnum=studnum)
    students = getall(TABLE)
    if not found:
        msg = "NOT YET REGISTERED"
    elif found[0]['attended'] == 'Yes':
        msg = "ALREADY ATTENDED"
    else:
        msg = "Student found. Click Yes/No below to record attendance."
    return render_template('attendance.html', students=students, msg=msg)

@app.route('/attendance/submit', methods=['POST'])
def attendance_submit():
    studnum = request.form['studnum']
    attended = request.form['attended']
    found = getrecord(TABLE, studnum=studnum)[0]
    if found['attended'] == 'Yes':
        msg = "ALREADY EXISTS. This will not update student's attendance record."
    else:
        updaterecord(TABLE, studnum=studnum, attended=attended)
        msg = "SUCCESSFULLY RECORDED"
    students = getall(TABLE)
    return render_template('attendance.html', students=students, msg=msg)

# ---------- Raffle ----------
@app.route('/raffle', methods=['GET', 'POST'])
def raffle():
    winner = None
    if request.method == 'POST':
        students = getall(TABLE)
        winner = random.choice(students) if students else None
    return render_template('raffle.html', winner=winner)

# ---------- Check My Campus ----------
@app.route('/campus', methods=['GET', 'POST'])
def campus():
    result, searched = None, False
    if request.method == 'POST':
        searched = True
        studnum = request.form['studnum']
        found = getrecord(TABLE, studnum=studnum)
        result = found[0] if found else None
    return render_template('campus.html', result=result, searched=searched)

# ---------- Report ----------
@app.route('/report')
def report():
    students = getall(TABLE)

    campuses = sorted(set(s['studcam'] for s in students))
    campus_summary = []
    for c in campuses:
        members = [s for s in students if s['studcam'] == c]
        attended = len([s for s in members if s['attended'] == 'Yes'])
        campus_summary.append({'studcam': c, 'count': len(members), 'attended': attended})

    total_count = len(students)
    total_attended = len([s for s in students if s['attended'] == 'Yes'])
    total_collection = sum(s['amountPaid'] for s in students)

    return render_template('report.html', students=students, campus_summary=campus_summary,
                            total_count=total_count, total_attended=total_attended,
                            total_collection=total_collection, today=date.today().strftime('%m/%d/%Y'))

if __name__ == '__main__':
    app.run(debug=True)
