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
  