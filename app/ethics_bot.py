# app/ethics_bot.py

# Ethics & Bias Review Assistant (Modular Version)
# This module simulates a GPT-based assistant for ethical reflection in AI projects

def run_ethics_bot(project_desc):
    if not project_desc.strip():
        return "[Guiding Questions]\n- Please provide a description of your project so I can help identify ethical considerations."

    # Simulated response for demonstration
    return f"""
[Guiding Questions]
- What kind of data are you collecting, and is it representative of all affected groups?
- Could this project introduce bias against certain populations?
- Are users aware their data is being used in this way?
- What social impact might result from incorrect predictions?
- Is there a feedback loop to mitigate negative outcomes?

[Fairness Concerns]
There may be risks related to fairness or exclusion, especially if sensitive attributes like demographics are involved.

[Reflection Prompt]
Please consider conducting a deeper fairness audit or consulting an ethics panel during development.
"""