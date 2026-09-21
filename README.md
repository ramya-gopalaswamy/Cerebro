Inspiration
Every New Year, I make resolutions, but I rarely follow them through. I also tend to procrastinate and over time I realized that a traditional to do list wasn’t enough to keep me accountable to my goals.

I was also inspired by the movie Inside Out. The characters in the movie show how emotions play a crucial role in human decision-making and motivation. That insight became the foundation of Cerebro.

What it does
Cerebro is an autonomous system designed to help users achieve their goals. After a user defines a goal, the system breaks it down into actionable daily tasks tailored to the user’s context. For demo purpose I have just built it for job goal, So in this system, it goes through the user's resume to identify skill gaps and recommend them something to learn. It also lists relevant jobs and leetcode questions which the user has to solve daily.

Cerebro doesn’t stop at task creation—it also automatically verifies progress by checking gmail/leetcode, user doesn't need to give this input. Based on user performance users are awarded with orbs. At the end of the week, a progress journal is created where feedback is given using the characters of Joy, Sadness, Anxiety, Anger and logic which help users better understand their momentum over time. Cerebro also generates a reflective summary and actionable feedback to guide the user forward.

How we built it
Cerebro was built using a multi-agent architecture, where each agent has a focused responsibility.

A Planner Agent breaks goals into structured daily tasks. Using tool Yutori, it extracts relevant LeetCode problems , analyzes the user’s resume, and recommends jobs the user can apply for.
A Verification Agent using tool tinyfish checks task completion by reviewing the user’s LeetCode profile and Gmail inbox for job applications and interview updates. When interviews are detected, the system automatically adjusts the learning plan.
Claude is used to summarize weekly progress for the discussion between the emotions to provide user feedback. We use ElevenLabs for text-to-speech to turn weekly reflections into narrated stories. I also used Freepik to generate image of jobland landing page and also in the journal page
Challenges we ran into
One of the biggest challenges was reliably verifying user progress using real-world signals. Integrating with external platforms like LeetCode and Gmail required careful handling of permissions.

Designing the emotional feedback system was another challenge. I wanted emotions like Sadness, Anxiety, and Anger to reflect missed tasks without discouraging users or making the experience feel punitive.

Building a multi-agent system introduced orchestration complexity. Ensuring that planner, verification, emotion, and reflection agents communicated clearly, and that their decisions were explainable to the user was critical to maintaining trust in the system.

Accomplishments that we're proud of
I built a fully functioning autonomous, multi-agent accountability system that goes beyond static to-do lists and actively adapts to real user behavior. Cerebro is able to plan tasks, verify real-world progress, and adjust future actions without manual intervention.

I am particularly proud of integrating real-world verification into the system. By checking platforms like LeetCode and Gmail, Cerebro closes the loop between intention and execution.

I brought the experience together through weekly emotional storytelling, using Claude for reflective discussions and ElevenLabs for voice narration. This transformed raw progress metrics into a meaningful narrative, helping users better understand their journey and stay motivated.

What we learned
One of the biggest takeaways was that accountability works best when it is adaptive. Automatically adjusting plans based on real-world signals, such as upcoming interviews, made the system feel supportive rather than rigid.

Building Cerebro reinforced the importance of clear responsibility boundaries in multi-agent systems. Separating planning, verification, emotional evaluation, and reflection into distinct agents made the system easier to reason about, debug, and iterate on.

What's next for Project Cerebro
This project can be expanded to include more goals. Richer Verification Signals: Expand beyond Gmail & LeetCode,Support GitHub commits, portfolio updates, learning platforms, Stronger multi-signal confidence scoring instead of binary checks
