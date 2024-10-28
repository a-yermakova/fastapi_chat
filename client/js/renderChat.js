import { renderLogin } from "./renderLogin.js";
import { renderUserInfo } from "./renderUserInfo.js";
import { renderRecipientInfo } from "./renderRecipientInfo.js";
import { renderAvailableRecipients } from "./renderAvailableRecipients.js";
import { renderMessages } from "./renderMessages.js";
import { renderInputMessage } from "./renderInputMessage.js";
import { waitForNewMessages } from "./waitForNewMessages.js";

export function renderChat(element) {
    const user = JSON.parse(sessionStorage.getItem("user"))

    if (!user) {
        element.appendChild(renderLogin())

        return
    }

    element.appendChild(renderUserInfo(user))

    const recipient = JSON.parse(sessionStorage.getItem("recipient"))

    if (!recipient) {
        element.appendChild(renderAvailableRecipients())

        return
    }

    element.appendChild(renderRecipientInfo(recipient))

    const messagesBlock = renderMessages(user, recipient)
    element.appendChild(messagesBlock)

    element.appendChild(renderInputMessage(messagesBlock, user, recipient))

    waitForNewMessages(messagesBlock, user, recipient)
}