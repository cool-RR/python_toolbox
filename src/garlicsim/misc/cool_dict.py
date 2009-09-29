
class CoolDict(dict):
    def raise_to(self, key, value):
        has_key = self.has_key(key)
        if not has_key:
            self[key] = value
        else:
            self[key] = max(value, self[key])
            
    def lower_to(self, key, value):
        has_key = self.has_key(key)
        if not has_key:
            self[key] = value
        else:
            self[key] = min(value, self[key])
            
    def copy(self):
        return CoolDict(self)
    
    def transfer_value(self, key, new_key):
        assert self.has_key(key)
        assert not self.has_key(new_key)
        
        value = self[key]
        self[new_key] = value
        del self[key]
        
        return value
    
    
        
            