from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/',methods=['GET','POST'])
@login_required
def home():
    if request.method=='POST':
        note = request.form.get('notes')
        if len(note)<1:
            flash("note is too sort!",category="error")
        else:
            new_note = Note(data = note,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("note addedd",category="success")

    return render_template("main.html",user = current_user)

@views.route('/delete-note',methods=['POST'])
def delete_note():
    if request.method == 'POST':
        note = json.loads(request.data)
        print(note)
        noteId = note['noteId']
        print(noteId)
        note = Note.query.get(noteId)
        
        db.session.delete(note)
        db.session.commit()

    return jsonify({})
   