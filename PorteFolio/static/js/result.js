  const toggleButtons = document.querySelectorAll('.toggle-btn');

  toggleButtons.forEach(button => {
    button.addEventListener('click', () => {
      const dataDetails = button.nextElementSibling;
      dataDetails.classList.toggle('show');
    });
  });