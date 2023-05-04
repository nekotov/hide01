import requests
import re
import os
import threading
import sqlite3


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def bypass(url :str) -> str:
    # connect to db.db and query in bypass table orig == url and get bypass
    db = sqlite3.connect("db.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM bypass WHERE orig = ?", (url,))
    data = cursor.fetchone()
    if data:
        return data[1]
    # create fireefox driver without window
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Firefox(options=options)
    # driver = webdriver.Firefox()
    vars = {}

    driver.get(url)
    driver.set_window_size(550, 691)
    driver.find_element(By.ID, "invisibleCaptchaShortlink").click()
    driver.execute_script("window.scrollTo(0,658)")
    try:
        WebDriverWait(driver, 15).until(
            expected_conditions.visibility_of_element_located((By.LINK_TEXT, "رد تبلیغ و مشاهده لینک")))
    except Exception as e:
        print("Error in", url)
        print(e)
        driver.quit()
        bypass(url)
    out =  driver.find_element(By.LINK_TEXT, "رد تبلیغ و مشاهده لینک").get_attribute('href')
    driver.quit()
    # insert into db.db bypass table
    cursor.execute("INSERT INTO bypass VALUES (?, ?)", (url, out))
    db.commit()
    db.close()
    return out

def getNumPages() -> int:
    ses = requests.session()
    data = ses.get("https://hide01.ir/page/1/")
    return max([int(x) for x in re.findall(r"page\/(\d+)", data.text, re.MULTILINE)])

def getPageUnits(url :str) -> [str]: # https://hide01.ir/downloads/???/
    ses = requests.session()
    data = ses.get(url)
    return list(dict.fromkeys([(i) for i in re.findall(r"downloads\/(.*?)\/\"",data.text) if not "hide01" in i]))

def dwLinksExtractor(data :str) -> [str]:
    return list(dict.fromkeys([(i) for i in re.findall(r"""(https:\/\/rizy\.ir\/\S.*?)\"""", data) if not "maral" in i]))

def pageExtractor(url :str):
    sess = requests.session()
    data = sess.get(url)
    if data.status_code != 200:
        print(url, "NOT 200")
        return
    url = data.url
    dir_name = re.findall(r"\.ir/(.*?)/", url)[0]
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    with open(dir_name + "/index.html", "w") as f:
        f.write(data.text)
    with open(dir_name + "/links.txt", "w") as f:
        lk = dwLinksExtractor(data.text)
        print(lk)
        for i in lk:
            if "value" not in i:
                print("Bypassing", i)
                url = bypass(i)
                print(url)
                f.write(url + "\n")
    print("Done", url)




pages = getNumPages()
print("Pages:", pages)
out = []#[['securing-the-cloud-foundations-andrew-krug', 'sec554', 'fundamentals-of-virtualization', 'rmaap', 'mgt551', 'istaawn', 'exploit-pack-pro', 'sonarqube', 'psfodso', 'esmwosnidsips', 'psbtt', 'cssocatsiems', 'hackercool-magazine', 'bbhwbs', 'cesc-as'], ['ccrta', 'sec510', 'cracking-software-practicals', 'cracking-software-legally', 'p201fh', 'sec201', 'tryhackme', 'chfi', 'acpatmaamf', 'tcmmapt', 'psrtt', 'whptbbh', 'linux-101', 'pmat', 'cnd', 'securing-the-cloud-foundations-andrew-krug', 'sec554', 'fundamentals-of-virtualization', 'rmaap', 'mgt551', 'istaawn'], ['wahs', 'pawspf', 'pawpb', 'palpeb', 'pacsb', 'padsob', 'pawasb', 'mcdlpe', 'pacsaeb', 'fniao21', 'fnio21', 'harwarehp', 'security-plus', 'tepptcm', 'ppatcm', 'securing-the-cloud-foundations-andrew-krug', 'sec554', 'fundamentals-of-virtualization', 'rmaap', 'mgt551', 'istaawn'], ['aeharoe', 'cellebrite-physical-analyzer', 'mr-robot', 'rtowe', 'ida-pro', 'ewdp', 'ecthpv2', 'ecmap', 'ecir', 'endp', 'ecre', 'ecdfp', 'emapt', 'ecxd', 'ewptxv2', 'securing-the-cloud-foundations-andrew-krug', 'sec554', 'fundamentals-of-virtualization', 'rmaap', 'mgt551', 'istaawn'], ['ewpt', 'ecptx', 'ecpptv2', 'mpap', 'p101fh', 'ejpt', 'acunetix-premium', 'aourn', 'blackhat-2020', 'urxxehb', 'nessus-pro', 'cw32edb', 'feweir', 'blackhat-2021', 'hrabg', 'securing-the-cloud-foundations-andrew-krug', 'sec554', 'fundamentals-of-virtualization', 'rmaap', 'mgt551', 'istaawn'], ['itezddad', 'lhep12', 'ccrhlfc', 'sckbjs', 'ksma', 'fema', 'oiote', 'gcbecr', 'cpent', 'psmapath', 'psehf', 'psdfi', 'psdff', 'urbbg21', 'wdbgfum', 'securing-the-cloud-foundations-andrew-krug', 'sec554', 'fundamentals-of-virtualization', 'rmaap', 'mgt551', 'istaawn'], ['wdbgfkm', 'gsiswbhismitrea', 'mgt535', 'sec509', 'cyberwar16', 'nssaih', 'nssawh', 'blackhatiot18', 'epwittd', 'rtowp', 'rtopeiw', 'rtomdi', 'rtomde', 'sss7oifbtel', 'zpsrto', 'securing-the-cloud-foundations-andrew-krug', 'sec554', 'fundamentals-of-virtualization', 'rmaap', 'mgt551', 'istaawn'], ['sec588', 'silkroad2021', 'sec583', 'sec552', 'pen300', 'tudwapascud', 'chud101', 'aehnawptiv', 'rfehptbb', 'ehptbbhv2', 'osintopil2', 'osintopil1', 'osintfhapt', 'osifcm', 'pehtcccm', 'securing-the-cloud-foundations-andrew-krug', 'sec554', 'fundamentals-of-virtualization', 'rmaap', 'mgt551', 'istaawn'], ['wpefbcm', 'lpefbcm', 'cehb21ztm', 'zero2automated', 'whshhlaetodaho', 'redteam-blueprint', 'maltego', 'cehv11', 'revhcex', 'bbpbv1v2', 'sec455', 'blackhat-2019', 'blackhat-2018', 'socialdilemma', 'greathack', 'securing-the-cloud-foundations-andrew-krug', 'sec554', 'fundamentals-of-virtualization', 'rmaap', 'mgt551', 'istaawn'], ['deepweb', 'zer0day', 'sec550', 'sec579', 'ositosintit', 'pasccit', 'project-plus', 'casp-plus', 'pentest-plus', 'cysa-plus', 'network-plus', 'a-plus', 'x8664alasolpa', 'x86alasolpa', 'wmiaadpa', 'securing-the-cloud-foundations-andrew-krug', 'sec554', 'fundamentals-of-virtualization', 'rmaap', 'mgt551', 'istaawn'], ['wrtlpa', 'wfbpa', 'waerptamrw', 'wfmfrbtpa', 'wappa', 'wapcpa', 'vitapa', 'ufappa', 'tatsupa', 'swfptippa', 'rew32apa', 'rel32apa', 'pyfppa', 'psfppa', 'pwmpa', 'securing-the-cloud-foundations-andrew-krug', 'sec554', 'fundamentals-of-virtualization', 'rmaap', 'mgt551', 'istaawn'], ['piapa', 'pcpa', 'pfppa', 'ofwosi', 'nppa', 'mrfrbt', 'myohg', 'sec699', 'lfa', 'lrfrbt', 'linuxf', 'jsfp', 'hpscpb', 'gdm', 'gde', 'securing-the-cloud-foundations-andrew-krug', 'sec554', 'fundamentals-of-virtualization', 'rmaap', 'mgt551', 'istaawn'], ['esboow', 'eifrbt', 'asamlfi', 'aadad', 'arma', 'asaefp', 'ansv', 'asstiawd', 'ares', 'ctp', 'wifu', 'awe', 'awae', 'pwk', 'for526', 'securing-the-cloud-foundations-andrew-krug', 'sec554', 'fundamentals-of-virtualization', 'rmaap', 'mgt551', 'istaawn'], ['for585', 'for518', 'for498', 'for610', 'for578', 'for572', 'for508', 'for500', 'sec599', 'sec566', 'sec540', 'sec530', 'sec555', 'sec506', 'sec505', 'securing-the-cloud-foundations-andrew-krug', 'sec554', 'fundamentals-of-virtualization', 'rmaap', 'mgt551', 'istaawn'], ['sec545', 'sec501', 'sec487', 'sec450', 'sec511', 'sec503', 'sec401', 'mgt517', 'mgt512', 'mgt514', 'mgt414', 'ics515', 'ics410', 'aud507', 'sec580', 'securing-the-cloud-foundations-andrew-krug', 'sec554', 'fundamentals-of-virtualization', 'rmaap', 'mgt551', 'istaawn'], ['sec564', 'sec573', 'sec617', 'sec575', 'sec642', 'sec760', 'sec660', 'sec460', 'sec542', 'sec560', 'sec504', 'securing-the-cloud-foundations-andrew-krug', 'sec554', 'fundamentals-of-virtualization', 'rmaap', 'mgt551', 'istaawn']]

for x in range(1,pages+1):
   out.append(getPageUnits(f"https://hide01.ir/page/{x}/"))
   print(x)

x = []
for i in out:
    for ii in i:
        x.append(ii)
out = list(dict.fromkeys(x))


threads = []
for i in out:
    pageExtractor(f"https://hide01.ir/downloads/{i}/")
    #t = threading.Thread(target=pageExtractor, args=(f"https://hide01.ir/downloads/{i}/",))
    #threads.append(t)
    #t.start()
    #print(f"started {i}")