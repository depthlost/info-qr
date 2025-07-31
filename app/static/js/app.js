
function updateAppSize(size) {
    document.documentElement.style.setProperty('--bs-body-font-size', size + 'px');
}

function updateAppTheme(theme) {
    document.documentElement.dataset.bsTheme = theme;
}

size = localStorage.getItem('size')
theme = localStorage.getItem('theme')

if (size == null) {
    size = 16
    localStorage.setItem('size', size)
}

if (theme == null) {
    theme = 'light'
    localStorage.setItem('theme', theme);
}

updateAppSize(size);
updateAppTheme(theme);
