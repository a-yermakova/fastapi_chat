import { url } from "../url.js";

export function renderUserInfo(user) {
    const userInfoElement = document.createElement("div")
    userInfoElement.classList.add("info")

    userInfoElement.innerHTML = `<h5>Current user: ${user.username}</h5>`

    const logoutButton = document.createElement("button")
    logoutButton.innerHTML = "Sign Out"

    logoutButton.addEventListener("click", () => {
        logoutButton.disabled = true

        fetch(`${url}/users/logout`, {
            method: "POST",
            headers: {
                "Authorization": "Bearer " + user.access_token
            }
        })
            .then(() => {
                sessionStorage.clear()
                window.dispatchEvent(new Event("storage"))
            })
            .catch(() => {
                logoutButton.disabled = false
            })
    })

    userInfoElement.appendChild(logoutButton)

    return userInfoElement
}