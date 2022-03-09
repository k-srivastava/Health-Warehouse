function showWarningCard(warningCard, infoCard) {
    infoCard.style.visibility = 'hidden';
    warningCard.style.visibility = warningCard.style.visibility === 'hidden' ? 'visible' : 'hidden';
}

function showInfoCard(infoCard, warningCard) {
    warningCard.style.visibility = 'hidden';
    infoCard.style.visibility = infoCard.style.visibility === 'hidden' ? 'visible' : 'hidden';
}
