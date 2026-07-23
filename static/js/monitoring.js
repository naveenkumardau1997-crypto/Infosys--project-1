// -------------------------------------
// Browser Activity Monitoring
// -------------------------------------

function logEvent(message) {
    console.log(message);

    fetch("/log_event", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            event: message
        })
    });
}

// -------------------------------------
// Tab Switch Detection
// -------------------------------------

document.addEventListener("visibilitychange", function () {

    if (document.hidden) {

        logEvent("Tab Switched");

    } else {

        logEvent("Returned to Exam");
    }

});

// -------------------------------------
// Window Focus Detection
// -------------------------------------

window.addEventListener("blur", function () {

    logEvent("Window Lost Focus");

});

window.addEventListener("focus", function () {

    logEvent("Window Focused");

});

// -------------------------------------
// Right Click Detection
// -------------------------------------

document.addEventListener("contextmenu", function (e) {

    e.preventDefault();

    logEvent("Right Click Detected");

});

// -------------------------------------
// Copy Detection
// -------------------------------------

document.addEventListener("copy", function () {

    logEvent("Copy Attempt");

});

// -------------------------------------
// Paste Detection
// -------------------------------------

document.addEventListener("paste", function () {

    logEvent("Paste Attempt");

});

// -------------------------------------
// Keyboard Shortcut Detection
// -------------------------------------

document.addEventListener("keydown", function (e) {

    // Ctrl + C
    if (e.ctrlKey && e.key.toLowerCase() === "c") {

        logEvent("Ctrl + C");

    }

    // Ctrl + V
    if (e.ctrlKey && e.key.toLowerCase() === "v") {

        logEvent("Ctrl + V");

    }

    // Ctrl + X
    if (e.ctrlKey && e.key.toLowerCase() === "x") {

        logEvent("Ctrl + X");

    }

    // Ctrl + A
    if (e.ctrlKey && e.key.toLowerCase() === "a") {

        logEvent("Ctrl + A");

    }

    // F12
    if (e.key === "F12") {

        e.preventDefault();

        logEvent("Developer Tools Attempt");

    }

     // ----------------------
     // Live Dashboard Update
     // ----------------------

     function loadDashboard(){

     fetch("/dashboard_data")

     .then(response => response.json())

     .then(data => {

        if (data.level === "HIGH") {

            showAlert("🚨 High Risk Activity Detected!");
        
        }
        else if (data.level === "MEDIUM") {
        
            showAlert("⚠ Suspicious Activity Detected!");
        
        }

        document.getElementById("riskScore").innerHTML = data.score;

        document.getElementById("riskLevel").innerHTML = data.level;

        let list = document.getElementById("eventList");

        list.innerHTML = "";

        data.events.slice().reverse().forEach(event=>{

            list.innerHTML += `
                <li>
                    ${event.event}
                    (+${event.points})
                </li>
            `;

        });

    });

}

setInterval(loadDashboard,1000);

// ----------------------
// Live Dashboard Update
// ----------------------

function loadDashboard() {

    fetch("/dashboard_data")
        .then(response => response.json())
        .then(data => {

            document.getElementById("riskScore").innerHTML = data.score;
            document.getElementById("riskLevel").innerHTML = data.level;

            let list = document.getElementById("eventList");
            list.innerHTML = "";

            data.events.slice().reverse().forEach(event => {

                list.innerHTML += `
                    <li>${event.event} (+${event.points})</li>
                `;

            });

        });

}

// Load immediately
loadDashboard();

// Refresh every second
setInterval(loadDashboard, 1000);

// -----------------------------
// Live Alert System
// -----------------------------

function showAlert(message) {

    let alertBox = document.createElement("div");

    alertBox.className = "alert-box";

    alertBox.innerHTML = message;

    document.body.appendChild(alertBox);

    setTimeout(() => {

        alertBox.remove();

    }, 3000);

}

});