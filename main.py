import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random

UID = os.environ["USERNAME"]
PWD = os.environ["PASSWORD"]
RNDTM = os.environ["RANDOMTIME"]

#登录打卡
def sign_in(uid, pwd):
    msg=""
    url=""
    img_list=list()
    a_list=list()
    # set to no-window
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")

    # simulate a browser to open the website
    browser = webdriver.Chrome(options=chrome_options)
    # browser = webdriver.Chrome()
    browser.get("http://ids.hhu.edu.cn/amserver/UI/Login?goto=http%3A%2F%2Fform.hhu.edu.cn%2Fpdc%2Fform%2Flist")

    try:
        # input uid and password
        print("正在进行登陆...")
        browser.find_element_by_id("IDToken1").send_keys(uid)
        browser.find_element_by_id("IDToken2").send_keys(pwd)
        # click to sign in
        #browser.find_element_by_xpath("/html/body/table[1]/tr[2]/td[1]/table[2]/tr[2]/td[2]/table[1]/tr[3]/td[1]/IMG[1]").click()
        img_list=browser.find_elements_by_tag_name("IMG")
        '''
        for li in img_list:
            print(li)
        '''
        img_list[4].click()
        time.sleep(3)
    
        #获取当前页面URL
        msg=browser.title
        url=browser.current_url

        if msg == "防疫上报统计系统":
            print('登陆成功,即将进行打卡')
            a_list=browser.find_elements_by_tag_name("a")
            a_list[0].click()
            time.sleep(2)
            browser.find_element_by_id("saveBtn").click()
        else:
            print('登陆失败')
            return False

    except Exception as e:
        msg = "登录过程中发生错误: " + str(e)
        print(msg)
    finally:
        browser.quit()
        
    # quit the browser
    print('打卡成功')
    return True

#随机时间
def randomTime(seconds=3600):
    randomnumber = random.randint(0, seconds)
    counter = 0
    while counter < randomnumber:
        restTime = randomnumber - counter
        restMinutes = int(restTime / 60)
        restSeconds = restTime % 60
        if restTime < 300:
            if restTime < 60:
                print("倒计时: "+ str(restSeconds) + "秒")
            else:
                print("倒计时: " + str(restMinutes) + "分" + str(restSeconds) + "秒")
            time.sleep(restTime)
            counter += restTime
        else:
            print("倒计时: " + str(restMinutes) + "分" + str(restSeconds) + "秒")
            time.sleep(300)
            counter += 300

if __name__ == "__main__":
	#检查账号密码数量是否一致
    if not PWD or not UID:
        print("你还没有添加账户\n")
        exit(1)
    uid_list = UID.split()
    pwd_list = PWD.split()
    uid_length = len(uid_list)
    pwd_length = len(pwd_list)
    if uid_length!=pwd_length:
        print("账号和密码数量不一致\n");
        exit(1)
    #随机时间
    if RNDTM:
        randomTime(int(RNDTM)*60)
    else:
        randomTime(3600)
    #开始打卡
    for i in range(pwd_length):
        print("**************************************\n正在给第 "+str(i+1)+" 个账号打卡")
        flag=sign_in(uid_list[i], pwd_list[i])
        if flag:
            print("第 "+str(i+1)+" 个账号打卡成功!")
        else:
            print("第 "+str(i+1)+" 个账号打卡失败!\n正在发起第2次尝试")
            flag = sign_in(uid_list[i], pwd_list[i])
            if flag:
                print("第 2 次尝试成功!")
            else:
                print("第 2 次尝试失败!\n请自行手动打卡!")
        time.sleep(30)
    print("**************************************")
    print("本次任务执行完毕")
