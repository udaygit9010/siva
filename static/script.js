async function checkNews() {
    let newsText = document.getElementById("newsInput").value;
    let resultDiv = document.getElementById("result");
    let loader = document.getElementById("loader");

    if (!newsText) {
        alert("⚠️ Please enter news text!");
        return;
    }

    // Show loader while waiting for response
    loader.style.display = "block";
    resultDiv.style.display = "none";

    let response = await fetch("https://news-det.onrender.com/predict", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `news_text=${encodeURIComponent(newsText)}`
    });

    let data = await response.json();
    loader.style.display = "none";  // Hide loader
    resultDiv.style.display = "block";  // Show result

    resultDiv.innerHTML = `
        <p><strong>🧠 AI Analysis:</strong> ${data.AI_Analysis}</p>
        <p><strong>🔗 Trusted Sources:</strong></p>
        <ul>
            ${data.Trusted_News_Links.map(link => `<li><a href="${link.link}" target="_blank">${link.title}</a></li>`).join('')}
        </ul>
    `;
}
