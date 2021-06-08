{

//For the carousel
  $(document).ready(function() {
    $('.carousel .carousel-caption').css('zoom', $('.carousel').width()/850);
  });

  $(window).resize(function() {
    $('.carousel .carousel-caption').css('zoom', $('.carousel').width()/850);
  });
  
  //For the scroll top
  const toTop = document.querySelector(".to-top");

  window.addEventListener("scroll", () => {
    if (window.pageYOffset > 100) {
      toTop.classList.add("active");
    } else {
      toTop.classList.remove("active");
    }
  })
  
  //Confirm the password
  function onChange() {
    const password = document.querySelector('input[name=password]');
    const confirm = document.querySelector('input[name=password2]');
    if (confirm.value === password.value) {
      confirm.setCustomValidity('');
    } else {
      confirm.setCustomValidity('Passwords do not match');
    }
  }
  }
