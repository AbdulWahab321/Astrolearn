document.addEventListener('DOMContentLoaded', function() {
    const quizForm = document.getElementById('quiz-form');
    const resultsDiv = document.getElementById('results');

    if (quizForm) {
        quizForm.addEventListener('submit', function(e) {
            e.preventDefault();

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
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                resultsDiv.innerHTML = `You scored ${data.score} out of ${data.total}`;
            })
            .catch(error => {
                console.error('Error:', error);
                resultsDiv.innerHTML = 'An error occurred while submitting the quiz. Please try again.';
            });
        });
    }
});
