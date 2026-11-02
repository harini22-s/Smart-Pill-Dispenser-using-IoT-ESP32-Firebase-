document.getElementById("schedule-form").addEventListener("submit", function (event) {
    event.preventDefault();

    let newSchedule = {
        "time1": document.getElementById("time1").value,
        "time2": document.getElementById("time2").value,
        "time3": document.getElementById("time3").value,
        "time4": document.getElementById("time4").value
    };

    fetch("/set_schedule", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newSchedule)
    }).then(response => {
        if (response.ok) {
            alert("Schedule updated successfully!");
            fetchSchedule();
        } else {
            alert("Error updating schedule.");
        }
    });
});

function fetchSchedule() {
    fetch('/get_schedule')
        .then(response => response.json())
        .then(data => {
            // Update dispense_status table
            let tableRows = "";
            for (let key in data.dispense_status) {
                let details = data.dispense_status[key];
                let dispensed = details.dispensed ? "✅" : "❌";
                let taken = details.taken ? "✅" : "❌";
                tableRows += `<tr><td>${key} (${details.time})</td><td>${dispensed}</td><td>${taken}</td></tr>`;
            }
            document.querySelector("table").innerHTML = `
                <tr><th>Time</th><th>Dispensed</th><th>Taken</th></tr>` + tableRows;

            // Update missed_doses (skip any value like "none")
            let missedDoses = [];
            if (data.alerts && data.alerts.missed_doses) {
                Object.entries(data.alerts.missed_doses).forEach(([key, timeKey]) => {
                    if (timeKey === "none") return;

                    const timeData = data.dispense_status[timeKey];
                    if (timeData && timeData.time) {
                        missedDoses.push(`<li>${timeKey} - ${timeData.time}</li>`);
                    } else {
                        missedDoses.push(`<li>${timeKey} - (time unknown)</li>`);
                    }
                });

            }

            document.getElementById("missed-doses").innerHTML = missedDoses.length
                ? missedDoses.join("")
                : "<li>None</li>";
        })
        .catch(error => console.error("Error fetching schedule:", error));
}

// Auto refresh every 3 seconds
setInterval(fetchSchedule, 3000);
