import requests,re,platform,sys
    
class CMCore():
    def __init__(self,
                 url:str,
                 electron_version:int = None,
                 icon:str = None,
                 upgrade_version_dir:str = None,
                 loading_color:str = None,
                 always_on_top:bool = False,
                 fullscreen:bool = False,
                 disable_devtools:bool = False,
                 disable_right_click:bool = False,
                 app_name:str = None,
                 nativefier_command:str = "nativefier"):
        self.url = url
        self.electron_version = electron_version
        self.icon = icon
        self.upgrade_version_dir = upgrade_version_dir
        self.loading_color = loading_color
        self.always_on_top = always_on_top
        self.fullscreen = fullscreen
        self.disable_devtools = disable_devtools
        self.disable_right_click = disable_right_click
        self.app_name = app_name
        self.nativefier_command = nativefier_command
    
            
    def get_full_command(self):
        cm_raw = f"{self.nativefier_command} "
        cm_raw += self.url
        if(self.icon != None):
            cm_raw += f' --icon "{self.icon}"'
        if(self.upgrade_version_dir != None):
            cm_raw += f' --upgrade "{self.upgrade_version_dir}"'
        if(self.loading_color != None):
            cm_raw += f' --background-color "{self.loading_color}'
        if(self.fullscreen):
            cm_raw += " --full-screen"
        if(self.always_on_top):
            cm_raw += " --always-on-top"
        if(self.disable_devtools):
            cm_raw += " --disable-dev-tools"
        if(self.disable_right_click):
            cm_raw += " --disable-context-menu"
        if(self.app_name != None):
            cm_raw += f' --name {self.app_name}'
        return cm_raw
        
    def get_full_dir(self):
        try:
            response = requests.get(self.url)
            response.encoding = response.apparent_encoding
            if response.status_code == 200:
                title = re.search(r'<title>(.*?)</title>', response.text).group(1)
                arch = ""
                if(platform.architecture()[0] == "64bit"):
                    arch = "x64"
                elif(platform.architecture()[0] == "32bit"):
                    arch = "x86"
            full_dir = f"{title}-{sys.platform}-{arch}"
            return {"status": True,"full_dir": full_dir}
        except Exception as err:
            return {"status": False, "error_code":err}