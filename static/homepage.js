
let button1 = document.querySelector('#button1');
let button2 = document.querySelector('#button2');
let button3 = document.querySelector('#button3');
let button4 = document.querySelector('#button4');
let button5 = document.querySelector('#button5');
let button6 = document.querySelector('#button6');

let currentEmotion = null;

// redButton.addEventListener('click', e => { responseBox.style.backgroundColor ='red';
//   console.log("You clicked the red button!"); responseBox.innerHTML = 'red';
// })
/*
button1.addEventListener('click', e =>{document.style.backgroundColor = '#4CAF50'; console.log("you clicked button1")

})
*/
function handleEmotion(myEmotion, callingButton) {
  currentEmotion = myEmotion;
  clearButtonBackgrounds();
  callingButton.style.backgroundColor = 'blue';
  
}

function clearButtonBackgrounds() {
  var buttons = document.getElementsByClassName("button");
  for (var i = 0; i < buttons.length; i++) {
    buttons[i].style.backgroundColor = 'lightgreen';
  }
}
