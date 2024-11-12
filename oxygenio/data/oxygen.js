window.addEventListener("contextmenu", event => event.preventDefault());

window.addEventListener("keydown", (event) => {
    if(["F5", "F12"].includes(event.key)) {
        event.preventDefault()
    }
})