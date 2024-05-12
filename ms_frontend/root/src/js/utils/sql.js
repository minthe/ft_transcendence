
function containsSQLInjection(input) {
    const injectionChars = ["'", '"', ';', '--', '/*', '*/', '*', '%', '&', '|', '+', '-', '/', '\\', '=', '!', '?'
								, ':', '_', '[', ']', '{', '}', '(', ')', '<', '>', '\n', '\r', '\t', '\v', '\f', '\0'];
    const sqlKeywords = ["SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "UNION", "OR", "AND", "WHERE"];
    const lowercaseInput = input.toLowerCase();

    for (let char of injectionChars) {
        if (lowercaseInput.includes(char))
            return true;
    }
    for (let keyword of sqlKeywords) {
        if (lowercaseInput.includes(keyword.toLowerCase()))
            return true;
    }
    return false;
}

function sqlCheckLogin(usernameElement, passwordElement) {
    if (containsSQLInjection(usernameElement.value) || containsSQLInjection(passwordElement.value)) {
        clearLoginInput(usernameElement, passwordElement);
        document.getElementById("wrong-password").innerHTML = "Entered not allowed input!";
        return true;
    }
    return false;
}

function sqlCheckRegister(usernameElement, passwordElement, mail) {
    if (containsSQLInjection(usernameElement.value) || containsSQLInjection(passwordElement.value)
    || containsSQLInjection(mail.value)) {
        clearRegisterInput(usernameElement, passwordElement, mail);
        document.getElementById("wrong-register").innerHTML = "Entered not allowed input!";
        return true;
    }
    return false;
}
