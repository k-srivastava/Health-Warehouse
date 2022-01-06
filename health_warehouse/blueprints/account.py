"""
File to manage the account page and its respective subpages. These pages contain general information about the store
and help manage sales, profits, stock and other items.
"""
from flask import Blueprint, render_template, redirect, url_for, request, session, Response

from models.cards import text_cards, data_cards
from models.employee import Employee
from models.medicine import Medicine
from models.sale import Sale

# Set up the blueprint for the account and its subpages.
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
    Dashboard page where major / important information is displayed as cards.

    :return: If the user is logged in, rendering of the template for 'dashboard.html' else, a redirect to the login
             page.
    :rtype: Response | str
    """
    if 'email_address' in session:
        return render_template('account/dashboard/dashboard.html', text_cards=text_cards, data_cards=data_cards)

    return redirect(url_for('account.login'))


@account.route('/profile')
def profile() -> Response | str:
    """
    Profile page where employee information is displayed.

    :return: If the user is logged in, rendering of the template for 'dashboard.html' else, a redirect to the login
             page.
    :rtype: Response | str
    """
    if 'email_address' in session:
        current_employee = Employee.get_by_email_address(session['email_address'])
        return render_template('account/dashboard/profile.html', employee=current_employee)

    return redirect(url_for('account.login'))


@account.route('/warehouse')
def warehouse() -> Response | str:
    """
    Warehouse page where data related to medicines stored, their stock and sales made is shown as tables.

    :return: If the user is logged in, rendering of the template for 'dashboard.html' else, a redirect to the login
             page.
    :rtype: Response | str
    """
    if 'email_address' in session:
        return render_template('account/dashboard/warehouse/warehouse.html', medicines=Medicine.get_all(),
                               sales=Sale.get_all()[-10:])

    return redirect(url_for('account.login'))


@account.route('/warehouse/add-medicine', methods=['POST', 'GET'])
def warehouse_add_medicine() -> Response | str:
    """
    Add medicine page where new medicines for the database can be added using a form.

    :return: If the user is logged in, rendering of the template for 'dashboard.html' else, a redirect to the login
             page.
    :rtype: Response | str
    """
    if 'email_address' in session:
        return render_template('account/dashboard/warehouse/add_medicine.html', new_id=Medicine.generate_random_id())

    return redirect(url_for('account.login'))


@account.route('/warehouse/update-stock', methods=['POST', 'GET'])
def warehouse_update_stock() -> Response | str:
    """
    Update stock page where stock of existing medicines can be updated using a form.

    :return: If the user is logged in, rendering of the template for 'dashboard.html' else, a redirect to the login
             page.
    :rtype: Response | str
    """
    if 'email_address' in session:
        return render_template('account/dashboard/warehouse/update_stock.html')

    return redirect(url_for('account.login'))


@account.route('/warehouse/new-sale', methods=['POST', 'GET'])
def warehouse_new_sale() -> Response | str:
    """
    New sale page where new sales can be logged using a form.

    :return: If the user is logged in, rendering of the template for 'dashboard.html' else, a redirect to the login
             page.
    :rtype: Response | str
    """
    if 'email_address' in session:
        return render_template('account/dashboard/warehouse/new_sale.html')

    return redirect(url_for('account.login'))
