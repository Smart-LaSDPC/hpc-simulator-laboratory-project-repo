class Asset(object):

    def __init__(self, id_asset, type_, description, posX=0, posY=0, 
                    path_state1 = "asset/media_default_on.png",  path_state2 = "asset/media_default_off.png"):
        self.id_asset = id_asset
        self.type = type_
        self.description = description
        self.posX = posX
        self.posY = posY
        self.status = "OFF" #OF => CLOSE | ON => OPEN
        self.path_state1 = path_state1 #active state (ON, true, 1)
        self.path_state2 = path_state2 #desactive state (OFF, false, 0)
        
    def set_posXY(self, posX, posY):
        self.posX = posX
        self.posY = posY

    def get_id(self):
        return self.id_asset

    def get_id_asset(self):
        return self.id_asset

    def get_type(self):
        return self.type

    def get_description(self):
        return self.description

    def get_posX(self):
        return self.posX

    def get_posY(self):
        return self.posY
        
    def get_status(self):
        return self.status

    def get_path_state1(self):
        return self.path_state1

    def get_path_state2(self):
        return self.path_state2            

    def set_status(self, new_status):
        self.status = new_status

    def display(self):
        print('Asset: ', self.id_asset, self.type, self.description)
