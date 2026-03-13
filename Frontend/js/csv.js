async function uploadCSV(event) {

  if (event) event.preventDefault();

  const fileInput = document.getElementById("csvFile");
  const resultBox = document.getElementById("result");
  const errorBox = document.getElementById("errorBox");

  errorBox.style.display = "none";
  resultBox.style.display = "none";

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

    console.log("CSV API RESPONSE:", data);

    // If backend returns summary
    if (data.total_records !== undefined) {

      resultBox.style.background = "linear-gradient(90deg, #22d3ee, #06b6d4)";
      resultBox.innerHTML = `
        📄 CSV Processed Successfully<br><br>
        Total Records: <b>${data.total_records}</b><br>
        Normal Users: <b>${data.normal_users}</b><br>
        Suspicious Users: <b>${data.suspicious_users}</b>
      `;

    } 
    // If backend returns list of predictions
    else if (data.results) {

      const total = data.results.length;
      const suspicious = data.results.filter(r => r.prediction === "Suspicious").length;
      const normal = total - suspicious;

      resultBox.style.background = "linear-gradient(90deg, #22d3ee, #06b6d4)";
      resultBox.innerHTML = `
        📄 CSV Processed Successfully<br><br>
        Total Records: <b>${total}</b><br>
        Normal Users: <b>${normal}</b><br>
        Suspicious Users: <b>${suspicious}</b>
      `;
    }

    resultBox.style.display = "block";

  } catch (err) {

    console.error(err);

    errorBox.innerText = "❌ Backend not reachable or error occurred";
    errorBox.style.display = "block";
  }
}