function changeText() {
  document.getElementById("text").innerText = "You clicked the button!";
}

function toggleSigninWindow() {
  var signinWindow = document.getElementById("signinWindow");
  if (signinWindow.style.display === "none" || signinWindow.style.display === "") {
    signinWindow.style.display = "block";
  } else {
    signinWindow.style.display = "none";
  }
}
document.addEventListener('click', function (event) {
  var signinWindow = document.getElementById('signinWindow');
  var signinButton = document.querySelector('.signin-button');

  if (!signinWindow.contains(event.target) && event.target !== signinButton) {
    signinWindow.style.display = 'none';
  }
});

function switchMode(mode) {
  document.querySelectorAll('.mode').forEach(el => el.classList.add('hidden'));
  document.getElementById(mode).classList.remove('hidden');
}



// Game screen code


// document.getElementById('close-popup-btn').addEventListener('click', function() {
//     document.getElementById('signinWindow').style.display = 'block';
//     document.getElementById('overlay').style.display = 'block';
// });

// Close the popup when the close button is clicked
document.getElementById('close-popup-btn').addEventListener('click', function () {
  document.getElementById('popup').style.display = 'none';
  document.getElementById('overlay').style.display = 'none';
});

// // Close the popup if the user clicks on the overlay
// document.getElementById('overlay').addEventListener('click', function() {
//   document.getElementById('popup').style.display = 'none';
//   document.getElementById('overlay').style.display = 'none';
// });


// Handle the "account" button click
document.querySelector('.account_button')?.addEventListener('click', function () {
  // Send a request to the server to log in or display login form
  fetch('/view_account', {
    method: 'POST',
    body: new URLSearchParams({
      'action': 'account'
    }),
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  })
    // .then(response => response.json())
    // .then(data => {
    //     if (data.status === 'success') {
    //         window.location.reload(); // Reload the page if login is successful
    //     } else {
    //         alert('Login failed');
    //     }
    // })
    .catch(error => console.error('Error:', error));
});


// Loop through each button and add an event listener
document.querySelectorAll('.button').forEach(button => {
  button.addEventListener('click', function () {
    // Get the article title (article[0]) from the data-attribute
    const button_id = button.getAttribute('button-type');

    // Send the value to the Flask server using a POST request
    fetch('/button_pressed', {
      method: 'POST',
      body: new URLSearchParams({
        'button_id': button_id,
        'time_left': timeLeft
      }),
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          let popup = document.getElementById('popup');
          let popupText = popup.querySelector('h2'); // Select the <h2> inside #popup

          // Change text based on win condition
          if (data.win === "True") {
            popupText.innerText = "You answered correctly!";
          } else {
            popupText.innerText = "You guessed incorrectly...";
          }

          // Show the popup
          popup.style.display = 'block';
          document.getElementById('overlay').style.display = 'block';
        }
      })
      .catch(error => console.error('Error:', error));
  });
});
window.onload = function () {
  if (!window.loggedIn) {
    document.getElementById("forcesignin").style.display = "block";
    document.getElementById("overlay").style.display = "block";
  }
};

//attempt at making a confirmation for deleting account, did not work
// document.getElementsByClassName('signup-btn')[0].addEventListener('click', function() {
//     document.getElementById("deleteconfirm").style.display = "block";
//     document.getElementById("overlay").style.display = "block";
// });

const overlay = document.getElementById('overlay');
const allPopups = document.querySelectorAll('.popup');
const pop_up_btn = document.getElementById('close-popup-btn');

overlay.addEventListener('click', () => {
  next_article()
});

pop_up_btn.addEventListener('click', () => {
  next_article()
});



function next_article(){
  const overlay = document.getElementById('overlay');
  const allPopups = document.querySelectorAll('.popup');
  allPopups.forEach(p => p.style.display = 'none');
  overlay.style.display = 'none';
  fetch('/next_article', {
    method: 'POST', 
    body: new URLSearchParams({
    }),
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  })
  .then(response => response.json())
  .then(data => {
    console.log("Server Response:", data);  // Debugging

    if (data.status === 'success') {
      window.location.href = data.url;
    }
  })
    .catch(error => console.error('Error:', error));
}

  let timeLeft = 100; // Set the timer in seconds
  let timerElement;

  function startTimer() {
      timerElement = document.getElementById("timer"); // Ensure it's assigned after page load

      if (!timerElement) {
          console.error("Timer element not found!");
          return;
      }

      let timerInterval = setInterval(() => {
          if (timeLeft < 0) {
              clearInterval(timerInterval);
              document.getElementById("time-up-message").innerText = "Time's up!";
              sendTimeOverEvent();
          } else {
              timerElement.innerText = timeLeft;
              timeLeft--;
          }
      }, 1000);
  }

  function sendTimeOverEvent() {
      fetch("/time_over", { method: "POST" })
      .then(response => response.json())
      .then(data => {
          alert(data.message);
      })
      .catch(error => console.error("Error sending time over event:", error));
  }

  // Ensure script runs only after DOM is fully loaded
  document.addEventListener("DOMContentLoaded", startTimer);
