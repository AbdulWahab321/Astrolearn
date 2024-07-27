<<<<<<< HEAD
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
    window.dispatchEvent(new Event('themeChanged'));
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


document.addEventListener('DOMContentLoaded', (event) => {
    const developmentBox = document.getElementById('developmentBox');
    const closeBtn = document.getElementById('closeBtn');
    // Check if the development box has been closed before
    if (localStorage.getItem('developmentBoxClosed') === 'true') {
        developmentBox.style.display = 'none';
    }
    
    closeBtn.addEventListener('click', () => {
        developmentBox.style.display = 'none';
        localStorage.setItem('developmentBoxClosed', 'true');
    });
    update_images(theme)
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
=======
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
    window.dispatchEvent(new Event('themeChanged'));
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


document.addEventListener('DOMContentLoaded', (event) => {
    const developmentBox = document.getElementById('developmentBox');
    const closeBtn = document.getElementById('closeBtn');
    // Check if the development box has been closed before
    if (localStorage.getItem('developmentBoxClosed') === 'true') {
        developmentBox.style.display = 'none';
    }
    
    closeBtn.addEventListener('click', () => {
        developmentBox.style.display = 'none';
        localStorage.setItem('developmentBoxClosed', 'true');
    });
    update_images(theme)
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
>>>>>>> 77990087da15310786318a82e2d150ed2cfa2a62
window.addEventListener('load', animateOnScroll);