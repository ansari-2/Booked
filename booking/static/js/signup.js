
function validation() {
    submitOK = true;
    checkname();
    checkpassword();
    checkphone();
    if (submitOK === false) {
      return false;
    }
  }
  function checkname() {
    const username = document.getElementById("username").value;
    if (username.length > 150) {
      alert("usename cannot be more than 150 characters");
      submitOK = false;
    }
  }
  function checkpassword() {
    let check = false;
    const pass1 = document.getElementById("password1").value;
    const pass2 = document.getElementById("password2").value;
    let passString = pass1.toString();
    console.log(passString.length);
    console.log(pass1);
    if (pass1 != pass2) {
      alert("passwords donot match");
      submitOK = false;
    } else if (pass1.length < 8) {
      alert("password should be 8 characters long");
      submitOK = false;
    } else {
      const alpha =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz@.+-_";
      let arr = [];
      for (let i = 0; i < alpha.length; i++) {
        arr.push(alpha[i]);
      }
      console.log(arr, "this is an array");

      for (let i = 0; i < passString.length; i++) {
        if (arr.includes(pass1[i])) {
          console.log(pass1[i]);
          submitOK = true;
          check = true;
          break;
        }
      }
      console.log(check);
      if (check != true) {
        alert("password should contain atleast 1 character");
        submitOK = false;
      }
    }
  }

  function checkphone() {
    const phone = document.getElementById("phone").value;
    if (phone.length != 10) {
      alert("enter a 10 digit phone number ");
      submitOK = false;
    }
  }