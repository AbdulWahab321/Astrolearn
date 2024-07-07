document.addEventListener('DOMContentLoaded', function() {
    const quizForm = document.getElementById('quiz-form');
    const resultsDiv = document.getElementById('results');

    if (quizForm) {
        quizForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(quizForm);
            
            fetch(quizForm.action, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                resultsDiv.innerHTML = `You scored ${data.score} out of ${data.total}!`;
                resultsDiv.style.display = 'block';
            })
            .catch(error => {
                console.error('Error:', error);
                resultsDiv.innerHTML = 'An error occurred while submitting the quiz.';
                resultsDiv.style.display = 'block';
            });
        });
    }
});