const otpValue = document.getElementById("otp_data");
async function noRequestClicked() {
  let resendNow = false;
  console.log(resendNow, "at the top");
  console.log("before await");
  const confirmPayment = document.getElementById("confirmFirst");

  const resendOtp = document.getElementById("resendOtp");

  const myformDisplay = document.getElementById("myform-otp");
  if (confirmPayment.style.display != "none") {
    confirmPayment.style.display = "none";
    myformDisplay.style.display = "block";
    console.log("Inside if block");
    resendOtp.style.display = "inline";
    const response = await fetch("submit");
    console.log("IN fetch");
    const jsonData = await response.json();

    // console.log(jsonData);
    console.log(jsonData.otp);

    json_otp = JSON.parse(jsonData.otp);
    json_otp = json_otp;
    otpValue.value = json_otp;

    console.log(typeof otpValue.value);
    console.log(typeof otpValue);
    console.log(otpValue);
    resendDelay();

    return;
  }
  function resendDelay() {
    console.log("inside the rrsenddelay");
    let timer = setTimeout(function () {
      resendOtp.addEventListener(
        "click",
        function myFunction(event) {
          alert("an otp has been set to your email");
          resendNow = true;
          console.log(resendNow, "inside the settime mode");
          window.clearTimeout(timer);

          insideResend();
        },
        { once: "true" }
      );
    }, 30000);
    console.log("in delaay");
    insideResend();
  }
  async function insideResend() {
    console.log(resendNow, "after reasinging");

    if (!resendNow) {
      console.log(resendNow, "inside timerblock if statement");
      alert("Wait 30 seconds before clicking Resend Otp");
    }
    console.log(resendNow, "outside if all blocks");
    if (resendNow) {
      console.log(resendNow, "in the if block after 30 sec");

      resendNow = false;
      resendDelay();
      const response = await fetch("submit");
      console.log("IN HERE");
      const jsonData = await response.json();
      console.log(jsonData, "thisis data");
      // console.log(jsonData);
      console.log(jsonData.otp);
      console.log("in here");

      // document.getElementById("noRequest").innerHTML = jsonData.number;
    } else {
      console.log("resendNOw is false");
      console.log(resendNow, "else block");
    }
  }
}
console.log("IN HERE");
console.log(otpValue, "inside submit");
function check() {
  let submitOk = false;
  console.log(otpValue, "this is value put side if all blocks");
  const userOtp = document.getElementById("otp-password").value;
  console.log(userOtp, "this vaue can ypup see");

  console.log(typeof otpValue);
  console.log(typeof userOtp);
  if (otpValue.value == userOtp && userOtp != "") {
    submitOk = true;

    return submitOk;
  } else {
    alert("Entered wrong OTP");

    console.log("wrong OTP");
    return submitOk;
  }
}
