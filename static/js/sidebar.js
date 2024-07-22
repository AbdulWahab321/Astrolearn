$(document).ready(function () {
    $("a").on('click', function (event) {
        if (this.hash !== "") {
            event.preventDefault();

            // Get the target element
            var targetElement = $(this.hash);
            if (targetElement.length) {
                // Get the offset from the top of the document
                var offset = targetElement.offset().top;

                // Get the height of the navbar, if it exists
                var navbarHeight = $("#navbar").outerHeight() || 0;

                // Adjust the scroll position by subtracting the navbar height
                var scrollPosition = offset - navbarHeight - 10;

                // Animate the scroll
                $('html, body').animate({
                    scrollTop: scrollPosition
                }, 800);
            }
        }
    });
});
document.addEventListener('DOMContentLoaded', () => {
    var buttons = document.querySelectorAll(".q_and_a_button");
    buttons.forEach(function (button) {
        button.addEventListener("click", function () {
            var answer = this.parentElement.querySelector('.q_and_a_answer');
            if (!answer) {
                return;
            }
            if (answer.classList.contains('show')) {
                answer.classList.remove('show');
                this.textContent = "Show Answer";
                answer.style.maxHeight = null;
                answer.style.opacity = 0;
                answer.style.padding = 0;
            } else {
                answer.classList.add('show');
                this.textContent = "Hide Answer";
                answer.style.maxHeight = answer.scrollHeight + "10px";
                answer.style.opacity = 1;
                answer.style.padding = "10px";
            }
        });
    });
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const tocTree = document.getElementById('tocTree');
    const content = document.querySelector(".chapter-container");
    const actual_contents = document.querySelector(".markdown-content");

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
            content.classList.toggle('shifted');
            if (sidebarToggle.style.transform === 'rotate(180deg)') {
                sidebarToggle.style.transform = 'rotate(0deg)';
            } else {
                sidebarToggle.style.transform = 'rotate(180deg)';
            }
            if (sidebarToggle.querySelector('.icon')) {
                const icon = sidebarToggle.querySelector('.icon');

            }
        });
    }
    document.addEventListener('click', (e) => {
        if (sidebar.classList.contains('active') && !sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
            sidebar.classList.remove('active');

            content.classList.remove('shifted');
            if (sidebarToggle.querySelector('.icon')) {
                const icon = sidebarToggle.querySelector('.icon');

            }
        }
    });
    function createTocItem(heading, index, level) {
        const li = document.createElement('li');
        const a = document.createElement('a');
        heading.id = "heading-id-" + index;
        a.textContent = heading.textContent;
        a.href = `#${heading.id}`;

        // Add padding based on the heading level
        a.style.paddingLeft = `${(level - 1) * 30}px`;

        li.appendChild(a);
        return [li, a];
    }
    function createTocTree(headings) {
        const tree = document.createElement('ul');
        const stack = [{ level: 0, element: tree }];
        let currentH1 = null;

        headings.forEach((heading, index) => {
            const level = parseInt(heading.tagName.charAt(1));
            const item_and_a = createTocItem(heading, index, level);
            const item = item_and_a[0]
            const a = item_and_a[1]

            a.classList.add("toc-li-a-" + level)
            if (level === 1) {
                // Start a new top-level section for each h1
                currentH1 = item;
                tree.appendChild(item);
                stack.length = 1; // Reset stack to root level
                stack[0] = { level: 1, element: item };
            } else {
                // For other levels, find the appropriate parent
                while (level <= stack[stack.length - 1].level) {
                    stack.pop();
                }

                if (!stack[stack.length - 1].element.querySelector('ul')) {
                    const ul = document.createElement('ul');
                    stack[stack.length - 1].element.appendChild(ul);
                }

                const parentUl = stack[stack.length - 1].element.querySelector('ul');
                parentUl.appendChild(item);
                stack.push({ level: level, element: item });
            }
        });

        return tree;
    }

    if (content && tocTree) {
        const headings = Array.from(actual_contents.querySelectorAll('h1, h2, h3, h4, h5, h6'));
        tocTree.innerHTML = ''; // Clear any existing content
        tocTree.appendChild(createTocTree(headings));

        // Add some basic styling to the TOC
        tocTree.style.listStyleType = 'none';
        tocTree.style.padding = '0';
        tocTree.style.margin = '0';

        // Style all anchors in the TOC
        const tocAnchors = tocTree.querySelectorAll('a');
        tocAnchors.forEach(a => {
            a.style.display = 'block';
            a.style.padding = '5px 0';
            a.style.textDecoration = 'none';
            a.style.color = 'inherit';
        });
    }

});