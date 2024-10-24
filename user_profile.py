from flask import Blueprint, render_template, redirect, url_for, session

profile = Blueprint("profile", __name__)

@profile.route("/profile")
def about_profile():
    if 'user' in session:
        return render_template('profile.html', username=session['user'], useremail=session['email'])
    else:
        return redirect(url_for('account.create_account'))