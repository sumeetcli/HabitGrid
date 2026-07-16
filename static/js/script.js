const themeButton = document.getElementById("theme-btn");
const htmlBody = document.body;

// check if dark mode was saved before
if (localStorage.getItem("isDarkMode") === "true") {
    htmlBody.classList.add("dark");
    themeButton.textContent = "☀️";
}

// toggle dark mode when user clicks button
themeButton.addEventListener("click", function() {
    htmlBody.classList.toggle("dark");
    
    if (htmlBody.classList.contains("dark")) {
        localStorage.setItem("isDarkMode", "true");
        themeButton.textContent = "☀️";
    } else {
        localStorage.setItem("isDarkMode", "false");
        themeButton.textContent = "🌙";
    }
});

document.addEventListener("click", function(event) {
    if (event.target.classList.contains("day")) {
        const date = event.target.getAttribute("date");
        const habitId = event.target.getAttribute("habit-id");
        //console.log("Clicked date:", date);

        event.target.classList.toggle("done");
        
        fetch("/log", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({date: date, habitId: habitId})
        });
    }
});