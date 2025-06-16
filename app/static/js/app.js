function updateAppSize(size = 16) {
    document.documentElement.style.setProperty('--bs-body-font-size', size + 'px');
}

function updateAppTheme(theme = 'light') {
    document.documentElement.dataset.bsTheme = theme;
}

updateAppSize(localStorage.getItem('size'));
updateAppTheme(localStorage.getItem('theme'));