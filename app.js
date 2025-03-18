// // app.js
// function chatBot() {
//     return {
//         messages: [{
//             from: 'bot',
//             text: 'Hello, how can I assist you today?'
//         }],
//         botTyping: false,
//         updateChat: function(inputField) {
//             let userMessage = inputField.value.trim();
//             if (!userMessage) return;
//             this.messages.push({ from: 'user', text: userMessage });
//             inputField.value = '';
//             this.scrollChat();

//             this.botTyping = true;
//             this.scrollChat();

//             // Simulate an API call to your Python backend
//             fetch('http://127.0.0.1:5000/chat', {
//                 method: 'POST',
//                 headers: { 'Content-Type': 'application/json' },
//                 body: JSON.stringify({ message: userMessage })
//             })
//                 .then(response => response.json())
//                 .then(data => {
//                     this.botTyping = false;
//                     this.messages.push({ from: 'bot', text: data.reply });
//                     this.scrollChat();
//                 })
//                 .catch(error => {
//                     this.botTyping = false;
//                     this.messages.push({ from: 'bot', text: "Sorry, something went wrong!" });
//                     this.scrollChat();
//                 });
//         },
//         scrollChat: function() {
//             const messagesContainer = document.getElementById("messages");
//             messagesContainer.scrollTop = messagesContainer.scrollHeight;
//         }
//     }
// }
