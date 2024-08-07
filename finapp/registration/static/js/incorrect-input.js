document.addEventListener('DOMContentLoaded', function() {
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const emailError = document.getElementById('email-error');
    const passwordError = document.getElementById('password-error');

    // Функция для проверки формы
    function validateForm() {
        let isValid = true;

        // Проверка Email
        const emailValue = emailInput.value.trim();
        emailError.style.display = 'none'; // Скрываем сообщение
        if (!emailValue) {
            emailError.textContent = 'Введите E-mail.';
            emailError.style.display = 'block';
            isValid = false;
        } else if (!/\S+@\S+\.\S+/.test(emailValue)) {
            emailError.textContent = 'Введите корректный E-mail.';
            emailError.style.display = 'block';
            isValid = false;
        }

        // Проверка пароля
        const passwordValue = passwordInput.value.trim();
        passwordError.innerHTML = ''; // Сбрасываем сообщения об ошибках
        let passwordErrors = [];

        if (!passwordValue) {
            passwordErrors.push('Введите пароль.');
            isValid = false;
        } else {
            // Проверка длины пароля
            if (passwordValue.length < 8) {
                passwordErrors.push('Пароль должен содержать минимум 8 символов.');
            }
            // Проверка наличия заглавной буквы
            if (!/[A-Z]/.test(passwordValue)) {
                passwordErrors.push('Пароль должен содержать хотя бы одну заглавную букву.');
            }
            // Проверка наличия строчной буквы
            if (!/[a-z]/.test(passwordValue)) {
                passwordErrors.push('Пароль должен содержать хотя бы одну строчную букву.');
            }
            // Проверка наличия цифры
            if (!/\d/.test(passwordValue)) {
                passwordErrors.push('Пароль должен содержать хотя бы одну цифру.');
            }
            // Проверка наличия специального символа
            if (!/[\W_]/.test(passwordValue)) {
                passwordErrors.push('Пароль должен содержать хотя бы один специальный символ (например, !@#$%^&*).');
            }
            // Проверка на пробелы
            if (/\s/.test(passwordValue)) {
                passwordErrors.push('Пароль не должен содержать пробелов.');
            }
        }

        // Выводим ошибки пароля
        if (passwordErrors.length > 0) {
            passwordError.innerHTML = passwordErrors.join('<br>');
            passwordError.style.display = 'block';
        }

        return isValid; // Возвращаем результат проверки
    }

    // Добавляем событие на наведение
    emailInput.addEventListener('focus', validateForm);
    passwordInput.addEventListener('focus', validateForm);

    // Дополнительно, можно сделать валидацию при отправке формы
    document.querySelector('form').addEventListener('submit', function(event) {
        if (!validateForm()) {
            event.preventDefault(); // Отменяем отправку формы если есть ошибки
        }
    });
});
