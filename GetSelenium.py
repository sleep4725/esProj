from selenium import webdriver

class GetSelenium:

    @classmethod
    def retSeleObj(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("window-size=1920x1080")
        options.add_argument("--disable-gpu")

        chromeObj = webdriver.Chrome(executable_path="/home/kim/PycharmProjects/stu_01/config/chromedriver",
                                     chrome_options=options)

        return chromeObj