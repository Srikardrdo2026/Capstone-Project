let chart;

async function analyzeWebsite() {
  const errorBox = document.getElementById("errorBox");
  const website = document.getElementById("website").value.trim();
  const numUsers = Number(document.getElementById("num_users").value);

  errorBox.style.display = "none";

  if (!website || numUsers <= 0) {
    errorBox.innerText = "⚠️ Please enter a valid website URL and user count";
    errorBox.style.display = "block";
    return;
  }

  try {
    const res = await fetch(
      "https://behavioral-fingerprinting-backend.onrender.com/api/analyze-website",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          website: website,
          num_users: numUsers
        })
      }
    );

    if (!res.ok) throw new Error("Server error");

    const data = await res.json();

    const ctx = document.getElementById("chart").getContext("2d");
    if (chart) chart.destroy();

    chart = new Chart(ctx, {
      type: "pie",
      data: {
        labels: ["Normal", "Suspicious"],
        datasets: [{
          data: [
            Number(data.normal_percent),
            Number(data.suspicious_percent)
          ],
          backgroundColor: ["#22d3ee", "#ec4899"]
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: "bottom" },
          tooltip: {
            callbacks: {
              label: (context) => `${context.label}: ${context.raw}%`
            }
          }
        }
      }
    });

  } catch {
    errorBox.innerText = "❌ Backend not reachable or error occurred";
    errorBox.style.display = "block";
  }
}
