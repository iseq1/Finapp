document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('.editable-input');

    inputs.forEach(input => {
        input.addEventListener('input', function() {
            // Удаляем все, что не соответствует формату, в том числе '-'
            this.value = this.value.replace(/[^0-9.,\-\/]/g, '');

            // Проверка на формат: -x/x.xx/-x,xx/-x/x,x
            const validFormat = /^-?\d+([.,]\d{1,2})?((\/-?\d+([.,]\d{1,2})?)*)?$/;

            // Если значение не соответствует формату, убираем последний символ
            if (!validFormat.test(this.value) && this.value !== '') {
                // Сохраняем текущее значение
                let lastChar = this.value.slice(-1);

                // Если последний символ - не число, запятая, точка или минус, убираем его
                if (!/[0-9.,-]/.test(lastChar)) {
                    this.value = this.value.slice(0, -1);
                }
            }
        });
    });
});
