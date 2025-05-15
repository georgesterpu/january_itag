import streamlit as st
import requests

def create_profile_page():
    st.header("Create Your Profile")
    full_name = st.text_input("Full Name")
    headline = st.text_input("Headline")
    about = st.text_area("Describe your experience")
    skills = st.text_input("Skills (comma-separated)")
    github_url = st.text_input("GitHub URL")

    # Add contact information fields
    email = st.text_input("Email")
    phone = st.text_input("Phone")

    if st.button("Submit"):
        response = requests.post("http://localhost:8000/candidate/", json={
            "full_name": full_name,
            "headline": headline,
            "about": about,
            "skills": [s.strip() for s in skills.split(",")],
            "github_url": github_url,
            "email": email,
            "phone": phone
        })

        if response.status_code == 200:
            st.success("Profile submitted successfully!")
            st.write("AI Summary:")
            st.markdown(response.json()["summary"])
        else:
            st.error("Something went wrong.")

def get_relevance_color(similarity: float) -> str:
    if similarity >= 0.8:
        return "green"
    elif similarity >= 0.7:
        return "orange"
    return "red"

def search_profiles_page():
    st.header("Find Relevant Profiles")
    query = st.text_area("Enter your query (e.g., 'software engineer with Python and React experience'):")

    if st.button("Search"):
        if query:
            # Call Supabase to search for relevant profiles
            try:
                api_url = f"http://localhost:8000/search/?query={query}"  # Construct the URL
                response = requests.get(api_url)

                if response.status_code == 200:
                    profiles = response.json()  # Parse the JSON response

                if profiles:
                    st.subheader("Matching Profiles:")
                    for i, profile in enumerate(profiles):
                        # Create a container for each profile
                        with st.container():
                            # Display similarity score as a progress bar
                            similarity = profile.get('similarity', 0)
                            color = get_relevance_color(similarity)
                            st.progress(similarity, text=f"Match Score: {similarity:.0%}")
                            st.caption(f"Relevance: :{color}[{'●' * int(similarity * 5)}]")
                            # Profile information
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.markdown(f"### {profile['full_name']}")
                                st.markdown(f"**{profile['headline']}**")
                                st.markdown(f"**About:** {profile['about']}")
                                st.markdown(f"**Skills:** {', '.join(profile['skills'])}")
                                st.markdown(f"**GitHub:** {profile['github_url']}")
                            
                            with col2:
                                # Contact information and actions
                                # Show contact info if toggle is on
                                st.markdown(f"**📞 Phone:** {profile.get('phone', 'N/A')}")
                                st.markdown(f"**📧 Email:** {profile.get('email', 'N/A')}")
                                if profile.get('github_url'):
                                    st.markdown(f"[💻 URL]({profile['github_url']})")
                            
                            st.write("---")
                else:
                    st.info("No matching profiles found.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a search query.")

def main():
    st.title("Mission-Driven Careers Portal")

    # Create a sidebar for navigation
    page = st.sidebar.selectbox("Choose a page", ["Create Profile", "Search Profiles"])

    if page == "Create Profile":
        create_profile_page()
    elif page == "Search Profiles":
        search_profiles_page()

if __name__ == "__main__":
    main()