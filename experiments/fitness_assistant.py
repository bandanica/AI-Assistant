import streamlit as st
from openai import OpenAI

class LocalFitnessAssistant:
    def __init__(self):
        self.client = OpenAI(
            api_key="ollama",
            base_url="http://localhost:11434/v1/",
        )
        self.model = "deepseek-r1:14b"

    def process_request(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                stream=True,
            )

            result = st.empty()
            collected_chunks = []

            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    collected_chunks.append(chunk.choices[0].delta.content)
                    result.markdown("".join(collected_chunks))

            return "".join(collected_chunks)

        except Exception as e:
            return f"Error: {str(e)}"


def get_system_prompt():
    return """You are a personal AI fitness coach.
Your task is to help the user plan customized gym workouts.
You should:
- Ask relevant follow-up questions if not enough information is provided
- Adjust workouts based on the user’s preferences, energy levels, past history, and goals
- Track previous workouts and feedback
- Adapt training intensity (light/medium/hard) based on user input
- Be supportive, motivating, and clear in your communication
Assume the user is moderately active and working out 3–4 times per week."""


def main():
    st.set_page_config(page_title="🏋️ AI Fitness Coach", layout="wide")
    st.title("🏋️ Local AI Fitness Assistant")
    st.markdown("Personalized gym plans powered by a local language model via Ollama")

    system_prompt = get_system_prompt()

    user_prompt = st.text_area(
        "🗨️ Describe what kind of training you want today (duration, intensity, focus, etc.):",
        height=200,
        placeholder="Example: 'I want a 45-minute gym workout focused on strength, not too intense.'",
    )

    submit = st.button("💪 Generate My Training Plan")

    if submit:
        if user_prompt.strip():
            with st.spinner("Your fitness coach is preparing a plan..."):
                assistant = LocalFitnessAssistant()
                assistant.process_request(system_prompt, user_prompt)
        else:
            st.warning("⚠️ Please enter some training preferences first!")

    st.markdown("---")
    st.markdown("<div style='text-align:center'>Created using DeepSeek + Ollama</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
