import { renderChat } from "./js/renderChat.js";
import { renderRegister } from "./js/renderRegister.js";
import './style.css'

document.querySelector('#app').innerHTML = `
    <h1>Chat</h1>
    <div class="column" id="register"></div>
    <div id="chat"></div>
`

const chatElement = document.querySelector("#chat")

renderRegister(document.querySelector("#register"))
renderChat(chatElement)

window.addEventListener('storage', () => {
    chatElement.innerHTML = ``
    renderChat(chatElement)
})