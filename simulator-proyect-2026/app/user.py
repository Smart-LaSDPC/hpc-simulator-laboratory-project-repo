class User(object):

    def __init__(self, id_user, rol, description, posX=0, posY=0, 
                    path = "media/user/media_default_user.png"):
        self.id_user = id_user
        self.rol = rol
        self.description = description
        self.posX = posX
        self.posY = posY
        self.status = "OFF" #OF => CLOSE | ON => OPEN
        self.path = path #active state (ON, true, 1)
        self.platform = None

    def get_valuesInJson(self):
        # Creating a dictionary to hold the user attributes
        user_dict = {
            'id_user': self.id_user,
            'rol': self.rol
        }
        return user_dict
        
    def set_posXY(self, posX, posY):
        self.posX = posX
        self.posY = posY

    def get_id(self):
        return self.id_user

    def get_id_user(self):
        return self.id_user

    def get_rol(self):
        return self.rol

    def get_type(self):
        return self.rol        

    def get_description(self):
        return self.description

    def get_posX(self):
        return self.posX

    def get_posY(self):
        return self.posY
        
    def get_status(self):
        return self.status

    def get_path(self):
        return self.path          

    def set_status(self, new_status):
        self.status = new_status

    def display(self):
        print('User: ', self.id_user, self.rol, self.description)

    def get_ValuesInJson(self):
        user_dict = {

        } 

    def get_platform(self):       
        return self.platform

    def set_platform(self, id_platform):
        self.platform = id_platform
