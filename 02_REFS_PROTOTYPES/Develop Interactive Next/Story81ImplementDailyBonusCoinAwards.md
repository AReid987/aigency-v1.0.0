---
type: Page
collections: sportsclub backlog
title: 'Story 8.1: Implement Daily Bonus Coin Awards'
description: null
icon: null
createdAt: '2025-06-10T03:37:28.745Z'
creationDate: 2025-06-09 22:37
modificationDate: 2025-06-11 23:11
tags: [Story]
coverImage: null
---

# Story 8.1: Implement Daily Bonus Coin Awards

# Story 8.1: Implement Daily Bonus Coin Awards

## Status: Draft

## Story

- As a **Sportsclub subscriber**,

- I want to **automatically receive a daily bonus of virtual coins**,

- so that I can **be rewarded for my consistent engagement and have more coins for predictions.**

## Acceptance Criteria (ACs)

1. The system automatically awards a daily bonus of virtual coins to eligible users upon their first login or qualifying app activity of the day.

2. Users must be active subscribers to be eligible for the daily bonus.

3. Users are notified of their daily bonus coin deposit via an in-app status icon/notification.

4. *(Amount TBD: The specific amount of the daily bonus coins, or the formula to determine it (e.g., fixed, variable), needs to be defined).*

5. The daily bonus is awarded once per 24-hour period per eligible user.

## Tasks / Subtasks

- [ ] Implement backend service/logic to detect the first login or qualifying app activity of the day for a user.

- [ ] Implement backend logic to check if the user is an active subscriber.

- [ ] Implement backend logic for awarding the daily bonus virtual coins to the user's wallet.

- [ ] Integrate with the Notification Service for in-app status icons/notifications about the daily bonus.

- [ ] Ensure the daily bonus mechanism is idempotent to prevent multiple awards in a single day.

- [ ] Implement robust error handling and logging for the bonus distribution process.

- [ ] Implement logic to track the last awarded daily bonus for each user to enforce the 24-hour period.

## Dev Technical Guidance

This story initiates the gamification layer, focusing on a simple, consistent reward. Ensure accurate eligibility checks, secure coin transfers, and reliable daily execution.

- **Dependency:** This story **depends on Epic 1** for foundational setup (user accounts, basic infrastructure) and **Epic 2** for active subscribers and wallet management (specifically Story 2.3 for wallet creation). It relies on the **Gamification Service** (from Component View in Architecture Document) for core logic and the **Notification Service** for user alerts. It also uses the concept of "qualifying app activity" which might be linked to general user interaction logging.

- **Business Rule (TBD):** The specific amount or formula for the daily bonus coins needs to be obtained from the Product Manager. This is a **CRITICAL EXTERNAL DEPENDENCY** for this story's full implementation. The current story defines the *mechanism* to apply this rule.

- **Data Models:** Refer to the `VirtualWallet`, `User`, `CoinTransaction`, and `GamificationActivity` data models in the Architecture Document for schema definitions. A new field on the User or Wallet model (e.g., `lastDailyBonusAwardedDate`) might be necessary.

- **Scheduling/Triggers:** The bonus award should be triggered by user activity (first login/activity), not a separate scheduler, but the system must track daily eligibility.

- **Transaction Management:** Ensure coin awards are handled atomically and securely, guaranteeing data consistency. Refer to "Error Handling Strategy" for principles.

- **Notifications:** Integrate with the Notification Service (from Component View) for all user alerts.

- **Security:** Implement rigorous security measures to prevent unauthorized coin generation or manipulation of the daily bonus. Adhere to "Security Best Practices."

- **Testing Guidance:**

    - **Approach:** Unit tests for eligibility checks, bonus calculation (once amount is defined), and idempotency. Integration tests for user activity detection, wallet updates, and notification triggers. Manual testing for user experience of receiving the bonus.

    - **Special Considerations:** Thoroughly test the "once per 24-hour period" rule. Test with active and inactive subscribers to verify eligibility. Rigorous security testing to prevent fraudulent bonus awards.

## Story Progress Notes

### Agent Model Used: Bob (SM Agent)

### Completion Notes List

- (To be filled by Developer Agent upon completion)

### Change Log

- (To be filled by Developer Agent upon completion)


