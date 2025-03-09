function changeText() {
  document.getElementById("text").innerText = "You clicked the button!";
}

function toggleSigninWindow() {
  var signinWindow = document.getElementById("signinWindow");
  if (signinWindow.style.display === "none" || signinWindow.style.display === ""){
    signinWindow.style.display = "block";
  } else {
    signinWindow.style.display = "none";
  }
}
document.addEventListener('click', function(event) {
  var signinWindow = document.getElementById('signinWindow');
  var signinButton = document.querySelector('.signin-button');
  
  if (!signinWindow.contains(event.target) && event.target !== signinButton) {
    signinWindow.style.display = 'none';
  }
});
