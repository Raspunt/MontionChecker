import hashlib

class Config:

    is_detector_active = False

    class pin:
        DETECTOR = 23

    res ={
        "login":"/login",
        "turnOnDetector":("/turn_on_detector","включить детектор"),
        "turnOFFDetector":("/turn_off_detector","выключить детектор")
    }

    

    def encrypt_string(self,hash_string):
        sha_signature = \
            hashlib.sha256(hash_string.encode()).hexdigest()
        return sha_signature


conf = Config()

