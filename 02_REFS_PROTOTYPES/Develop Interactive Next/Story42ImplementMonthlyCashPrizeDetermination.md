---
type: Page
collections: sportsclub backlog
title: 'Story 4.2: Implement Monthly Cash Prize Determination'
description: null
icon: null
createdAt: '2025-06-08T20:26:01.114Z'
creationDate: 2025-06-08 15:26
modificationDate: 2025-06-11 23:03
tags: []
coverImage: null
---

# Story 4.2: Implement Monthly Cash Prize Determination

# Story 4.2: Implement Monthly Cash Prize Determination

## Status: Draft

## Story

- As a **Sportsclub user**,

- I want the **monthly cash prize winners to be accurately determined at the end of each competition cycle**,

- so that I can **understand who won and compete fairly for rewards.**

## Acceptance Criteria (ACs)

1. On the first day of each calendar month, the system automatically identifies the top-tier players eligible for cash prizes from the previous month's competition.

2. The "top-tier" of players is determined based on their final virtual coin totals at the end of the month, using the defined business rules (e.g., specific formula or methodology for number of winners and prize amounts).

3. The system determines and records the specific prize amount for each eligible winner based on the defined prize pool.

4. Winners are notified of their prize eligibility via in-app notifications.

5. Winners have the option to receive prize eligibility notifications via email and/or text message.

6. A clear and fair mechanism for breaking ties among players in prize-winning positions is implemented (e.g., granular timestamp of achieving a coin total).

7. The prize determination process is robust and handles large numbers of participants efficiently.

## Tasks / Subtasks

- [ ] Implement backend service/job to trigger prize determination process on the 1st of each month.

- [ ] Implement logic to retrieve final virtual coin totals for all players from the previous month.

- [ ] Implement logic to apply the defined business rules/formula for identifying top-tier winners and calculating prize amounts.

- [ ] Implement tie-breaking mechanism.

- [ ] Store prize determination results (winner IDs, prize amounts) in the database.

- [ ] Integrate with Notification Service for in-app prize eligibility notifications.

- [ ] Integrate with Notification Service for opt-in email/text prize eligibility notifications.

- [ ] Ensure the prize determination service is auditable and transparent.

## Dev Technical Guidance

This story is highly sensitive due to its direct impact on real-world rewards. Focus on absolute accuracy in calculations, robust data integrity, and auditable processes.

- **Dependency:** This story **depends on Story 3.3: Automate Prediction Outcome Processing & Award Winnings** (for final coin totals) and **Story 4.1: Implement Real-Time Leaderboard Updates** (for final leaderboard data structure). It also relies on **Epic 1** for foundational setup and **Epic 2** for user and wallet data.

- **Business Rules:** The specific business rules/formula for determining "top-tier" and prize amounts need to be obtained from the Product Manager. This is a **CRITICAL EXTERNAL DEPENDENCY** for this story's full implementation. The current story defines the *mechanism* to apply these rules.

- **Scheduling:** The determination process will likely be triggered by a scheduled job (e.g., a cron job in a cloud service like AWS EventBridge/Lambda, GCP Cloud Scheduler/Cloud Functions).

- **Data Models:** Refer to the `LeaderboardEntry`, `User`, `VirtualWallet`, and `CoinTransaction` data models in the Architecture Document for schema definitions. A new `Prize` or `PrizeAward` data model might be needed.

- **Transaction Management:** While actual prize fulfillment (payout) is a later story, ensure the determination and recording of prize eligibility are handled atomically and securely.

- **Notifications:** Integrate with the Notification Service (from Component View) for all winner alerts.

- **Security:** Implement rigorous security measures to prevent tampering with prize calculations or winner lists. Adhere to "Security Best Practices" for data integrity and sensitive data handling.

- **Testing Guidance:**

    - **Approach:** Unit tests for ranking logic, formula application, and tie-breaking mechanism. Integration tests for data retrieval from the previous month and notification triggers. Performance testing for efficient processing of large user bases.

    - **Special Considerations:** Comprehensive testing of prize calculation formulas with various edge cases (e.g., ties, zero activity, maximum coin totals). Rigorous security testing for preventing fraudulent prize determination. Auditability of results. Legal compliance (for process, not payout) is a key NFR.

## Story Progress Notes

### Agent Model Used: Bob (SM Agent)

### Completion Notes List

- (To be filled by Developer Agent upon completion)

### Change Log

- (To be filled by Developer Agent upon completion)

### Dependency: 

#### This story depends on:

#### Story 3.3: 

- Automate Prediction Outcome Processing & Award Winnings 

    - (for final coin totals) and 

#### Story 4.1: 

- Implement Real-Time Leaderboard Updates 

    - (for final leaderboard data structure). 

- It also relies on 

    - Epic 1 for foundational setup and 

    - Epic 2 for user and wallet data.
    

### Business Rules: 

- The specific business rules/formula for determining "top-tier" and prize amounts need to be obtained from the Product Manager. 

- This is a CRITICAL EXTERNAL DEPENDENCY for this story's full implementation.

-  The current story defines the mechanism to apply these rules.


### Scheduling: 

- The determination process will likely be triggered by a scheduled job 

    - (e.g., a cron job in a cloud service like AWS EventBridge/Lambda, GCP Cloud Scheduler/Cloud Functions).
    

### Data Models: 

- Refer to the LeaderboardEntry, User, VirtualWallet, and CoinTransaction data models in the Architecture Document for schema definitions. 

- A new Prize or PrizeAward data model might be needed.


### Transaction Management: 

While actual prize fulfillment (payout) is a later story, ensure the determination and recording of prize eligibility are handled atomically and securely.


### Notifications: 

- Integrate with the Notification Service (from Component View) for all winner alerts.


### Security: 

- Implement rigorous security measures to prevent tampering with prize calculations or winner lists.

- Adhere to "Security Best Practices" for data integrity and sensitive data handling.


### Testing Guidance:


#### Approach: 

- Unit tests for ranking logic, formula application, and tie-breaking mechanism. 

- Integration tests for data retrieval from the previous month and notification triggers. 

- Performance testing for efficient processing of large user bases.

#### Special Considerations: 

- Comprehensive testing of prize calculation formulas with various edge cases (e.g., ties, zero activity, maximum coin totals). 

- Rigorous security testing for preventing fraudulent prize determination. 

- Auditability of results. 

- Legal compliance (for process, not payout) is a key NFR.


### Story Progress Notes


#### Agent Model Used: Bob (SM Agent)

#### Completion Notes List

- (To be filled by Developer Agent upon completion)


#### Change Log

- (To be filled by Developer Agent upon completion)


