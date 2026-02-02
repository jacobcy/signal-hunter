# Task 002: Fix Signal Hunter Telegram Channel ID

## 🎯 Objective
Configure the correct Telegram Channel ID for the Signal Hunter (v0.2.0) module to enable message broadcasting.

## 🚨 Urgency
**Critical / Live Issue**. The system is currently unable to forward discovered signals to the user.

## 📋 Context
- **Project:** Signal Hunter
- **Current Status:** v0.2.0 (Live)
- **Issue:** Missing or incorrect `TELEGRAM_CHANNEL_ID`.
- **Impact:** Signal detection works, but delivery fails.

## 🛠 Requirements

### 1. Discovery
- Determine the correct numeric Channel ID for the target channel.
- **Status:** Found. ID is `-1003848721376`.

### 2. Implementation
- Update the environment variable `TELEGRAM_CHANNEL_ID` in `.env` to `-1003848721376`.
- Ensure `src/utils/notifier.py` (or relevant sender) reads this variable correctly.

### 3. Verification
- Send a "System Test" message to the channel.
- Confirm receipt.

## 👥 Assignments
- **PM:** Coordinate user input.
- **Dev:** Update configuration.
- **QA:** Verify message delivery.
