var counterdiv = document.getElementsByClassName("counterdiv")[0];
var divs = counterdiv.getElementsByTagName("DIV");
var msg = "";
var x;

for (x of divs) {
  if (x["className"].includes("counter-title")) {
    msg += "=" + x.textContent;
  } else if (x["className"].includes("counter-header") || x["className"].includes("counter-group")) {
    number = x.getElementsByClassName("counter-number")[0].textContent;
    if (x["className"].includes("double")) {
      item = x.getElementsByClassName("counter-item-double")[0].textContent;
    } else {
      item = x.getElementsByClassName("counter-item")[0].textContent;
    }
    msg += "|" + number + "|" + item;
  }
}

return msg;
