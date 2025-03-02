# Exam Prep Bot

Exam Prep Bot is a Telegram bot that helps users prepare for their exams by generating a personalized study schedule. The bot assigns study days for each topic and conducts daily mini-tests to reinforce learning.

## Features
- 📅 **Personalized Study Schedule**: Users provide the exam topic, and the bot generates a structured preparation plan.
- ✅ **Daily Check-ins**: After each study session, the bot asks short questions to test knowledge.

## Usage
1. **Start the bot**: `/start`
2. **Set an exam topic**: `/set_exam [subject]`
3. **Get your study plan**: The bot will generate a schedule using GigaChat AI.
4. **Daily Check-ins**: Answer questions after study sessions.
5. **Track progress**: See your stats with `/progress`

## Technologies Used
- **Python**
- **Aiogram** (Telegram bot framework)
- **SQLite** (to store user progress)
- **GigaChat API (Sber)** (for generating study plans and quizzes)




