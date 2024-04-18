    const form = document.getElementById('myForm');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const usernameError = document.getElementById('usernameError');
    const passwordError = document.getElementById('passwordError');

    form.addEventListener('submit', function(event) {
      event.preventDefault();

      // Validation du nom d'utilisateur
      const username = usernameInput.value.trim();
      if (username.length !== 8 || !/^[a-zA-Z]+$/.test(username)) {
        usernameError.textContent = "Le nom d'utilisateur doit être de 8 caractères alpha";
        usernameInput.classList.add('error');
      } else {
        usernameError.textContent = "";
        usernameInput.classList.remove('error');
      }

      // Validation du mot de passe
      const password = passwordInput.value.trim();
      const passwordRegex = /^[a-zA-Z0-9?;:!]{8,}$/;
      if (!passwordRegex.test(password)) {
        passwordError.textContent = "Le mot de passe doit être de 8 caractères (a-zA-Z0-9?;:!)";
        passwordInput.classList.add('error');
      } else {
        passwordError.textContent = "";
        passwordInput.classList.remove('error');
      }

      // Si les deux champs sont valides, envoyer le formulaire
      if (usernameError.textContent === "" && passwordError.textContent === "") {
        form.submit();
      }
    });

