function checkNews() {
    const newsText = document.getElementById("newsText").value.trim();
    const resultDiv = document.getElementById("result");
    const loader = document.getElementById("loader");

    if (!newsText) {
        alert("Please enter a news headline.");
        return;
    }

    loader.style.display = "block";
    resultDiv.style.display = "none";
    resultDiv.innerHTML = "";

    fetch("https://detect-blix.onrender.com//analyze", {  // 🔹 Updated endpoint
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: newsText }) // 🔹 Ensure key matches Flask API
    })
    .then(response => response.json())
    .then(data => {
        loader.style.display = "none";
        resultDiv.style.display = "block";

        if (data.error) {
            resultDiv.innerHTML = `<p style="color: red;">${data.error}</p>`;
            return;
        }

        let analysis = `<p><strong>AI Analysis:</strong> ${data.analysis}</p>`;

        let newsResults = data.google_results.items;  // 🔹 Updated key to match API response
        if (!newsResults || newsResults.length === 0) {
            resultDiv.innerHTML = `${analysis} <p>No matching news found.</p>`;
            return;
        }

        let tableHTML = `
            <div class="table-container">
                <table>
                    <tr>
                        <th>Title</th>
                        <th>Source</th>
                        <th>Link</th>
                    </tr>`;

        newsResults.forEach(news => {
            tableHTML += `
                <tr>
                    <td>${news.title}</td>
                    <td>${news.displayLink}</td>
                    <td><a href="${news.link}" target="_blank">Read More</a></td>
                </tr>`;
        });

        tableHTML += `</table></div>`;
        resultDiv.innerHTML = `${analysis} ${tableHTML}`;
    })
    .catch(error => {
        loader.style.display = "none";
        resultDiv.style.display = "block";
        resultDiv.innerHTML = `<p style="color: red;">Error fetching results: ${error.message}</p>`;
    });
}
