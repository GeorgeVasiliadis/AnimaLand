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
  
  function findText(){
    let text=document.getElementById("search").value;
	     window.find(text);
  }
  
  }
