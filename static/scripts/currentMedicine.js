/**
 * Script to get the current medicine selected in the form.
 * */

/**
 * Get the currently selected medicine from its ID by matching against all medicines in the database.
 *
 * @param medicineData Data of all medicines in the database a JavaScript object.
 * @return {*} Current medicine being selected.
 */
function getCurrentMedicine(medicineData) {
    const selectedName = document.getElementById('medicine-name').value;

    for (let medicine of medicineData) {
        if (medicine.name === selectedName) {
            return medicine
        }
    }
}

/**
 * Get the matching medicine from the search bar by checking it against all medicine names in the database.
 *
 * @param medicineData Data of all medicines in the database as a JavaScript object.
 * @return {*[]} Array of all matching medicines.
 */
function getValidMedicines(medicineData) {
    const medicineName = document.getElementById('search-bar').value.toLowerCase();
    const validMedicines = [];

    // Show the first five medicines if search bar is empty.
    if (medicineName === '') {
        return medicineData.slice(0, 5);
    }

    for (let medicine of medicineData) {
        if (medicine.name.toLowerCase().includes(medicineName)) {
            validMedicines.push(medicine);
        }
    }

    return validMedicines.slice(0, 6);
}
