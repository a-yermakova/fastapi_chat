import { url } from "../url.js";

export function renderInputMessage(messagesListElement, user, recipient) {
    const inputElement = document.createElement("div")
    inputElement.classList.add("input-line")

    inputElement.innerHTML = `
        <input type="text" id="message-input">
        <button id="send-message-button">Send</button>
    `

    const sendMessageButton = inputElement.querySelector("#send-message-button")
    const messageInput = inputElement.querySelector("#message-input")

    sendMessageButton.addEventListener("click", async () => {
        const message = messageInput.value

        if (message === "") {
            return
        }

        sendMessageButton.disabled = true
        messageInput.disabled = true

        fetch(`${url}/messages/send`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${user.access_token}`
            },
            body: JSON.stringify({
                recipient_id: recipient.id,
                content: message
            })
        })
            .then((res) => res.json())
            .then((data) => {
                const newMessageElement = document.createElement("span")
                newMessageElement.classList.add("sent")
                newMessageElement.innerHTML = data.content

                messagesListElement.appendChild(newMessageElement)
                newMessageElement.scrollIntoView()

                messageInput.value = ""
            })
            .catch((err) => {
                console.error(err)
            })
            .finally(() => {
                sendMessageButton.disabled = false
                messageInput.disabled = false
            })
    })

    return inputElement
}