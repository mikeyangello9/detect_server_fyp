import { io } from "https://cdn.socket.io/4.4.1/socket.io.esm.min.js";

const socket = io("http://localhost:8000")
const alertList = document.querySelector(".alert-list")

socket.on("connect", () => {
    console.log("connected to server");
})

socket.on("Alert", (data) => {
    console.log("receive alert: ", data.message)

    const now = new Date();
    const time = now.toLocaleTimeString();
    const date = now.toLocaleDateString();

    const listOfAlerts = document.createElement("li")
    listOfAlerts.textContent = `${data.message} on ${time} ${date}`
    alertList.prepend(listOfAlerts)
    
})

