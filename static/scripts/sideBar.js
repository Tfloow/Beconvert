function openNav() {
    document.getElementById("mySidenav").style.width = "100%";
}
  
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

// Function to be triggered when viewport is under 600px
function handleViewportUnder600px() {
    document.getElementById("menu").style.display = "block";
    document.getElementById("hb").style.display = "none";
}

function handleViewportOver600px() {
    document.getElementById("menu").style.display = "none";
    document.getElementById("hb").style.display = "block";
}

// Check viewport width initially and on resize
function checkViewportWidth() {
    if (window.innerWidth < 600) {
        handleViewportUnder600px();
    }
    else if (window.innerWidth > 600){
        handleViewportOver600px();
    }
}

// Initial check
checkViewportWidth();

// Check on window resize
window.addEventListener('resize', checkViewportWidth);