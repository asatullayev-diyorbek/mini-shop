document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.rating-stars i');
    const ratingInput = document.getElementById('rating');

    stars.forEach(star => {
        // Yulduzchaga bosish
        star.addEventListener('click', function() {
            const ratingValue = this.getAttribute('data-value');
            ratingInput.value = ratingValue;
            updateStars(ratingValue);
        });

        // Hover qilganda yulduzchalarni yangilash
        star.addEventListener('mouseover', function() {
            const hoverValue = this.getAttribute('data-value');
            updateStars(hoverValue);
        });

        // Hoverdan keyin avvalgi bahoga qaytish
        star.addEventListener('mouseout', function() {
            updateStars(ratingInput.value);
        });
    });

    // Yulduzchalarni yangilash
    function updateStars(value) {
        stars.forEach(star => {
            if (star.getAttribute('data-value') <= value) {
                star.classList.add('fa');
                star.classList.remove('far');
            } else {
                star.classList.remove('fa');
                star.classList.add('far');
            }
        });
    }
});
