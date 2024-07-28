let editMode = false;
let homeworkData = {};
var currentTime = new Date();
var dayOfWeek = null
function initializeHomeworkManager(data, currentTime, dayOfWeek_) {
    homeworkData = data;
    dayOfWeek = dayOfWeek_
    currentTime = serverTime = new Date(currentTime);
    renderHomeworkTable();
    document.getElementById('addHomeworkBtn').addEventListener('click', addHomework);
    //highlightCurrentPeriod(dayOfWeek);
    
}

function renderHomeworkTable() {
    const tbody = document.querySelector('#homeworkTable tbody');
    tbody.innerHTML = '';

    for (const [subject, homeworks] of Object.entries(homeworkData)) {
        for (const homework of homeworks) {
            const row = createHomeworkRow(subject, homework);
            tbody.appendChild(row);
        }
    }
}

function createHomeworkRow(subject, homework) {
    const row = document.createElement('tr');
    let due_date_block
    if (homework.due.startsWith('[NEXT:')){
        due_date_block = `<a href="#" class="clickable_due">${formatDueDate(homework.due)}</a>`
    }else{
        due_date_block = formatDueDate(homework.due)
    }

    row.innerHTML = `
        <td class="editable" contenteditable="${editMode}">${subject}</td>
        <td class="editable" contenteditable="${editMode}">${homework.chapter}</td>
        <td class="editable" contenteditable="${editMode}">${homework.homework_title}</td>
        <td class="editable" contenteditable="${editMode}">${homework.description}</td>
        <td class="editable" contenteditable="${editMode}" data-full-value="${homework.due}">${due_date_block}</td>
        <td>
            <button class="deleteBtn" style="display: ${editMode ? 'inline-block' : 'none'};">
                <i class="fas fa-trash-alt"></i>
            </button>
        </td>
    `;
    row.querySelector('.deleteBtn').addEventListener('click', () => removeHomework(subject, homework.homework_title));
    row.querySelector('td:nth-child(5)').addEventListener('click', (e) => handleDueDateClick(e.target));
    row.getElementsByClassName('clickable_due')[0].addEventListener('click', (e) => handleDueDateClick(row.querySelector('td:nth-child(5)')));
    return row;
}

function formatDueDate(dueDate) {
    if (dueDate.startsWith('[NEXT:')) {
        if (editMode) {
            return dueDate;
        } else {
            return dueDate.split("[NEXT:")[1].split("]")[0];
        }
    } else {
        const date = new Date(dueDate);
        return `${date.getDate().toString().padStart(2, '0')}/${(date.getMonth() + 1).toString().padStart(2, '0')}/${date.getFullYear()}`;
    }
}

function handleDueDateClick(element) {
    if(element.hasAttribute('data-full-value')){
        var fullValue = element.getAttribute('data-full-value');
    }else{
        var fullValue = element.parentElement.getAttribute('data-full-value');
    }
    if (fullValue.startsWith('[NEXT:') && editMode == false) {
        const subject = fullValue.slice(6, -1);
        scrollToNextPeriod(subject);
    }
}

function scrollToNextPeriod(subject) {
    const timetable = document.getElementById('timetable');
    if (!timetable) {
        console.error('Timetable element not found.');
        return;
    }

    const today = serverTime.getDay(); // 0 is Sunday, 1 is Monday, etc.
    let startDay = today;
    let found = false;

    // If it's after 4:30 PM, start looking from the next day
    if (serverTime.getHours() > 16 || (serverTime.getHours() === 16 && serverTime.getMinutes() >= 30)) {
        startDay = (today + 1) % 7;
    }

    for (let i = 0; i < 7; i++) {
        const dayIndex = (startDay + i) % 7;
        if (dayIndex === 0) continue; // Skip Sunday

        const dayRow = timetable.rows[dayIndex];
        if (!dayRow) continue; // Skip if row does not exist

        for (let j = 1; j < dayRow.cells.length; j++) {
            if (dayRow.cells[j].textContent.trim().toLowerCase() === subject.toLowerCase()) {
                dayRow.cells[j].scrollIntoView({ behavior: 'smooth', block: 'center' });
                console.log(dayRow.cells,dayRow.cells[j])
                highlightCell(dayRow.cells[j]);
                found = true;
                break;
            }
        }
        if (found) break;
    }

    if (!found) {
        alert(`No upcoming ${subject} class found in the timetable.`);
    }
}
function highlightCell(cell) {
    // First, clear any existing highlight from the table
    const timetable = document.getElementById('timetable');
    const highlightedCells = timetable.getElementsByClassName('highlighted');
    for (let highlightedCell of highlightedCells) {
        highlightedCell.classList.remove('highlighted');
    }
    console.log(cell)
    // Add the highlight to the specified cell
    cell.classList.add('highlighted');

    // Remove the highlight after 15 seconds
    setTimeout(() => {
        cell.classList.remove('highlighted');
        cell.style.border = ''; // Reset the border
    }, 15000); // 15 seconds
}
function highlightCurrentPeriod(dayOfWeek) {
    const hour = serverTime.getHours();
    const minute = serverTime.getMinutes();

    if (dayOfWeek === 'Sunday' || dayOfWeek === 'Saturday') return; // Weekend
    if (hour < 8 || (hour === 16 && minute >= 30) || hour > 16) return; // Outside school hours

    const timetable = document.getElementById('timetable');
    if (!timetable) {
        console.error('Timetable element not found.');
        return;
    }

    const dayIndex = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'].indexOf(dayOfWeek) + 1;
    const currentRow = timetable.rows[dayIndex];
    if (!currentRow) {
        console.error('Timetable row for the day not found.');
        return;
    }

    const periodIndex = Math.floor((hour - 8) + (minute >= 30 ? 1 : 0));
    if (periodIndex >= 0 && periodIndex < currentRow.cells.length - 1) {
        highlightCell(currentRow.cells[periodIndex + 1]);
    }
}
/*
function highlightCurrentTimeTable(dayOfWeek){
    const hour = serverTime.getHours();
    const minute = serverTime.getMinutes();

    if (dayOfWeek === 'Sunday' || dayOfWeek === 'Saturday') return; // Weekend
    if (hour < 8 || (hour === 16 && minute >= 30) || hour > 16) return; // Outside school hours

    const timetable = document.getElementById('timetable');
    if (!timetable) {
        console.error('Timetable element not found.');
        return;
    }

    const dayIndex = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'].indexOf(dayOfWeek) + 1;
    const currentRow = timetable.rows[dayIndex];
    if (!currentRow) {
        console.error('Timetable row for the day not found.');
        return;
    }
    console.log(dayIndex)
    currentRow.classList.add("current-dayofweek");
}
*/

function toggleEditMode() {
    editMode = !editMode;
    const table = document.getElementById('homeworkTable');
    const editables = table.getElementsByClassName('editable');
    const deleteBtns = table.getElementsByClassName('deleteBtn');
    let due_date_block;

    for (let editable of editables) {
        editable.contentEditable = editMode;
        if (editable.cellIndex === 4) { // Due date column
            const fullValue = editable.getAttribute('data-full-value');
            
            if (editMode == false){
                if (fullValue.startsWith('[NEXT:')){
                    due_date_block = `<a href="#" class="clickable_due">${formatDueDate(fullValue)}</a>`
                }    
            }    
            if(due_date_block === undefined){
                due_date_block = formatDueDate(fullValue)
            }
            editable.innerHTML = due_date_block;
        }
    }

    for (let deleteBtn of deleteBtns) {
        deleteBtn.style.display = editMode ? 'inline-block' : 'none';
    }

    document.getElementById('updateButton').style.display = editMode ? 'block' : 'none';
    document.getElementById('addHomeworkBtn').style.display = editMode ? 'inline-block' : 'none';
}
function addHomework() {
    if (!editMode) return;
    const newHomework = {
        chapter: '',
        homework_title: '',
        description: '',
        due: new Date().toISOString().split('T')[0]
    };
    const subject = 'New Subject'; // You might want to prompt the user for the subject
    if (!homeworkData[subject]) {
        homeworkData[subject] = [];
    }
    homeworkData[subject].push(newHomework);
    renderHomeworkTable();
}

function removeHomework(subject, title) {
    if (!editMode) return;
    homeworkData[subject] = homeworkData[subject].filter(hw => hw.homework_title !== title);
    if (homeworkData[subject].length === 0) {
        delete homeworkData[subject];
    }
    renderHomeworkTable();
}

function updateHomework() {
    const table = document.getElementById('homeworkTable');
    const rows = table.querySelectorAll('tbody tr');
    const newData = {};

    rows.forEach(row => {
        const subject = row.cells[0].textContent.trim();
        const dueDateCell = row.cells[4];
        const homework = {
            chapter: row.cells[1].textContent.trim(),
            homework_title: row.cells[2].textContent.trim(),
            description: row.cells[3].textContent.trim(),
            due: dueDateCell.getAttribute('data-full-value') || dueDateCell.textContent.trim()
        };
        if (!newData[subject]) {
            newData[subject] = [];
        }
        newData[subject].push(homework);
    });


    fetch('/update_homework', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(newData),
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            alert('Homework updated successfully!');
            homeworkData = newData;
            toggleEditMode();
            document.getElementById('editModeCheckbox').checked = false;
            renderHomeworkTable();
        } else {
            alert('Failed to update homework. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to update homework. Please try again.');
    });
}

function parseDueDate(dueDateString) {
    if (dueDateString.startsWith('[NEXT:')) {
        return dueDateString;
    } else {
        const [day, month, year] = dueDateString.split('/');
        return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
    }
}
function updateServerTime() {
    serverTime = new Date(serverTime.getTime() + 60000); // Add one minute
    highlightCurrentPeriod(getDayOfWeek(serverTime.getDay()));
}

function getDayOfWeek(day) {
    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
    return days[day];
}

// Call this function when the page loads
window.addEventListener('load', () => {
    initializeHomeworkManager(homeworkData, currentTime, dayOfWeek);
    setInterval(updateServerTime, 60000); // Update every minute
});