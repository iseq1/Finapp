document.addEventListener('DOMContentLoaded', () => {
        // Находим все вкладки и содержимое вкладок
        const tabs = document.querySelectorAll('.tabs .tab');
        const contents = document.querySelectorAll('.tabs-content');

        // Функция для обновления активного состояния
        function updateActiveTab(targetId) {
            // Удаляем класс is-active у всех вкладок
            tabs.forEach(tab => tab.classList.remove('is-active'));

            // Удаляем класс is-active у всех содержимых вкладок
            contents.forEach(content => content.classList.remove('is-active'));

            // Находим и добавляем класс is-active к выбранной вкладке
            const activeTab = document.querySelector(`.tabs .tab[data-id="${targetId}"]`);
            if (activeTab) {
                activeTab.classList.add('is-active');
            }

            // Находим и добавляем класс is-active к соответствующему содержимому вкладки
            const activeContent = document.getElementById(targetId);
            if (activeContent) {
                activeContent.classList.add('is-active');
            }
        }

        // Добавляем обработчик кликов для всех вкладок
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const targetId = tab.getAttribute('data-id');
                updateActiveTab(targetId);
            });
        });

        // Изначально показываем активный контент на основе начального состояния
        const initialTab = document.querySelector('.tabs .tab.is-active');
        if (initialTab) {
            const initialId = initialTab.getAttribute('data-id');
            updateActiveTab(initialId);
        }
    });