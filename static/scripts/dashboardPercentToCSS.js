/**
 * Script to change the percentage graph of the card by reading the HTML h3 tag value.
 * */
const h3Tags = document.getElementsByTagName('h3');
const circleTags = document.getElementsByTagName('circle')

for (let i = 0; i < h3Tags.length; i++) {
    const h3Tag = h3Tags[i];
    const circleTag = circleTags[(i * 2) + 1];  // Get every second circle per data card.
    const percentageText = h3Tag.innerText;

    let percentageNum = ""

    for (let j = 0; j < percentageText.indexOf('%'); j++) {
        percentageNum += percentageText[j];
    }

    // Add the CSS style.
    circleTag.style.setProperty('stroke-dashoffset', `calc(440px - (440px * ${percentageNum}) / 100)`)
}
