document.getElementById("budget-change-button").addEventListener("click", function(event) {
    event.preventDefault(); // Предотвращает перезагрузку страницы при нажатии на ссылку

    // Переключение для show-fixed и show-nofixed
    let showFixedElements = document.querySelectorAll("#show-fixed");
    let showNoFixedElements = document.querySelectorAll("#show-nofixed");

    showFixedElements.forEach(function(element) {
        element.style.display = "none";
    });

    showNoFixedElements.forEach(function(element) {
        element.style.display = "none";
    });

    // Переключение для write-fixed и write-nofixed
    let writeFixedElements = document.querySelectorAll("#write-fixed");
    let writeNoFixedElements = document.querySelectorAll("#write-nofixed");

    writeFixedElements.forEach(function(element) {
        element.style.display = "table-cell";
    });

    writeNoFixedElements.forEach(function(element) {
        element.style.display = "table-cell";
    });

    // Изменение стиля кнопки "Сохранить изменения"
    document.getElementById("budget-save-changes-button").style.display = "block"; // Изменяем на block, чтобы кнопка появилась
    document.getElementById("budget-change-button").style.display = "none"; // Изменяем на block, чтобы кнопка пропала
    document.getElementById("budget-change-p").style.display = "none"; // Изменяем на none, чтобы фраза пропала
});