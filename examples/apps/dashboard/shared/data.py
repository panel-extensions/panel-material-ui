import pandas as pd

_AUTHORS_DATA = pd.DataFrame(
    [
        {
            "image": "https://randomuser.me/api/portraits/men/1.jpg",
            "name": "John Michael",
            "email": "john.michael@example.com",
            "title": "Manager",
            "team": "Organization",
            "status": "Online",
            "employed": "23/04/18",
        },
        {
            "image": "https://randomuser.me/api/portraits/women/2.jpg",
            "name": "Alexa Liras",
            "email": "alexa.liras@example.com",
            "title": "Programmer",
            "team": "Developer",
            "status": "Offline",
            "employed": "11/01/19",
        },
        {
            "image": "https://randomuser.me/api/portraits/men/3.jpg",
            "name": "Laurent Perrier",
            "email": "laurent.perrier@example.com",
            "title": "Executive",
            "team": "Projects",
            "status": "Online",
            "employed": "19/09/17",
        },
        {
            "image": "https://randomuser.me/api/portraits/women/4.jpg",
            "name": "Michael Levi",
            "email": "michael.levi@example.com",
            "title": "Designer",
            "team": "Creative",
            "status": "Online",
            "employed": "24/12/08",
        },
    ]
)


def get_authors_data():
    return _AUTHORS_DATA
