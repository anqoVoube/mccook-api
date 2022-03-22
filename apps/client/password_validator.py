class PasswordValidator:
    __SPECIAL_SYMBOLS = ['$', '@', '#', '%']
    final_response = {}
    password: str
    
    def __init__(self, password: str):
        self.password = password
    
    def minlength(self, length: int):
        if len(self.password) < length:
            message = "Length less than required"
            self.final_response['min-length'] = [message]
        return self
    
    def maxlength(self, length: int):
        if len(self.password) > length:
            message = "Length greater than permited"
            self.final_response['max-length'] = [message]
        return self
    
    def has_uppercase(self):
        if not any(str(char).isupper() for char in self.password):
            message = "Password should have at least one uppercase letter"
            self.final_response['uppercase'] = [message]
        return self
    
    def has_lowercase(self):
        if not any(str(char).islower() for char in self.password):
            message = "Password should have at least one lowercase letter"
            self.final_response['lowercase'] = [message]
        return self
    
    def has_numeral(self):
        if not any(str(char).isdigit() for char in self.password):
            message = ["Password should have at least one numeral"]
            self.final_response['digit'] = [message]
        return self
    
    def has_specific_symbol(self):
        if not any(char in self.__SPECIAL_SYMBOLS for char in self.password):
            message = "Password should have at least one of those symbols: $@#%"
            self.final_response['symbol'] = [message]
        return self
    
    def get_response(self) -> dict:
        return self.final_response
 
# a = PasswordValidator("Jujo")
# print(a.minlength(5).has_lowercase().get_response())
# -> ["Password should have at least one uppercase letter"]