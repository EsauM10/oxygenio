window.addEventListener("contextmenu", event => event.preventDefault());

window.addEventListener("keydown", (event) => {
    if(["F5", "F12"].includes(event.key)) {
        event.preventDefault()
    }
})

const fixedDimensions = !OXYGEN_MAXIMIZE && !OXYGEN_RESIZABLE;
const fixedMaximizedDimensions = OXYGEN_MAXIMIZE && !OXYGEN_RESIZABLE;
const maximizedDimensions = OXYGEN_MAXIMIZE && OXYGEN_RESIZABLE;

function setDimensions() {
    if(fixedDimensions) {
        window.resizeTo(OXYGEN_WIDTH, OXYGEN_HEIGHT);
        window.addEventListener('resize', function() {
            window.resizeTo(OXYGEN_WIDTH, OXYGEN_HEIGHT);
        });
        return;
    }
    
    if(fixedMaximizedDimensions) {
        window.moveTo(0, 0);
        window.resizeTo(screen.availWidth, screen.availHeight);
        window.addEventListener('resize', function() {
            window.resizeTo(screen.availWidth, screen.availHeight);
        });
        return;
    }

    if(maximizedDimensions) {
        window.moveTo(0, 0);
        window.resizeTo(screen.availWidth, screen.availHeight);
        return;
    }

    window.resizeTo(OXYGEN_WIDTH, OXYGEN_HEIGHT);
}

setDimensions()