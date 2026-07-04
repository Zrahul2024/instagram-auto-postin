async function generatePost() {

    let topic = document.getElementById("topic").value;
    let tone = document.getElementById("tone").value;

    let loading = document.getElementById("loading");

    if (topic.trim() === "") {
        alert("Please enter a post topic");
        return;
    }

    loading.innerText = "Generating AI content...";

    try {

        let response = await fetch("/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                topic: topic,
                tone: tone
            })
        });

        let data = await response.json();

        console.log(data);

        if (!response.ok) {
            loading.innerText = "";
            alert(data.error);
            return;
        }

        document.getElementById("caption").innerText = data.caption;
        document.getElementById("hashtags").innerText = data.hashtags;
        document.getElementById("bestTime").innerText = data.bestTime;

        // Show Generated Image
        if (data.image) {
            let img = document.getElementById("generatedImage");
            img.src = data.image;
            img.style.display = "block";
        }

        loading.innerText = "";

    } catch (error) {

        console.error(error);

        loading.innerText = "";

        alert("Something went wrong.");

    }

}


function copyPost() {

    let caption = document.getElementById("caption").innerText;
    let hashtags = document.getElementById("hashtags").innerText;
    let bestTime = document.getElementById("bestTime").innerText;

    let finalPost =
        caption +
        "\n\n" +
        hashtags +
        "\n\nBest Time: " +
        bestTime;

    navigator.clipboard.writeText(finalPost);

    alert("Post copied successfully!");

}


function downloadImage() {

    let img = document.getElementById("generatedImage");

    if (!img.src) {
        alert("No image generated yet.");
        return;
    }

    let link = document.createElement("a");

    link.href = img.src;
    link.download = "instagram_post.png";

    link.click();

}


function postToInstagram() {

    window.open("https://www.instagram.com/", "_blank");

}