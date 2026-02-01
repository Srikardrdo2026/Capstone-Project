async function uploadCSV() {
  const fileInput = document.getElementById("csvFile");
  const resultBox = document.getElementById("result");
  const errorBox = document.getElementById("errorBox");

  // Reset UI
  errorBox.style.display = "none";
  resultBox.style.display = "none";

  // Validation
  if (!fileInput.files.length) {
    errorBox.innerText = "⚠️ Please select a CSV file before uploading";
    errorBox.style.display = "block";
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    const res = await fetch("http://127.0.0.1:5000/api/predict-csv", {
      method: "POST",
      body: formData
    });

    if (!res.ok) {
      throw new Error("Server error");
    }

    const data = await res.json();

    resultBox.style.background = "linear-gradient(90deg, #22d3ee, #06b6d4)";
    resultBox.innerHTML = `
      📄 CSV Processed Successfully<br>
      Total Records: ${data.total_records}<br>
      Normal Users: ${data.normal_users}<br>
      Suspicious Users: ${data.suspicious_users}
    `;
    resultBox.style.display = "block";

  } catch (err) {
    errorBox.innerText = "❌ Backend not reachable or error occurred";
    errorBox.style.display = "block";
  }
}
