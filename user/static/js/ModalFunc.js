function generateOTP() {
          
    // Declare a digits variable 
    // which stores all digits
    var digits = '0123456789';
    let OTP = '';
    for (let i = 0; i < 6; i++ ) {
        OTP += digits[Math.floor(Math.random() * 10)];
    }
    return OTP;
}
  
// document.write("OTP of 6 digits: ")
// document.write( generateOTP() );
let o = "";
var sendOTP = function(){
  otp=generateOTP();
  o = otp;
  msg="To verify your otp for MediStop, kindly enter the otp"+otp+".";
  // number lelena yaha
  number= document.getElementById("floatingPhone").value;
  console.log(otp)
  var settings = {
      "async": true,
      "crossDomain": true,
      "url": "https://www.fast2sms.com/dev/bulkV2?authorization=GPhaYo5Xmngz9WudTE6HJIMLfrDwtpkOKiZF7qb8VcjCxNA3sl4tXkvEKbyQPdh6zwLDIqABH23TVFmR&sender_id=TXTIND&message="+msg+"&route=v3&numbers="+number,
      "method": "GET"
    }
    
    $.ajax(settings).done(function (response) {
      console.log(response);
  });
}

// pass check
var check = function () {
    if (document.getElementById('floatingPassword').value ==
      document.getElementById('floatingCPassword').value) {
      document.getElementById('message').style.color = 'green';
      document.getElementById('message').innerHTML = 'matching';
      next();
    } else {
      document.getElementById('message').style.color = 'red';
      document.getElementById('message').innerHTML = 'not matching';
    }
  }


  // phone check
  var pass =/^.{8,}$/
  var em = /^[a-zA-Z0-9.!#$%&’+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)$/;
  var phoneno = /^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$/;
  var pcheck = function () {

    if (document.getElementById('floatingPhone').value.match(phoneno)) {
      document.getElementById('pmessage').innerHTML = '';
      otp();

    } else {
      document.getElementById('pmessage').style.color = 'red';
      document.getElementById('pmessage').innerHTML = 'Enter a 10 digit valid Phone number';
    }
  }

  var otp = function () {
    if ((document.getElementById('floatingPassword').value ==
      document.getElementById('floatingCPassword').value) && (document.getElementById('floatingPhone').value.match(phoneno))
      && (document.getElementById('floatingPassword').value && document.getElementById('floatingCPassword').value && document.getElementById('floatingPhone').value && document.getElementById('floatingInput').value && document.getElementById('floatingInputName').value !== "")) {

        document.getElementById("buttonOTP").style.display= "inline";
        document.getElementById("button1").style.display= "none";


    }
  }

  var next = function () {
    if ((document.getElementById('floatingPassword').value ==
      document.getElementById('floatingCPassword').value) && (document.getElementById('floatingInput').value.match(em)) && (document.getElementById('floatingInput').value.match(pass))
      && (document.getElementById('floatingPassword').value && document.getElementById('floatingCPassword').value && document.getElementById('floatingInput').value && document.getElementById('floatingInputName').value !== "")) {

        document.getElementById("buttonNext").disabled = false;


    }
  }

  var enablephone = function(){
      document.getElementById("1").style.display= "none";
      document.getElementById("2").style.display= "inline";

  }

  var prev = function(){
      document.getElementById("1").style.display= "inline";
      document.getElementById("2").style.display= "none";
      document.getElementById("buttonNext").disabled = false;
  }



var otpcheck = function(){
  if (document.getElementById('floatingOTP').value.match(o)) {
      document.getElementById('otpmessage').style.color = 'green';
      document.getElementById('otpmessage').innerHTML = 'Verified';
      document.getElementById("buttonOTP").style.display= "none";
      document.getElementById("buttonPrev").style.display= "none";
      document.getElementById("button1").style.display= "inline";
      document.getElementById("button1").disabled = false
    } else {
      document.getElementById('otpmessage').style.color = 'red';
      document.getElementById('otpmessage').innerHTML = 'incorrect';
    }
  }


  // EMAIL VALIDATION
  var em = /^[a-zA-Z0-9.!#$%&’+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)$/;
  var echeck = function () {

    if (document.getElementById('floatingInput').value.match(em)) {
      document.getElementById('emmessage').innerHTML = '';
     
    } else {
      document.getElementById('emmessage').style.color = 'red';
      document.getElementById('emmessage').innerHTML = 'Enter a valid EmailID';
    }
  }

  var passcheck = function () {

if (document.getElementById('floatingPassword').value.match(pass)) {
document.getElementById('passmessage').innerHTML = '';

} else {
document.getElementById('passmessage').style.color = 'red';
document.getElementById('passmessage').innerHTML = 'Enter a minimum 8 digit password';
}
}

function reset() {
    // document.getElementById("LfloatingInput").type = "email";
    // document.getElementById("LLfloatingInput").placeholder = "ENTER YOUR EMAIL-ID";
    // document.getElementById("Llabelemail").innerHTML = "Enter your registered Email-Id";
    document.getElementById("loginform").action = "reset";
    document.getElementById("LfloatingPassword").value = "-";
    document.getElementById("LfloatingPassword").style.display = "none";
    document.getElementById("Llabelpassword").style.display = "none";
    document.getElementById("forgot").style.display = "none";
    document.getElementById("Lbutton1").innerHTML = "Reset Password";
    
}
