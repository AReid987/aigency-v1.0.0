---
type: Page
title: 'Story 2.4: Automate Monthly Coin Distribution'
description: null
icon: null
createdAt: '2025-06-08T14:25:29.494Z'
creationDate: 2025-06-08 09:25
modificationDate: 2025-06-08 10:29
tags: []
coverImage: null
---

# Story 2.4: Automate Monthly Coin Distribution

# Story 2.4: Automate Monthly Coin Distribution

## Status: Draft

## Story

- As a **Sportsclub subscriber**,

- I want to **automatically receive my monthly virtual coin distribution**,

- so that I can **always have coins to make predictions and continue engaging with the platform.**

## Acceptance Criteria (ACs)

1. On the first day of each calendar month, a set amount of virtual coins (e.g., 50,000) is automatically distributed to the virtual wallets of all active, ID-verified subscribers.

2. Users are notified of their monthly coin deposit via an in-app status icon/notification.

3. Users are also notified of their monthly coin deposit via email.

4. If a user subscribes mid-month, they receive a pro-rated amount of virtual coins based on the remaining days in that subscription month.

5. The full standard coin distribution commences on the first of the following month for mid-month subscribers.

6. The coin distribution process is robust and handles a large number of subscribers efficiently.

## Tasks / Subtasks

- [ ] Implement backend service/job to trigger coin distribution on the 1st of each month.

- [ ] Implement logic to identify all active, ID-verified subscribers.

- [ ] Implement logic for calculating and distributing the standard monthly coin amount.

- [ ] Implement logic for calculating and distributing pro-rated coin amounts for mid-month subscribers.

- [ ] Integrate with the Notification Service for in-app status icons/notifications.

- [ ] Integrate with the Notification Service for email notifications of coin deposits.

- [ ] Implement robust error handling and logging for the distribution process (e.g., for failed distributions, partial distributions).

- [ ] Ensure the coin distribution service is idempotent (can be run multiple times without adverse effects for the same distribution period).

## Dev Technical Guidance

This story is critical for maintaining the platform's economy and ensuring consistent user engagement. Focus on accuracy, automation, and handling of large-scale operations.

- **Dependency:** This story **depends on Story 2.1: Implement Subscription Purchase and Management** (for active subscribers) and **Story 2.3: Create Virtual Wallet and Display Balance** (for wallet creation and balance updates). It also depends on **Epic 1** for foundational setup including ID verification and database persistence.

- **Scheduling:** The distribution process will likely be triggered by a scheduled job (e.g., a cron job in a cloud service like AWS EventBridge/Lambda, GCP Cloud Scheduler/Cloud Functions).

- **Data Models:** Refer to the `User`, `Subscription`, `VirtualWallet`, and `CoinTransaction` data models in the Architecture Document for schema definitions.

- **Transaction Management:** Ensure the coin distribution is handled atomically per user or in batches with proper transaction management to guarantee data consistency.

- **Notifications:** Integrate with the Notification Service (from Component View) for all user alerts.

- **Error Handling:** Implement robust error handling and logging for the distribution process as per the "Error Handling Strategy" in the Architecture Document.

- **Scalability:** Consider the scalability of the distribution process as the number of subscribers grows, aiming for efficient batch processing.

- **Security:** Implement strong security measures to prevent unauthorized coin generation or distribution.

- **Testing Guidance:**

    - **Approach:** Unit tests will be developed for distribution logic and calculations. Integration tests will verify the scheduled job triggers and successful interaction with database and notification services. Performance testing will be conducted to ensure the process efficiently handles a large number of subscribers.

    - **Special Considerations:** Performance testing for scalability and efficiency of distribution is critical. Security testing should specifically focus on preventing unauthorized coin generation or distribution, and ensuring coin integrity.

## Story Progress Notes

### Agent Model Used: Bob (SM Agent)

### Completion Notes List

- (To be filled by Developer Agent upon completion)

### Change Log

- (To be filled by Developer Agent upon completion)

