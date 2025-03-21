class Developer:
  def __init__(self, 
               user_id: int,
               project_id: int,
               role: str = ""):
    self.user_id = user_id
    self.project_id = project_id
    self.role = role

  def to_dict(self) -> dict:
    return {
      "user_id": self.user_id,
      "project_id": self.project_id,
      "role": self.role
    }