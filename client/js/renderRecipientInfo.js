export function renderRecipientInfo(recipient) {
    const recipientInfoElement =  document.createElement("div")
    recipientInfoElement.classList.add("info")

    recipientInfoElement.innerHTML = `<h5>Recipient: ${recipient.username}</h5>`

    const deleteButton = document.createElement("button")
    deleteButton.innerHTML = "Change recipient"
    deleteButton.addEventListener("click", () => {
        sessionStorage.removeItem("recipient")

        window.dispatchEvent(new Event("storage"))
    })

    recipientInfoElement.appendChild(deleteButton)

    return recipientInfoElement
}