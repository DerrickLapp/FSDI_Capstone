// Getting CSRFToken
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Toggling the Favorite Star
document.addEventListener("DOMContentLoaded", function() {
    // Check favorite status on page load
    document.querySelectorAll(".star-icon").forEach(star => {
        let gameId = star.dataset.gameId;
        let streamerId = star.dataset.streamerId;

        if (gameId) {
            fetch(`/check-favorite-game/${gameId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.favorited) {
                    star.classList.add("active"); //Marked as favorited
                }
            });
        }

        if (streamerId) {
            fetch(`/check-favorite-game/${streamerId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.favorited) {
                    star.classList.add("active"); //Marked as favorited
                }
            });
        }


    });
});

document.querySelectorAll(".star-icon").forEach(star => {
    star.addEventListener("click", function() {
        this.classList.toggle("active"); // toggles star color
        console.log("Clicked!", this.classList.contains("active"));
        
        
        let gameId = this.dataset.gameId; // gets game.id if present
        let streamerId = this.dataset.streamId; // gets streamer.id if present

        let data = {}; // making the object to send
        if (gameId) {
            data.game_id = gameId; // Assigns the game ID
        }
        if (streamerId) {
            data.streamer_id = streamerId; // Assigns the streamer ID
        }


        fetch("/toggle_favorite/", {
            method: "POST",
            headers: { "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/json"
             },
            body: JSON.stringify(data) //sends only the relevant ID
        }).then(response => response.json()).then(data => console.log("Response:", data)).catch(error => console.error("Error:", error));
    });
});