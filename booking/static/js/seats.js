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


(function () {
  window.onpageshow = function (event) {
    if (event.persisted) {
      window.location.reload();
    }
  };
})();

let total = 0;
const mySeats = [];
const myVenue = [];

function clicked(number) {
  const myArray = number.split(",");

  const buttonPressed = document.getElementById(myArray[0]);
  buttonPressed.classList.toggle("select");
  buttonPressed.classList.toggle("choose");

  if (buttonPressed.classList[0] == "select") {
    total += Number(myArray[1]);
    myVenue.push(Number(myArray[2]));
    mySeats.push(Number(myArray[0]));
  } else if (buttonPressed.classList[0] == "choose") {
    total -= Number(myArray[1]);
    const index = mySeats.indexOf(Number(myArray[0]));
    const indexVenue = myVenue.indexOf(Number(myArray[2]));

    mySeats.splice(index, 1);
    myVenue.splice(index, 1);
  }
  const calculateTotal = document.getElementById("total");
  calculateTotal.value = total.toString();

  const myCollection = [];
  myCollection.push(total, mySeats, myVenue);
  calculateTotal.value = JSON.stringify(myCollection);
}