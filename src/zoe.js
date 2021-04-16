{


  $(document).ready(function() {
    $('.carousel .carousel-caption').css('zoom', $('.carousel').width()/850);
  });

  $(window).resize(function() {
    $('.carousel .carousel-caption').css('zoom', $('.carousel').width()/850);
  });
  }
