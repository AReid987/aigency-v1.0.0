---
type: Page
collections: sportsclub backlog
title: 'Story 8.3: Implement Prediction Win Streak Bonuses'
description: null
icon: null
createdAt: '2025-06-10T06:41:44.254Z'
creationDate: 2025-06-10 01:41
modificationDate: 2025-06-11 23:11
tags: [Story]
coverImage: null
---

# Story 8.3: Implement Prediction Win Streak Bonuses

# Story 8.3: Implement Prediction Win Streak Bonuses

## Status: Draft

## Story

- As a **Sportsclub user**,

- I want to **be rewarded with bonus virtual coins for achieving prediction win streaks**,

- so that I can **feel incentivized to make accurate predictions and accumulate more coins.**

## Acceptance Criteria (ACs)

1. The system tracks a user's prediction win streak, defined by achieving a number of consecutive correct predictions.

2. The system awards users with bonus virtual coins for achieving predefined prediction win streak milestones.

3. The bonus coin rewards for prediction win streaks increase for longer streaks.

4. Users are notified of their prediction win streak achievements and any awarded bonuses via in-app status icon/notification.

5. A user's prediction win streak is broken by:

    - An incorrect prediction.

    - A defined period of inactivity in making predictions *(Specific period TBD)*.

6. Users can view their current prediction win streak count in their profile or a dedicated gamification section.

7. *(Scope TBD: We need to define if prediction win streaks are counted across all sports/events or if they can be sport-specific).*

## Tasks / Subtasks

- [ ] Implement backend service/logic to track a user's consecutive correct predictions.

- [ ] Implement backend logic for identifying an incorrect prediction to reset the streak.

- [ ] Implement backend logic for identifying a defined period of inactivity to reset the streak.

- [ ] Implement backend logic to identify predefined prediction win streak milestones achieved.

- [ ] Implement backend logic for awarding increasing bonus virtual coins for milestones.

- [ ] Integrate with the Notification Service for in-app notifications about streak achievements and bonuses.

- [ ] Implement frontend UI to display the user's current prediction win streak count.

- [ ] Implement robust error handling and logging for the streak tracking and award process.

- [ ] Ensure the streak tracking mechanism is idempotent and handles edge cases (e.g., cancelled events affecting streak, multiple predictions on the same event).

## Dev Technical Guidance

This story further enhances gamification by rewarding predictive skill. Focus on accurate streak calculation, flexible milestone configuration, and secure coin awards tied to prediction outcomes.

- **Dependency:** This story **depends on Story 3.3: Automate Prediction Outcome Processing & Award Winnings** (for identifying correct/incorrect predictions). It also relies on **Epic 1** for foundational setup (user accounts, basic infrastructure) and **Epic 2** for wallet management (specifically Story 2.3 for wallet creation). It uses the **Gamification Service** (from Component View in Architecture Document) for core logic and the **Notification Service** for user alerts.

- **Business Rules (TBD):** The specific streak milestones, corresponding increasing coin amounts, and the defined period of inactivity to break a streak need to be obtained from the Product Manager. Whether streaks are counted across all sports/events or are sport-specific also needs clarification. These are **CRITICAL EXTERNAL DEPENDENCIES** for this story's full implementation. The current story defines the *mechanism* to track and apply these rules.

- **Data Models:** Refer to the `User`, `VirtualWallet`, `CoinTransaction`, `GamificationActivity`, and `Prediction` data models in the Architecture Document for schema definitions. A new field on the User model (e.g., `currentWinStreakCount`, `lastPredictionDate`) might be necessary to persist streak data.

- **Triggers:** Streak tracking and award logic will be triggered by the processing of prediction outcomes.

- **Transaction Management:** Ensure coin awards are handled atomically and securely, guaranteeing data consistency. Refer to "Error Handling Strategy" for principles.

- **Notifications:** Integrate with the Notification Service (from Component View) for all user alerts.

- **Security:** Implement rigorous security measures to prevent manipulation of prediction win streaks or fraudulent bonus awards. Adhere to "Security Best Practices."

- **Testing Guidance:**

    - **Approach:** Unit tests for streak tracking logic (increment, reset based on correct/incorrect predictions, reset based on inactivity), milestone detection, and bonus calculation. Integration tests for prediction outcome processing, wallet updates, and notification triggers. Manual testing for user experience of seeing streak count and receiving bonuses.

    - **Special Considerations:** Thoroughly test various streak scenarios (e.g., wins, losses, mixed outcomes, periods of inactivity). Test milestone awards at exact breakpoints. Rigorous security testing to prevent fraudulent streak manipulation or bonus awards.

## Story Progress Notes

### Agent Model Used: Bob (SM Agent)

### Completion Notes List

- (To be filled by Developer Agent upon completion)

### Change Log

- (To be filled by Developer Agent upon completion)


