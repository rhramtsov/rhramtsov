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

$(document).on('click', '[data-toggle="lightbox"]', function(event) {
    event.preventDefault();
    var galleryId = $(this).attr('data-gallery');
    var items = [];
    
    // Build the gallery items array
    $('[data-gallery="' + galleryId + '"]').each(function() {
        var itemType = $(this).attr('data-type');
        var itemRemote = $(this).attr('data-remote');
        var itemTitle = $(this).attr('data-title');
        var itemFooter = $(this).attr('data-footer');
        
        if (itemType === 'image') {
            items.push({
                href: itemRemote,
                title: itemTitle,
                footer: itemFooter
            });
        } else if (itemType === 'video') {
            items.push({
                remote: '<video controls><source src="' + itemRemote + '" type="video/mp4">Your browser does not support the video tag.</video>',
                title: itemTitle,
                footer: itemFooter
            });
        }
    });

    // Initialize the lightbox with the gallery
    $.ekkoLightbox({
        alwaysShowClose: true,
        leftArrow: '<span>&lt;</span>',
        rightArrow: '<span>&gt;</span>',
        gallery: galleryId,
        loadShow: true,
        initialIndex: 0,
        galleryParentSelector: 'body',
        onContentLoaded: function() {
            // Handle custom navigation here if needed
        }
    });
});
