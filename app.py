import streamlit as st

from experiments.fitness_assistant import LocalFitnessAssistant
from agents.what_to_wear import create_what_to_wear_agent

def main():
    st.set_page_config(page_title="AI Multi-Assistant", page_icon="🤖", layout="wide")

    st.title("🤖 AI Multi-Assistant")

    st.sidebar.title("Select Your Assistant")

    assistant_choice = st.sidebar.selectbox(
        "Choose Assistant", ["Fitness Assistant", "What To Wear Assistant"]
    )

    if assistant_choice == "Fitness Assistant":
        st.sidebar.markdown("**Mode Description:**")
        st.sidebar.markdown(
            "This assistant will help you plan fitness workouts based on your preferences, "
            "activity level, and previous workouts."
        )

        user_input = st.text_area(
            "Enter workout preferences:",
            height=200,
            placeholder="For example: 'I want to focus on strength training for 45 minutes.'"
        )

        if st.button("Generate Workout Plan"):
            if user_input:
                assistant = LocalFitnessAssistant()  
                workout_plan = assistant.generate_workout_plan(user_input)
                st.write("### Workout Plan")
                st.write(workout_plan)
            else:
                st.warning("Please provide workout preferences.")

    elif assistant_choice == "What To Wear Assistant":
        st.sidebar.markdown("**Mode Description:**")
        st.sidebar.markdown(
            "This assistant will suggest an outfit based on the current weather in your city."
        )

        city = st.text_input("Enter your city:", placeholder="Enter city name (e.g., Rijeka)")

        if st.button("Get Outfit Recommendation"):
            if city:
                agent = create_what_to_wear_agent()
                outfit_suggestion = agent.run(city)

                if 'ask_user' in outfit_suggestion:
                    user_response = st.text_input(outfit_suggestion['ask_user'])
                    
                    if user_response:
                        final_outfit = agent.process_user_response(user_response)
                        st.write("### Outfit Suggestion")
                        st.write(final_outfit)
                else:
                    st.write("### Outfit Suggestion")
                    st.write(outfit_suggestion)
            else:
                st.warning("Please enter a city name.")

    # Footer
    st.markdown("---")
    st.markdown(
        """
    <div style='text-align: center'>
        <p>Made using Python and Ollama</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
