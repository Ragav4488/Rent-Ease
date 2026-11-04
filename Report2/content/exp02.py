from .. import theme


def build(doc):
    theme.exp_head(doc, "02", "15/07/2026", "BMI Calculator using JavaScript")
    theme.heading_plain(doc, "AIM:")
    theme.body(doc, "To design a Body Mass Index calculator using HTML, CSS and JavaScript "
                    "that reads height and weight, computes the BMI value, classifies the "
                    "result and validates the input.")
    theme.heading_plain(doc, "PROCEDURE:")
    theme.numbered(doc, [
        "Create the files bmi.html and bmi.css.",
        "Build a form with height (cm) and weight (kg) number inputs and a Calculate button.",
        "Add a result panel that stays hidden until a valid calculation runs.",
        "Attach a submit handler to the form and call preventDefault().",
        "Read both values with parseFloat() and reject empty or non-numeric input.",
        "Convert height from centimetres to metres and compute weight / height².",
        "Round the result to one decimal place with toFixed(1).",
        "Classify the value into Underweight, Normal, Overweight or Obese using standard cut-offs.",
        "Write the value and the category into the result panel and colour-code the category.",
        "Test with boundary inputs, zero, negative values and non-numeric text.",
    ])
    theme.heading_plain(doc, "JAVASCRIPT FEATURES USED:")
    theme.body(doc, "addEventListener, preventDefault, parseFloat, isNaN, toFixed, "
                    "template literals, classList, textContent, conditional (ternary) "
                    "expressions.")
    theme.heading_plain(doc, "CODE:")
    theme.code(doc, """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>BMI Calculator</title>
    <link rel="stylesheet" href="bmi.css">
</head>
<body>
    <div class="card">
        <h1>BMI Calculator</h1>

        <form id="bmiForm">
            <label for="height">Height (cm)</label>
            <input type="number" id="height" min="50" max="250" step="0.1" required>

            <label for="weight">Weight (kg)</label>
            <input type="number" id="weight" min="10" max="300" step="0.1" required>

            <button type="submit">Calculate</button>
        </form>

        <div id="result" class="result hidden"></div>
    </div>

    <script src="bmi.js"></script>
</body>
</html>""")
    theme.code(doc, """const form   = document.getElementById('bmiForm');
const result = document.getElementById('result');

form.addEventListener('submit', function (event) {
    event.preventDefault();

    const heightCm = parseFloat(document.getElementById('height').value);
    const weightKg = parseFloat(document.getElementById('weight').value);

    if (isNaN(heightCm) || isNaN(weightKg) || heightCm <= 0 || weightKg <= 0) {
        result.textContent = 'Please enter valid positive numbers.';
        result.className = 'result error';
        return;
    }

    const heightM = heightCm / 100;
    const bmi     = weightKg / (heightM * heightM);

    let category, colour;

    if (bmi < 18.5) {
        category = 'Underweight'; colour = '#0369a1';
    } else if (bmi < 25) {
        category = 'Normal';      colour = '#15803d';
    } else if (bmi < 30) {
        category = 'Overweight';  colour = '#b45309';
    } else {
        category = 'Obese';       colour = '#b91c1c';
    }

    result.innerHTML =
        `<strong>Your BMI is ${bmi.toFixed(1)}</strong><br>` +
        `<span style="color:${colour}">Category: ${category}</span>`;
    result.className = 'result';
});""")
    theme.heading_plain(doc, "OUTPUT:")
    theme.body(doc, "For a height of 172 cm and a weight of 68 kg the calculator reports "
                    "BMI 23.0 and the category Normal. Entering a zero or blank value shows "
                    "the validation message instead of a result.")
    theme.heading_plain(doc, "RESULT:")
    theme.body(doc, "Thus the BMI calculator was designed using HTML, CSS and JavaScript and "
                    "the computed value and category were verified for several inputs.")
    theme.rubric_table(doc)
    theme.page_break(doc)
