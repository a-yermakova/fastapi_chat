import { url } from "../url.js";

export function renderAvailableRecipients() {
    const availableRecipientsElement = document.createElement("ul")
    availableRecipientsElement.innerHTML = `<h5>Loading...</h5>`

    fetch(`${url}/users`, {
        headers: {
            "ngrok-skip-browser-warning": true,
            "Authorization": "Bearer " + JSON.parse(sessionStorage.getItem("user")).access_token
        }
    })
        .then(res => res.json())
        .then(data => {
            availableRecipientsElement.innerHTML = data.map(recipient => `<li class="recipient">${recipient.username}</li>`).join("")

            availableRecipientsElement.querySelectorAll(".recipient").forEach(element => {
                element.addEventListener("click", (event) => {
                    sessionStorage.setItem("recipient", JSON.stringify(
                        data.find(user => user.username === event.target.innerText)
                    ))

                    window.dispatchEvent(new Event("storage"))
                })
            })})
        .catch(() => availableRecipientsElement.innerHTML = `<h5>Error loading recipients, please reload the page</h5>`)

    return availableRecipientsElement
}