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
