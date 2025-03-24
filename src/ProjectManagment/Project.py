from ProjectManagment.Developer import Developer

class Project:
    def __init__(self,
                 title: str = "",
                 description: str = "",
                 repo_link: str = "",
                 owner_id: str = "",
                 team: list = []):
        self.title = title
        self.description = description
        self.repo_link = repo_link
        self.owner_id = owner_id
        self.team = team

    """ Setter for all """
    def set_title(self, title: str):
        self.title = title

    def set_description(self, description: str):
        self.description = description

    def set_repo_link(self, link_rep: str):
        self.repo_link = link_rep

    def set_owner_id(self, id_owner: str):
        self.owner_id = id_owner


    """ Getter for all """
    def get_name(self) -> str:
        return self.title

    def get_description(self) -> str:
        return self.description

    def get_link_rep(self) -> str:
        return self.repo_link

    def get_team(self) -> list:
        return self.team

    
    
    def addDeveloper(self, dev: Developer):
        self.team.append(dev.to_dict())

    """ Returns project data in the form of a dictionary """
    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "repo_link": self.repo_link,
            "owner_id": self.owner_id,
            "team": self.team
        }

    def __str__(self):
        return (f"Название: {self.title}\n"
                f"Описание: {self.description}\n"
                f"Ссылка на репозиторий: {self.repo_link if self.repo_link else 'Не указано'}\n"
                )
