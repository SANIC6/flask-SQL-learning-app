// API Configuration
const API_BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:5000/api'
    : '/api';

// State Management
let currentLesson = null;
let allLessons = [];

// DOM Elements
const lessonNav = document.getElementById('lessonNav');
const lessonBadge = document.getElementById('lessonBadge');
const lessonTitle = document.getElementById('lessonTitle');
const lessonDescription = document.getElementById('lessonDescription');
const theorySection = document.getElementById('theorySection');
const examplesSection = document.getElementById('examplesSection');
const sqlEditor = document.getElementById('sqlEditor');
const runButton = document.getElementById('runButton');
const resultsContainer = document.getElementById('resultsContainer');

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    loadLessons();
    setupEventListeners();
});

// Setup Event Listeners
function setupEventListeners() {
    runButton.addEventListener('click', executeQuery);

    // Allow Ctrl+Enter to run query
    sqlEditor.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            executeQuery();
        }
    });
}

// Load All Lessons
async function loadLessons() {
    try {
        const response = await fetch(`${API_BASE_URL}/lessons`);
        const data = await response.json();

        if (data.success) {
            allLessons = data.lessons;
            renderLessonNav(allLessons);

            // Load first lesson by default
            if (allLessons.length > 0) {
                loadLesson(allLessons[0].id);
            }
        }
    } catch (error) {
        console.error('Error loading lessons:', error);
        showError('Failed to load lessons. Please refresh the page.');
    }
}

// Render Lesson Navigation
function renderLessonNav(lessons) {
    // Group lessons by category
    const categories = {};
    lessons.forEach(lesson => {
        if (!categories[lesson.category]) {
            categories[lesson.category] = [];
        }
        categories[lesson.category].push(lesson);
    });

    // Render each category
    let html = '';
    Object.keys(categories).forEach(category => {
        html += `
            <div class="lesson-category">
                <div class="category-title">${category}</div>
                ${categories[category].map(lesson => `
                    <div class="lesson-item" data-lesson-id="${lesson.id}" onclick="loadLesson(${lesson.id})">
                        <div class="lesson-icon">${lesson.id}</div>
                        <span>${lesson.title}</span>
                    </div>
                `).join('')}
            </div>
        `;
    });

    lessonNav.innerHTML = html;
}

// Load Specific Lesson
async function loadLesson(lessonId) {
    try {
        // Update active state in nav
        document.querySelectorAll('.lesson-item').forEach(item => {
            item.classList.remove('active');
        });
        const activeItem = document.querySelector(`[data-lesson-id="${lessonId}"]`);
        if (activeItem) {
            activeItem.classList.add('active');
        }

        // Fetch lesson content
        const response = await fetch(`${API_BASE_URL}/lessons/${lessonId}`);
        const data = await response.json();

        if (data.success) {
            currentLesson = data.lesson;
            renderLesson(currentLesson);
        }
    } catch (error) {
        console.error('Error loading lesson:', error);
        showError('Failed to load lesson content.');
    }
}

// Render Lesson Content
function renderLesson(lesson) {
    // Update header
    lessonBadge.textContent = lesson.category;
    lessonTitle.textContent = lesson.title;
    lessonDescription.textContent = lesson.content.description;

    // Render theory section
    theorySection.innerHTML = `
        <h3>What You'll Learn</h3>
        ${formatTheoryContent(lesson.content.theory)}
    `;

    // Render examples
    if (lesson.content.examples && lesson.content.examples.length > 0) {
        examplesSection.innerHTML = `
            <h3 style="color: var(--text-primary); margin-bottom: var(--spacing-lg);">Interactive Examples</h3>
            ${lesson.content.examples.map((example, index) => `
                <div class="example-card">
                    <div class="example-header">
                        <div class="example-title">${example.title}</div>
                        <button class="try-button" onclick="loadExample(${index})">Try It</button>
                    </div>
                    <p class="example-description">${example.description}</p>
                    <div class="example-query">${escapeHtml(example.query)}</div>
                    <p class="example-explanation">💡 ${example.explanation}</p>
                </div>
            `).join('')}
        `;
    } else {
        examplesSection.innerHTML = '';
    }

    // Clear editor and results
    sqlEditor.value = '';
    resultsContainer.innerHTML = `
        <div class="results-placeholder">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="8" y="8" width="32" height="32" rx="2" stroke="currentColor" stroke-width="2" opacity="0.3"/>
                <line x1="8" y1="16" x2="40" y2="16" stroke="currentColor" stroke-width="2" opacity="0.3"/>
                <line x1="16" y1="16" x2="16" y2="40" stroke="currentColor" stroke-width="2" opacity="0.3"/>
            </svg>
            <p>Run a query to see results</p>
        </div>
    `;
}

// Format Theory Content (convert markdown-like syntax to HTML)
function formatTheoryContent(theory) {
    // Split by double newlines for paragraphs
    const paragraphs = theory.split('\n\n');

    return paragraphs.map(para => {
        // Check if it's a code block (starts with ```)
        if (para.trim().startsWith('```')) {
            const code = para.replace(/```sql\n?/g, '').replace(/```\n?/g, '');
            return `<pre><code>${escapeHtml(code)}</code></pre>`;
        }

        // Check if it's a list item
        if (para.trim().startsWith('-')) {
            const items = para.split('\n').filter(line => line.trim().startsWith('-'));
            return `<ul style="margin-left: var(--spacing-lg); color: var(--text-secondary);">
                ${items.map(item => `<li>${formatInlineMarkdown(item.replace(/^-\s*/, ''))}</li>`).join('')}
            </ul>`;
        }

        // Regular paragraph
        return `<p>${formatInlineMarkdown(para)}</p>`;
    }).join('');
}

// Format Inline Markdown (bold, code, etc.)
function formatInlineMarkdown(text) {
    // Bold text **text**
    text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

    // Inline code `code`
    text = text.replace(/`([^`]+)`/g, '<code>$1</code>');

    return text;
}

// Load Example into Editor
function loadExample(exampleIndex) {
    if (currentLesson && currentLesson.content.examples[exampleIndex]) {
        const example = currentLesson.content.examples[exampleIndex];
        sqlEditor.value = example.query;
        sqlEditor.focus();

        // Optionally auto-run the query
        // executeQuery();
    }
}

// Execute SQL Query
async function executeQuery() {
    const query = sqlEditor.value.trim();

    if (!query) {
        showError('Please enter a SQL query.');
        return;
    }

    // Disable button during execution
    runButton.disabled = true;
    runButton.textContent = 'Running...';

    try {
        const response = await fetch(`${API_BASE_URL}/execute`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query })
        });

        const data = await response.json();

        if (response.ok) {
            // Check if it's a multi-statement response
            if (data.multiStatement || data.results) {
                renderMultiStatementResults(data);
            } else if (data.success) {
                // Legacy single statement support
                if (data.data) {
                    renderResults(data);
                } else {
                    renderSuccessMessage(data.message);
                }
            } else {
                showError(data.error);
            }
        } else {
            showError(data.error || 'An error occurred while executing the query.');
        }
    } catch (error) {
        console.error('Error executing query:', error);
        showError('Failed to execute query. Please try again.');
    } finally {
        runButton.disabled = false;
        runButton.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 2L13 8L3 14V2Z" fill="currentColor"/>
            </svg>
            Run Query
        `;
    }
}

// Render Multi-Statement Results
function renderMultiStatementResults(data) {
    let html = '';

    // Add summary header if multiple statements
    if (data.multiStatement) {
        const summaryClass = data.stopped ? 'warning' : 'success';
        html += `
            <div class="results-summary ${summaryClass}">
                <strong>Executed ${data.executedStatements} of ${data.totalStatements} statement(s)</strong>
                ${data.stopped ? '<br><span style="color: var(--warning);">⚠️ Execution stopped due to error</span>' : ''}
            </div>
        `;
    }

    // Render each statement result
    data.results.forEach((result, index) => {
        html += `<div class="statement-result">`;

        // Statement header with number
        html += `
            <div class="statement-header">
                <span class="statement-number">Statement ${result.statementNumber}</span>
                <span class="statement-status ${result.success ? 'success' : 'error'}">
                    ${result.success ? '✓ Success' : '✗ Error'}
                </span>
            </div>
        `;

        // Show the SQL statement
        html += `
            <div class="statement-code">
                <code>${escapeHtml(result.statement)}</code>
            </div>
        `;

        // Show result based on success/failure
        if (result.success) {
            if (result.data) {
                // SELECT query - show table
                if (result.data.length === 0) {
                    html += `
                        <div class="statement-message success">
                            Query executed successfully. No rows returned.
                        </div>
                    `;
                } else {
                    html += `
                        <div class="statement-message success">
                            ${result.rowCount} row(s) returned
                        </div>
                        <table class="results-table">
                            <thead>
                                <tr>
                                    ${result.columns.map(col => `<th>${escapeHtml(col)}</th>`).join('')}
                                </tr>
                            </thead>
                            <tbody>
                                ${result.data.map(row => `
                                    <tr>
                                        ${result.columns.map(col => {
                        if (col === 'sprite_url' && row[col]) {
                            return `<td><img src="${row[col]}" alt="sprite" class="pokemon-sprite" /></td>`;
                        } else if (col === 'type' && row[col]) {
                            return `<td><span class="type-badge type-${row[col].toLowerCase()}">${escapeHtml(String(row[col]))}</span></td>`;
                        } else {
                            return `<td>${escapeHtml(String(row[col] ?? 'NULL'))}</td>`;
                        }
                    }).join('')}
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    `;
                }
            } else {
                // Non-SELECT query - show message
                html += `
                    <div class="statement-message success">
                        ${escapeHtml(result.message)}
                    </div>
                `;
            }
        } else {
            // Error
            html += `
                <div class="statement-message error">
                    ${escapeHtml(result.error)}
                </div>
            `;
        }

        html += `</div>`; // Close statement-result
    });

    resultsContainer.innerHTML = html;
}

// Render Query Results (legacy single statement)
function renderResults(data) {
    if (!data.data || data.data.length === 0) {
        resultsContainer.innerHTML = `
            <div class="results-info success">
                <span>✓ Query executed successfully. No rows returned.</span>
            </div>
        `;
        return;
    }

    const html = `
        <div class="results-info success">
            <span>✓ Query executed successfully. ${data.rowCount} row(s) returned.</span>
        </div>
        <table class="results-table">
            <thead>
                <tr>
                    ${data.columns.map(col => `<th>${escapeHtml(col)}</th>`).join('')}
                </tr>
            </thead>
            <tbody>
                ${data.data.map(row => `
                    <tr>
                        ${data.columns.map(col => {
        if (col === 'sprite_url' && row[col]) {
            return `<td><img src="${row[col]}" alt="sprite" class="pokemon-sprite" /></td>`;
        } else if (col === 'type' && row[col]) {
            return `<td><span class="type-badge type-${row[col].toLowerCase()}">${escapeHtml(String(row[col]))}</span></td>`;
        } else {
            return `<td>${escapeHtml(String(row[col] ?? 'NULL'))}</td>`;
        }
    }).join('')}
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;

    resultsContainer.innerHTML = html;
}

// Render Success Message
function renderSuccessMessage(message) {
    resultsContainer.innerHTML = `
        <div class="results-info success">
            <span>✓ ${escapeHtml(message)}</span>
        </div>
    `;
}

// Show Error Message
function showError(message) {
    resultsContainer.innerHTML = `
        <div class="error-message">
            ⚠️ ${escapeHtml(message)}
        </div>
    `;
}

// Utility: Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Make functions globally available
window.loadLesson = loadLesson;
window.loadExample = loadExample;
