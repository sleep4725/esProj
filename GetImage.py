from GetSelenium import GetSelenium
from urllib.parse import urlencode
import time
import yaml
from urllib.request import urlretrieve
from PIL import Image
import shutil

#
# 작성자 : 김준현 선임
#

class GetImage:

    TOTAL_PAGE =522
    IMAGE_COUNT=0

    def __init__(self):

        self.url = GetImage.getInformation()
        self.chromeObj = GetSelenium.retSeleObj()
        self.timeObj = time.strftime("%Y%m%d", time.localtime())
        self.totalImgUrl = list()
        self.saveImagePath = "/home/kim/Desktop/wild_boar_img"
        self.reSaveImagePath = "/home/kim/Desktop/re_wild_boar"

    def getRegImg(self):

        with open("./logs/success.log", "a", encoding="utf-8") as successLog:

            successLog.write("일시 : {}".format(self.timeObj)     + "\n")
            successLog.write("시작 시간 : {}".format(time.strftime("%H:%M:%S", time.localtime())) + "\n")
            successLog.write("진행자 : 김준현 선임"                  + "\n")
            successLog.write("============================="     + "\n")

            for p in range(1, GetImage.TOTAL_PAGE+1):
                print ("page : {}".format(p))
                params = urlencode({
                    "page": p
                })

                try:
                    # ------------------------------------------------------------
                    # 요청에 대한 예외처리를 진행한다. 페이지 수가 많기 때문에 timeout 걸릴 수 있다.
                    # ------------------------------------------------------------
                    self.chromeObj.get(url= self.url + params)
                except:
                    # ======================================================
                    # fail log write
                    with open("./logs/error.log", "w", encoding="utf-8") as fw:
                        fw.write("requests error page : {}".format(p))
                        fw.close()
                    # ======================================================
                    return
                else:
                    self.chromeObj.implicitly_wait(time_to_wait=3)
                    # ======================================================
                    # success log write
                    successLog.write("[success] page : {}".format(p) + "\n")
                    # ======================================================

                    self.chromeObj.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)

                    aTags = self.chromeObj.find_elements_by_css_selector("img")
                    srcList = [str(a.get_attribute(name="src")).replace("https", "http") for a in aTags]
                    self.imageSave(srcList)
                    self.reImageSize(srcList)

            # ====================================
            # I/O close
            successLog.write("끝 시간 : {}".format(time.strftime("%H:%M:%S", time.localtime())) + "\n")

            successLog.close()
            self.chromeObj.close()

    def imageSave(self, srcList):

        for c, u in enumerate(srcList):

            try:

                urlretrieve(url=u, filename= self.saveImagePath+"/wild_boar_{}.jpg".format(c+1))
            except:
                f = open("./logs/img_save_error.log", "a", encoding="utf-8")
                f.write(u + "\n")
                f.close()
                pass
            else:
                time.sleep(0.5)

    def reImageSize(self, srcList):

        for c, u in enumerate(srcList):
            GetImage.IMAGE_COUNT = GetImage.IMAGE_COUNT + 1
            try:

                i = Image.open(self.saveImagePath+"/wild_boar_{}.jpg".format(c+1))
            except Image.UnidentifiedImageError as e:
                f = open("./logs/re_img_save_error.log", "a", encoding="utf-8")
                f.write(u + "\n")
                f.close()
                pass
            else:
                w, h = i.size
                reSizeImage = i.resize((w*2,h*2))
                reSizeImage.save(self.reSaveImagePath + "/resize_wild_boar_{}.jpg".format(GetImage.IMAGE_COUNT))

    @classmethod
    def getInformation(cls):

        try:
            f=open("./config/info.yml", "r", encoding="utf-8")
        except FileNotFoundError as e:
            print(e)
            return
        else:
            info = yaml.safe_load(f)
            f.close()
            return info["url"]

if __name__ == "__main__":
    o = GetImage()
    o.getRegImg()