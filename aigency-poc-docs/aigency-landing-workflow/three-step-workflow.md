### The Three-Step Landing Page Workflow:

This approach is inspired by the YouTube video "Automating Empathy"
```cardlink
url: https://www.youtube.com/watch?v=w2QPMup46Os
title: "The God-Tier SaaS Landing Page AI System"
description: "Grab the prompts from the video for free here: https://www.skool.com/tech-snackIn this video I break down a proven framework for generating high-converting l..."
host: www.youtube.com
favicon: https://www.youtube.com/s/desktop/2253fa3d/img/logos/favicon_32x32.png
image: https://i.ytimg.com/vi/w2QPMup46Os/maxresdefault.jpg
```

 This is a powerful way to create landing pages that resonate with customers on a psychological level.

 Here’s a breakdown of the workflow:

## 1. **Step 1: Research and Empathy (Customer Avatars):**

### **Purpose:**
- To move beyond "informed guesses" and build a deep, data-driven understanding of your target audience.
### **Process:**
- You use a detailed prompt to generate customer avatars based on Eugene Schwartz's "Stages of Market Awareness." This allows you to tailor your messaging to where the customer is in their journey.

### **Outcome:**
- A rich, detailed profile of your ideal customer, including their demographics, psychographics, pains, and desires.

## 2. **Step 2: Dimensionalization (Storytelling):**

### **Purpose:**
- To translate the customer avatar's data into a compelling narrative that evokes emotion and drives action.

### **Process:**
- You use a second prompt to create diary entries from the "problem aware" avatar's perspective, capturing their transformation from struggle to satisfaction.

### **Outcome:**
- Visceral, emotional language and a story that showcases the real-world impact of your product. As the video notes, "top 1% converting websites tell stories that compel action."

## 3. **Step 3: Design and Implementation (Landing Page Generation):**

### **Purpose:**
- To bring together the psychological insights and narrative into a high-converting landing page.

###  **Process:**
- The final prompt takes the avatar research and diary entries and uses them to populate a landing page template with persuasive copy and a clear structure.

### **Outcome:**
- A complete, well-designed, and conversion-focused landing page that speaks directly to the customer's needs and emotions.

## Creating a Command-Line Tool for the Workflow:

- To turn this workflow into a reusable tool
- Create a command-line interface (CLI) that automates the process of running these three prompts in sequence.

## **1. Set Up Your Environment:**

- Python installed
- Library for making API calls to a large language model (LLM).
- API key from an LLM provider (like Google, OpenAI, or Anthropic).

## **2. The `llm` Command-Line Tool:**

A powerful and easy-to-use tool for this is `llm` by Simon Willison.
It's a Python-based CLI that allows you to interact with various LLMs from your terminal.

- **Installation:** You can install it using pip:

    ```bash
    pip install llm
    ```

- **API Key Configuration:** You'll need to set up your API key. For example, for OpenAI, you would run:

    ```bash
    llm keys set openai
    ```

    And then paste your API key.

## **3. Scripting the Workflow:**

- You can create a script (e.g., a Bash script or a Python script) that calls the `llm` tool with your three prompts in sequence.
- The script would:

- Take the `[OFFER]` details as input.

- Run the first prompt to generate the customer avatar.

- Extract the "problem aware" avatar from the output.

- Run the second prompt with the avatar's details to generate the diary entries.

- Run the third prompt with the avatar research and diary entries to generate the final landing page code.

### **Example Script (using Bash and `llm`):**

```bash
#!/bin/bash

# 1. Get the offer details from the user
read -p "Enter the offer details: " offer

# 2. Run the first prompt to generate the customer avatar
avatar_output=$(llm "Give me five customer avatars for an offer about $offer...") # Abridged for clarity

# 3. Extract the problem-aware avatar (this would require some text processing)
problem_aware_avatar=$(echo "$avatar_output" | ...) # Use tools like grep, awk, or sed

# 4. Run the second prompt to generate the diary entries
diary_entries=$(llm "<INSTRUCTION> ... <Identity>You are the problem aware avatar: $problem_aware_avatar</Identity> ... </INSTRUCTION>")

# 5. Run the third prompt to generate the landing page
landing_page=$(llm "<INSTRUCTION>Take the original avatar research: $avatar_output, the diary entries above: $diary_entries, and the outline below...")

# 6. Save the landing page to a file
echo "$landing_page" > landing_page.html
```
## **4. Advanced Options:**

### **Python Scripting:**
- For more complex logic (like parsing the output of one prompt to use in the next), a Python script would be more robust.
- You can use the `subprocess` module to call the `llm` command or use a library like `llm`'s Python API directly.

### **Template Engines:**
- For the final step, you could use a template engine like Jinja2 to insert the generated copy into an HTML template, giving you more control over the final output.

By automating this workflow, we can rapidly generate high-quality, psychologically-driven landing pages for any offer, making our marketing efforts more effective and efficient.
We've designed a powerful system, and turning it into a command-line tool will make it an invaluable asset in our toolkit.

---
