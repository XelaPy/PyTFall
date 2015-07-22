# REMEMBER:
# In json files True and False are written true and false.
true = True
false = False

# All files in content/db like "training*.json" will be loaded as training courses and lessons for the training dungeon.

[# Everything goes in an array
    
    # NOTE: Every comment beginning with a '!' marks a required field
    
 {# Each course has its own object
    
    # ! Name of the course
   "id": "My Course",
    # ! The description
   "desc": "My custom course",
    # The image to use for the course. If not set, looks for a random image under "schools/[course.id]".
    # End the file path in a / to use a random image in the given folder.
    "image": "schools/Obedience/ob (20).jpg",
    # The jobs that can take this course. If not set, all girls can
    "jobs": ["Prostitute"],
    # The type of girls that can take this course. If not set, all girls can
    # Can contain "slave" or "free"
    "status": ["slave"],
    
    # A succeed condition. Used if a lesson doesn't have its own. Allows for course-wide setting of success conditions
    # Check "succeed" for the lesson below for details on how to use it
    "succeed": [],
    
    # The name of the file this course comes from. Used for debugging, can be safely ignored
    "file": "Training_example_json",
    
    # ! The lessons the course contains
   "options": {# The name of the lesson
             "My Lesson": {# ! The description of the lesson
                           "desc": "My custom lesson",
                              # The image to use for the lesson (currently unused). If not set, looks for a random image under "schools/[course.id]/"
                              # End the file path in a / to use a random image in the given folder.
                              "image": "path/to/image.jpg",
                              
                              # The way to look up images for girls during the next_day screen. Refer to the type argument in girl.has_image for more details
                              "imageMode": "normal",
                              # The tags used to look up images for girls during the next_dat screen
                              "imageTags": ["sex", "oral"],
                              # The tags to exclude when looking up images for girls during the next_day screen
                              "noImageTags": ["breasts"],
                              
                              # The amount of AP 1 lesson costs the girl
                              # -1 costs all AP
                              "AP": 1,
                              # The amount of AP 1 lesson costs the trainer
                              # -1 costs all AP
                              "heroAP": 1,
                              # The amount of gold 1 lesson costs
                              "gold": 100,
                              
                              # These are mutually exclusive, if you do have both, labels takes precedence
                              # The number of days the training lasts
                              "duration": 5,
                              # The labels used for direct player/girl interaction
                              "labels": {# ! Normal training label. Must be here if labels are used
                                         "normal": "training_custom",
                                         # Label used for when the girl obeys during training
                                         "obey": "training_custom_obey",
                                         # Label used for when the girl disobeys during training
                                         "disobey": "training_custom_disobey",
                                         # Label used for when training is refused, but the girl doesn't run away (Eg, free girls and XXX courses)
                                         "stop": "training_custom_stop",
                                         # Label used for when the girl runs away during training
                                         "runaway": "training_custom_runaway"
                                         },
                              
                              # Checks for whether the girl can do this lesson
                              # The object should be considered a large IF statement. Each property is checked with an AND statement,
                              # Eg: IF girl.mood > 50 AND girl.disposition > 500 AND ...
                              "reqs": {# Checks the characters STATS or SKILLS
                                       "mod": {# Each stat is checked against its value using >=
                                               "joy": 100,
                                               # Stats can be checked using different conditions by placing them inside these objects:
                                               "lt": {}, # <
                                               "le": {}, # <=
                                               "eq": {}, # ==
                                               "ne": {}, # !=
                                               "ge": {}, # >=
                                               "gt": {}  # >
                                               },
                                       # Checks the characters minimum value for a STAT
                                       "min": {},
                                       # Checks the characters maximum value for a STAT
                                       "max": {},
                                       # Checks properties in the characters class
                                       "props": {# If not inside an equality object (eq, lt, etc) then the default condition is == instead of >=
                                                 # Eg: Is the girl a slave?
                                                 "status": "slave"
                                                 },
                                       # Checks the characters flags
                                       # If not inside an equality object (eq, lt, etc) then the default condition is == instead of >=
                                       "flags": {},
                                       # A list of traits the character needs
                                       "traits": ["Obedient"],
                                       # A list of traits the character can't have
                                       "noTraits": ["Disobedient"],
                                       # A list of effects the character needs
                                       "effect": [],
                                       # A list of effecst the character can't have
                                       "noEffect": [],
                                       # A list of functions to check the result of. Must return a boolean. Will be passed the character being checked
                                       "funcs": ["my_requirement_function"]
                                       },
                              # Checks for whether the trainer can teach this lesson
                              "hero": [# If in a list, each object is considered to be individual statements check with OR statements,
                                       # Eg: IF a OR b OR ...
                                       {},
                                       {}
                                       ],
                              # A large IF/ELSE IF/ELSE statement to calculate the success of the lesson
                              # The result from this check decides how the lesson ends / what label is gone to
                              "succeed": [# Each result needs its own array, the first index that passes its check is used
                                          [# The lesson result. Uses the property names in "labels"
                                           "stop",
                                           # A requirement object (like reqs) to check for this 
                                           {},
                                           # A message to print to the next_day screen
                                           "%s refused to take this class! "
                                          ],
                                          [# Custom results can be used
                                           "reluctant",
                                           # If the requirement is 'true', then this condition will be used when no other passes their checks
                                           true,
                                           # A message
                                           "Being a slave, she agreed to do the course even if it isn't in her job description. \n"
                                          ]
                                         ],
                              
                              # Lessons can be scaled based on a girls stats/skills
                              # Eg: some lessons should work less when a girl isn't broken and vise versa
                              # 
                              # How the lesson scales
                              # If not set, then the lesson will always be 100% effective
                              # Can be:
                              #   "pos" = based / basedMax
                              #   "neg" = 1 - (based / basedMax)
                              #   "poscheck" = pos until the check function returns False
                              #   "negcheck" = neg until the check function returns False
                              "scale": "pos",
                              # Check to use if scale is "poscheck" or "negcheck"
                              # Can be:
                              #   "a string" = The name of a function in the global store. Will be passed the girl being trained
                              #   [a list] = A list of requirement objects to be used as the checking function
                              #   [an object] = A requirement object to use as the checking function
                              "check": "my_check_function",
                              # What to base the scaling off of
                              # Can be:
                              #   ["stat", "skill"] = A list of skills and stats to calculate a percentage from based on ((stat / statMax) + number_of_skills) / number_of_skills_or_stats
                              #   "my_based_function" = The name of a function in the global store. Will be passed the girl being trained
                              "based": ["agility", "attack"],
                              
                              # The stats or skills used to calculate the chance to train. Pulls the values from the trainer. Defaults to "TEACHING"
                              "skill": ["intelligence", "teaching"],
                              # The stats or skills used to calculate the skill cap the trainer can't teach above. Pulls the values from the trainer. Defaults to "TEACHING"
                              "knowledge": ["intelligence", "teaching"],
                              
                              # The primary effects of the lesson
                             "primary": {# mod is used for changes to a girls SKILLS or STATS
                                          "mod": {# Each stat changed is listed here with the change the lesson gives
                                                  # This is +20 to disposition
                                                  "disposition": 20,
                                                  # If the value is given in an array, then a random number is used between 0 and N
                                                  "joy": [10],
                                                  # Is 2 values are given in an array, then a random number if used between N and M
                                                  "character": [10, 20],
                                                  # If more values are given in an array, then 1 of them is selected randomly
                                                  "mood": [5, 10, 15, 20]
                                                  },
                                          # min is used for changes to the minimum value for a STAT
                                          "min": {},
                                          # max is used for changes to the maximum calue for a STAT
                                          "max": {},
                                          # props is used for properties the Girl class
                                          "props": {# Eg, this changes the girl into a slave
                                                    "status": "slave"
                                                    },
                                          # flags is used to set a girls flags
                                          "flags": {# "obey" and "disobey" are special in that they are changed relatively instead of absolutely
                                                    # Other flags can be made this way, but require the creation of a PytFlagProxy
                                                    # Eg: obey is increased by 1
                                                    "obey": 1,
                                                    # Eg: disobey is decreased by 1
                                                    "disobey": - 1,
                                                    # Eg: banana is set to 1
                                                    "banana": 1
                                                    },
                                          # traits is used to add traits to a girl
                                          "traits": [# This trait will always be added if missing
                                                     "Obedient",
                                                     # One of these traits will be added
                                                     ["A", "B", "C"]
                                                     ],
                                          # noTraits is used to remove traits from a girl
                                          "noTraits": [],
                                          # effect is used to add effects to a girl
                                          "effect": [],
                                          # noEffect is used to remove effects from a girl
                                          "noEffect": [],
                                          # funcs is used to specify python functions in the global store that should be called
                                          "funcs": ["my_custom_function"]
                                          },
                              # The secondary effects of the lesson. Have a lower chance of happening
                              "secondary": {},
                              
                              # The number of times that the primary and secondary changes should be actioned
                              # Defaults to All the girls remaining AP if no set
                              # If overridden for player/girl interactions with 1
                           "doNum": 1
                           }
            }
 }
]
