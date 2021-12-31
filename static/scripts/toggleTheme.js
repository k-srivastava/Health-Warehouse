const themeMap = {
    dark: 'light',
    light: 'dark'
}

const iconMap = {
    dark: 'moon',
    light: 'sun'
}

const theme = localStorage.getItem('theme') ||
    (temp = Object.keys(themeMap)[0], localStorage.setItem('theme', temp), temp);

const themeButton = document.getElementById('icon-theme')

const bodyClass = document.body.classList;
bodyClass.add(theme);

function toggleTheme() {
    const current = localStorage.getItem('theme');
    const next = themeMap[current];

    bodyClass.replace(current, next);
    localStorage.setItem('theme', next)

    themeButton.innerHTML = `<i class="fa fa-${iconMap[next]}" aria-hidden="true"/>`;
    console.log('Theme toggled!');
}

document.getElementById('icon-theme').onclick = toggleTheme;
document.getElementsByClassName('icon-clickable')[0].onclick = toggleTheme;
