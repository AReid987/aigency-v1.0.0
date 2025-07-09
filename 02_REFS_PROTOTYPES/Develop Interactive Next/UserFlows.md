---
type: Page
title: User Flows
description: null
icon: null
createdAt: '2025-06-05T00:07:51.52Z'
creationDate: 2025-06-04 19:07
modificationDate: 2025-06-04 19:44
tags: []
coverImage: null
---

# User Flows

# User Registration & Initial Subscription

## **Goal:** 

- For a new user to successfully create an account, complete ID verification, 

- and activate their first monthly subscription, gaining access to virtual coins for predictions.

### **Steps / Diagram:**

![User Registration & Initial Subscription](../MediaFiles/Images/User%20Registration%20&%20Initial%20Subscription.svg)

[[User Registration & Initial Subscription]]

#### Mermaid

```markdown
graph TD
    A[Start: Arrive at Sportsclub Platform] --> B{Choose Sign-up Method};
    B -- Email/Password --> C[Provide Sign-up Details: Email, Password, Age, Address];
    C --> D[Agree to ToS & Privacy Policy];
    B -- OAuth --> E[Select OAuth Provider];
    E --> F[Authenticate with OAuth Provider];
    F --> D;
    D --> G[Account Created / Initial Login];
    G --> H[Access Basic Features / Dashboard (Non-Transactional)];
    H --> I{Attempt to Subscribe / Make Prediction};
    I --> J[Trigger ID Verification Process];
    J --> K[Submit ID Documents via Camera];
    K --> L{ID Verification Pending};
    L -- Verified --> M[Subscription Purchase Page];
    L -- Failed/More Info --> N[Notify User of Verification Status];
    N --> K;
    M --> O[Select Payment Method & Complete Subscription];
    O --> P[Subscription Active / First Coins Distributed (Pro-rata if mid-month)];
    P --> Q[Access Full Platform Features];
    Q --> End[End: User Fully Onboarded and Engaged];
```



### **Description of Steps:**

#### **Start: Arrive at Sportsclub Platform:** 

- User lands on the Sportsclub homepage or login screen.

#### **Choose Sign-up Method:** 

- User selects between email/password registration or an OAuth provider (e.g., Google).

#### **Provide Sign-up Details:** 

- If choosing email/password, user enters email, desired password, age, and address.

#### **Agree to ToS & Privacy Policy:** 

- User must agree to legal terms before proceeding.

#### **Select OAuth Provider / Authenticate:** 

- If choosing OAuth, user selects provider and completes authentication via that service.

#### **Account Created / Initial Login:** 

- User's account is created, and they are logged in for the first time.

#### **Access Basic Features / Dashboard (Non-Transactional):** 

- User can access general parts of the app 

    - (e.g., news, forums - if accessible without verification) while full features are locked.

#### **Attempt to Subscribe / Make Prediction:** 

- User attempts an action that requires a subscription and ID verification.

#### **Trigger ID Verification Process:** 

- The system initiates the ID verification flow.

#### **Submit ID Documents via Camera:** 

- User submits required identification documents 

    - (e.g., state ID, passport) using their device's camera.

#### **ID Verification Pending:** 

- The system processes the verification. 

- User is informed of pending status, 

    - and restricted features remain grayed out or unavailable.

#### **Notify User of Verification Status:** 

- User is informed of success, failure, or if more information is needed. 

- If failed, they are prompted to retry.

#### **Subscription Purchase Page:** 

- Upon successful ID verification, 

    - the user is directed to complete their subscription purchase.

#### **Select Payment Method & Complete Subscription:** 

- User selects a payment method and finalizes the subscription.

#### **Subscription Active / First Coins Distributed:** 

- The subscription becomes active, 

    - and the user receives their first virtual coin distribution 

    - (pro-rata if mid-month).

#### **Access Full Platform Features:** 

- User now has full access to all features, including prediction placement.

#### **End: User Fully Onboarded and Engaged:** 

- The user has successfully completed the onboarding journey.



---

# 2. Placing a Prediction & Receiving Winnings

### **Goal:** 

- For an active, verified, and subscribed user to successfully find a major sporting event, 

    - place a prediction with virtual coins, and receive their winnings for a correct pick.

#### **Steps / Diagram:**

[[Mermaid Chart Editor June 4 2025 (1)]]

#### Markdown

```markdown
graph TD
    A[Start: User on Dashboard/Events Page] --> B[Browse/Filter/Search Major Sporting Events];
    B --> C{Select an Event};
    C --> D[View Event Details & Odds];
    D --> E[Choose Predicted Winner];
    E --> F[Specify Coin Amount (increments of 1,000; min 1,000; max wallet balance)];
    F --> G[Confirm Prediction Details];
    G --> H[Submit Prediction];
    H --> I[Receive In-App Confirmation of Prediction];
    I --> J[View Active/Pending Predictions];
    J --> K[Wait for Event Outcome];
    K --> L{Event Concludes & Outcome Verified};
    L -- Correct Prediction --> M[Winnings Calculated (coins * odds) & Credited to Wallet];
    L -- Incorrect Prediction --> N[Coins Deducted from Wallet];
    M --> O[Receive In-App Notification of Result];
    N --> O;
    O --> P[View Updated Wallet Balance & Transaction History];
    O --> Q[Leaderboard Updates in Real-Time];
    Q --> End[End: Prediction Cycle Complete];
```

- **Description of Steps:**

    1. **Start: User on Dashboard/Events Page:** User begins their session, either from the main dashboard or directly on the event listings.

    2. **Browse/Filter/Search Major Sporting Events:** User navigates the list of available events, using filters or search if needed.

    3. **Select an Event:** User taps/clicks on a specific sporting event they are interested in.

    4. **View Event Details & Odds:** The system displays comprehensive details about the event, including teams/participants, date/time, and odds for each potential outcome.

    5. **Choose Predicted Winner:** User selects their pick for the winner of the chosen event.

    6. **Specify Coin Amount:** User inputs the amount of virtual coins they wish to place, adhering to the specified increments, minimums, and maximums based on their wallet balance.

    7. **Confirm Prediction Details:** User reviews their selected pick and coin amount before final submission.

    8. **Submit Prediction:** User confirms and submits their prediction.

    9. **Receive In-App Confirmation of Prediction:** The system provides immediate in-app feedback that the prediction has been successfully placed.

    10. **View Active/Pending Predictions:** User can access a section to see all their predictions that are awaiting an outcome.

    11. **Wait for Event Outcome:** User waits for the actual sporting event to conclude.

    12. **Event Concludes & Outcome Verified:** The system officially determines and records the outcome of the completed event.

    13. **Winnings Calculated & Credited to Wallet:** If the prediction is correct, winnings are calculated (coins placed * odds) and promptly added to the user's virtual wallet.

    14. **Coins Deducted from Wallet:** If the prediction is incorrect, the coins placed are deducted from the user's wallet.

    15. **Receive In-App Notification of Result:** User receives an in-app notification about the outcome of their prediction (win or loss), with an option for email/text alerts.

    16. **View Updated Wallet Balance & Transaction History:** User can check their wallet to see the updated coin balance and the transaction history reflecting the prediction result.

    17. **Leaderboard Updates in Real-Time:** The leaderboard dynamically updates to reflect the user's new coin total.

    18. **End: Prediction Cycle Complete:** The user has completed a full prediction cycle.

---

## 3. Interacting with the AI Assistant for Data Visualization

### **Goal:** 

- For a user to successfully leverage the AI Assistant to request 

    - and view a visualization of sports-related data, 

    - enhancing their understanding and strategic analysis.

#### **Steps / Diagram:**

![Mermaid Chart Editor June 4 2025 (2)](../MediaFiles/Images/Mermaid%20Chart%20Editor%20June%204%202025%20(2).svg)

[[Mermaid Chart Editor June 4 2025 (2)]]

#### Mermaid

```markdown
graph TD
    A[Start: User accesses AI Assistant Interface] --> B[Input Query for Data/Visualization (Text or Voice)];
    B --> C{AI Processes Request};
    C -- Recognizes data/viz need --> D[AI Generates Data/Visualization];
    D --> E[Display Loading Indicator];
    E --> F[Present Generated Visualization to User];
    F --> G[User Analyzes Visualization];
    G --> H{User Asks Follow-up Questions / Requests more data};
    H -- Yes --> B;
    H -- No --> End[End: User Gains Insight];
```

### **Description of Steps:**

#### **Start: User accesses AI Assistant Interface:** 

- User navigates to the dedicated AI Assistant section of the platform.

#### **Input Query for Data/Visualization:** 

- User types or speaks a request for specific sports data or a visualization 

    - (e.g., "Show me Team A's home game win rate as a bar chart," 

    - "Visualize my prediction accuracy over the last month").

#### **AI Processes Request:** 

- The AI Assistant interprets the user's natural language query.

#### **AI Generates Data/Visualization:** 

- If the request is for data visualization, 

    - the AI processes the relevant sports data 

    - and generates the appropriate chart or graph.

#### **Display Loading Indicator:** 

- A loading animation is displayed while the AI processes the request 

    - and generates the visual.

#### **Present Generated Visualization to User:** 

- The generated chart, graph, or other visualization is displayed clearly on the screen.

#### **User Analyzes Visualization:** 

- The user reviews and interprets the presented data.

#### **User Asks Follow-up Questions / Requests more data:** 

- User can ask clarifying questions about the visualization 

    - or request further data/visualizations, 

    - restarting the interaction loop.

#### **End: User Gains Insight:** 

- The user concludes their interaction having gained new insights 

    - or understanding from the AI-generated data.

---

# 4. Engaging in a Community Forum Discussion

## **Goal:** 

- For a user to successfully browse, interact with, 

    - or create content within the Sportsclub community forum, 

    - fostering engagement and shared interest.

### **Steps / Diagram:**

![sportsclub-ux-flow-engaging-in-community-forum](../MediaFiles/Images/sportsclub-ux-flow-engaging-in-community-forum.svg)

[[sportsclub-ux-flow-engaging-in-community-forum]]

#### Mermaid

```text
graph TD
    A[Start: User accesses Community Forum] --> B[Browse Forum Categories/Topics];
    B --> C{Select Category/Existing Post};
    C -- Select Category --> D[View Posts in Category];
    C -- Select Post --> E[View Individual Forum Post & Comments];
    D --> E;
    E --> F{User Wants to Interact};
    F -- Create New Post --> G[Draft New Post (Text, Link, Image)];
    G --> H[Submit New Post];
    F -- Comment on Post --> I[Draft Comment];
    I --> J[Submit Comment];
    F -- Vote on Content --> K[Upvote/Downvote Post/Comment];
    F -- Bookmark Post --> L[Bookmark Post for Later];
    H --> M[Post Appears in Forum];
    J --> M;
    M --> N{AI Agent Participation};
    N -- AI Posts Prompt --> O[AI-Initiated Discussion];
    N -- AI Responds to User --> P[AI Provides Info/Facilitates Discussion];
    N -- AI Flags Content --> Q[Content Flagged for Moderation Dashboard];
    O --> E;
    P --> E;
    M --> End[End: Community Interaction];
```

### **Description of Steps:**

#### **Start: User accesses Community Forum:** 

- User navigates to the main Sportsclub community forum section.

#### **Browse Forum Categories/Topics:** 

- User sees a list of predefined or user-created forum categories and topics.

#### **Select Category/Existing Post:** 

- User chooses to view posts within a specific category or clicks on an existing post.

#### **View Posts in Category:** 

- If a category is selected, user sees a list of posts within that category.

#### **View Individual Forum Post & Comments:** 

- User can read a specific post and all associated comments.

#### **User Wants to Interact:** 

- User decides to create new content or interact with existing content.

#### **Draft New Post:** 

- User composes a new post, including text, links, or images.

#### **Submit New Post:** 

- User submits their new post to the forum.

#### **Draft Comment:** 

- User composes a comment in response to a post or another comment.

#### **Submit Comment:** 

- User submits their comment.

#### **Upvote/Downvote Post/Comment:** 

- User can express their sentiment by voting on forum content.

#### **Bookmark Post for Later:** 

- User saves a post for easy access later.

#### **Content Appears in Forum:** 

- The user's new post or comment is now visible in the forum.

#### **AI Agent Participation:** 

- AI agents actively engage in the forum.

#### **AI-Initiated Discussion:** 

- AI agents may post discussion prompts or relevant topics.

#### **AI Provides Info/Facilitates Discussion:** 

- AI agents respond to user posts or comments, 

    - providing factual information or facilitating the conversation.

#### **Content Flagged for Moderation Dashboard:** 

- AI agents automatically flag potentially problematic content for human review.

#### **End: Community Interaction:** 

- The user's interaction within the community forum concludes.

---

# 5. Participating in a Live Event Chat

## **Goal:** 

- For a user to engage in real-time discussions during a live sporting event, 

- view real-time scores, and benefit from AI-assisted moderation and updates.

#### **Steps / Diagram:**

![sportsclub-ux-flow-participating-in-live-chat](../MediaFiles/Images/sportsclub-ux-flow-participating-in-live-chat.svg)

[[sportsclub-ux-flow-participating-in-live-chat]]

#### Mermaid

```text
graph TD
    A[Start: User accesses Live Event Chat Room] --> B[View Real-Time Scores & Event Updates];
    B --> C[View List of Active Participants];
    C --> D{User Sends Message/Reaction};
    D -- Send Message --> E[Type and Send Text Message];
    D -- Send Reaction --> F[Select and Send Emoji Reaction];
    E --> G[Message Appears in Chat Feed];
    F --> G;
    G --> H{AI Agent Participation};
    H -- AI Moderates --> I[AI Filters Inappropriate Content];
    H -- AI Answers Questions --> J[AI Responds to General Event Queries];
    H -- AI Posts Updates --> K[AI Posts Automated Updates/Highlights];
    I --> G;
    J --> G;
    K --> G;
    G --> L[Continue Chatting];
    L --> End[End: User Exits Chat Room];
```

### **Description of Steps:**

#### **Start: User accesses Live Event Chat Room:** 

- User navigates to a dedicated chat room for a specific live sporting event 

    - (from Live Events page, leaderboard, or user profile).

#### **View Real-Time Scores & Event Updates:** 

- The chat interface displays real-time scores and key updates for the associated live event.

#### **View List of Active Participants:** 

- User sees a list of other individuals currently present in the chat room.

#### **User Sends Message/Reaction:** 

- User decides to contribute to the chat by typing a message or sending an emoji reaction.

#### **Type and Send Text Message:** 

- User types their message and sends it.

#### **Select and Send Emoji Reaction:** 

- User selects an emoji to react to a message or event and sends it.

#### **Message Appears in Chat Feed:** 

- The user's message or reaction is displayed in the live chat feed.

#### **AI Agent Participation:** 

- AI agents actively participate in the live chat.

#### **AI Filters Inappropriate Content:** 

- AI agents automatically filter and potentially flag inappropriate language or content.

#### **AI Responds to General Event Queries:** 

- AI agents answer factual questions related to the live event 

    - (e.g., rules, current game state).

#### **AI Posts Automated Updates/Highlights:** 

- AI agents post automated updates, highlights, or interesting statistics about the game.

#### **Continue Chatting:** 

- Users continue to interact in the live chat as the event progresses.

#### **End: User Exits Chat Room:** 

- User leaves the live event chat room.

---

# 6. Claiming a Monthly Cash Prize

## **Goal:** 

- For a top-tier player to be successfully notified of their cash prize win 

    - and initiate the process for prize fulfillment.

### **Steps / Diagram:**

![sportsclub-ux-flow-claiming-cash-prize](../MediaFiles/Images/sportsclub-ux-flow-claiming-cash-prize.svg)

[[sportsclub-ux-flow-claiming-cash-prize]]

#### Mermaid

```markdown
graph TD
    A[Start: End of Month / Prize Determination] --> B{User Identified as Top-Tier Winner};
    B --> C[Receive In-App Notification of Prize Win];
    C --> D{User Opts-in for Email/Text Notification};
    D -- Yes --> E[Receive Email/Text Notification];
    E --> F[Access Prize Claim Interface];
    C -- No --> F;
    F --> G[Provide Required Information for Prize Fulfillment (TBD Process)];
    G --> H[Submit Claim Request];
    H --> I[Claim Request Pending Review];
    I --> J{Verification & Fulfillment (TBD Legal/Payment Process)};
    J -- Successful --> K[Cash Prize Disbursed to User];
    J -- Failed/More Info --> L[Notify User of Issue / Request More Info];
    L --> G;
    K --> End[End: Prize Successfully Claimed];
```

### **Description of Steps:**

#### **Start: End of Month / Prize Determination:** 

- The monthly competition period concludes, 

- and the system identifies top-tier winners based on defined criteria.

#### **User Identified as Top-Tier Winner:** 

- The system flags a user as eligible for a cash prize.

#### **Receive In-App Notification of Prize Win:** 

- The user receives a prominent in-app notification about their prize win.

#### **User Opts-in for Email/Text Notification:** 

- User can choose to receive additional notifications via email and/or text message.

#### **Receive Email/Text Notification:** 

- If opted in, the user receives an external notification confirming their win.

#### **Access Prize Claim Interface:** 

- User navigates to a dedicated section to claim their prize 

    - (either directly from the notification or via their profile/wallet).

#### **Provide Required Information for Prize Fulfillment (TBD Process):** 

- User is prompted to provide necessary information 

    - (e.g., payment details, tax info) 

- as part of a process that still needs to be legally defined.

#### **Submit Claim Request:** 

- User submits the provided information to initiate the prize claim.

#### **Claim Request Pending Review:** 

- The system processes the claim request, which may involve internal review.

#### **Verification & Fulfillment (TBD Legal/Payment Process):** 

- The system or an external service conducts verification 

    - and initiates the payment process, which is a legally complex "TBD" area.

#### **Cash Prize Disbursed to User:** 

- Upon successful verification and processing, the cash prize is transferred to the user.

#### **Notify User of Issue / Request More Info:** 

- If there are issues with the claim 

    - (e.g., incomplete info, verification failure), 

- the user is notified and prompted for correction.

#### **End: Prize Successfully Claimed:** 

- The user has successfully received their cash prize.

---

# 7. Receiving a Gamification Bonus (e.g., Daily Login)

## **Goal:** 

- For a user to automatically receive various gamification bonuses 

    - (like daily coins, login streaks, prediction win streaks, 

    - or community challenge rewards) that enhance their engagement and enjoyment.

### **Steps / Diagram:**

[[sportsclub-ux-flow-gamification-bonus]]

#### Mermaid

```markdown
graph TD
    A[Start: User Performs Qualifying Action] --> B{System Detects Eligible Bonus};
    B -- Daily Login --> C[First Login/Activity of Day];
    B -- Login Streak --> D[Consecutive Login/Activity Day];
    B -- Prediction Win Streak --> E[Consecutive Correct Prediction];
    B -- Community Challenge --> F[Completes Challenge Criteria];
    C --> G[Award Daily Bonus Coins (Automatic)];
    D --> H[Award Login Streak Bonus (Coins/Badges)];
    E --> I[Award Prediction Win Streak Bonus (Coins)];
    F --> J[Award Community Challenge Bonus Coins];
    G --> K[Notify User of Bonus Received (In-App)];
    H --> K;
    I --> K;
    J --> K;
    K --> L[Wallet Balance Updates];
    L --> End[End: User Engaged with Gamification];
```

### **Description of Steps:**

#### **Start: User Performs Qualifying Action:** 

- The user performs an action that could trigger a gamification bonus 

    - (e.g., logging in, making a prediction, participating in a community activity).

#### **System Detects Eligible Bonus:** 

- The system continuously monitors user activity 

    - to determine if they are eligible for any bonuses.

#### **First Login/Activity of Day:** 

- (For Daily Bonus Coins) 

- The system detects the user's first qualifying login or activity of the current day.

#### **Consecutive Login/Activity Day:** 

- (For Login Streak Bonuses) 

- The system detects that the user has maintained their login streak 

    - by logging in on consecutive days.

#### **Consecutive Correct Prediction:** 

- (For Prediction Win Streak Bonuses) 

- The system identifies a new correct prediction that extends a user's win streak.

#### **Completes Challenge Criteria:** 

- (For Community Challenges) 

- The system confirms the user has met the criteria for a specific community challenge.

#### **Award Daily Bonus Coins** 

- (Automatic): 

- The system automatically adds the defined daily bonus coins to the user's wallet.

#### **Award Login Streak Bonus** 

- (Coins/Badges): 

- The system automatically awards bonus coins and/or digital badges 

    - for achieving a new login streak milestone.

#### **Award Prediction Win Streak Bonus** 

- (Coins): 

- The system automatically awards increasing bonus coins 

    - for extending a prediction win streak.

#### **Award Community Challenge Bonus Coins:** 

- The system automatically awards bonus coins 

    - for successful participation in a community challenge.

#### **Notify User of Bonus Received** 

- (In-App): 

- The user receives an immediate in-app notification 

    - confirming which bonus they received.

#### **Wallet Balance Updates:** 

- The user's virtual coin balance in their wallet automatically updates 

    - to reflect the new bonus.

#### **End: User Engaged with Gamification:** 

- The user experiences the positive reinforcement of the gamification system.

---

