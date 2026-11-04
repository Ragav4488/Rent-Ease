from .. import theme


def build(doc):
    theme.exp_head(doc, "03", "22/07/2026",
                        "User registration form validation using JavaScript")
    theme.heading_plain(doc, "AIM:")
    theme.body(doc, "To design a user registration form and validate every field on the client "
                    "side using JavaScript regular expressions before the form is submitted.")
    theme.heading_plain(doc, "PROCEDURE:")
    theme.numbered(doc, [
        "Create register.html, register.css and validate.js.",
        "Build the form with name, email, mobile, password, confirm password and gender fields.",
        "Reserve an inline error span under each field (<span data-error-for=...>).",
        "Attach an input listener to each field so the error clears as the user types.",
        "Write a rule table mapping each field name to a validation function.",
        "Validate the name length, the email pattern, the ten-digit mobile number, the "
        "password strength and the confirm-password match.",
        "On submit, run every rule, show the first error and focus that field.",
        "Call event.preventDefault() when any rule fails so nothing is posted.",
        "Re-check the rules on the server as well, since client checks can be bypassed.",
        "Test with a valid record, an invalid email, a nine-digit mobile and mismatched passwords.",
    ])
    theme.heading_plain(doc, "JAVASCRIPT FEATURES USED:")
    theme.body(doc, "Regular expressions, addEventListener, querySelectorAll, classList, "
                    "textContent, focus, event.preventDefault, form dataset attributes.")
    theme.heading_plain(doc, "CODE:")
    theme.code(doc, """const rules = {
    full_name: v => v.trim().length >= 3
                  || 'Enter your full name (min 3 characters)',
    email:     v => /^[^\\s@]+@[^\\s@]+\\.[a-z]{2,}$/i.test(v.trim())
                  || 'Enter a valid email address',
    phone:     v => /^[6-9]\\d{9}$/.test(v.trim())
                  || 'Enter a valid 10-digit mobile number',
    password:  v => v.length >= 8
                  || 'Password must be at least 8 characters',
    confirm:   v => v === document.getElementById('password').value
                  || 'Passwords do not match'
};

document.querySelectorAll('form[data-validate]').forEach(function (form) {
    form.addEventListener('submit', function (event) {
        let firstBad = null;

        form.querySelectorAll('input, select, textarea').forEach(function (field) {
            const rule   = rules[field.name];
            const msgBox = form.querySelector(
                '[data-error-for="' + field.name + '"]');
            if (!rule) return;

            const result = rule(field.value);
            const ok     = result === true;

            field.classList.toggle('invalid', !ok);
            if (msgBox) {
                msgBox.textContent   = ok ? '' : result;
                msgBox.style.display = ok ? 'none' : 'block';
            }
            if (!ok && !firstBad) firstBad = field;
        });

        if (firstBad) {
            event.preventDefault();
            firstBad.focus();
        }
    });
});""")
    theme.heading_plain(doc, "SERVER-SIDE RE-CHECK:")
    theme.code(doc, """if (mb_strlen($name) < 3) {
    $errors['full_name'] = 'Enter your full name (minimum 3 characters).';
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $errors['email'] = 'Enter a valid email address.';
}
if (!preg_match('/^[6-9]\\d{9}$/', $phone)) {
    $errors['phone'] = 'Enter a valid 10-digit Indian mobile number.';
}
if (strlen($pass) < 8) {
    $errors['password'] = 'Password must be at least 8 characters.';
} elseif ($pass !== $confirm) {
    $errors['confirm'] = 'Passwords do not match.';
}""")
    theme.heading_plain(doc, "OUTPUT:")
    theme.body(doc, "A valid submission proceeds to the server. An invalid email, a nine-digit "
                    "mobile number or a mismatched password prefixes the field with a red message "
                    "and the form does not submit.")
    theme.heading_plain(doc, "RESULT:")
    theme.body(doc, "Thus the user registration form was designed and validated on the client "
                    "side with JavaScript and re-validated on the server with PHP.")
    theme.rubric_table(doc)
    theme.page_break(doc)
