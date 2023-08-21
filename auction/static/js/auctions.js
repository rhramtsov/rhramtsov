let lastScrollTop = 0; // Declare the lastScrollTop variable
let navbar = document.querySelector('.navbar'); // Assuming you have a class 'navbar' in your HTML

window.addEventListener('scroll', function() {
  console.log("Scroll event triggered"); // This line will print a message to the browser console every time the scroll event is triggered.
  
  let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
  
  if (scrollTop > lastScrollTop) {
    navbar.style.top = '-100px'; // Hide the navbar by moving it further above the screen
  } else {
    navbar.style.top = '0'; // Show the navbar
  }

  lastScrollTop = scrollTop; // Update the lastScrollTop value
});


document.addEventListener('DOMContentLoaded', function() {
    var artPieces = document.querySelectorAll('.art-piece');
    artPieces.forEach(function(artPiece) {
      var images = artPiece.querySelectorAll('.art-piece-images img');
      var currentIndex = 0;
  
      var nextButton = artPiece.querySelector('.next-button');
      var prevButton = artPiece.querySelector('.prev-button');
  
      nextButton.addEventListener('click', function() {
        images[currentIndex].classList.remove('active');
        currentIndex = (currentIndex + 1) % images.length;
        images[currentIndex].classList.add('active');
      });
  
      prevButton.addEventListener('click', function() {
        images[currentIndex].classList.remove('active');
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        images[currentIndex].classList.add('active');
      });
    });
  });
  $(document).on('click', '[data-toggle="lightbox"]', function(event) {
    event.preventDefault();
    var galleryId = $(this).attr('data-gallery');
    var images = [];
    
    // Build the gallery images array
    $('[data-gallery="' + galleryId + '"]').each(function() {
        images.push({
            href: $(this).attr('href'),
            title: $(this).attr('data-title'),
            footer: $(this).attr('data-footer')
        });
    });

    // Initialize the lightbox with the gallery
    $.ekkoLightbox({
        alwaysShowClose: true,
        leftArrow: '<span>&lt;</span>',
        rightArrow: '<span>&gt;</span>',
        gallery: galleryId,
        loadShow: true,
        initialIndex: 0, // Start from the first image
        galleryParentSelector: 'body',
        onContentLoaded: function() {
            // Handle custom navigation here if needed
        }
    });
});

