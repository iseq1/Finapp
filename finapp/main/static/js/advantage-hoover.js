document.querySelectorAll('.advantages-items li').forEach(item => {
    item.addEventListener('mouseover', () => {
        const iconDefault = item.querySelector('.advantage-icon-default');
        const iconActive = item.querySelector('.advantage-icon-active');

        if (iconDefault && iconActive) {
            iconDefault.classList.add('advantage-icon-active');
            iconDefault.classList.remove('advantage-icon-default');
            iconActive.classList.add('advantage-icon-default');
            iconActive.classList.remove('advantage-icon-active');
        }
    });

    item.addEventListener('mouseout', () => {
        const iconDefault = item.querySelector('.advantage-icon-active');
        const iconActive = item.querySelector('.advantage-icon-default');

        if (iconDefault && iconActive) {
            iconDefault.classList.add('advantage-icon-default');
            iconDefault.classList.remove('advantage-icon-active');
            iconActive.classList.add('advantage-icon-active');
            iconActive.classList.remove('advantage-icon-default');
        }
    });
});
