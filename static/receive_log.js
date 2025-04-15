import { io } from "https://cdn.socket.io/4.4.1/socket.io.esm.min.js";

const socket = io("http://localhost:8000")

socket.on("connect", () => {
    console.log("connected to server");
})

socket.on("Alert", (data) => {
    console.log("receive alert: ", data.message)
    
})

