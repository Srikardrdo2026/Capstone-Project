async function analyzeUser() {
  const errorBox = document.getElementById("errorBox");
  const resultBox = document.getElementById("result");
  const loader = document.getElementById("loader");
  const btn = document.getElementById("scanBtn");

  errorBox.style.display = "none";
  resultBox.style.display = "none";

  const hour = Number(document.getElementById("login_hour").value);
  if (hour < 0 || hour > 23) {
    errorBox.innerText = "⚠️ Login hour must be between 0 and 23";
    errorBox.style.display = "block";
    return;
  }

  const sessionDuration = Number(document.getElementById("session_duration").value);
  const failedLogins = Number(document.getElementById("failed_logins").value);
  const typingSpeed = Number(document.getElementById("typing_speed").value);
  const protocol = document.getElementById("protocol").value;
  const commandsCount = Number(document.getElementById("commands").value);

  if (sessionDuration < 0 || failedLogins < 0 || typingSpeed < 0 || commandsCount < 0) {
    errorBox.innerText = "⚠️ Numeric fields must be non-negative";
    errorBox.style.display = "block";
    return;
  }

  const commandsArray = Array(commandsCount).fill("cmd");

  const payload = {
    login_time: hour.toString().padStart(2, "0") + ":00",
    session_duration: sessionDuration,
    commands: commandsArray,
    failed_logins: failedLogins,
    protocol: protocol,
    typing_speed: typingSpeed
  };

  btn.disabled = true;
  loader.style.display = "block";

  try {
    const res = await fetch(
      "https://behavioral-fingerprinting-backend.onrender.com/api/predict",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      }
    );

    if (!res.ok) throw new Error("Server error");

    const data = await res.json();

    resultBox.style.background =
      data.prediction === "Suspicious"
        ? "linear-gradient(90deg, #ec4899, #be185d)"
        : "linear-gradient(90deg, #22d3ee, #06b6d4)";

    resultBox.innerHTML = `
      ${data.prediction === "Suspicious" ? "🚨" : "✅"} ${data.prediction}<br>
      Confidence: ${data.confidence}
    `;
    resultBox.style.display = "block";

  } catch {
    errorBox.innerText = "❌ Backend not reachable or error occurred";
    errorBox.style.display = "block";
  }

  loader.style.display = "none";
  btn.disabled = false;
}
