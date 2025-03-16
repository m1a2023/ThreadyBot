class Project:
    def __init__(self, name: str = "", description: str = "", link_rep: str = "", team: str = []):
        self.name = name
        self.description = description
        self.link_rep = link_rep
        self.team = team

    """ Setter for all """
    def set_name(self, name: str):
        self.name = name

    def set_description(self, description: str):
        self.description = description

    def set_link_rep(self, link_rep: str):
        self.link_rep = link_rep

    def set_team(self, team: str):
        self.team = team.split(" ")


    """ Getter for all """
    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description

    def get_link_rep(self) -> str:
        return self.link_rep

    """ Returns project data in the form of a dictionary """
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "link_rep": self.link_rep,
            "team": self.team
        }