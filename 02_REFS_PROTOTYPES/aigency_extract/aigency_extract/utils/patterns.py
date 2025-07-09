"""Fabric-inspired extraction patterns."""

from typing import Dict, List

# Dictionary of pattern names to their descriptions
PATTERN_DESCRIPTIONS: Dict[str, str] = {
    "youtube_summary": "Extract key information from YouTube videos with timestamps and quotes",
    "extract_wisdom": "Extract the wisdom, insights, and practical knowledge from content",
    "summarize": "Create a comprehensive yet concise summary of the content",
    "extract_insights": "Extract novel ideas and unexpected connections from the content",
    "extract_main_idea": "Identify and explain the central thesis of the content",
    "create_5_sentence_summary": "Summarize the entire content in exactly 5 sentences",
}

# Dictionary of pattern names to their example outputs
PATTERN_EXAMPLES: Dict[str, str] = {
    "youtube_summary": """
# How to Learn Anything Fast

## Summary
This video presents a systematic approach to learning new skills quickly and effectively. The speaker outlines a five-step process that focuses on breaking down complex skills, identifying the most important sub-skills to practice first, and using deliberate practice techniques. The method emphasizes the importance of immediate feedback, setting specific goals, and maintaining consistent practice schedules.

## Key Insights
- The 80/20 principle applies to learning: 20% of the sub-skills will give you 80% of the results
- Immediate feedback is crucial for rapid skill development
- Deliberate practice (focused on weaknesses) is more effective than casual practice
- Mental rehearsal can be almost as effective as physical practice
- Learning multiple related skills simultaneously can create beneficial cross-pollination

## Main Points
- Break down the skill into component sub-skills
- Identify the most critical sub-skills to focus on first
- Create a system for immediate feedback
- Practice deliberately with specific goals
- Maintain consistency with a regular practice schedule

## Notable Quotes
> "It's not just about the hours you put in, but what you put into those hours."
> "The difference between experts and amateurs is that experts practice what they're not good at."
> "Five minutes of daily practice is better than an hour once a week."

## Questions Raised
- How do you identify which sub-skills are in the critical 20%?
- How can you create feedback systems for skills that don't have obvious metrics?
- What's the optimal balance between learning breadth and depth?

## Action Items
- Choose one skill to apply this method to immediately
- Create a breakdown of sub-skills for that chosen skill
- Set up a feedback mechanism before beginning practice
- Schedule daily 20-minute practice sessions
- Find a community of practitioners for support and accountability
    """,
    
    "extract_wisdom": """
# The Psychology of Money by Morgan Housel

## Summary
The Psychology of Money explores how people's relationship with money is shaped more by psychology and personal history than by mathematical formulas or financial knowledge. Housel argues that financial decisions are deeply personal and influenced by one's unique experiences, values, and goals rather than purely rational calculations. The book emphasizes that success with money requires understanding your own psychological biases and developing reasonable expectations rather than pursuing optimal returns or following others' financial paths.

## Key Insights
- Financial decisions are heavily influenced by personal history, psychology, and emotions rather than pure mathematics
- Luck and risk play enormous roles in financial outcomes but are often overlooked or misattributed
- Compounding is powerful but requires patience and consistency over long periods
- The ability to adapt to financial setbacks is more important than brilliant planning
- Wealth is what you don't see - it's the money not spent, representing financial freedom and options
- Reasonable financial goals are more likely to succeed than optimal ones

## Main Points
- Financial success depends more on behavior than knowledge
- Everyone has their own unique relationship with money based on their personal experiences
- Long-term thinking and patience are the most important financial skills
- Saving is more important than investing brilliance for most people
- Financial goals should align with personal values rather than social comparison

## Notable Quotes
> "Doing well with money has little to do with how smart you are and a lot to do with how you behave."
> "The highest form of wealth is the ability to wake up every morning and say 'I can do whatever I want today.'"
> "Good investing is not about making good decisions. It's about consistently not screwing up."
> "Money's greatest intrinsic value is its ability to give you control over your time."

## Questions Raised
- How can we better recognize the role of luck in financial outcomes?
- What psychological biases most affect your own financial decisions?
- How much money is "enough" for your personal definition of freedom?
- How can we balance enjoying today with saving for tomorrow?

## Action Items
- Reflect on your personal history with money and how it shapes your current decisions
- Define what "enough" means for your financial goals
- Build a financial margin of safety that allows for unexpected events
- Focus on consistent saving habits rather than investment performance
- Create a financial plan that prioritizes your personal values over social comparison
    """,
}

def get_pattern_names() -> List[str]:
    """Get a list of all available pattern names."""
    return list(PATTERN_DESCRIPTIONS.keys())

def get_pattern_description(pattern_name: str) -> str:
    """Get the description for a specific pattern."""
    return PATTERN_DESCRIPTIONS.get(pattern_name, "No description available")

def get_pattern_example(pattern_name: str) -> str:
    """Get an example output for a specific pattern."""
    return PATTERN_EXAMPLES.get(pattern_name, "No example available")
