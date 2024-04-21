// Function to send a message when the "Send" button is clicked or the Enter key is pressed
function sendMessage(event) {
  event.preventDefault(); // Prevent form submission

  // Get the user input and trim extra spaces
  var userInput = document.getElementById("user-input").value.trim();

  // If the input field is empty, show an alert
  if (userInput === "") {
      alert("Please enter a message.");
      return;
  }

  // Display the user's message in the chat box
  var chatBox = document.getElementById("chat-box");
  var userMessage = document.createElement("div");
  userMessage.className = "message user-message";
  userMessage.textContent = userInput;
  chatBox.appendChild(userMessage);

  // Clear the input field to avoid re-sending the same message
  document.getElementById("user-input").value = "";

  // Scroll to the bottom of the chat box
  chatBox.scrollTop = chatBox.scrollHeight;

  // Fetch the bot's response by sending a POST request to Flask
  fetch('/ask', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json', // Content type for JSON data
      },
      body: JSON.stringify({ question: userInput }) // Send the user input as JSON
  })
  .then(response => response.json()) // Parse the response JSON
  .then(data => {
      // Display the bot's response in the chat box
      displayBotMessage(data.answer); // Use the answer from the response
  })
  .catch(error => {
      console.error('Error fetching response:', error);
      displayBotMessage("An error occurred while fetching the response."); // Error message for the user
  });
}

// Function to display the bot's response in the chat box
function displayBotMessage(response) {
  var chatBox = document.getElementById("chat-box");
  var botMessage = document.createElement("div");
  botMessage.className = "message bot-message";
  botMessage.textContent = response; // Bot's response
  chatBox.appendChild(botMessage);

  // Scroll to the bottom of the chat box to ensure the new message is visible
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Function to handle Enter key press for sending messages
function handleKeyPress(event) {
  if (event.key === "Enter") {
      sendMessage(event); // Send the message on pressing Enter
  }
}

// Function to clear the chat box
function clearChat() {
  var chatBox = document.getElementById("chat-box");
  chatBox.innerHTML = ""; // Clears all chat messages
}
