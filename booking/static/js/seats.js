const body = document.getElementsByTagName("body");
console.log(body);
const myArray = [];
myArray[1] = 1;
myArray[2] = 2;
myArray[3] = 3;

const index = myArray.indexOf(5);
myArray.splice(index, 1);

const notPressed = document.getElementById("total");

function pressed() {
  console.log(notPressed.value);
  if (notPressed.value == "0" || notPressed.value == "[0,[],[]]") {
    alert("select atleast 1 seat");
    return false;
  }
}
