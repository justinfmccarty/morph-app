// when page is too small activate the responsive nav menu
function openResponsive() {
  var x = document.getElementById("mainNav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}

function logSubmit(event) {
  // event.preventDefault();
  console.log(`Form Submitted! Timestamp: ${event.timeStamp}`);
  // console.log(form.elements)
}
// const form = document.getElementById("configuration");
// form.addEventListener("lock", logSubmit);

const configForm = document.getElementById("configuration")
configForm.addEventListener("submit", function (e) {
  e.preventDefault();

  const data = new FormData(configForm);
  let temp = document.getElementById("temp-output")
  temp.innerText = "---" + "\n"
  for (const [name, value] of data) {
    console.log(name, ":", value)
    temp.innerText += name + ":" + value + "\n"
  }
  console.log(data.innerText)
})


var text = $('.typewriter').text();

var length = text.length;
var timeOut;
var character = 0;


(function typeWriter() {
  timeOut = setTimeout(function () {
    character++;
    var type = text.substring(0, character);
    $('.typewriter').text(type);
    typeWriter();

    if (character == length) {
      clearTimeout(timeOut);
    }

  }, 150);
}());

async function execGetCMIP() {
  const response = await fetch('/exec-get-cmip');
  // let data = await response.text();
  // console.log(data.json())
  // .then(response => response.json()) 
  // // .then(data => console.log(data)) 
  // .then(data => sessionStorage.setItem("key", data))
  // .catch(error => console.error(error)); 
  // sessionStorage.setItem("myData", data)

}

function execMorphEPW() {
  let data = sessionStorage.getItem("myData");
  console.log(data)
  fetch('/exec-morph-epw')
  //   .then(response => response.json()) 
  //   .then(data => console.log(data)) 
  //   .catch(error => console.error(error)); 
}


function execGetResults() {
  fetch('/exec-get-results')
    // .then(res => {
    //   res.json(); // **
    // }).catch(err => console.log(err));
  // .then(response => response.json()) 
  // .then(data => console.log(data)) 
  // .catch(error => console.error(error)); 
} 