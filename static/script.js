function checkNews() {
    let newsText = document.getElementById("news_text").value;
    fetch("/predict", {
        method: "POST",
        body: new URLSearchParams({ news_text: newsText }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerText = "Prediction: " + data.prediction;
    })
    .catch(error => console.error("Error:", error));
}
