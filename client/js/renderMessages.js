import { url } from "../url.js";

export function renderMessages(user, recipient) {
    const chatElement = document.createElement("div")
    chatElement.classList.add("messages-block")

    const loadingElement = document.createElement("h5")
    chatElement.appendChild(loadingElement)

    loadingElement.innerHTML = "Loading..."

    fetch(`${url}/messages/history/${recipient.id}`, {
        headers: {
            "ngrok-skip-browser-warning": true,
            "Authorization": "Bearer " + user.access_token
        }
    })
        .then(res => res.json())
        .then(data => {
            chatElement.innerHTML = data.map(message => `
                <span class="${message.recipient_id === Number(recipient.id) ? 'sent' : 'received'}">${message.content}</span>
            `).join("")
        })
        .catch(() => {
            loadingElement.innerHTML = "Error"
        })

    return chatElement
}