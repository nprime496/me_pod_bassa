from PIL import Image
from io import BytesIO
import requests
import random 
import string
#from google_images_search import GoogleImagesSearch
import streamlit as st
import pandas as pd
from PIL import UnidentifiedImageError
import os



# # Set page title and description
# st.set_page_config(page_title="MCQ de traduction français-bassa",
#                    page_icon=":books:",
#                    layout="wide")


def generate_random_string(length):
    """
    Generate a random string of the specified length.
    """
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


@st.cache_resource
def read_csv(filename):
    return pd.read_csv(filename)

import requests
import random
import json
from urllib import parse, request

# Set up the Giphy API endpoint URL and API key
#url = "https://api.giphy.com/v1/gifs/random"

url = "http://api.giphy.com/v1/gifs/search"


#print(json.dumps(data, sort_keys=True, indent=4))
# you can provide API key and CX using arguments,
# or you can set environment variables: GCS_DEVELOPER_KEY, GCS_CX


import streamlit as st


# @st.cache_resource
# def get_gis():
#     return GoogleImagesSearch(API_KEY, CX)


DATABASE = read_csv("src/db.csv")
print(DATABASE.head())
#GIS_API = get_gis()


# Define a function to retrieve the image urls for a given query
@st.cache_data
def get_image_urls(query, num_imgs=4):
    # define search params
    # option for commonly used search param are shown below for easy reference.
    # For param marked with '##':
    #   - Multiselect is currently not feasible. Choose ONE option only
    #   - This param can also be omitted from _search_params if you do not wish to define any value
    # print('"' * 40)
    # print(f" {query}")
    # print('"' * 40)
    # _search_params = {
    #     "q": "une photo montrant " + query,
    #     "num": num_imgs,
    #     "fileType": "png",
    #     #'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived',
    #     "safe": "active",  ## |high|medium|off|safeUndefined
    #     "imgType": "photo",  ## 'clipart|face|lineart|stock|photo|animated|imgTypeUndefined
    #     "lang": "fr",
    #     "imgSize": "medium",  ## |small|xlarge|xxlarge|imgSizeUndefined
    #     #'imgDominantColor': '', ##black|blue|brown|gray|green|orange|pink|purple|red|teal|white|yellow|imgDominantColorUndefined
    #     #'imgColorType': 'color|gray|mono|trans|imgColorTypeUndefined' ##
    # }

    # # this will search, download and resize:
    # GIS_API.search(
    #     search_params=_search_params, width=250, height=500
    # )  # path_to_dir='/path/'

    # results = [image.url for image in GIS_API.results()]
    # # assert(len(results)==num_imgs),f"Retrieved {len(results)} is different form {num_imgs}"
    # return results
    
    params = parse.urlencode({
    "q": query,
    "api_key": st.secrets['api_key'],
    "limit": "2"
    })

    with request.urlopen("".join((url, "?", params))) as response:
        data = json.loads(response.read())
        url_ = data['data'][0]['images']['original']['url']
    return url_.split('?')[0]


def write_question():
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
    urls = get_image_urls(query)
    print(urls)
    propositions = [
        selected_bassa,
        *random.sample(set(DATABASE["bassa"]) - {selected_bassa}, 3),
    ]
    random.shuffle(propositions)
    return urls, correct_, selected_fr, propositions


# @st.cache_data
# def get_images(img_urls):
#     imgs_ = []
#     for url in img_urls:
#         try:
#             imgs_.append(Image.open(BytesIO(requests.get(url).content)))
#         except UnidentifiedImageError:
#             imgs_.append(
#                 Image.open(
#                     BytesIO(
#                         requests.get(
#                             "https://data.pixiz.com/output/user/frame/preview/400x400/7/8/0/3/1863087_a0870.jpg"
#                         ).content
#                     )
#                 )
#             )
#     return imgs_


def display_question(img_url, correct, traduction, choices, container=st):
    print(img_url, correct, traduction, choices)
    if img_url == None or correct == None or traduction == None or choices == None:
        return

    st.title(traduction)
    st.markdown(f"![Alt Text]({img_url})")
 
    # mygrid = [[], []]
    # with st.container():
    #     mygrid[0] = st.columns(2)
    # with st.container():
    #     mygrid[1] = st.columns(2)
    # Display the images in a 4 image one word style
    # imgs = get_images(tuple(img_urls))
    # for i in range(2):
    #     for j in range(2):
    #         with mygrid[i][j]:
    #             try:
    #                 st.image(imgs[i * 2 + j], width=150)
    #             except IndexError:
    #                 pass

    # Display the question and radio buttons
    answer = st.radio(
        f"Quelle est la traduction correcte pour : {traduction} ?", choices
    )

    style = """
        <style>
            div[data-baseweb="radio"] label {
                font-size: 20px !important;
            }
                    body {
            font-size: 50px;
        }

        </style>
    """

    st.markdown(style, unsafe_allow_html=True)
    # Check if the answer is correct and display a message
    submit = st.button("Soumettre")
    if submit:
        if answer == correct:
            st.write("Correct!")
        else:
            st.write(f"Faux. La bonne réponse est [{correct}].")

    # if st.button('Prochaine Question'):
    #     write_question()


# Define the Streamlit app
def main():
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

    if st.button("Nouvelle question"):
        (
            st.session_state.image_urls,
            st.session_state.correct_answer,
            st.session_state.correct_question,
            st.session_state.answer_choices,
        ) = write_question()
    # image_urls,correct_answer,correct_question,answer_choices = None,None,None,None
    display_question(
        st.session_state.image_urls,
        st.session_state.correct_answer,
        st.session_state.correct_question,
        st.session_state.answer_choices,
    )

    # display_question(image_urls,correct_answer,correct_question,answer_choices)


# Run the Streamlit app
if __name__ == "__main__":
    main()
