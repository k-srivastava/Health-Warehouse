Blueprints
==========

Account
-------

.. py:data:: File Description

    File to manage the account page and its respective subpages. These pages contain general information about the store
    and help manage sales, profits, stock and other items.

.. py:function:: account.login() -> Response | str

    Main login page for the project.

    :return: If the user is logged in, rendering of the template for 'login.html' else, a redirect to the login
             page.
    :rtype: Response | str

.. py:function:: account.logout() -> Response

    Logout pseudo-page to delete session data and redirect back to the login page.

    :return: Redirect to the login page.
    :rtype: Response

.. py:function:: account.dashboard() -> Response | str

    Dashboard page where major / important information is displayed as cards.

    :return: If the user is logged in, rendering of the template for 'dashboard.html' else, a redirect to the login
             page.
    :rtype: Response | str

.. py:function:: account.profile() -> Response | str

    Profile page where employee information is displayed.

    :return: If the user is logged in, rendering of the template for 'profile.html' else, a redirect to the login
             page.
    :rtype: Response | str

.. py:function:: account.warehouse() -> Response | str

    Warehouse page where data related to medicines stored, their stock and sales made is shown as tables.

    :return: If the user is logged in, rendering of the template for 'warehouse.html' else, a redirect to the login
             page.
    :rtype: Response | str

.. py:function:: account.warehouse_add_medicine() -> Response | str

    Add medicine page where new medicines for the database can be added using a form.

    :return: If the user is logged in, rendering of the template for 'add_medicine.html' else, a redirect to the login
             page.
    :rtype: Response | str

.. py:function:: account.warehouse_update_stock() -> Response | str

    Update stock page where stock of existing medicines can be updated using a form.

    :return: If the user is logged in, rendering of the template for 'update_stock.html' else, a redirect to the login
             page.
    :rtype: Response | str

.. py:function:: account.warehouse_new_sale() -> Response | str

    New sale page where new sales can be logged using a form.

    :return: If the user is logged in, rendering of the template for 'new_sale.html' else, a redirect to the login
             page.
    :rtype: Response | str

.. py:function:: account.warehouse_medicine_list() -> Response | str

    Custom list view for each medicine in the database.

    :return: If the user is logged in, rendering of the template for 'medicine_list.html' else, a redirect to the login
             page.
    :rtype: Response | str

.. py:function:: account.warehouse_medicine(medicine_id: int) -> Response | str

    Custom page view for each medicine in the database with corresponding actions.

    :param medicine_id: Medicine ID to identify the medicine; primary key.
    :type medicine_id: int
    :return: If the user is logged in, rendering of the template for 'medicine_detail.html' else, a redirect to the
             login page.
    :rtype: Response | str

.. py:function:: account.warehouse_medicine_delete(medicine_id: int) -> Response | str

    Pseudo-page to delete a specific medicine from the database. Immediately redirects to the main warehouse page.

    :param medicine_id: Medicine ID to identify the medicine; primary key.
    :type medicine_id: int
    :return: If the user is logged in, rendering of the template for 'medicine_delete.html' else, a redirect to the
             login page.
    :rtype: Response | str
