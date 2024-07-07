// quiz.js

document.addEventListener('DOMContentLoaded', function() {
    const quizForm = document.getElementById('quiz-form');
    const resultsDiv = document.getElementById('results');

    if (quizForm && typeof quizData !== 'undefined') {
        quizForm.addEventListener('submit', function(e) {
            e.preventDefault();
            let score = 0;
            quizData.forEach((q, i) => {
                const selected = document.querySelector(`input[name="q${i}"]:checked`);
                if (selected && selected.value === q.correct_answer) {
                    score++;
                }
            });
            resultsDiv.innerHTML = `You scored ${score} out of ${quizData.length}`;
        });
    }
});