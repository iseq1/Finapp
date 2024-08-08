document.addEventListener('DOMContentLoaded', function() {
    const firstNameInput = document.getElementById('first-name');
    const lastNameInput = document.getElementById('last-name');
    const dateOfBirthInput = document.getElementById('date-of-birth');
    const phoneNumberInput = document.getElementById('phone-number');
    const addressInput = document.getElementById('address');

    const firstNameError = document.getElementById('first-name-error');
    const lastNameError = document.getElementById('last-name-error');
    const dateOfBirthError = document.getElementById('date-of-birth-error');
    const phoneNumberError = document.getElementById('phone-number-error');
    const addressError = document.getElementById('address-error');

    // Скрываем сообщения об ошибках при загрузке страницы
    firstNameError.style.display = 'none';
    lastNameError.style.display = 'none';
    dateOfBirthError.style.display = 'none';
    phoneNumberError.style.display = 'none';
    addressError.style.display = 'none';

    // Функция для проверки формы
    function validateForm() {
        let isValid = true;

        // Проверка имени
        firstNameError.style.display = 'none';
        const namePattern = /^[A-Za-zА-Яа-яЁё\s]+$/; // Разрешаем только буквы и пробелы
        if (!firstNameInput.value.trim() || !namePattern.test(firstNameInput.value.trim())) {
            firstNameError.textContent = '· Пожалуйста, введите корректное имя.';
            firstNameError.style.display = 'block';
            isValid = false;
        }

        // Проверка фамилии
        lastNameError.style.display = 'none';
        if (!lastNameInput.value.trim() || !namePattern.test(lastNameInput.value.trim())) {
            lastNameError.textContent = '· Пожалуйста, введите корректную фамилию.';
            lastNameError.style.display = 'block';
            isValid = false;
        }

       // Проверка даты рождения
        dateOfBirthError.style.display = 'none';
        const currentYear = new Date().getFullYear();
        const minYear = currentYear - 100;
        const dateOfBirth = new Date(dateOfBirthInput.value);
        if (!dateOfBirthInput.value ||
            dateOfBirth.getFullYear() < minYear ||
            dateOfBirth.getFullYear() > currentYear ||
            isNaN(dateOfBirth.getTime())) {
            dateOfBirthError.textContent = '· Пожалуйста, введите корректную дату рождения.';
            dateOfBirthError.style.display = 'block';
            isValid = false;
        }

        // Проверка номера телефона
        phoneNumberError.style.display = 'none';
        const phoneValue = phoneNumberInput.value.trim();

        // Узнаем длину телефона без "+" и пробелов
        const digitCount = phoneValue.replace('+', '').length;
        const phonePattern = /^\+?[0-9]+$/; // Разрешаем только цифры и, возможно, "+"

        // Проверка по условиям
        if (!phoneValue ||
            !phonePattern.test(phoneValue) ||
            (phoneValue.startsWith('+') && digitCount !== 12) || // с "+" (12 символов)
            (!phoneValue.startsWith('+') && digitCount !== 11)) { // другие случаи
            phoneNumberError.textContent = '· Пожалуйста, введите корректный номер телефона.';
            phoneNumberError.style.display = 'block';
            isValid = false;
        }

        // Проверка адреса
        addressError.style.display = 'none';
        if (!addressInput.value.trim()) {
            addressError.textContent = '· Пожалуйста, введите ваш адрес.';
            addressError.style.display = 'block';
            isValid = false;
        }

        return isValid; // Возвращаем результат проверки
    }

    // Обработка отправки формы
    document.querySelector('form').addEventListener('submit', function(event) {
        if (!validateForm()) {
            event.preventDefault(); // Отменяем отправку формы, если есть ошибки
        }
    });

    // Применение валидации на ввод
    firstNameInput.addEventListener('input', validateForm);
    lastNameInput.addEventListener('input', validateForm);
    dateOfBirthInput.addEventListener('input', validateForm);
    phoneNumberInput.addEventListener('input', validateForm);
    addressInput.addEventListener('input', validateForm);
});
