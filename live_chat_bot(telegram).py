import random
import time
import telebot
import threading

# Create a bot
bot = telebot.TeleBot('YOUR_API_KEY_HERE')

# Last bot response to avoid repetition
last_answer = {}
last_question_time = {}  # Stores the last time a question was asked for each chat
conversation_end_time = {}  # Stores the end time of the conversation for each chat
question_interval = 20 * 60  # Minimum interval for questions in seconds (20 minutes)
max_question_interval = 120 * 60  # Maximum interval for questions in seconds (120 minutes)

# Welcome message when the bot starts
@bot.message_handler(commands=['start'])
def greet(message):
    bot.send_message(message.chat.id,
                     "Welcome, fans tg bot. I show you my little think\n"
                     "\n The bot will improve over time, but this is what we have for now!")

# A set of random responses for different questions
general_phrases = {
    # Greetings
    'hello': [
        "Hi! How are you doing?",
        "Oh, hello! What are you up to?",
        "Greetings! How's your mood today?",
        "Hey! What's new in your life?",
        "Hey there! Glad to see you!",
    ],
    'yo': [
        "Hi! How are you doing?",
        "Oh, hello! What are you up to?",
        "Greetings! How's your mood today?",
        "Hey! What's new in your life?",
        "Hey there! Glad to see you!",
    ],
    'sup': [
        "Hi! How are you doing?",
        "Oh, hello! What are you up to?",
        "Greetings! How's your mood today?",
        "Hey! What's new in your life?",
        "Hey there! Glad to see you!",
    ],

    'hi': [
        "Hi! How are you doing?",
        "Oh, hello! What are you up to?",
        "Greetings! How's your mood today?",
        "Hey! What's new in your life?",
        "Hey there! Glad to see you!",
    ],
    # Questions about mood
    'how are you?': [
        "I'm great! How about you?",
        "I'm doing fine, thanks! How about you?",
        "Not bad, a bit busy, and you?",
        "Great, thanks! How's everything with you?",
        "A bit tired, but overall good. How about you?",
    ],
    'what's up': [
        "Nothing much, how about you?",
        "I'm doing great! What about you?",
        "Things are going well, thanks! How about you?",
        "Not bad, just a bit busy. And you?",
        "Great, thanks! How's everything with you?",
        "A bit tired, but overall not bad. And you?",
    ],
    'how’s your day?': [
        "Everything's good, thanks for asking, and you?",
        "It could have been better, thanks for asking, and you?",
    ],
    # Questions about age
    'how old are you?': [
        "I'm a little over 20 years old.",
        "About 20 years, but it's hard to say exactly :)",
        "I'm 20, but that's not really important.",
        "I don't like to talk about my age, but I'm 20.",
    ],
    # Travel questions
    'where have you been?': [
        "I've been in the virtual world, as always.",
        "I traveled through the internet, and you?",
        "Just relaxing and reading.",
        "Traveling through chats, what's new with you?",
    ],
    # Name
    'what’s your name?': [
        "My name is Mark, what about you?",
        "I'm Mark, a bot.",
        "You can call me Mark.",
        "Just Mark. What's your name?",
    ],
    # Farewell
    'bye': [
        "Goodbye, have a great day!"
    ],
    'have a good day': [
        "Thanks for the kind wishes!"
    ],
}

# Filler phrases or emotional inserts
filler_phrases = [
    "Well...", "How should I put this...", "Hmm...", "You know, it's complicated...", "Hmm..."
]

# Function to simulate typing
def typing_simulation(chat_id):
    bot.send_chat_action(chat_id, 'typing')  # Displays "Typing..."
    time.sleep(random.uniform(1, 3))  # Simulates typing delay

# Function to generate unique responses
def generate_answer(question, chat_id):
    global last_answer

    # Keywords with response variations
    for keyword, variations in general_phrases.items():
        if keyword in question.lower():
            # Avoid repeating the last response
            possible_answers = [ans for ans in variations if ans != last_answer.get(chat_id)]
            if not possible_answers:  # If all responses have been used, pick any
                possible_answers = variations
            answer = random.choice(filler_phrases) + " " + random.choice(possible_answers)
            last_answer[chat_id] = answer  # Update last answer for this chat
            return answer

    # Fallback responses
    fallback_answers = [
        "It depends on many factors...",
        "Hmm... Maybe we should think a bit longer?",
        "It's hard to say exactly.",
        "That's an interesting but difficult question."
    ]
    return random.choice(filler_phrases) + " " + random.choice(fallback_answers)

# Function for periodic questions
def periodic_questions(chat_id):
    global last_question_time, conversation_end_time

    while True:
        current_time = time.time()
        # Check if the conversation ended recently
        if chat_id in conversation_end_time:
            elapsed_time = current_time - conversation_end_time[chat_id]
            if elapsed_time >= question_interval:
                # Randomly choose the next question interval
                interval = random.randint(question_interval, max_question_interval)
                # Schedule questions
                time.sleep(interval)
                bot.send_message(chat_id, "What are you doing right now?")
                time.sleep(5)  # Delay before sending the next question
                bot.send_message(chat_id, "How's your mood?")
                conversation_end_time[chat_id] = time.time()  # Update the last conversation time

        time.sleep(60)  # Check every minute

# Handle any text message
@bot.message_handler(func=lambda message: True)
def answer_question(message):
    typing_simulation(message.chat.id)  # Simulate typing
    response = generate_answer(message.text, message.chat.id)

    # Update conversation end time
    conversation_end_time[message.chat.id] = time.time()

    bot.send_message(message.chat.id, response)

    # Start the thread for periodic questions if not already started
    if message.chat.id not in last_question_time:
        threading.Thread(target=periodic_questions, args=(message.chat.id,), daemon=True).start()

# Start the bot
bot.polling()
