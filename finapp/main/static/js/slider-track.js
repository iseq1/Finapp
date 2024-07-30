document.addEventListener('DOMContentLoaded', () => {
const slides = document.querySelectorAll('.slick-slide');
const prevButton = document.querySelector('.btn-prev');
const nextButton = document.querySelector('.btn-next');
const track = document.querySelector('.slick-track.slick-track-cards');
const slideWidth = 1180; // ширина одного слайда
const maxSlides = 4; // максимальное количество слайдов
let currentSlide = 0;

function updateSlides() {
    slides.forEach((slide, index) => {
        slide.classList.toggle('slick-current', index === currentSlide);
        slide.classList.toggle('slick-active', index === currentSlide);
        slide.setAttribute('aria-hidden', index !== currentSlide);
    });


    // Обновление состояния кнопок
    const isFirstSlide = currentSlide === 0;
    const isLastSlide = currentSlide >= maxSlides - 1;

    prevButton.setAttribute('aria-disabled', isFirstSlide);
    nextButton.setAttribute('aria-disabled', isLastSlide);

    prevButton.classList.toggle('slick-disabled', isFirstSlide);
    nextButton.classList.toggle('slick-disabled', isLastSlide);


    const translateX = -currentSlide * slideWidth;
    track.style.transform = `translate3d(${translateX}px, 0, 0)`;
}

prevButton.addEventListener('click', () => {
    if (currentSlide > 0) {
        currentSlide--;
        updateSlides();
    }
});

nextButton.addEventListener('click', () => {
    if (currentSlide < slides.length - 1 && currentSlide < maxSlides - 1) {
    currentSlide++;
    updateSlides();
}
});

updateSlides();
});
