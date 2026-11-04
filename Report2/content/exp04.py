from .. import theme


def build(doc):
    theme.exp_head(doc, "04", "29/07/2026",
                        "Implementing web applications with API calls using JavaScript")
    theme.heading_plain(doc, "AIM:")
    theme.body(doc, "To build a web page that fetches data from a remote REST API with the Fetch "
                    "API, renders the response dynamically and handles loading and error states.")
    theme.heading_plain(doc, "PROCEDURE:")
    theme.numbered(doc, [
        "Create api.html, api.css and api.js.",
        "Add a search box, a category selector and a results container.",
        "Use fetch() with the async/await syntax to call the JSON endpoint.",
        "Show a loading indicator before the request and hide it on completion.",
        "Check response.ok and throw an Error carrying the HTTP status on failure.",
        "Parse the body with response.json() and render one card per record.",
        "Wrap the call in try/catch/finally so network failures show a friendly message.",
        "Debounce the search input so the API is not called on every keystroke.",
        "Use AbortController to cancel an in-flight request when a new one starts.",
        "Verify behaviour with a valid query, an empty query and the network switched off.",
    ])
    theme.heading_plain(doc, "JAVASCRIPT FEATURES USED:")
    theme.body(doc, "fetch, async/await, Promises, response.json, AbortController, try/catch/"
                    "finally, template literals, Array.map, debouncing with setTimeout.")
    theme.heading_plain(doc, "CODE:")
    theme.code(doc, """const list    = document.getElementById('list');
const status  = document.getElementById('status');
const search  = document.getElementById('search');
let   controller = null;

async function loadProperties(query = '') {
    // cancel any request still in flight
    if (controller) controller.abort();
    controller = new AbortController();

    status.textContent = 'Loading...';

    try {
        const res = await fetch(
            'api/properties.php?q=' + encodeURIComponent(query),
            { signal: controller.signal }
        );

        if (!res.ok) {
            throw new Error('Request failed: ' + res.status);
        }

        const data = await res.json();

        if (!data.length) {
            list.innerHTML = '<p class="empty">No properties matched.</p>';
            status.textContent = '';
            return;
        }

        list.innerHTML = data.map(p => `
            <article class="card">
                <h3>${p.title}</h3>
                <p>${p.locality}, ${p.city}</p>
                <p class="rent">Rs. ${Number(p.rent_amount).toLocaleString('en-IN')}/mo</p>
            </article>
        `).join('');

        status.textContent = data.length + ' properties loaded';
    } catch (err) {
        if (err.name === 'AbortError') return;
        status.textContent = 'Could not load properties. ' + err.message;
    }
}

let timer;
search.addEventListener('input', function () {
    clearTimeout(timer);
    timer = setTimeout(() => loadProperties(this.value), 300);
});

loadProperties();""")
    theme.heading_plain(doc, "JSON ENDPOINT:")
    theme.code(doc, """<?php
// api/properties.php - returns JSON instead of HTML
require_once __DIR__ . '/../includes/functions.php';
header('Content-Type: application/json; charset=utf-8');

$q = trim($_GET['q'] ?? '');

$stmt = db()->prepare(
    'SELECT property_id, title, city, locality, rent_amount, bhk
       FROM properties
      WHERE status = "available" AND title LIKE ?
      ORDER BY created_at DESC'
);
$stmt->execute(['%' . $q . '%']);

echo json_encode($stmt->fetchAll(), JSON_UNESCAPED_UNICODE);""")
    theme.heading_plain(doc, "OUTPUT:")
    theme.body(doc, "The page lists properties as cards. Typing in the search box refreshes the "
                    "list after a 300 ms debounce. Stopping the server shows the error message "
                    "instead of an empty page.")
    theme.heading_plain(doc, "RESULT:")
    theme.body(doc, "Thus a web application consuming a REST endpoint with the Fetch API was "
                    "implemented and the success, empty and error states were verified.")
    theme.rubric_table(doc)
    theme.page_break(doc)
