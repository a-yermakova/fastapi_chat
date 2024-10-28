import { wsUrl } from "../url.js";

export function waitForNewMessages(messagesListElement, user, recipient) {
    const websocket = new WebSocket(`${wsUrl}/messages/ws/${user.access_token}`);

    websocket.onopen = () => {
        console.log("Connected to the server");
    };

    websocket.onmessage = (event) => {
        const data = JSON.parse(event.data)
        if (recipient.id !== data.sender_id) {
            return
        }

        const newMessageElement = document.createElement("span")
        newMessageElement.classList.add("received")
        newMessageElement.innerHTML = data.content

        messagesListElement.appendChild(newMessageElement)
        newMessageElement.scrollIntoView()
    };

    websocket.onclose = () => {
        console.log("Disconnected from the server");
    };

    websocket.onerror = (error) => {
        console.error("WebSocket error:", error);
    };
}