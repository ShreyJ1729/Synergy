import json
from queue import Queue
from threading import Thread
import time
import datetime
import openai

# Initialize Queue
transcription_queue = Queue()

# Mock partial transcriptions
partial_transcriptions = [
    "hey! let's brainstorm",
    "an idea that i might want to",
    "turn into a startup?",
    "It's kind",
    "of like a mix between",
    "Uber and real estate where you can",
    "rent out your house",
    "to people who are traveling to your",
    "city",
    "What do you think? Is that a good",
    "idea?",
]


# Mock function to simulate Whisper dropping partial transcriptions into a queue
def mock_whisper_streaming():
    for transcription in partial_transcriptions:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        transcription_queue.put(
            {"transcription": transcription, "timestamp": timestamp}
        )
        time.sleep(1)  # Simulate a 1-second delay between each partial transcription


# queue to catch gpt responses
gpt_response_queue = Queue()


def call_gpt(messages):
    # system prompt is first
    messages.insert(
        0,
        {
            "role": "system",
            "content": "You are a speech assistant and you respond how humans speak, not how humans type. You are receiving a partial transcription as you actively listen to a user. Respond with 3 segments:\n1. Your spoken response to the user.\n2. Confidence score in the quality of our response (0-1).\n3. Whether or not we should speak this response (True/False)",
        },
    )

    # stream gpt responses to a queue
    for chunk in openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, stream=True
    ):
        content = chunk["choices"][0]["delta"].get("content")
        if content:
            gpt_response_queue.put(content)
            print(f"Response: {content}")


def analyze_queue():
    last_timestamp = None
    entire_transcription = []
    messages = []

    while True:
        if not transcription_queue.empty():
            current_item = transcription_queue.get()
            current_timestamp = datetime.datetime.strptime(
                current_item["timestamp"], "%Y-%m-%d %H:%M:%S.%f"
            )

            entire_transcription.extend(current_item["transcription"].split())
            messages.append({"role": "user", "content": current_item["transcription"]})

            print(f"{current_item['transcription']}")

            if "?" in current_item["transcription"]:
                print("*DECISION AGENT*: User is asking a question.")

            if len(entire_transcription) > 25:
                print(
                    f"*DECISION AGENT*: Entire transcription length exceeds 25 words."
                )
                # gpt_response = call_gpt(messages)
                # print(f"GPT Response: {gpt_response}")

            if last_timestamp:
                delta = current_timestamp - last_timestamp
                if delta.total_seconds() > 2:
                    print(
                        f"*DECISION AGENT*: Long delay between transcriptions ({delta.total_seconds()} seconds)."
                    )

            last_timestamp = current_timestamp


# Main Function
def main():
    mock_whisper_thread = Thread(target=mock_whisper_streaming)
    mock_whisper_thread.start()

    analyze_thread = Thread(target=analyze_queue)
    analyze_thread.start()


if __name__ == "__main__":
    main()
