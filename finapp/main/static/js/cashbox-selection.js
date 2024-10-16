document.addEventListener('DOMContentLoaded', function() {
    const selectedCashboxes = new Set();  // Массив для хранения выбранных cashbox-ов

    // Функция для выбора/отмены выбора cashbox-а
    document.querySelectorAll('.selectable-cashbox').forEach(item => {
        item.addEventListener('click', function() {
            const cashboxId = this.getAttribute('data-id');

            // Проверка наличия класса для показа предупреждения
            if (this.classList.contains('already-have')) {
                // Показываем окно подтверждения
                const confirmSelection = confirm("Вы уверены, что хотите выбрать этот элемент? Удаление выбранного кэшбокса приведёт к критическим изменениям бюджета!");

                if (!confirmSelection) {
                    alert("Вы отменили свой выбор.");
                    return;  // Если пользователь отменяет выбор, выходим
                }
            }

            // Если выбор подтвержден или элемент не имеет класса 'already-have'
            if (selectedCashboxes.has(cashboxId)) {
                selectedCashboxes.delete(cashboxId);
                this.style.borderColor = 'transparent';
            } else {
                selectedCashboxes.add(cashboxId);
                this.style.borderColor = '#000';  // Пример стиля для выбранного элемента
            }
        });
    });

    // Обработчик для кнопки "Зафиксировать"
    document.getElementById('confirm-selection').addEventListener('click', function() {
        if (selectedCashboxes.size === 0) {
            alert('Выберите хотя бы один элемент');
            return;
        }

        // AJAX-запрос для отправки данных на сервер
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const formData = new FormData();
        formData.append('selected_cashboxes', Array.from(selectedCashboxes).join(','));  // Преобразуем Set в строку

        fetch(saveSelectedCashboxesUrl, {  // Используем переменную
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Выбор сохранен!');
                // Дополнительные действия, например, перезагрузка страницы или обновление UI
            } else {
                alert('Ошибка при сохранении!');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Ошибка при сохранении!');
        });
    });
});
