 document.addEventListener('DOMContentLoaded', function() {
    var tooltips = document.querySelectorAll('.tooltip-info');

    tooltips.forEach(function(tooltip) {
        var tariff = tooltip.closest('.tariff');
        var tariffsSwitch = tariff.querySelector('.tariffs-switch');
        var allTariffLists = document.querySelectorAll('.tariff-lists');

        tooltip.addEventListener('mouseover', function() {
            // Делаем tariffs-switch видимым для получения высоты
            tariffsSwitch.style.visibility = 'hidden';
            tariffsSwitch.style.display = 'block';
            var switchHeight = tariffsSwitch.offsetHeight + 35;
            tariffsSwitch.style.display = 'none';
            tariffsSwitch.style.visibility = '';

            // Показать tariffs-switch
            tariffsSwitch.style.display = 'block';

            // Устанавливаем margin-top для всех остальных .tariff-lists
            allTariffLists.forEach(function(list) {
                if (list !== tariff.querySelector('.tariff-lists')) {
                    list.style.marginTop = switchHeight + 'px';

                }
            });
        });

        tooltip.addEventListener('mouseout', function() {
            // Скрыть tariffs-switch
            tariffsSwitch.style.display = 'none';

            // Возвращаем margin-top ко всем .tariff-lists
            allTariffLists.forEach(function(list) {
                list.style.marginTop = '';
            });
        });
    });
});