"""
File to manage the account page and its respective subpages. These pages contain general information about the store
and help manage sales, profits, stock and other items.
"""
import datetime

from flask import Blueprint, render_template, redirect, url_for, request, session, Response
from werkzeug.datastructures import ImmutableMultiDict

from models.cards import generate_all_text_cards, generate_all_data_cards
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
        return render_template('account/dashboard/dashboard.html', text_cards=generate_all_text_cards(),
                               data_cards=generate_all_data_cards())

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
    if request.method == 'POST':
        form_output: list[int | str | tuple[str, ...]] = list(dict(request.form).values())

        # Convert all the numerical data into int() types.
        for idx, form_item in enumerate(form_output):
            try:
                form_output[idx] = int(form_item)

            except ValueError:
                pass

        # Reformatting output for medicine salts; converting into a tuple.
        form_output[-2] = tuple([salt.strip() for salt in form_output[-2].split(',')])

        new_medicine = Medicine(*form_output)
        new_medicine.add_to_database()

        submission_message = 'Medicine added to database.'

        return render_template(
            'account/dashboard/warehouse/add_medicine.html',
            new_id=Medicine.generate_random_id(), submission_message=submission_message
        )

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
    if request.method == 'POST':
        form_output: ImmutableMultiDict[str, str] = request.form
        Medicine.update_in_database(int(form_output['id']), 'stock', int(form_output['new_stock']))

        submission_message = 'Updated medicine stock.'

        return render_template(
            'account/dashboard/warehouse/update_stock.html',
            all_medicines=Medicine.get_all(), medicines_json=Medicine.get_as_json(),
            submission_message=submission_message
        )

    if 'email_address' in session:
        return render_template(
            'account/dashboard/warehouse/update_stock.html',
            all_medicines=Medicine.get_all(), medicines_json=Medicine.get_as_json()
        )

    return redirect(url_for('account.login'))


@account.route('/warehouse/new-sale', methods=['POST', 'GET'])
def warehouse_new_sale() -> Response | str:
    """
    New sale page where new sales can be logged using a form.

    :return: If the user is logged in, rendering of the template for 'dashboard.html' else, a redirect to the login
             page.
    :rtype: Response | str
    """
    if request.method == 'POST':
        form_output: ImmutableMultiDict[str, str] = request.form

        new_sale = Sale(
            int(form_output['sale-id']), datetime.date.fromisoformat(form_output['sale_date']),
            int(form_output['medicine-id']), int(form_output['quantity'])
        )
        medicine_sold = Medicine.get_by_id(new_sale.medicine_id)

        Medicine.update_in_database(medicine_sold.id, 'stock', medicine_sold.stock - new_sale.quantity)
        new_sale.add_to_database()

    if 'email_address' in session:
        return render_template(
            'account/dashboard/warehouse/new_sale.html',
            new_id=Sale.generate_random_id(),
            all_medicines=Medicine.get_all(),
            medicines_json=Medicine.get_as_json()
        )

    return redirect(url_for('account.login'))


@account.route('/warehouse/medicine-list')
def warehouse_medicine_list() -> Response | str:
    if 'email_address' in session:
        return render_template('account/dashboard/warehouse/medicine_list.html', medicines=Medicine.get_all(),
                               medicines_json=Medicine.get_as_json())

    return redirect(url_for('account.login'))


@account.route('warehouse/medicine/<medicine_id>')
def warehouse_medicine(medicine_id: int) -> Response | str:
    if 'email_address' in session:
        return render_template('account/dashboard/warehouse/medicine_detail.html',
                               medicine=Medicine.get_by_id(medicine_id), today=datetime.date.today())

    return redirect(url_for('account.login'))


@account.route('warehouse/medicine/<medicine_id>/delete')
def warehouse_medicine_delete(medicine_id: int) -> Response | str:
    if 'email_address' in session:
        return render_template('account/dashboard/warehouse/medicine_delete.html',
                               medicine=Medicine.get_by_id(medicine_id))

    return redirect(url_for('account.login'))
