JavaScript
==========

Current Medicine
----------------

.. js:data:: File Description

    Script to get the current medicine selected in the form.

.. js:function:: currentMedicine.getCurrentMedicine(medicineData)

    Get the currently selected medicine from its ID by matching against all medicines in the database.

    :param medicineData: Data of all medicines in the database as a JavaScript object.
    :return: Current medicine being selected.

.. js:function:: currentMedicine.getValidMedicines(medicineData)

    Get the matching medicine from the search bar by checking it against all medicine names in the database.

    :param medicineData: Data of all medicines in the database as a JavaScript object.
    :return: Array of all matching medicines.

.. js:function:: currentMedicine.getMatchingResult(medicineData, validMedicineList)

    Create a new HTML list element with the medicine details that match the query in the search box and add that list
    element to an unordered list on the page.

    :param medicineData: Data of all medicines in the database as a JavaScript object.
    :param validMedicineList: Unordered HTML list to which medicines are appended as list elements.

Dashboard Percent To CSS
------------------------

.. js:data:: File Description

    Script to change the percentage graph of the card by reading the HTML h3 tag value.

Image Picker
------------

.. js:data:: File Description

    Script to change the main image when the thumbnail images are selected.

.. js:function:: imagePicker.thumbnailPicker(image)

    Function to change the main display image when the smaller thumbnail images are selected.

    :param image: Thumbnail image being selected.

Medicine Detail Cards
---------------------

.. js:data:: File Description

    Script to toggle the visibility of medicine warning and information cards.

.. js:function:: medicineDetailCards.showWarningCard(warningCard, infoCard)

    Toggle the visibility of the medicine warning card.

    :param warningCard: Medicine warning card.
    :param infoCard: Medicine information card.

.. js:function:: medicineDetailCards.showInfoCard(infoCard, warningCard)

    Toggle the visibility of the medicine information card.

    :param infoCard: Medicine information card.
    :param warningCard: Medicine warning card.

Toggle Theme
------------

.. js:data:: File Description

    Script to toggle the website theme between light and dark mode.

.. js:function:: toggleTheme.toggleTheme()

    Function to toggle the website theme.
