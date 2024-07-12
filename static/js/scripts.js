// Mobile menu toggle
document.getElementById('mobile-menu-button').addEventListener('click', function() {
    document.getElementById('mobile-menu').classList.toggle('hidden');
});

// Flashcard functionality
document.addEventListener("DOMContentLoaded", function () {
    const flashcardContainer = document.getElementById('flashcard-container');
    const flashcard = document.getElementById('flashcard');
    const question = document.getElementById('question');
    const answer = document.getElementById('answer');
    const flipBtn = document.getElementById('flip-btn');
    const nextBtn = document.getElementById('next-btn');

    // Example flashcards (replace with actual data)
    const flashcards = [
        { question: "What is the capital of France?", answer: "Paris" },
        { question: "What is 2 + 2?", answer: "4" },
        // Add more flashcards here
    ];

    let currentCard = 0;

    function showCard() {
        question.textContent = flashcards[currentCard].question;
        answer.textContent = flashcards[currentCard].answer;
        answer.classList.add('hidden');
        flashcardContainer.classList.remove('hidden');
        
        anime({
            targets: flashcard,
            scale: [0.9, 1],
            opacity: [0, 1],
            easing: 'easeOutElastic(1, .8)',
            duration: 600
        });
    }

    flipBtn.addEventListener('click', () => {
        flashcard.style.transform = 'rotateY(180deg)';
        setTimeout(() => {
            question.classList.toggle('hidden');
            answer.classList.toggle('hidden');
            flashcard.style.transform = 'rotateY(0deg)';
        }, 150);
    });

    nextBtn.addEventListener('click', () => {
        currentCard = (currentCard + 1) % flashcards.length;
        showCard();
    });

    showCard();
});

// Add smooth scrolling to all links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Animate elements on scroll
const animateOnScroll = () => {
    const elements = document.querySelectorAll('.animate-on-scroll');
    elements.forEach(element => {
        if (isElementInViewport(element)) {
            element.classList.add('animate__animated', 'animate__fadeInUp');
        }
    });
};

const isElementInViewport = (el) => {
    const rect = el.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
};

window.addEventListener('scroll', animateOnScroll);
window.addEventListener('resize', animateOnScroll);
window.addEventListener('load', animateOnScroll);