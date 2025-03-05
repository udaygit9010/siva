function checkNews() {
    let newsText = document.getElementById("news_input").value;
    let responseDiv = document.getElementById("response");

    if (newsText.trim() === "") {
        responseDiv.innerHTML = "<p style='color: red;'>⚠️ Please enter news text.</p>";
        return;
    }

    responseDiv.innerHTML = "<p>⏳ Checking for fake news...</p>";

    fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ news_text: newsText })
    })
    .then(response => response.json())
    .then(data => {
        responseDiv.innerHTML = `<p>🧠 ChatGPT Response: ${data.chatgpt_response}</p>`;
    })
    .catch(error => {
        responseDiv.innerHTML = "<p style='color: red;'>❌ Error checking news. Try again.</p>";
        console.error(error);
    });
}
