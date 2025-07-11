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


def chance_for_new_candidate(salary):

    # create random indywiduals
    people = []

    max_of_people = (salary - 3000) // 500
    number_of_people = random.randint(0,max_of_people)

    for i in range(number_of_people):
        expected_salary = random.randint(3000, 8000) # 3000 minimum, then increase to 3500 for that 500 window

        # only if salary is met, then add them to candidate list and give them names
        if salary >= expected_salary - 1000:

            genders = ["male", "female"]
            gender = random.choice(genders)
            name = "Scooby-Dooby Doo"
            if gender == "male":
                name = random.choice(male_names)
            elif gender == "female":
                name = random.choice(female_names)

            family_name = random.choice(family_names)
            age = random.randint(18,60)
            expirience = random.randint(0, 20)

            if age - expirience < 18:
                expirience = 0 # intern

            person = [name, family_name, age, expected_salary, expirience]
            people.append(person)
    
    return people # return all candidates