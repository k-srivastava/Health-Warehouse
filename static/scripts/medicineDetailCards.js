/**
 * Script to toggle the visibility of medicine warning and information cards.
 * */

/**
 * Toggle the visibility of the medicine warning card.
 *
 * @param warningCard Medicine warning card.
 * @param infoCard Medicine information card.
 */
function showWarningCard(warningCard, infoCard) {
    infoCard.style.visibility = 'hidden';
    warningCard.style.visibility = warningCard.style.visibility === 'hidden' ? 'visible' : 'hidden';
}

/**
 * Toggle the visibility of the medicine information card,
 *
 * @param infoCard Medicine information card.
 * @param warningCard Medicine warning card.
 */
function showInfoCard(infoCard, warningCard) {
    warningCard.style.visibility = 'hidden';
    infoCard.style.visibility = infoCard.style.visibility === 'hidden' ? 'visible' : 'hidden';
}
