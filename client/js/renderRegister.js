import { url } from "../url.js";

export function renderRegister(element) {
    element.innerHTML = `
        <input type="text" id="register-username" placeholder="Username">
        <input type="email" id="register-email" placeholder="Email">
        <input type="password" id="register-password" placeholder="Password">
        <button id="register-button">Sign Up</button>
    `

    const username = element.querySelector("#register-username")
    const email = element.querySelector("#register-email")
    const password = element.querySelector("#register-password")
    const button = element.querySelector("#register-button")

    const loadingElement = document.createElement("h5")
    element.appendChild(loadingElement)

    button.addEventListener("click", () => {
        if (username.value === "" || email.value === "" || password.value === "") {
            return
        }

        username.disabled = true
        email.disabled = true
        password.disabled = true
        button.disabled = true

        loadingElement.innerHTML = "Loading..."

        fetch(`${url}/users/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username.value,
                email: email.value,
                password: password.value
            })
        })
            .then(res => res.json())
            .then(data => {
                if (!data.id) {
                    loadingElement.innerHTML = "Error"

                    return
                }

                username.value = ""
                email.value = ""
                password.value = ""

                loadingElement.innerHTML = "Success"
            })
            .catch(() =>
                loadingElement.innerHTML = "Error"
            )
            .finally(() => {
                username.disabled = false
                email.disabled = false
                password.disabled = false
                button.disabled = false
            })
    })
}