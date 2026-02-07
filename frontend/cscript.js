const response = await fetch("/people?my_name=YOUR_USERNAME");
const card = document.getElementById('active-card');
const connectBtn = document.getElementById('connect-btn');
const skipBtn = document.getElementById('skip-btn');

connectBtn.addEventListener('click', () => {
    card.style.transform = 'translateX(100%) rotate(30deg)';
    card.style.opacity = '0';
    setTimeout(() => {
        card.style.transform = 'translateX(0) rotate(0)';
        card.style.transition = none;

        document.getElementById('display-name').innerText = "Loading..";

        card.style.transition = 'transform 0.4s ease, opacity 0.4s ease';
        card.style.opacity = '1';

    }, 400);
});

skipBtn.addEventListener('click', () => {
    card.style.transform = 'translateX(-100%) rotate(-30deg)';
    card.style.opacity = '0';

    setTimeout(() => {
        card.style.transition = 'none';
        card.style.transform = 'translateX(0) rotate(0)';
        document.getElementById('display-name').innerText = "Loading...";

        setTimeout(() => {
            card.style.transition = 'transform 0.4s ease, opacity 0.4s ease';
            card.style.opacity = '1';
        }, 10);
    }, 400);
});