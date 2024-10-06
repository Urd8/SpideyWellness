flowchart = {
    "Layer 1": {
        "Question": "Choose a category:",
        "Options": ["Category A", "Category B"],
        "Layer 2": {
            "Category A": {
                "Question": "Select a subcategory under A:",
                "Options": ["A1", "A2"],
                "Layer 3": {
                    "A1": {
                        "Question": "Do you want more details on A1?",
                        "Options": ["Yes", "No"],
                        "Layer 4": {
                            "Yes": "Here are more details about A1.",
                            "No": "You chose no further details."
                        }
                    },
                    "A2": {
                        "Question": "Do you want more details on A2?",
                        "Options": ["Yes", "No"],
                        "Layer 4": {
                            "Yes": "Here are more details about A2.",
                            "No": "You chose no further details."
                        }
                    }
                }
            },
            "Category B": {
                "Question": "Select a subcategory under B:",
                "Options": ["B1", "B2"],
                "Layer 3": {
                    "B1": {
                        "Question": "Do you want more details on B1?",
                        "Options": ["Yes", "No"],
                        "Layer 4": {
                            "Yes": "Here are more details about B1.",
                            "No": "You chose no further details."
                        }
                    },
                    "B2": {
                        "Question": "Do you want more details on B2?",
                        "Options": ["Yes", "No"],
                        "Layer 4": {
                            "Yes": "Here are more details about B2.",
                            "No": "You chose no further details."
                        }
                    }
                }
            }
        }
    }
}