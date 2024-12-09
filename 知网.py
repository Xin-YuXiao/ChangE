# -*- coding: utf-8 -*-

import ssl
import time

import warnings

import requests
import os

from DrissionPage import WebPage
from pyquery import PyQuery as pq

ssl._create_default_https_context = ssl._create_unverified_context
warnings.filterwarnings("ignore")


class DzSpider(object):
    def __init__(self):
        self.folder = fr'{os.getcwd()}'
        self.keywords = ''
        self.start_page = 1
        self.end_page = 10
        self.spider_num = 1
        self.spder_min = 10
        self.spder_max = 30
        self.has_spider = 2000
        self.page_size = 20
        self.has_finish = False
        self.reset_end_page = True
        self.headers_str = '''
        Accept: */*
		Accept-Language: zh-CN,zh;q=0.9
		Cache-Control: no-cache
		Connection: keep-alive
		Content-Type: application/x-www-form-urlencoded; charset=UTF-8
		Cookie: Ecp_notFirstLogin=qfzQOR; Ecp_ClientId=3241014151600348884; Ecp_loginuserbk=bnu001; Ecp_IpLoginFail=24102114.112.49.140; SID_kns_new=kns2618108; knsadv-searchtype=%7B%22BLZOG7CK%22%3A%22gradeSearch%2CmajorSearch%22%2C%22MPMFIG1A%22%3A%22gradeSearch%2CmajorSearch%2CsentenceSearch%22%2C%22T2VC03OH%22%3A%22gradeSearch%2CmajorSearch%22%2C%22JQIRZIYA%22%3A%22gradeSearch%2CmajorSearch%2CsentenceSearch%22%2C%22S81HNSV3%22%3A%22gradeSearch%22%2C%22YSTT4HG0%22%3A%22gradeSearch%2CmajorSearch%2CauthorSearch%2CsentenceSearch%22%2C%22ML4DRIDX%22%3A%22gradeSearch%2CmajorSearch%22%2C%22WQ0UVIAA%22%3A%22gradeSearch%2CmajorSearch%22%2C%22VUDIXAIY%22%3A%22gradeSearch%2CmajorSearch%22%2C%22NN3FJMUV%22%3A%22gradeSearch%2CmajorSearch%2CauthorSearch%2CsentenceSearch%22%2C%22LSTPFY1C%22%3A%22gradeSearch%2CmajorSearch%2CsentenceSearch%22%2C%22HHCPM1F8%22%3A%22gradeSearch%2CmajorSearch%22%2C%22OORPU5FE%22%3A%22gradeSearch%2CmajorSearch%22%2C%22WD0FTY92%22%3A%22gradeSearch%2CmajorSearch%2CauthorSearch%2CsentenceSearch%22%2C%22BPBAFJ5S%22%3A%22gradeSearch%2CmajorSearch%2CauthorSearch%2CsentenceSearch%22%2C%22EMRPGLPA%22%3A%22gradeSearch%2CmajorSearch%22%2C%22PWFIRAGL%22%3A%22gradeSearch%2CmajorSearch%2CsentenceSearch%22%2C%22U8J8LYLV%22%3A%22gradeSearch%2CmajorSearch%22%2C%22R79MZMCB%22%3A%22gradeSearch%22%2C%22J708GVCE%22%3A%22gradeSearch%2CmajorSearch%22%2C%22HR1YT1Z9%22%3A%22gradeSearch%2CmajorSearch%22%2C%22JUP3MUPD%22%3A%22gradeSearch%2CmajorSearch%2CauthorSearch%2CsentenceSearch%22%2C%22NLBO1Z6R%22%3A%22gradeSearch%2CmajorSearch%22%2C%22RMJLXHZ3%22%3A%22gradeSearch%2CmajorSearch%2CsentenceSearch%22%2C%221UR4K4HZ%22%3A%22gradeSearch%2CmajorSearch%2CauthorSearch%2CsentenceSearch%22%2C%22NB3BWEHK%22%3A%22gradeSearch%2CmajorSearch%22%2C%22XVLO76FD%22%3A%22gradeSearch%2CmajorSearch%22%7D; cnkiUserKey=6ff078ad-43c9-6bea-d058-18dfa6263f40; Ecp_ClientIp=14.112.49.140; Hm_lvt_dcec09ba2227fd02c55623c1bb82776a=1728096890,1728548581,1729214890,1729473179; HMACCOUNT=99292B01804910B4; SID_sug=018133; LID=WEEvREcwSlJHSldSdmVpdm1HOSs1SlhCTGlPV2hZeEd2a2owUDFDV21ZUT0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!; Ecp_LoginStuts={"IsAutoLogin":false,"UserName":"bnu001","ShowName":"%E5%8C%97%E4%BA%AC%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6%E5%9B%BE%E4%B9%A6%E9%A6%86","UserType":"bk","BShowName":"","r":"qfzQOR","Members":[]}; Ecp_session=1; dblang=both; Hm_lpvt_dcec09ba2227fd02c55623c1bb82776a=1729496037; c_m_LinID=LinID=WEEvREcwSlJHSldSdmVpdm1HOSs1SlhCTGlPV2hZeEd2a2owUDFDV21ZUT0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!&ot=11%2F20%2F2024%2015%3A33%3A45; c_m_expire=2024-11-20%2015%3A33%3A45; tfstk=gCVKU44pYGjHfCYwa36iESLsbT7ip7UUBkzXZ0mHFlETAlAnFMzl2_nTjJAoOk2-V2zrA7bFzbd7brguKD0hy4i_vYVl8QYUQo4XtWXEZQhEabscmsf0-ylrNkr9hg8E143vF_mIVcaUfSq7isf08yg6eIkPiWvn8vmIVbMIR1Msb4oWOuOW1N3SrH9WOua1WcuydeMSAFis82KSNbZS1N3orboh2cTIqQeyVI00-TCpaQPtJvnJZcO-w5RmLmsKfQd-v0kpKyi9NQNaQAhktD62S0lnYygL4sREOYe4r4Ed9BZ8u5rt5o1JiDaao-DUOsJrHXiZEWGvP6at9DHbtATB1oaTP-DTsZ1q9XiQEXzkkM4T9k4U6zYWCXh3BxFKGs-IqR4Yw4FP41EYu5rt5o1RAgWbiSBhLnmxrp_OWLJrdVzLRx9KoNp_UVncJ_pyUA7ZWmbOWLJrdVutmwIpULkN7
		Origin: https://kns.cnki.net
		Pragma: no-cache
		Referer: https://kns.cnki.net/kns8s/defaultresult/index?crossids=YSTT4HG0%2CLSTPFY1C%2CJUP3MUPD%2CMPMFIG1A%2CWQ0UVIAA%2CBLZOG7CK%2CEMRPGLPA%2CPWFIRAGL%2CNLBO1Z6R%2CNN3FJMUV&korder=SU&kw=%5B1%5D%20%E7%99%BD%E9%9B%AA%2C%E5%88%98%E5%AE%8F%E5%88%A9%2C%E7%8E%8B%E6%96%87%2C%E9%99%88%E6%B5%A9%E5%87%AF%2C%E9%BB%84%E5%9B%AD.%20%E5%85%A8%E5%9F%9F%E7%AD%96%E5%88%92%EF%BC%9A%E5%9F%B9%E8%82%B2%E4%B8%96%E7%95%8C%E4%B8%80%E6%B5%81%E7%A7%91%E6%8A%80%E6%9C%9F%E5%88%8A%E6%96%B0%E6%96%B9%E7%95%A5%E2%80%94%E2%80%94%E4%BB%A5%E3%80%8A%E4%B8%AD%E5%A4%96%E5%85%AC%E8%B7%AF%E3%80%8B%E6%8E%A2%E7%B4%A2%E5%AE%9E%E8%B7%B5%E4%B8%BA%E4%BE%8B%5BJ%5D.%20%E7%BC%96%E8%BE%91%E5%AD%A6%E6%8A%A5%2C2024%2Cv.36%2802%29%3A209-213.
		Sec-Fetch-Dest: empty
		Sec-Fetch-Mode: cors
		Sec-Fetch-Site: same-origin
		User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36
		X-Requested-With: XMLHttpRequest
		sec-ch-ua: "Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"
		sec-ch-ua-mobile: ?0
		sec-ch-ua-platform: "Windows"
		Cookie: Ecp_notFirstLogin=wpkIRG; Ecp_ClientId=h241104175201277596; cnkiUserKey=111a9982-df45-6044-7538-2d40223e2ddf; Ecp_ClientIp=14.112.59.3; Ecp_loginuserbk=bnu001; SID_kns_new=kns2618131; Ecp_session=1; Hm_lvt_dcec09ba2227fd02c55623c1bb82776a=1730713994,1731288238,1731977340,1732494224; HMACCOUNT=7B98E9CDA0F03549; SID_restapi=018131; Hm_lpvt_dcec09ba2227fd02c55623c1bb82776a=1732494287; SID_sug=018105; LID=WEEvREcwSlJHSldSdmVpa3VEcjFaQU03Zk1vY2NJYTBhUU0vMXI3OGVQbz0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw\u0021\u0021; Ecp_LoginStuts={"IsAutoLogin":false,"UserName":"bnu001","ShowName":"%E5%8C%97%E4%BA%AC%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6%E5%9B%BE%E4%B9%A6%E9%A6%86","UserType":"bk","BShowName":"","r":"wpkIRG","Members":[]}; knsadv-searchtype=%7B%22BLZOG7CK%22%3A%22gradeSearch%2CmajorSearch%22%2C%22MPMFIG1A%22%3A%22gradeSearch%2CmajorSearch%2CsentenceSearch%22%2C%22T2VC03OH%22%3A%22gradeSearch%2CmajorSearch%22%2C%22JQIRZIYA%22%3A%22gradeSearch%2CmajorSearch%2CsentenceSearch%22%2C%22S81HNSV3%22%3A%22gradeSearch%22%2C%22YSTT4HG0%22%3A%22gradeSearch%2CmajorSearch%2CauthorSearch%2CsentenceSearch%22%2C%22ML4DRIDX%22%3A%22gradeSearch%2CmajorSearch%22%2C%22WQ0UVIAA%22%3A%22gradeSearch%2CmajorSearch%22%2C%22VUDIXAIY%22%3A%22gradeSearch%2CmajorSearch%22%2C%22NN3FJMUV%22%3A%22gradeSearch%2CmajorSearch%2CauthorSearch%2CsentenceSearch%22%2C%22LSTPFY1C%22%3A%22gradeSearch%2CmajorSearch%2CsentenceSearch%22%2C%22HHCPM1F8%22%3A%22gradeSearch%2CmajorSearch%22%2C%22OORPU5FE%22%3A%22gradeSearch%2CmajorSearch%22%2C%22WD0FTY92%22%3A%22gradeSearch%2CmajorSearch%2CauthorSearch%2CsentenceSearch%22%2C%22BPBAFJ5S%22%3A%22gradeSearch%2CmajorSearch%2CauthorSearch%2CsentenceSearch%22%2C%22EMRPGLPA%22%3A%22gradeSearch%2CmajorSearch%22%2C%22PWFIRAGL%22%3A%22gradeSearch%2CmajorSearch%2CsentenceSearch%22%2C%22U8J8LYLV%22%3A%22gradeSearch%2CmajorSearch%22%2C%22R79MZMCB%22%3A%22gradeSearch%22%2C%22J708GVCE%22%3A%22gradeSearch%2CmajorSearch%22%2C%22HR1YT1Z9%22%3A%22gradeSearch%2CmajorSearch%22%2C%22JUP3MUPD%22%3A%22gradeSearch%2CmajorSearch%2CauthorSearch%2CsentenceSearch%22%2C%22NLBO1Z6R%22%3A%22gradeSearch%2CmajorSearch%22%2C%22RMJLXHZ3%22%3A%22gradeSearch%2CmajorSearch%2CsentenceSearch%22%2C%221UR4K4HZ%22%3A%22gradeSearch%2CmajorSearch%2CauthorSearch%2CsentenceSearch%22%2C%22NB3BWEHK%22%3A%22gradeSearch%2CmajorSearch%22%2C%22XVLO76FD%22%3A%22gradeSearch%2CmajorSearch%22%7D; c_m_LinID=LinID=WEEvREcwSlJHSldSdmVpa3VEcjFaQU03Zk1vY2NJYTBhUU0vMXI3OGVQbz0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw\u0021\u0021&ot=12%2F26%2F2024%2016%3A42%3A49; c_m_expire=2024-12-26%2016%3A42%3A49; tfstk=fpwZFDDQ6OBaDH6Xhck2LP_y15MtIAbSi-gjmoqmfV0g5og0Tr4IClZ0cKom-PhXCK0_8mz7PGd_lqGD3oqrhKMg1So4Pl4qMG3joqzbm5sCFTZTXxHmua65F2L4HD4ZmfvGm2m-jVNYnaETXxKL66s7IlL4FOsYSx4mKpmsbxvinjjexm3HImvimejEJmDmjq0mKemsDEmmjrqhYmgnojmajovEVfj-9OSNy3lS_4qFwKJmfLGirX3ena2KbF0uj2JDhVnEv_ZUfNJ8AAezz0a1Kdzz2JUExzXV8xULirm4-TLjB7aTeXz1Zpqnp2huiXSGIkkZ7bwZa3AEQS4T3fFwDgEnIyF-yffdJDy_Fju-TebgAkuiaSz1JK0_ak4ENJTBFxULirm4-FSPzEnHv1yY_EAqsDnEPMSUQHQ06Cq3bbRvMXD-Y4ssfIdxsDnEPMSeMIhnJDu5fc1..; dblang=both
        '''
        self.headers = dict(
            [[y.strip() for y in x.strip().split(':', 1)] for x in self.headers_str.strip().split('\n') if x.strip()])

    def run_task(self):
        self.keywords = '大数据'  #在此处修改关键词
        req_url = 'https://kns.cnki.net/kns8s/brief/grid'
        data = {
            "boolSearch": "true",
            "QueryJson": "{\"Platform\":\"\",\"Resource\":\"CROSSDB\",\"Classid\":\"WD0FTY92\",\"Products\":\"\",\"QNode\":{\"QGroup\":[{\"Key\":\"Subject\",\"Title\":\"\",\"Logic\":0,\"Items\":[{\"Field\":\"SU\",\"Value\":\"" + self.keywords + "\",\"Operator\":\"TOPRANK\",\"Logic\":0}],\"ChildItems\":[]}]},\"ExScope\":1,\"SearchType\":2,\"Rlang\":\"CHINESE\",\"KuaKuCode\":\"YSTT4HG0,LSTPFY1C,JUP3MUPD,MPMFIG1A,WQ0UVIAA,BLZOG7CK,EMRPGLPA,PWFIRAGL,NLBO1Z6R,NN3FJMUV\"}",
            "pageNum": "1",
            "pageSize": "20",
            "sortField": "",
            "sortType": "",
            "dstyle": "listmode",
            "productStr": "YSTT4HG0,LSTPFY1C,RMJLXHZ3,JQIRZIYA,JUP3MUPD,1UR4K4HZ,BPBAFJ5S,R79MZMCB,MPMFIG1A,WQ0UVIAA,NB3BWEHK,XVLO76FD,HR1YT1Z9,BLZOG7CK,EMRPGLPA,J708GVCE,ML4DRIDX,PWFIRAGL,NLBO1Z6R,NN3FJMUV,",
            "aside": f"主题：{self.keywords}",
            "searchFrom": "资源范围：总库",
            "CurPage": "1"
        }
        req = requests.post(req_url, headers=self.headers, data=data, verify=False)
        # req.encoding='gb2312'
        html = req.text
        # print(html)
        doc = pq(html)
        data_list = doc('.result-table-list tr').items()
        for item in data_list:
            title_a = item('td.name a')
            title = title_a.text()
            title_link = title_a.attr('href')
            if title is None or title_link is None:
                continue
            title = title.replace('\n', '')
            print(self.spider_num, title)
            self.get_pdf(title_link)
            if self.spider_num < self.spder_min:
                continue
            elif self.spider_num > self.spder_max:
                exit()
            time.sleep(3)
            self.spider_num += 1

    def get_pdf(self, link):
        page = WebPage('d')
        page.get(link, timeout=60)
        time.sleep(2)
        page.wait.ele_displayed('#pdfDown')
        page.ele('#pdfDown').click()



if __name__ == '__main__':
    spider = DzSpider()
    spider.keywords = ''
    # 索引区间
    spider.spder_min = 1
    spider.spder_max = 201
    spider.run_task()
