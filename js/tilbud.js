const form = document.querySelector('#frm-tilbud');
const submitBtn = document.querySelector('#btn-submit');

const messageInput = document.getElementById('message');
const charCount = document.getElementById('charCount');
const maxCharacters = 500;

charCount.textContent = `(maks. ${maxCharacters})`;

messageInput.addEventListener('input', () => {
    const remaining = maxCharacters - messageInput.value.length;
    charCount.textContent = `${remaining} tegn tilbage`;

    if (remaining <= 0) {
        messageInput.value = messageInput.value.slice(0, maxCharacters);
        charCount.textContent = `0 tegn tilbage`; // Optional: Update the text to show 0 remaining
    }
}); 

form.addEventListener('submit', function(event) {

    event.preventDefault();

    const isValid = validateForm(event);    

    if(!isValid) {
        console.log('validation failed');
        return false;
    } else {
        // Manually trigger the library to send the request to /tilbud after validation
        submitBtn.setAttribute('mix-post', '/tilbud');
        
        mixhtml(submitBtn); // Now, the library takes over and handles the form submission        
    }    
});

function prepareUserData(event)
{
    const formData = new FormData(event.target);

    const data = {
        name: formData.get('name').trim(),
        email: formData.get('email').trim(),
        password: formData.get('password')
    };
    
    return data;
}

function validateForm(event)
{        
    let isValid = false;                    

    const formData = new FormData(event.target);
    const answer = formData.get('question');

    const errorSpan = document.querySelector('#question-error');
    if(answer != 5) {        
        errorSpan.classList.add('error');
        errorSpan.innerText = "Forkert svar";
        return false;
    } else {
        errorSpan.classList.remove('error');
        errorSpan.innerText = "";
    }
    
    const name = formData.get('name');
    const email = formData.get('email');
    const phone = formData.get('phone');
    const postno = formData.get('postno');
    const city = formData.get('city');
    const message = formData.get('message');        

    const isValidName = validateName(name);
    const isValidEmail = validateEmail(email);
    const isValidPhone = validatePhone(phone);
    const isValidPostNo = validatePostNummer(postno);
    const isValidCity = validateCity(city);
    const isValidMessage = validateMessage(message, maxCharacters)

    if(isValidName && isValidEmail && isValidPhone && isValidPostNo && isValidCity && isValidMessage) {
        isValid = true;
    }    

    return isValid;
    
}

function validateName(name)
{
    const userNameRegex = /^[a-zA-Z_ ]{3,20}$/;

    const errorSpan = document.querySelector('#name-error');
    let isValid = true;

    if (name.length < 2 || name.length > 20 || !userNameRegex.test(name)) {
        // Handle too short input
        errorSpan.classList.add('error');
        errorSpan.innerText = "Angiv et gyldigt navn.";
        isValid = false;    
    } else {
        // If valid
        errorSpan.classList.remove('error');
        errorSpan.innerText = "";
    }

    return isValid;
}

function validateEmail(email)
{
    const userEmailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; 
    const errorSpan = document.querySelector('#email-error');
    let isValid = true;

    if (!userEmailRegex.test(email)) {
        // Handle too short input
        errorSpan.classList.add('error');
        errorSpan.innerText = "Angiv et gyldigt e-mail.";
        isValid = false;    
    } else {
        // If valid
        errorSpan.classList.remove('error');
        errorSpan.innerText = "";
    }

    return isValid;
}

function validatePhone(phone)
{
    const danishPhonePattern = /^(?:(?:\+45)?[\s-]?)?(?:[2-9]{1}\d{1})[\s-]?\d{2}[\s-]?\d{2}[\s-]?\d{2}$/;
    const errorSpan = document.querySelector('#phone-error');
    let isValid = true;

    if (!danishPhonePattern.test(phone)) {
        // Handle too short input
        errorSpan.classList.add('error');
        errorSpan.innerText = "Angiv et gyldigt telefon nummer.";
        isValid = false;    
    } else {
        // If valid
        errorSpan.classList.remove('error');
        errorSpan.innerText = "";
    }

    return isValid;
}

function validatePostNummer(postno)
{
    const danishPostalCodePattern = /^(?:[1-9]\d{3})$/;
    const errorSpan = document.querySelector('#postno-error');
    let isValid = true;

    if (!danishPostalCodePattern.test(postno)) {
        // Handle too short input
        errorSpan.classList.add('error');
        errorSpan.innerText = "Angiv et gyldigt post nr.";
        isValid = false;    
    } else {
        // If valid
        errorSpan.classList.remove('error');
        errorSpan.innerText = "";
    }

    return isValid;
}

function validateCity(city)
{
    const danishCityNamePattern = /^[a-zA-ZæøåÆØÅ\s-]+$/;
    const errorSpan = document.querySelector('#city-error');
    let isValid = true;

    if (!danishCityNamePattern.test(city)) {
        // Handle too short input
        errorSpan.classList.add('error');
        errorSpan.innerText = "Angiv et gyldigt by.";
        isValid = false;    
    } else {        
        errorSpan.classList.remove('error');
        errorSpan.innerText = "";
    }

    return isValid;
}

function validateMessage(message, maxCharacters) 
{
    const messageInput = document.querySelector('#message');
    
    const errorSpan = document.querySelector('#message-error');

    let isValid = true;
    
    if (message.length > maxCharacters) {
        errorSpan.classList.add('error');
        errorSpan.innerText = "Din besked må ikke overstige 500 tegn.";
        isValid = false;
    } else {
        errorSpan.classList.remove('error');
        errorSpan.innerText = "";
    }

    return isValid;
}
