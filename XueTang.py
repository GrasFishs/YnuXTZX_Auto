from selenium import webdriver
from time import sleep

class XueTang(object):
    def __init__(self, userName, passWord):
        self.driver = webdriver.Firefox()
        #self.driver.maximize_window()
        self.driver.get("http://ynu.xuetangx.com/")

        self.driver.find_element_by_id("login_btn").click()
        # login
        self.driver.switch_to_frame("iframe_register")
        sleep(3)
        self.driver.find_element_by_id("id").send_keys(userName)
        self.driver.find_element_by_id("password").send_keys(passWord)
        self.driver.find_element_by_id("sub_btn").click()
        print("-登录成功！")
        self.getToCourseWare()

    def getToCourseWare(self):
        sleep(5)
        self.driver.switch_to_default_content()
        checked = self.driver.find_element_by_css_selector("a.enter-course")
        self.driver.get(checked.get_attribute("href"))
        print("--进入第一个慕课")
        sleep(3)
        courseWare = self.driver.find_element_by_css_selector("a[href $='courseware']")
        self.driver.get(courseWare.get_attribute("href"))
        print("---进入课件")
        sleep(3)
        #self.driver.save_screenshot("scrennShot.png")

    def getChapters(self):
        chapters = self.driver.find_elements_by_class_name("chapter")
        return len(chapters)

    def autoWatchVideo(self,number):
        chapter = "ui-accordion-accordion-header-"+str(number)
        h3 = self.driver.find_element_by_id(chapter)
        a = h3.find_element_by_tag_name("a")
        self.driver.get(a.get_attribute("href"))
        sleep(3)
        active = self.driver.find_element_by_css_selector("ul[aria-labelledby='"+chapter+"']").find_elements_by_tag_name("a")

        for i in range(0, len(active)):
            links = self.driver.find_element_by_css_selector("ul[aria-labelledby='"+chapter+"']").find_elements_by_tag_name("a")
            self.driver.get(links[i].get_attribute("href"))
            sleep(10)#缓冲视频
            videoName = self.driver.find_element_by_css_selector("div.vert").find_element_by_tag_name("h2").text
            try:
                play = self.driver.find_element_by_css_selector("div.xt_video_player_play_btn")
            except Exception as e:
                print("-->此章节为练习题，请自行完成")
                return False
            startTime = str(self.driver.find_element_by_css_selector("div.xt_video_player_current_time_display span:first-child").text)
            stopTime = str(self.driver.find_element_by_css_selector("div.xt_video_player_current_time_display span:last-child").text)
            play.click()

            isPlaying = True
            while isPlaying:
                if int(startTime.split(":")[0]) <=0 and int(startTime.split(":")[1]) <= 30 :
                    startTime = self.driver.find_element_by_css_selector(
                        "div.xt_video_player_current_time_display span:first-child").text
                else:
                    print("<"+videoName+">播放完毕！")
                    self.driver.save_screenshot("截屏.png")
                    isPlaying = False
        return True

    def autoWatchFromStartToEnd(self):
        for chpater in range(0,self.getChapters()):
            print("<---进入第" + str(chpater + 1) + "章--->")
            if not self.autoWatchVideo(chpater):
                continue
        print("已全部播放完")

