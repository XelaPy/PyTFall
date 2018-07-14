# REMEMBER:
# In json files True and False are written true and false.
true = True
false = False

# All files in content/db like "school*.json" will be loaded as different schools and lessons.

[# Everything goes in an array
    
    # NOTE: Every comment beginning with a '!' marks a required field
    
    {# Each school has its own object
    
    # ! Name of the school
    "id": "My Course",
    # The image to use for the school.
    "image": "schools/Obedience/ob (20).jpg",
    
    # ! The amount that each primary stat changes in a lesson.
    # Can be:
    #    7 = A single value that all will change by
    #   [5] = A 1-length array, taken as the maximum random value
    #   [0,5] = A 2-length array, taken as min and max for a random value
    #   [0,1,...] = An n-length array, 1 value will be randomly chosen
    "primary": [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0],
    
    # ! The amount that each secondary stat/skill changes in a lesson. Chosen randomly from the list
    "secondary": [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2],
    
    # The amount that each primary skill changes in a lesson.
    # If null, will use "primary" instead.
    "skillPrimary": 20,
    
    # The amount that each secondary skill changes in a lesson.
    # If null, will use "secondary" instead.
    "skillSecondary": 20,
    
    # The name of the file this course comes from. Used for debugging, can be safely ignored
    "file": "School_example_json",
    
    # ! The lessons the school provides
    "options": {# Each lesson has its own object. The name of the lesson is the property name
                "Beauty": {# ! The description of the lesson
                           "desc": "This course focuses on training charsima. May also improve refinement! ",
                           
                           # The primary effects of the lesson
                           # This can be an object like in Training_example_json lessons,
                           # or a list of stats/skills to change by the Schools primary array above
                           "primary": ["charisma"],
                           
                           # The secondary effects of the lesson
                           # This can be an object like in Training_example_json lessons,
                           # or a list of stats/skills to change by the Schools secondary array above
                           "secondary": ["refinement"]
                           
                           ##################
                           # 
                           # All other properties in school lessons work the same as in training lessons.
                           # 
                           # Except:
                           #    skill: This property is overridden and a number is randomly generated
                           #    knowledge: This property is overridden and a number is randomly generated
                           #    doNum: This property is overridden and all of the girls AP is used
                           #    label: This property is ignored as all school lessons are duration based
                           #    duration: This property is ignored and a number is randomly generated
                           # 
                }
               }
     }
]
