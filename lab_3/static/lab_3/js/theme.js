/*const themeToggleButton = document.querySelector('.theme-toggle-button');
const body = document.body;
// Проверяем сохранённую тему в куки и применяем её
if (document.cookie.split('; ').find(row => row.startsWith('theme='))) 
    {
        const savedTheme = document.cookie.split('; ').find(row => row.startsWith('theme=')).split('=')[1];
        if (savedTheme === 'dark') 
        {
                body.classList.remove('light-theme');
                body.classList.add('dark-theme');
        }
    }
// Добавляем обработчик события для кнопки смены темы
themeToggleButton.addEventListener('click', () => 
    {
        // Меняем тему на клиенте
        body.classList.toggle('dark-theme');
        body.classList.toggle('light-theme');
    });*/