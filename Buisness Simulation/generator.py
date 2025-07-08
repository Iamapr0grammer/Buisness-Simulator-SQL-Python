import random, data




# list of male names
male_names = [
    # Standard Male Names
    "Adam", "Ben", "Carl", "David", "Ethan", "Frank", "George", "Henry",
    "Ian", "Jack", "Kyle", "Luke", "Mark", "Nathan", "Oliver", "Paul",
    "Quentin", "Ryan", "Steve", "Tom", "Victor", "William", "Xavier", "Yanni", "Zach",
    
    # Nerd-Approved Names
    "Alan", "Dennis", "Guido", "Linus", "Elon", "Bill", "Steve",
    "Richard", "Tim", "Bjarne",
    
    # version 2
    "Greg", "Todd", "Chuck", "Barry",
    "Neil", "Phil", "Craig",
    "Randy", "Doug", "Frank",
    
    # Overkill Names
    "Maximus", "Thorvald", "Magnus", "Apollo", "Xerxes", "Leonardo",
    "Hannibal", "Atticus", "Titan", "Zephyr"
]

# list of female names
female_names = [
    # Standard Female Names
    "Alice", "Beth", "Clara", "Diana", "Emma", "Fiona", "Grace", "Hannah",
    "Isla", "Jane", "Katie", "Luna", "Maria", "Nina", "Olivia", "Penny",
    "Queenie", "Rachel", "Sarah", "Tina", "Uma", "Vera", "Wendy", "Xena", "Yara", "Zoe",
    
    # Nerd-Approved Names
    "Ada",       
    "Grace",     
    "Radia",     
    "Margaret",  
    "Joan",      
    "Barbara",   
    "Karen",    
    "Frances",  
    "Marissa",   
    "Shafi",     

    # version 2
    "Sally", "Tina", "Claire", "Bonnie",
    "Nina", "Faye", "Cassie",
    "Rita", "Deb", "Wanda",

    # Overkill Names
    "Athena", "Freya", "Seraphina", "Bellatrix", "Juno", "Andromeda",
    "Lilith", "Electra", "Valkyrie", "Nova"
]


# list of family names
family_names = [
    # Common and Classic
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",

    # Nerd-Approved Surnames
    "Turing",       
    "Hopper",       
    "Lovelace",     
    "Hamilton",     
    "Knuth",        
    "Liskov",       
    "Torvalds",     
    "Dijkstra",     
    "Berners-Lee",  
    "Spärck Jones", 

    # Fictionally Spicy
    "Skywalker", "Kenobi", "Stark", "Wayne", "Potter", "Malfoy", "Snape",
    "Romanoff", "Banner", "Holmes", "Moriarty", "Riker", "Picard", "Ripley", "Kirk",

    # Unnecessarily Cool
    "Ravenwood", "Storm", "Blackthorn", "Graves", "Nightshade", "Blaze",
    "Ashcroft", "Thorne", "Hawke", "Crimson"
]



def generate_person():
    sex = random.randint(1,2)
    if sex == 1:
        sex = "male"
    else:
        sex = "female"
    
    name = ""

    if sex == "male":
        name = random.choice(male_names)
    else:
        name = random.choice(female_names)

    family_name = random.choice(family_names)

    age = random.randint(18,100)

    dish = random.choice(data.dish_full_list)

    person = [name, family_name, dish, age, sex]

    return person
