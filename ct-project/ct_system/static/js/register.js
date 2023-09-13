const usernameField = document.querySelector('#username');
const feedBackArea=document.querySelector('.invalid-feedback');
const emailField=document.querySelector('#email');
const emailFeedBackArea=document.querySelector('.emailFeedbackArea');
const usernameSuccessOutput=document.querySelector(".username-success");


usernameField.addEventListener("keyup", (e) => {

    const usernameVal = e.target.value;

    usernameSuccessOutput.style.display='block';

    usernameSuccessOutput.textContent = `Checando ${usernameVal}`;

    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display = "none";


    if (usernameVal.length > 0) {
        fetch('/auth/validate-username', {
        body: JSON.stringify({ username: usernameVal }),
        method: "POST",
    }).then(res=>res.json()).then(data=>{
        console.log('data', data);
        usernameSuccessOutput.style.display='none';
        if (data.username_error) {
            //usernameSuccessOutput.style.display='none';
            usernameField.classList.add("is-invalid");
            feedBackArea.style.display = "block";
            feedBackArea.innerHTML=`<p>${data.username_error}</p>`
        }
    });
    }
    


});

emailField.addEventListener('keyup', (e)=> {

    const emailVal = e.target.value;

    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display = "none";


    if (emailVal.length > 0) {
        fetch('/auth/validate-email', {
        body: JSON.stringify({ email: emailVal }),
        method: "POST",
    }).then(res=>res.json()).then(data=>{
        console.log('data', data);
        if (data.email_error) {
            emailField.classList.add("is-invalid");
            emailFeedBackArea.style.display = "block";
            emailFeedBackArea.innerHTML=`<p>${data.email_error}</p>`
        }
    });
    }
    

});