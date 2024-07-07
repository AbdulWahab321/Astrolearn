document.addEventListener('DOMContentLoaded', function () {
    // Theme Toggle
    const themeToggle = document.querySelector('.theme-toggle');
    const body = document.body;
    const currentTheme = localStorage.getItem('theme');

    if (currentTheme) {
        body.classList.add(currentTheme);
    }

    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark');
        if (body.classList.contains('dark')) {
            localStorage.setItem('theme', 'dark');
        } else {
            localStorage.removeItem('theme');
        }
    });

    // Quiz Logic
    const quizForm = document.querySelector('#quiz-form');
    if (quizForm) {
        quizForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(quizForm);
            const answers = {};
            formData.forEach((value, key) => {
                answers[key] = value;
            });
            fetch(quizForm.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(answers)
            })
            .then(response => response.json())
            .then(result => {
                const resultsContainer = document.querySelector('#results');
                resultsContainer.innerHTML = `You got ${result.correct} out of ${result.total} correct!`;
            });
        });
    }
});
