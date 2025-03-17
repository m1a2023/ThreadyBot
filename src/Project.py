class Project:
    def __init__(self, 
                 name: str = "", 
                 description: str = "", 
                 link_rep: str = "", 
                 team: str = set(),
                 id_owner: str = "", 
                 create_at: str = "", 
                 deadline_of_project: str = ""):
        self.name = name
        self.description = description
        self.link_rep = link_rep
        self.team = team
        self.id_owner = id_owner
        self.create_at = create_at
        self.deadline_of_project = deadline_of_project

    """ Setter for all """
    def set_name(self, name: str):
        self.name = name

    def set_description(self, description: str):
        self.description = description

    def set_link_rep(self, link_rep: str):
        self.link_rep = link_rep

    def set_team(self, team: str):
        self.team = team
    
    def set_id_owner(self, id_owner: str):
        self.id_owner = id_owner

    def set_create_at(self, create_at: str):
        self.create_at = create_at

    def set_deadline_of_project(self, deadline_of_project: str):
        self.deadline_of_project = deadline_of_project


    """ Getter for all """
    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description

    def get_link_rep(self) -> str:
        return self.link_rep
    
    def get_team(self):
        return self.team

    def get_create_at(self):
        return self.create_at

    def get_deadline_of_project(self):
        return self.deadline_of_project

    """ Returns project data in the form of a dictionary """
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "link_rep": self.link_rep,
            "team": self.team,
            "id_owner": self.id_owner,
            "create_at": self.create_at,
            "deadline_of_project": self.deadline_of_project
        }