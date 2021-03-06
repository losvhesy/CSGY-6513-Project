states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
       'Colorado', 'Connecticut', 'Delaware', 'District of Columbia',
       'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana',
       'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
       'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
       'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
       'New Jersey', 'New Mexico', 'New York', 'North Carolina',
       'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
       'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee',
       'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
       'West Virginia', 'Wisconsin', 'Wyoming']

divisions = [
    {
        "name": "New England",
        "states": ["Connecticut", "Maine", "Massachusetts", "New Hampshire", "Rhode Island", "Vermon"]
    },
    {
        "name": "Mid-Atlantic",
        "states": ["New Jersey", "New York", "Pennsylvania"]
    },
    {
        "name": "East North Central",
        "states": ["Illinois", "Indiana", "Michigan", "Ohio", "Wisconsin"],
    },
    {
        "name": "West North Central",
        "states": ["Iowa", "Kansas", "Minnesota", "Missouri", "Nebraska", "North Dakota", "South Dakota"]
    },
    {
        "name": "South Atlantic",
        "states": ["Delaware", "Florida", "Georgia", "Maryland", "North Carolina", "South Carolina", "Virginia", "District of Columbia", "West Virginia"]
    },
    {
        "name": "East South Central",
        "states": ["Alabama", "Kentucky", "Mississippi", "Tennessee"]
    },
    {
        "name": "West South Central",
        "states": ["Arkansas", "Louisiana", "Oklahoma", "Texas"]
    },
    {
        "name": "Mountain",
        "states": ["Arizona", "Colorado", "Idaho", "Montana", "Nevada", "New Mexico", "Utah", "Wyoming"]
    },
    {
        "name": "Pacific",
        "states": ["Alaska", "California", "Hawaii", "Oregon", "Washington"]
    }
]


spatial_terms = {}
state_configs = []
for state in states:
    state_configs.append(
        {
            "name": state,
            "states": [state],
            "type": state,
        }
    )
    # spatial_terms[state.lower()] =

spatial_commonsense = {
    "divisions": divisions,
    "states": state_configs
}