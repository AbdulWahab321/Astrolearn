// Mobile menu toggle
document.getElementById('mobile-menu-button').addEventListener('click', function() {
    document.getElementById('mobile-menu').classList.toggle('hidden');
});

// Dark mode toggle
function toggleDarkMode() {
    document.documentElement.classList.toggle('dark');
    let current_theme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
    update_images(current_theme);  // Update the images based on the new theme preference
    localStorage.setItem('theme', current_theme);
}
function update_images(current_theme){
    if (current_theme === "light") {
        let img_tags = document.getElementsByTagName("img");
        Array.prototype.forEach.call(img_tags, (img) => {
            let current_src = img.src;
            if (!current_src.endsWith("_light.svg")) {
                let light_src = current_src.replace(".svg", "_light.svg");
                img.src = light_src;
            } else if (current_src.endsWith("_light.svg")) {
                // Already a light image, do nothing
            } else {
                // Handle other cases if necessary
            }
        });
    } else {
        let img_tags = document.getElementsByTagName("img");
        Array.prototype.forEach.call(img_tags, (img) => {
            let current_src = img.src;
            if (current_src.endsWith("_light.svg")) {
                let original_src = current_src.replace("_light.svg", ".svg");
                img.src = original_src;
            } else if (current_src.endsWith(".svg")) {
                // Already a dark image, do nothing
            } else {
                // Handle other cases if necessary
            }
        });
    }
}
document.getElementById('dark-mode-toggle').addEventListener('click', toggleDarkMode);
document.getElementById('mobile-dark-mode-toggle').addEventListener('click', toggleDarkMode);

// Check for saved theme preference or use device preference
const theme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');

// Apply the saved theme on page load
if (theme === 'dark') {
    document.documentElement.classList.add('dark');
}

// The rest of your JavaScript code remains the same
// Flashcard functionality
document.addEventListener("DOMContentLoaded", function () {
    const flashcardContainer = document.getElementById('flashcard-container');
    if (flashcardContainer) {
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
        }

        flipBtn.addEventListener('click', () => {
            question.classList.toggle('hidden');
            answer.classList.toggle('hidden');
        });

        nextBtn.addEventListener('click', () => {
            currentCard = (currentCard + 1) % flashcards.length;
            showCard();
        });
        update_images(theme);
        showCard();
    }
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