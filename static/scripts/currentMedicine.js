/**
 * Script to get the current medicine selected in the form.
 * */

/**
 * Get the currently selected medicine from its ID by matching against all medicines in the database.
 *
 * @param medicineData Data of all medicines in the database as JavaScript objects.
 * @return {*} Current medicine being selected.
 */
function getCurrentMedicine(medicineData) {
    const selectedID = parseInt(document.getElementById('medicine-id').value);

    for (let medicine of medicineData) {
        if (medicine.id === selectedID) {
            return medicine
        }
    }
}
