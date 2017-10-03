from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import CareerForm, RoleForm, UserAssignForm
from .. import db
from ..models import Career, Role, User

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Career Views

@admin.route('/careers', methods=['GET', 'POST'])
@login_required
def list_careers():
    """
    List all career fields
    """
    check_admin()

    careers = Career.query.all()
    return render_template('admin/careers/careers.html',
                           careers=careers, title="Career Fields")

@admin.route('/careers/add', methods=['GET', 'POST'])
@login_required
def add_career():
    """
    Add a career field to the database
    """
    check_admin()

    add_career = True

    form = CareerForm()
    if form.validate_on_submit():
        career = Career(name=form.name.data,
                        description=form.description.data)
        try:
            # add career field to the database
            db.session.add(career)
            db.session.commit()
            flash('You have successfully added a career field to the database.')
        except:
            # in case career field already exists
            flash('Error: career field already exists.')

        # redirect to career field page
        return redirect(url_for('admin.list_careers'))

    # load career template
    return render_template('admin/careers/career.html', action="Add",
                           add_career=add_career, form=form,
                           title="Add a Career Field")

@admin.route('/careers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_career(id):
    """
    Edit a career field
    """
    check_admin()

    add_career = False

    career = Career.query.get_or_404(id)
    form = CareerForm(obj=career)
    if form.validate_on_submit():
        career.name = form.name.data
        career.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the career {}.'.format(career.name))

        # redirect to the careers page
        return redirect(url_for('admin.list_careers'))

    form.description.data = career.description
    form.name.data = career.name
    return render_template('admin/careers/career.html', action="Edit",
                           add_careert=add_career, form=form,
                           career=career, title="Edit Career Field")

@admin.route('/careers/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_career(id):
    """
    Delete a career field from the database
    """
    check_admin()

    career = Career.query.get_or_404(id)
    db.session.delete(career)
    db.session.commit()
    flash('You have successfully deleted the career.')

    # redirect to the careers page
    return redirect(url_for('admin.list_careers'))

    return render_template(title="Delete A Career Field")

# Role Views

@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')

@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')

@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")

@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")


# User Views

@admin.route('/users')
@login_required
def list_users():
    """
    List all users
    """
    check_admin()

    users = User.query.all()
    return render_template('admin/users/users.html',
                           users=users, title='Users')

@admin.route('/users/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_user(id):
    """
    Assign a career field and a role to an user
    """
    check_admin()

    user = User.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if user.is_admin:
        abort(403)

    form = UserAssignForm(obj=user)
    if form.validate_on_submit():
        user.career = form.career.data
        user.role = form.role.data
        db.session.add(user)
        db.session.commit()
        flash('You have successfully assigned a career path and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_users'))

    return render_template('admin/users/user.html',
                           user=user, form=form,
                           title='Assign User')