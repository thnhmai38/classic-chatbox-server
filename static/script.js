var menu = document.getElementById(`main`);
var hidden = document.getElementById(`chino`);

function show() {
    // document.getElementById(`main`).parentElement.removeChild(menu); //Thanks Belikhun, but I don't use it now
    menu.setAttribute("hidden", true); //I love this mod
    hidden.removeAttribute("hidden");
    document.documentElement.requestFullscreen()
}

function hide() {
    hidden.setAttribute("hidden", true); //I love this mod
    menu.removeAttribute("hidden");
    document.exitFullscreen()
}