import pandas as pd

_AUTHORS_DATA = [
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

_PROJECTS_DATA = [
    {
        "Company": "Material XD Version",
        "CompanyImage": "https://demos.creative-tim.com/material-dashboard/assets/img/small-logos/logo-xd.svg",
        "Members": [
            {"Name": "Ryan Tompson", "Image": "https://demos.creative-tim.com/material-dashboard/assets/img/team-1.jpg"},
            {"Name": "Romina Hadid", "Image": "https://demos.creative-tim.com/material-dashboard/assets/img/team-2.jpg"},
            {"Name": "Alexander Smith", "Image": "https://demos.creative-tim.com/material-dashboard/assets/img/team-3.jpg"},
            {"Name": "Jessica Doe", "Image": "https://demos.creative-tim.com/material-dashboard/assets/img/team-4.jpg"},
        ],
        "Budget": "$14,000",
        "Completion": 60,
    },
    {
        "Company": "Add Progress Track",
        "CompanyImage": "https://demos.creative-tim.com/material-dashboard/assets/img/small-logos/logo-atlassian.svg",
        "Members": [
            {"Name": "Romina Hadid", "Image": "https://demos.creative-tim.com/material-dashboard/assets/img/team-2.jpg"},
            {"Name": "Jessica Doe", "Image": "https://demos.creative-tim.com/material-dashboard/assets/img/team-4.jpg"},
        ],
        "Budget": "$3,000",
        "Completion": 10,
    },
    {
        "Company": "Fix Platform Errors",
        "CompanyImage": "https://demos.creative-tim.com/material-dashboard/assets/img/small-logos/logo-slack.svg",
        "Members": [
            {"Name": "Jessica Doe", "Image": "https://demos.creative-tim.com/material-dashboard/assets/img/team-4.jpg"},
            {"Name": "Romina Hadid", "Image": "https://demos.creative-tim.com/material-dashboard/assets/img/team-2.jpg"},
        ],
        "Budget": "Not set",
        "Completion": 100,
    },
    {
        "Company": "Launch our Mobile App",
        "CompanyImage": "https://demos.creative-tim.com/material-dashboard/assets/img/small-logos/logo-spotify.svg",
        "Members": [
            {"Name": "Ryan Tompson", "Image": "https://demos.creative-tim.com/material-dashboard/assets/img/team-2.jpg"},
            {"Name": "Romina Hadid", "Image": "https://demos.creative-tim.com/material-dashboard/assets/img/team-3.jpg"},
            {"Name": "Alexander Smith", "Image": "https://demos.creative-tim.com/material-dashboard/assets/img/team-4.jpg"},
            {"Name": "Jessica Doe", "Image": "https://demos.creative-tim.com/material-dashboard/assets/img/team-1.jpg"},
        ],
        "Budget": "$20,500",
        "Completion": 100,
    },
    {
        "Company": "Add the New Pricing Page",
        "CompanyImage": "https://demos.creative-tim.com/material-dashboard/assets/img/small-logos/logo-jira.svg",
        "Members": [
            {"Name": "Ryan Tompson", "Image": "https://demos.creative-tim.com/material-dashboard/assets/img/team-4.jpg"},
        ],
        "Budget": "$500",
        "Completion": 25,
    },
    {
        "Company": "Redesign New Online Shop",
        "CompanyImage": "https://demos.creative-tim.com/material-dashboard/assets/img/small-logos/logo-invision.svg",
        "Members": [
            {"Name": "Ryan Tompson", "Image": "https://demos.creative-tim.com/material-dashboard/assets/img/team-1.jpg"},
            {"Name": "Jessica Doe", "Image": "https://demos.creative-tim.com/material-dashboard/assets/img/team-4.jpg"},
        ],
        "Budget": "$2,000",
        "Completion": 40,
    }
]



def get_authors_data():
    return pd.DataFrame(_AUTHORS_DATA)

def get_project_data():
    return pd.DataFrame(_PROJECTS_DATA)
