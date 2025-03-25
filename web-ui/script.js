document.addEventListener("DOMContentLoaded", function() {
    const userList = document.getElementById("user-list");
    const messageList = document.getElementById("message-list");

    let selectedPair = null;

    // Fetch the list of user pairs from the backend
    async function fetchUserPairs() {
        try {
            // Fetch user pairs from the /user-pairs endpoint
            const response = await fetch("http://127.0.0.1:5000/user-pairs");
            if (!response.ok) {
                throw new Error("Failed to fetch user pairs");
            }
            const userPairs = await response.json();

            // Store unique pairs to avoid duplicates in either direction
            const uniquePairs = new Set();

            userPairs.forEach(pair => {
                // Sort the sender and recipient IDs alphabetically so that the pair is the same regardless of direction
                const sortedPair = [pair.sender_id, pair.recipient_id].sort().join("_");

                // Only add the pair if it's not already added (this ensures that the pair appears only once)
                if (!uniquePairs.has(sortedPair)) {
                    uniquePairs.add(sortedPair);

                    // Create the list item for the user pair
                    const listItem = document.createElement("li");
                    listItem.textContent = `${pair.sender_name} ↔ ${pair.recipient_name}`;
                    listItem.dataset.senderId = pair.sender_id;
                    listItem.dataset.recipientId = pair.recipient_id;
                    listItem.addEventListener("click", () => loadMessages(pair.sender_id, pair.recipient_id));
                    userList.appendChild(listItem);
                }
            });
        } catch (error) {
            console.error("Error fetching user pairs:", error);
            userList.innerHTML = "<p>Failed to load user pairs.</p>";
        }
    }

    // Fetch messages between the selected user pair
    async function loadMessages(senderId, recipientId) {
        selectedPair = { senderId, recipientId };
        
        // Clear the previous messages
        messageList.innerHTML = "<p>Loading messages...</p>";

        try {
            const response = await fetch(`http://127.0.0.1:5000/dms?sender_id=${senderId}&recipient_id=${recipientId}&last_message_id=0`);
            const messages = await response.json();

            // Clear the messages section
            messageList.innerHTML = "";

            if (messages.length === 0) {
                messageList.innerHTML = "<p>No messages available.</p>";
                return;
            }

            // Display each message
            messages.forEach(message => {
                const messageElem = document.createElement("div");
                messageElem.classList.add("message");

                const sender = document.createElement("div");
                sender.classList.add("sender");
                sender.textContent = message.sender_name;

                const timestamp = document.createElement("div");
                timestamp.classList.add("timestamp");
                timestamp.textContent = message.timestamp;

                const content = document.createElement("div");
                content.classList.add("content");
                content.textContent = message.message;

                messageElem.appendChild(sender);
                messageElem.appendChild(timestamp);
                messageElem.appendChild(content);

                messageList.appendChild(messageElem);
            });
        } catch (error) {
            console.error("Error fetching messages:", error);
            messageList.innerHTML = "<p>Failed to load messages.</p>";
        }
    }

    // Load user pairs on page load
    fetchUserPairs();
});
