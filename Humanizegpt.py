import openai
import datetime
import tkinter as tk
from tkinter import scrolledtext

openai.api_key = 'Your Key'

class Message:
    def __init__(self, original_text, text, created_at):
        self.original_text = original_text
        self.text = text
        self.created_at = created_at

class State:
    def __init__(self):
        self.text = ""
        self.messages = []

    @property
    def output(self):
        if not self.text.strip():
            return "Humanized text will appear here."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "assistant",
                 "content": f"When it comes to writing content, two factors are crucial, \"perplexity\" and \"burstiness\". Perplexity measures the complexity of text. Separately, burstiness compares the variations of sentences. Humans tend to write with greater burstiness, for example, with some longer or complex sentences alongside shorter ones. AI sentences tend to be more uniform. Therefore, when writing the following content, I am going to ask you to create, I need it to have a good amount of perplexity and burstiness. Using the concepts written previously, rewrite this text with a high degree of perplexity and burstiness: {self.text}"}
            ]
        )
        return response['choices'][0]['message']['content']

    def post(self):
        new_message = Message(
            original_text=self.text,
            text=self.output,
            created_at=datetime.datetime.now().strftime("%B %d, %Y %I:%M %p")
        )
        self.messages.insert(0, new_message)

class GPTHumanizerApp:
    def __init__(self, root):
        self.state = State()

        root.title("GPT-Humanizer")

        self.header_label = tk.Label(root, text="GPT-Humanizer", font=("Helvetica", 16))
        self.header_label.pack(pady=10)

        self.instructions_label = tk.Label(root, text="Humanize GPT-Text to avoid AI Detection!", font=("Helvetica", 10), fg="#666")
        self.instructions_label.pack()

        self.input_text = tk.Text(root, height=10, width=50, wrap=tk.WORD)
        self.input_text.pack(pady=10)

        self.humanize_button = tk.Button(root, text="Humanize", command=self.humanize_text)
        self.humanize_button.pack(pady=10)

        self.output_label = tk.Label(root, text="Output:", font=("Helvetica", 12))
        self.output_label.pack(pady=10)

        self.output_text = scrolledtext.ScrolledText(root, height=10, width=50, wrap=tk.WORD)
        self.output_text.pack(pady=10)

        self.messages_frame = tk.Frame(root)
        self.messages_frame.pack(pady=10)

    def humanize_text(self):
        self.state.text = self.input_text.get("1.0", tk.END).strip()
        self.state.post()
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, self.state.output)

        for widget in self.messages_frame.winfo_children():
            widget.destroy()

        for message in self.state.messages:
            self.display_message(message)

    def display_message(self, message):
        message_frame = tk.Frame(self.messages_frame, bg="#f5f5f5", bd=1, relief="solid")
        message_frame.pack(pady=5, padx=5, fill="x")

        original_text_label = tk.Label(message_frame, text=message.original_text, bg="#fff", wraplength=450, justify="left")
        original_text_label.pack(padx=10, pady=5, fill="x")

        humanized_text_label = tk.Label(message_frame, text=message.text, bg="#fff", wraplength=450, justify="left")
        humanized_text_label.pack(padx=10, pady=5, fill="x")

        timestamp_label = tk.Label(message_frame, text=message.created_at, font=("Helvetica", 8), fg="#666", bg="#f5f5f5")
        timestamp_label.pack(padx=10, pady=5, anchor="e")

if __name__ == "__main__":
    root = tk.Tk()
    app = GPTHumanizerApp(root)
    root.mainloop()
