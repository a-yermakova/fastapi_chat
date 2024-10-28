import { url } from "../url.js";

export function renderLogin() {
    const loginElement = document.createElement("div")
    loginElement.classList.add("column")

    loginElement.innerHTML = `
        <input type="email" id="login-email" placeholder="Email">
        <input type="password" id="login-password" placeholder="Password">
        <button id="login-button">Sign In</button>
    `

    const button = loginElement.querySelector("#login-button")
    const email = loginElement.querySelector("#login-email")
    const password = loginElement.querySelector("#login-password")

    const loadingElement = document.createElement("h5")
    loginElement.appendChild(loadingElement)

    button.addEventListener("click", () => {
        if (email.value === "" || password.value === "") {
            return
        }

        button.disabled = true
        email.disabled = true
        password.disabled = true

        loadingElement.innerHTML = "Loading..."

        fetch(`${url}/users/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email.value,
                password: password.value
            })
        })
            .then(res => res.json())
            .then(data => {
                if (!data.access_token) {
                    button.disabled = false
                    email.disabled = false
                    password.disabled = false
                    loadingElement.innerHTML = "Error"

                    return
                }
                sessionStorage.setItem("user", JSON.stringify(data))
                window.dispatchEvent(new Event("storage"))
            })
            .catch(() => {
                button.disabled = false
                email.disabled = false
                password.disabled = false
                loadingElement.innerHTML = "Error"
            })
    })

    return loginElement
}