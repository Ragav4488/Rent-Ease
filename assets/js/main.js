/* ============================================================
   RentEase – assets/js/main.js
   1. Client-side validation for the register / login / apply forms
   2. Live filtering of the property grid
   3. Property image gallery switcher
   4. Rent calculation helper on the payment form
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

  /* ---------------- 1. Form validation ---------------- */
  const rules = {
    full_name: v => v.trim().length >= 3 || 'Enter your full name (min 3 characters)',
    email:     v => /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(v.trim()) || 'Enter a valid email address',
    phone:     v => /^[6-9]\d{9}$/.test(v.trim()) || 'Enter a valid 10-digit mobile number',
    password:  v => v.length >= 8 || 'Password must be at least 8 characters',
    confirm:   v => v === (document.getElementById('password') || {}).value || 'Passwords do not match',
    rent_amount: v => Number(v) > 0 || 'Rent must be greater than zero',
    area_sqft:   v => Number(v) > 0 || 'Area must be greater than zero',
    subject:     v => v.trim().length >= 6 || 'Subject must be at least 6 characters',
    description: v => v.trim().length >= 15 || 'Describe the issue in at least 15 characters'
  };

  document.querySelectorAll('form[data-validate]').forEach(function (form) {
    form.addEventListener('submit', function (event) {
      let firstBad = null;

      form.querySelectorAll('input, select, textarea').forEach(function (field) {
        const rule = rules[field.name];
        const msgBox = form.querySelector('[data-error-for="' + field.name + '"]');
        if (!rule) return;

        const result = rule(field.value);
        const ok = result === true;

        field.classList.toggle('invalid', !ok);
        if (msgBox) {
          msgBox.textContent = ok ? '' : result;
          msgBox.style.display = ok ? 'none' : 'block';
        }
        if (!ok && !firstBad) firstBad = field;
      });

      if (firstBad) {
        event.preventDefault();
        firstBad.focus();
      }
    });
  });

  /* ---------------- 2. Live filter on properties page ---------------- */
  const filterInput = document.getElementById('liveFilter');
  if (filterInput) {
    filterInput.addEventListener('input', function () {
      const q = this.value.toLowerCase();
      let shown = 0;
      document.querySelectorAll('.prop-card').forEach(function (card) {
        const haystack = (card.dataset.search || card.textContent).toLowerCase();
        const hit = haystack.includes(q);
        card.style.display = hit ? '' : 'none';
        if (hit) shown++;
      });
      const counter = document.getElementById('filterCount');
      if (counter) counter.textContent = shown;
    });
  }

  /* ---------------- 3. Property gallery ---------------- */
  const mainImg = document.getElementById('galleryMain');
  if (mainImg) {
    document.querySelectorAll('.gallery-thumbs button').forEach(function (btn) {
      btn.addEventListener('click', function () {
        mainImg.src = this.dataset.src;
        document.querySelectorAll('.gallery-thumbs button')
          .forEach(b => b.classList.remove('active'));
        this.classList.add('active');
      });
    });
  }

  /* ---------------- 4. Rent / deposit preview ---------------- */
  const rentField = document.getElementById('rent_amount');
  const depositOut = document.getElementById('depositPreview');
  if (rentField && depositOut) {
    const compute = () => {
      // the field shows "₹16,500" — strip everything but digits before maths
      const rent = Number(rentField.value.replace(/[^\d.]/g, '')) || 0;
      depositOut.textContent = '₹' + (rent * 3).toLocaleString('en-IN');
    };
    rentField.addEventListener('input', compute);
    rentField.addEventListener('change', compute);
    compute();
  }

  /* ---------------- 5. Auto-dismiss flash messages ---------------- */
  const flashBox = document.querySelector('.flash');
  if (flashBox) {
    setTimeout(() => { flashBox.style.transition = 'opacity .4s'; flashBox.style.opacity = '0'; }, 4000);
    setTimeout(() => flashBox.remove(), 4500);
  }
});
