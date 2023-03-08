import json
import random
from typing import Any, Iterable
from urllib import parse, request

import pandas as pd
import streamlit as st

# # Set page title and description
# st.set_page_config(page_title="MCQ de traduction français-bassa",
#                    page_icon=":books:",
#                    layout="wide")


@st.cache_resource
def read_csv(filename: str) -> pd.DataFrame:
    return pd.read_csv(filename)


# Set up the Giphy API endpoint URL and API key
URL_API = "http://api.giphy.com/v1/gifs/search"
DATABASE_FILE = "data/db.csv"

DATABASE = read_csv(DATABASE_FILE)
print(DATABASE.head())


# Define a function to retrieve the image urls for a given query
@st.cache_data
def get_image_url(query: str) -> str:
    params = parse.urlencode(
        {
            "q": query,
            "api_key": st.secrets["api_key"],
            "lang": "fr",
            "limit": "2",
            "rating": "g",
        }
    )

    with request.urlopen("".join((URL_API, "?", params))) as response:
        data = json.loads(response.read())
        try:
            url = data["data"][0]["images"]["original"]["url"]
        except IndexError:
            url = "https://media.giphy.com/media/14uQ3cOFteDaU/giphy.gif"
    return url.split("?")[0]


def write_question() -> Iterable:
    """
    Selects a random question and displays it in the Streamlit app along with a multiple-choice question.

    Returns:
    - A list of image URLs related to the question.
    - A list of possible answers to the question, including the correct answer and 3 random incorrect answers.
    """
    selected = DATABASE.sample()

    selected_bassa = selected["bassa"].values[0]
    selected_fr = selected["traduction"].values[0]
    # Define the correct answer to the MCQ
    correct_ = selected_bassa

    # Test the function
    query = selected_fr

    # Set up the Google Images API
    urls = get_image_url(query)
    print(urls)
    propositions = [
        selected_bassa,
        *random.sample(set(DATABASE["bassa"]) - {selected_bassa}, 3),
    ]
    random.shuffle(propositions)
    return urls, correct_, selected_fr, propositions


def display_question(
    img_url: str, correct: str, traduction: str, choices: Iterable[str]
) -> Any:
    if not (
        img_url is None or correct is None or traduction is None or choices is None
    ):
        container = st.container()
        with container:
            st.title(traduction)
            col1, col2 = st.columns(2)

            gif_tag = f'<img src="{img_url}" alt="GIF" width="300" height="200">'

            # Show the GIF in the Streamlit app using st.markdown
            col1.markdown(gif_tag, unsafe_allow_html=True)
            # col1.markdown(f"![Alt Text]({img_url})")

            with col2:
                # Display the question and radio buttons
                answer = st.radio(
                    f"Quelle est la traduction correcte pour : {traduction} ?",
                    choices,
                )

                # style = """
                #     <style>
                #         div[data-baseweb="radio"] label {
                #             font-size: 50px !important;
                #         }
                #                 body {
                #         font-size: 70px;
                #     }

                #     </style>
                # """

                # st.markdown(style, unsafe_allow_html=True)
                # Check if the answer is correct and display a message
                submit = st.button(
                    f'Valider la traduction de "{traduction}"'
                )  # Very Important not to have duplicates
                if submit:
                    if answer == correct:
                        st.write(
                            '<p style="color:green; font-size: 40px;">Correct!</p>',
                            unsafe_allow_html=True,
                        )
                        # st.write("Correct!")
                    else:
                        st.write(
                            f'<span style="color:red; font-size: 25px;">{random.choice(["Raté","Faux","Perdu","Dommage","Zut"])}!</span> <span style="color:black; font-size: 20px;">La bonne réponse est </span><span style="color:green; font-size: 20px;">{correct}.</span>',
                            unsafe_allow_html=True,
                        )
        return container


# Define the Streamlit app
def main() -> None:
    # # Set page header
    # container = st.container()

    # container.write("<h1 style='text-align: center; color: #278899;'>MCQ de traduction français-bassa</h1>", unsafe_allow_html=True)
    # container.write("<hr>", unsafe_allow_html=True)

    # # Add description
    # container.write("<h3>Testez vos compétences en traduction français-bassa avec ce MCQ interactif !</h3>", unsafe_allow_html=True)
    # container.write("<p>Cliquez sur le bouton ci-dessous pour commencer le quiz.</p>", unsafe_allow_html=True)

    # # Add start button
    st.markdown("<style>body { font-size: 45px; }</style>", unsafe_allow_html=True)

    if "image_urls" not in st.session_state:
        st.session_state.image_urls = None
    if "correct_answer" not in st.session_state:
        st.session_state.correct_answer = None

    if "correct_question" not in st.session_state:
        st.session_state.correct_question = None
    if "answer_choices" not in st.session_state:
        st.session_state.answer_choices = None

    question = st.empty()
    with question:
        display_question(
            st.session_state.image_urls,
            st.session_state.correct_answer,
            st.session_state.correct_question,
            st.session_state.answer_choices,
        )

    _, col2 = st.columns(2)
    with col2:
        nextq = st.button("Nouvelle question")

    if nextq:
        (
            st.session_state.image_urls,
            st.session_state.correct_answer,
            st.session_state.correct_question,
            st.session_state.answer_choices,
        ) = write_question()
        question.empty()
        with question:
            display_question(
                st.session_state.image_urls,
                st.session_state.correct_answer,
                st.session_state.correct_question,
                st.session_state.answer_choices,
            )

        print(st.session_state.image_urls)


# Run the Streamlit app
if __name__ == "__main__":
    main()
