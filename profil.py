import streamlit as st

st.title("Team Profile")

team_members = [
    {"name": "Gwenn Chanaya Monard Deloveta", "major": "Actuarial Science", "foto": "https://raw.githubusercontent.com/gwenndeloveta-glitch/team-profile-images2/refs/heads/main/gwenn.jpg"},
    {"name": "Muhammad Fatan Rizal Azizi", "major": "Actuarial Science", "foto": "https://raw.githubusercontent.com/gwenndeloveta-glitch/team-profile-images2/refs/heads/main/fatan%20(1).jpg"},
    {"name": "Muhammad Fathdio Putra Sulistiyono", "major": "Actuarial Science", "foto": "https://raw.githubusercontent.com/gwenndeloveta-glitch/team-profile-images2/refs/heads/main/fathdio%20(1).jpg"},

]

cols = st.columns(3)
for i, member in enumerate(team_members):
    with cols[i % 3]:
        st.image(member["foto"], width=180)
        st.markdown(f"**{member['name']}**")
        st.caption(member["major"])
