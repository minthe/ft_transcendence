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

