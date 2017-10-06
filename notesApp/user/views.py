from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, current_user

from . import user
from forms import UserUpdateForm, NoteForm
from .. import db
from ..models import User, Career, Note


@user.route('/viewprofile', methods=['GET', 'POST'])
@login_required
def viewprofile():
    """
    Handle requests to the /register route
    Add an notetaker to the database through the registration form
    """
    user = current_user
    form=UserUpdateForm(obj=user)
    form.populate_obj(user)
    if form.validate_on_submit():

        form.populate_obj(user)

        db.session.commit()

        flash('You have successfully edited your profile!')
    return render_template('user/user.html', title="View Profile",
                           user=user, form=form, action='Edit')


@user.route('/notes')
@login_required
def list_notes():

    """
    List all roles
    """
    user = current_user
    try:
        notes = user.notes
    except:
        notes = False

    return render_template('user/notes.html', user=user,
                           notes=notes, title='Notes')

@user.route('/notes/add', methods=['GET', 'POST'])
@login_required
def add_note():
    """
    Add a role to the database
    """
    add_note = True
    user = current_user
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(title=form.title.data,
                    body=form.body.data)

        try:
            # add role to the database
            user.notes.append(note)
            db.session.add(note)
            db.session.commit()
            flash('You have successfully added a new note to the user.')
        except:
            # in case role name already exists
            flash('Error: .')
        # redirect to the roles page
        return redirect(url_for('user.list_notes'))

    # load role template
    return render_template('user/note.html', add_role=add_note,
                           form=form, title='Add Note')


@user.route('/notes/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    """
    Edit a role
    """

    add_note = False

    note = Note.query.get_or_404(id)
    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.body = form.body.data
        db.session.add(note)
        db.session.commit()
        flash('You have successfully edited the note.')

        # redirect to the roles page
        return redirect(url_for('user.list_notes'))

    form.body.data = note.body
    form.title.data = note.title
    return render_template('user/note.html', add_role=add_note,
                           form=form, title="Edit Note")

@user.route('/notes/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_note(id):
    """
    Delete a role from the database
    """

    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('user.list_notes'))

    return render_template(title="Delete Note")