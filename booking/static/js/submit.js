const otpValue = document.getElementById("otp_data").value;
function check() {
  let submitOk = false;
  console.log(typeof otpValue);
  const userOtp = document.getElementById("password").value;
  console.log(typeof userOtp);
  if (otpValue == userOtp) {
    submitOk = true;

    return submitOk;
  } else {
    alert("Entered wrong OTP");

    console.log("wrong OTP");
    return submitOk;
  }
}
