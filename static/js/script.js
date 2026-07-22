const themeButton = document.getElementById("theme-btn");
const htmlBody = document.body;

// check if dark mode was saved before

// javascript local storage feature
// escape from writing many SQL queries
// AI citation: Asked AI about how to store theme preference in browser localStorage instead of database
if (localStorage.getItem("isDarkMode") === "true") {
    htmlBody.classList.add("dark");
    //console.log(localStorage.getItem("isDarkMode") != "false")
    themeButton.textContent = "☀️";
}

// toggle dark mode when user clicks button
// AI citation: Asked AI about building a simple dark mode toggle.
themeButton.addEventListener("click", function() {
    htmlBody.classList.toggle("dark");
    
    if (htmlBody.classList.contains("dark")) {
        localStorage.setItem("isDarkMode", "true");
        themeButton.textContent = "☀️";
    }
    else {
        localStorage.setItem("isDarkMode", "false");
        themeButton.textContent = "🌙";
    }
});

document.addEventListener("click", function(event) {
    if (event.target.classList.contains("day") && !event.target.classList.contains("future")) {
        const date = event.target.getAttribute("date");
        const habitId = event.target.getAttribute("habit-id");
        //console.log("Clicked date:", date);

        event.target.classList.toggle("done");

        // AI citation: Asked AI about how to add a quick scale animation for click feedback
        event.target.animate([
            { transform: "scale(1)" },
            { transform: "scale(1.2)" },
            { transform: "scale(1)" }
        ],{ duration: 200 });
        
        fetch("/log", {
            method:"POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify({date: date, habitId: habitId})
        });
    }
});
