class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        };

        this.state = false;
        this.messages = [];
        this.API_KEY = '{{API_KEY}}'; 
    }

    display() {
        const { openButton, chatBox, sendButton } = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox));
        sendButton.addEventListener('click', () => this.onSendButton(chatBox));

        const inputField = chatBox.querySelector('input');
        inputField.addEventListener("keyup", ({ key }) => {
            if (key === "Enter") {
                this.onSendButton(chatBox);
            }
        });
    }

    toggleState(chatbox) {
        this.state = !this.state;

        if (this.state) {
            chatbox.classList.add('chatbox--active');
        } else {
            chatbox.classList.remove('chatbox--active');
        }
    }

    onSendButton(chatbox) {
        const textField = chatbox.querySelector('input');
        const userMessage = textField.value.trim();

        if (userMessage === "") {
            return;
        }

       
        this.messages.push({ name: "User", message: userMessage });

       
        fetch('https://university-bot-8sh1.onrender.com/predict', {
            method: 'POST',
            body: JSON.stringify({ message: userMessage }),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': this.API_KEY 
            },
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Server responded with status ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // Validate server response
                const assistantMessage = data.answer || "Sorry, I couldn't process your request.";
                this.messages.push({ name: "Assistant", message: assistantMessage });
                this.updateChatText(chatbox);
                textField.value = '';
            })
            .catch(error => {
                console.error('Error:', error);
                this.messages.push({ name: "Assistant", message: "An error occurred. Please try again later." });
                this.updateChatText(chatbox);
                textField.value = '';
            });
    }

    updateChatText(chatbox) {
        let html = '';

        this.messages.slice().reverse().forEach(function (item) {
            if (item.name === "Assistant") {
                html += `<div class="messages__item messages__item--visitor">${item.message}</div>`;
            } else {
                html += `<div class="messages__item messages__item--operator">${item.message}</div>`;
            }
        });

        const chatMessages = chatbox.querySelector('.chatbox__messages');
        chatMessages.innerHTML = html;
    }
}

const chatbox = new Chatbox();
chatbox.display();
