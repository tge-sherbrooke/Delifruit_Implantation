document.addEventListener('DOMContentLoaded', () => {

  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    const nameEl = document.getElementById('name');
    const emailEl = document.getElementById('email');
    const messageEl = document.getElementById('message');
    const formSuccess = document.getElementById('formSuccess');

    const showError = (field, msg) => {
      const el = document.getElementById(field + 'Error');
      if (el) el.textContent = msg;
    };

    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();
      document.querySelectorAll('.error-message').forEach(x => x.textContent = '');

      let isValid = true;
      const name = nameEl ? nameEl.value.trim() : '';
      const email = emailEl ? emailEl.value.trim() : '';
      const message = messageEl ? messageEl.value.trim() : '';

      if (!name || name.length < 2) {
        showError('name', 'Nom requis (min 2 caractères)');
        isValid = false;
      }
      if (!email || !/\S+@\S+\.\S+/.test(email)) {
        showError('email', 'Email valide requis');
        isValid = false;
      }
      if (!message || message.length < 10) {
        showError('message', 'Message requis (min 10 caractères)');
        isValid = false;
      }

      if (isValid) {
        contactForm.style.display = 'none';
        if (formSuccess) formSuccess.style.display = 'block';
        setTimeout(() => {
          contactForm.reset();
          contactForm.style.display = 'block';
          if (formSuccess) formSuccess.style.display = 'none';
        }, 3000);
      }
    });
  }

  const hamburger = document.querySelector('.hamburger');
  const navMenu = document.querySelector('.nav-menu');

  if (hamburger && navMenu) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('active');
      navMenu.classList.toggle('active');
    });

    navMenu.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
      });
    });
  }

  document.querySelectorAll('.cta-button').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const target = document.getElementById('services');
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      } else {
        window.location.href = 'services.html';
      }
    });
  });

  if (!document.getElementById('dynamic-form-style')) {
    const style = document.createElement('style');
    style.id = 'dynamic-form-style';
    style.textContent = `
      .error-message { color: #e74c3c; font-size: 14px; }
      .form-success { display: none; background: #d4edda; padding: 15px; border-radius: 5px; color: #155724; }
    `;
    document.head.appendChild(style);
  }

});
