<template>
  <div class="container mx-auto px-4">
    <h1 class="text-4xl font-bold mb-8">Ask your GPT</h1>
    <div class="chat-container">
      <div ref="chatbox" class="chatbox bg-gray-100 p-4 h-96 overflow-y-auto mb-4 rounded shadow font-mono">  
      </div>
      <div class="input-container space-y-4">
        <input v-model="userInput" @keydown.enter="sendMessage" type="text" placeholder="Type your message..." class="border border-gray-300 p-2 w-full py-2" />
        <input v-model="webpageInput" type="text" placeholder="Enter the URL of a webpage..." class="border border-gray-300 p-2 w-full py-2" />
        <div class="btn-container flex-row space-x-4">
          <button @click="sendWebpage" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Submit webpage</button>
          <button @click="sendMessage" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Send</button>
        </div>
      </div>
      <div class="mt-4 text-gray-600">{{ tokenInfo }}</div>
    </div>
  </div>
</template>
<script>
  const API_URL = "http://localhost:5000";
  export default {
    data() {
      return {
        userInput: "",
        webpageInput: "",
        tokenInfo: "",
      };
    },
    methods: {
      async appendMessage(role, content) {
        const messageContainer = document.createElement("div");
        messageContainer.className = role === "user" ? "user-message" : "bot-message";
        const nameElement = document.createElement("strong");
        nameElement.textContent = role === "user" ? "Me: " : "Toula: ";
        messageContainer.appendChild(nameElement);
        const contentElement = document.createElement("span");
        contentElement.textContent = content;
        messageContainer.appendChild(contentElement);
        this.$refs.chatbox.appendChild(messageContainer);
        this.$refs.chatbox.scrollTop = this.$refs.chatbox.scrollHeight;
      },
      async sendMessage() {
        const userInput = this.userInput.trim();
        if (!userInput) return;
        this.userInput = "";
        await this.appendMessage("user", userInput);
        try {
          const response = await fetch(`${API_URL}/chat`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ input: userInput }),
          });
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          const data = await response.json();
          await this.appendMessage("assistant", data.response);
          this.tokenInfo = data.token_info;
        } catch (error) {
          console.error("There was a problem with the fetch operation:", error);
          await this.appendMessage("assistant", "An error occurred while processing your message. Please try again.");
        }
      },
      async sendWebpage() {
        const webpageUrl = this.webpageInput.trim();
        if (!webpageUrl) return;
        this.webpageInput = "";
        try {
          const response = await fetch(`${API_URL}/webpage`, {
            method: "POST",
            headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ webpage: webpageUrl }),
        });
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        // Display success message to user
        await this.appendMessage("assistant", "Webpage sent successfully.");
        } catch (error) {
          console.error("There was a problem with the fetch operation:", error);
          // Display error message to user
          await this.appendMessage("assistant", "An error occurred while sending the webpage. Please try again.");
        }
      },
  },
};  
</script>
