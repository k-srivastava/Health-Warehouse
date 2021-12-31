"""
File to manage the account page and its respective subpages. These pages contain general information about the store
and help manage sales, profits, stock and other items.
"""
from flask import Blueprint, render_template, redirect, url_for, request, session, Response

from models.cards import text_cards, data_cards
# Set up the blueprint for the account and its subpages.
from models.employee import Employee

account = Blueprint('account', __name__, static_folder='static', template_folder='templates/account')


@account.route('/login', methods=['POST', 'GET'])
def login() -> Response | str:
    """
    Main login page for the project.

    :return: Returns either the rendering of the template for 'login.html' if the user does not already have a session,
             else returns a redirect to the dashboard page.
    :rtype: Response | str
    """
    login_message = ''

    if request.method == 'POST':
        email_address = request.form['email_address']
        password = request.form['password']

        if Employee.match_password(email_address, password):
            session.permanent = True
            session['email_address'] = email_address

            return redirect(url_for('account.dashboard'))

        else:
            login_message = 'Invalid email or password!'

    if 'email_address' in session:
        return redirect(url_for('account.dashboard'))

    return render_template('account/login.html', login_message=login_message)


@account.route('/logout')
def logout() -> Response:
    """
    Logout pseudo-page to delete session data and redirect back to the login page.

    :return: Redirect to the login page.
    :rtype: Response
    """
    if 'email_address' in session:
        session.pop('email_address', None)
        return redirect(url_for('account.login'))

    return redirect(url_for('account.dashboard'))


@account.route('/dashboard')
def dashboard() -> Response | str:
    """
    Dashboard page where major / important information is displayed as cards. The cards can be clicked to redirect to a
    detailed information page.

    :return: If the user is logged in, rendering of the template for 'dashboard.html' else, a redirect to the login
             page.
    :rtype: Response | str
    """
    if 'email_address' in session:
        return render_template('account/dashboard/dashboard.html', text_cards=text_cards, data_cards=data_cards)

    return redirect(url_for('account.login'))


@account.route('/profile')
def profile() -> Response | str:
    if 'email_address' in session:
        current_employee = Employee.get_by_email_address(session['email_address'])
        return render_template('account/dashboard/profile.html', employee=current_employee)

    return redirect(url_for('account.login'))


@account.route('/warehouse')
def warehouse() -> Response | str:
    if 'email_address' in session:
        return render_template('account/dashboard/warehouse.html')

    return redirect(url_for('account.login'))
