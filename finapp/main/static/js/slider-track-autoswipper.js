let count = 0;
let direction = 'next';

function clickButton() {
    const btnPrev = document.querySelector('.btn-prev');
    const btnNext = document.querySelector('.btn-next');

    if (direction === 'next') {
        if (count < 3) {
            btnNext.click();
            count++;
        } else {
            direction = 'prev';
            count = 0;
        }
    } else {
        if (count < 3) {
            btnPrev.click();
            count++;
        } else {
            direction = 'next';
            count = 0;
        }
    }
}

setInterval(clickButton, 7000);