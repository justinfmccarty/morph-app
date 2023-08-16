// when page is too small activate the responsive nav menu
function openResponsive() {
  var x = document.getElementById("mainNav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}
