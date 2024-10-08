// Получаем кнопку для смены темы и элемент body
const themeToggleButton = document.getElementById('theme-toggle');
const body = document.body;

// Проверяем сохранённую тему в localStorage и применяем её
if (localStorage.getItem('theme') === 'dark') {
    body.classList.remove('light-theme');
    body.classList.add('dark-theme');
}

// Добавляем обработчик события для кнопки смены темы
themeToggleButton.addEventListener('click', () => {
    body.classList.toggle('dark-theme');
    body.classList.toggle('light-theme');

    // Сохраняем выбранную тему в localStorage
    if (body.classList.contains('dark-theme')) {
        localStorage.setItem('theme', 'dark');
    } else {
        localStorage.setItem('theme', 'light');
    }
});