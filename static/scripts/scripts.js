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
configForm.addEventListener("submit", function(e) {
  e.preventDefault();
  
  const data = new FormData(configForm);
  let temp = document.getElementById("temp-output")
  temp.innerText = "---" + "\n"
  for (const [name,value] of data) {
    console.log(name, ":", value)
    temp.innerText += name + ":" + value + "\n"
  
  }
})