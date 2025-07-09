---
type: Page
collections: sportsclub backlog
title: 'Story 3.2: Enable Prediction Placement (Basic)'
description: null
icon: null
createdAt: '2025-06-08T17:24:55.788Z'
creationDate: 2025-06-08 12:24
modificationDate: 2025-06-11 23:10
tags: [Story]
coverImage: null
---

# Story 3.2: Enable Prediction Placement (Basic)

# Story 3.2: Enable Prediction Placement (Basic)

## Status: Draft

## Story

- As a **Sportsclub user**,

- I want to **select an event, choose my predicted winner, and specify the amount of coins to place**,

- so that I can **actively participate in the prediction game and use my virtual currency.**

## Acceptance Criteria (ACs)

1. Users can select an event from the displayed list (from Story 3.1).

2. After selecting an event, users can choose their predicted winner from the available outcomes.

3. Users can specify the amount of virtual coins they wish to place on their prediction.

4. Coin placement is enforced in increments of 1,000 coins.

5. The minimum number of coins for a single prediction is 1,000.

6. The maximum number of coins for a single prediction is limited to the user's current available wallet balance.

7. After submitting a prediction, users receive an in-app notification confirming their prediction details (event, pick, coin amount).

8. Users can view a list of their active/pending predictions.

9. Users can cancel or change a prediction before the official start time of the associated sporting event.

## Tasks / Subtasks

- [ ] Design and implement prediction UI within event details (e.g., pick selection, coin input field).

- [ ] Implement frontend logic for enforcing coin increments, minimums, and checking against wallet balance.

- [ ] Implement backend API endpoint for submitting a new prediction.

- [ ] Implement backend logic for validating prediction data and deducting coins from the user's wallet.

- [ ] Store prediction details (user, event, pick, coins placed, odds at prediction time) in the database.

- [ ] Implement in-app notification for prediction confirmation.

- [ ] Design and implement UI for viewing active/pending predictions.

- [ ] Implement backend API endpoint and logic for canceling/changing predictions.

- [ ] Implement frontend UI for canceling/changing predictions before event start.

## Dev Technical Guidance

This story is the heart of the core game loop. Focus on accurate transaction handling, real-time balance checks, and robust input validation.

- **Dependency:** This story **depends on Story 3.1: Display Major Sporting Events with Odds** (for selecting events) and **Story 2.3: Create Virtual Wallet and Display Balance** (for using coins from the wallet). It also relies on **Epic 1** (foundational setup) for user accounts and secure infrastructure.

- **Data Models:** Refer to the `Prediction`, `User`, `VirtualWallet`, `SportingEvent`, `Odds`, and `CoinTransaction` data models in the Architecture Document for schema definitions and relationships.

- **Database Interactions:** Ensure atomic transactions for coin deduction and prediction recording. Adhere to "Data Access Patterns" for secure and efficient operations.

- **API Design:** The new prediction submission endpoint should be designed according to the "API Design and Standards" in the Architecture Document.

- **Security:** Implement rigorous input validation for prediction submissions. Ensure secure handling of coin transactions to prevent tampering. Refer to "Security Best Practices" in the Architecture Document.

- **Error Handling:** Implement robust error handling for invalid predictions, insufficient funds, or network issues during submission, as per the "Error Handling Strategy."

- **Real-time Considerations:** While the full real-time leaderboard is a later Epic, ensure the prediction submission process is fast and responsive to the user.

## Story Progress Notes

### Agent Model Used: Bob (SM Agent)

### Completion Notes List

- (To be filled by Developer Agent upon completion)

### Change Log

- (To be filled by Developer Agent upon completion)

