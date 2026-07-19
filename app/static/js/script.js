document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".summarize-btn").forEach(button => {

        button.addEventListener("click", async function () {

            const noteText = this.dataset.content;

            const resultBox = this.nextElementSibling;

            resultBox.innerHTML = "⏳ Generating summary...";

            try {

                const response = await fetch("/ai/summarize", {

                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        text: noteText
                    })

                });

                const data = await response.json();

                if (data.summary) {

                    resultBox.innerHTML = `
                        <div class="alert alert-success mt-2">
                            <strong>AI Summary</strong><br>
                            ${data.summary.replace(/\n/g, "<br>")}
                        </div>
                    `;

                } else {

                    resultBox.innerHTML = `
                        <div class="alert alert-danger">
                            ${data.error}
                        </div>
                    `;
                }

            } catch (err) {

                resultBox.innerHTML = `
                    <div class="alert alert-danger">
                        AI request failed.
                    </div>
                `;
            }

        });

    });

});