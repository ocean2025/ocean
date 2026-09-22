#coding=utf-8
#!/usr/bin/python
import re
import sys
import json
import time
import random
from datetime import datetime
from urllib.parse import quote, unquote

import requests

sys.path.append('..')
from base.spider import Spider

class Spider(Spider):
    def getName(self):
        return "B站视频"

    def init(self, extend):
        try:
            self.extendDict = json.loads(extend)
        except:
            self.extendDict = {}
        
        cookie_str = "SESSDATA=8f3ff69f%2C1794310143%2C53c01%2A52CjBX4vniMP8UbH-FHHxtImWyVMCf_NkAmIFpLXuK3B9TH1uSPOG3A5ST5nKXpP5b06gSVmx2Q2FWY0xPY19yaGxqOUNoRnZuLVhselJhVXU5UWlQb093RnprU2xpLVk5bmpwWjZ6bEhLZWt2RTIwbVpHaFJsYXJVeGtGRnFMcTd1OHRoZ24zN2ZRIIEC; bili_jct=27dfcc874d1a3c0fe39b9651ca436394; DedeUserID=3546629682497943; DedeUserID__ckMd5=b11f007e7707c2a6; sid=pey664gw; b_lsid=922FAEA2_19E263F56EF"
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
            "Referer": "https://www.bilibili.com",
            "cookie": cookie_str
        }

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        result = {}
        result['filters'] = {}
        cookie = ''
        if 'cookie' in self.extendDict:
            cookie = self.extendDict['cookie']
        if 'json' in self.extendDict:
            r = self.fetch(self.extendDict['json'], timeout=10)
            if 'cookie' in r.json():
                cookie = r.json()['cookie']
        if cookie == '':
            cookie = '{}'
        elif type(cookie) == str and cookie.startswith('http'):
            cookie = self.fetch(cookie, timeout=10).text.strip()
        try:
            if type(cookie) == dict:
                cookie = json.dumps(cookie, ensure_ascii=False)
        except:
            pass
        _, _, _ = self.getCookie(cookie)
        bblogin = self.getCache('bblogin')
        if bblogin:
            result['class'] = []
        else:
            result['class'] = []
        if 'json' in self.extendDict:
            r = self.fetch(self.extendDict['json'], timeout=10)
            params = r.json()
            if 'classes' in params:
                result['class'] = result['class'] + params['classes']
            elif 'class' in params:            
                result['class'] = result['class'] + params['class']
            if filter:
                if 'filter' in params:
                    result['filters'] = params['filter']
            if 'filters' in params and not result['filters']:
                result['filters'] = params['filters']    
        elif 'categories' in self.extendDict or 'type' in self.extendDict:
            if 'categories' in self.extendDict:
                cateList = self.extendDict['categories'].split('#')
            else:
                cateList = self.extendDict['type'].split('#')
            for cate in cateList:
                result['class'].append({'type_name': cate, 'type_id': cate})
        # 添加搜索型分类：点击即搜索对应关键词
        search_classes = [
         {'type_name': '音乐', 'type_id': '音乐'},
    {"type_name": "新闻", "type_id": "新闻"},
    {"type_name": "白噪音", "type_id": "白噪音"},
    {"type_name": "沙雕动漫", "type_id": "沙雕动漫"},
    {"type_name": "虾仁", "type_id": "虾仁"},
    {"type_name": "短剧", "type_id": "短剧"},
    {"type_name": "电影", "type_id": "电影"},
    {"type_name": "歌曲", "type_id": "歌曲"},
    {"type_name": "演唱会", "type_id": "演唱会"},
    {"type_name": "鬼畜", "type_id": "鬼畜"},
    {"type_name": "搞笑", "type_id": "搞笑"},
    {"type_name": "脑洞乌托邦", "type_id": "脑洞乌托邦"},
    {"type_name": "相声", "type_id": "相声"},
    {"type_name": "小品", "type_id": "小品"},
    {"type_name": "戏曲", "type_id": "戏曲"},
    {"type_name": "音乐", "type_id": "音乐"},
    {"type_name": "MV", "type_id": "MV"},
    {"type_name": "舞曲", "type_id": "舞曲"},
    {"type_name": "舞蹈", "type_id": "舞蹈"},
    {"type_name": "纪录片", "type_id": "纪录片"},
    {"type_name": "健身", "type_id": "健身"},
    {"type_name": "帕梅拉", "type_id": "帕梅拉"},
    {"type_name": "武术", "type_id": "武术"},
    {"type_name": "太极拳", "type_id": "太极拳"},
    {"type_name": "广场舞", "type_id": "广场舞"},
    {"type_name": "体育", "type_id": "体育"},
    {"type_name": "球星", "type_id": "球星"},
    {"type_name": "世界杯", "type_id": "世界杯"},
    {"type_name": "UP主", "type_id": "UP主"},
    {"type_name": "小姐姐", "type_id": "小姐姐"},
    {"type_name": "女优", "type_id": "女优"},
    {"type_name": "美食", "type_id": "美食"},
    {"type_name": "食谱", "type_id": "食谱"},
    {"type_name": "荒野求生", "type_id": "荒野求生"},
    {"type_name": "旅游", "type_id": "旅游"},
    {"type_name": "风景", "type_id": "风景"},
    {"type_name": "游戏", "type_id": "游戏"},
    {"type_name": "解说", "type_id": "解说"},
    {"type_name": "演讲", "type_id": "演讲"},
    {"type_name": "考公考试", "type_id": "考公考试"},
    {"type_name": "平面设计", "type_id": "平面设计"},
    {"type_name": "软件教学", "type_id": "软件教学"},    
            {'type_name': '花鼓戏', 'type_id': '花鼓戏'},
            {'type_name': '京剧', 'type_id': '京剧'},
        ]
        # 去重追加
        existing_ids = {c.get('type_id') for c in result.get('class', [])}
        for sc in search_classes:
            if sc['type_id'] not in existing_ids:
                result['class'].append(sc)

        if not 'class' in result or result['class'] == []:
            result['class'] = []
        return result

    def homeVideoContent(self):
        result = {}
        cookie = ''
        if 'cookie' in self.extendDict:
            cookie = self.extendDict['cookie']
        if 'json' in self.extendDict:
            r = self.fetch(self.extendDict['json'], timeout=10)
            if 'cookie' in r.json():
                cookie = r.json()['cookie']
        if cookie == '':
            cookie = '{}'
        elif type(cookie) == str and cookie.startswith('http'):
            cookie = self.fetch(cookie, timeout=10).text.strip()
        try:
            if type(cookie) == dict:
                cookie = json.dumps(cookie, ensure_ascii=False)
        except:
            pass
        cookie, imgKey, subKey = self.getCookie(cookie)
        url = 'https://api.bilibili.com/x/web-interface/index/top/feed/rcmd?y_num=1&fresh_type=3&feed_version=SEO_VIDEO&fresh_idx_1h=1&fetch_row=1&fresh_idx=1&brush=0&homepage_ver=1&ps=20'
        r = requests.get(url, cookies=cookie, headers=self.header, timeout=5)
        data = json.loads(self.cleanText(r.text))
        try:
            result['list'] = []
            vodList = data['data']['item']
            for vod in vodList:
                aid = str(vod['id']).strip()
                title = self.removeHtmlTags(vod['title']).strip()
                img = vod['pic'].strip()
                remark = time.strftime('%H:%M:%S', time.gmtime(vod['duration']))
                if remark.startswith('00:'):
                    remark = remark[3:]
                if remark == '00:00':
                    continue
                result['list'].append({
                    'vod_id': aid,
                    'vod_name': title,
                    'vod_pic': img,
                    'vod_remarks': remark
                })
        except:
            pass
        return result

    def categoryContent(self, cid, page, filter, ext):
        page = int(page)
        result = {}
        videos = []
        cookie = ''
        pagecount = page
        if 'cookie' in self.extendDict:
            cookie = self.extendDict['cookie']
        if 'json' in self.extendDict:
            r = self.fetch(self.extendDict['json'], timeout=10)
            if 'cookie' in r.json():
                cookie = r.json()['cookie']
        if cookie == '':
            cookie = '{}'
        elif type(cookie) == str and cookie.startswith('http'):
            cookie = self.fetch(cookie, timeout=10).text.strip()
        try:
            if type(cookie) == dict:
                cookie = json.dumps(cookie, ensure_ascii=False)
        except:
            pass
        cookie, imgKey, subKey = self.getCookie(cookie)
        if cid == '动态':
            if page > 1:
                offset = self.getCache('offset')
                if not offset:
                    offset = ''
                url = f'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all?timezone_offset=-480&type=all&offset={offset}&page={page}'
            else:
                url = f'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all?timezone_offset=-480&type=all&page={page}'
            r = self.fetch(url, cookies=cookie, headers=self.header, timeout=5)
            data = json.loads(self.cleanText(r.text))
            self.setCache('offset', data['data']['offset'])
            vodList = data['data']['items']
            if data['data']['has_more']:
                pagecount = page + 1
            for vod in vodList:
                if vod['type'] != 'DYNAMIC_TYPE_AV':
                    continue
                vid = str(vod['modules']['module_dynamic']['major']['archive']['aid']).strip()
                remark = vod['modules']['module_dynamic']['major']['archive']['duration_text'].strip()
                title = self.removeHtmlTags(vod['modules']['module_dynamic']['major']['archive']['title']).strip()
                img = vod['modules']['module_dynamic']['major']['archive']['cover']
                videos.append({
                    "vod_id": vid,
                    "vod_name": title,
                    "vod_pic": img,
                    "vod_remarks": remark
                })
        elif cid == "收藏夹":
            userid = self.getUserid(cookie)
            if userid is None:
                return {}, 1
            url = f'http://api.bilibili.com/x/v3/fav/folder/created/list-all?up_mid={userid}&jsonp=jsonp'
            r = self.fetch(url, cookies=cookie, headers=self.header, timeout=5)
            data = json.loads(self.cleanText(r.text))
            vodList = data['data']['list']
            pagecount = page
            for vod in vodList:
                vid = vod['id']
                title = vod['title'].strip()
                remark = vod['media_count']
                img = 'https://api-lmteam.koyeb.app/files/shoucang.png'
                videos.append({
                    "vod_id": f'fav&&&{vid}',
                    "vod_name": title,
                    "vod_pic": img,
                    "vod_tag": 'folder',
                    "vod_remarks": remark
                })
        elif cid.startswith('fav&&&'):
            cid = cid[6:]
            url = f'http://api.bilibili.com/x/v3/fav/resource/list?media_id={cid}&pn={page}&ps=20&platform=web&type=0'
            r = self.fetch(url, cookies=cookie, headers=self.header, timeout=5)
            data = json.loads(self.cleanText(r.text))
            if data['data']['has_more']:
                pagecount = page + 1
            else:
                pagecount = page
            vodList = data['data']['medias']
            for vod in vodList:
                vid = str(vod['id']).strip()
                title = self.removeHtmlTags(vod['title']).replace("&quot;", '"')
                img = vod['cover'].strip()
                remark = time.strftime('%H:%M:%S', time.gmtime(vod['duration']))
                if remark.startswith('00:'):
                    remark = remark[3:]
                videos.append({
                    "vod_id": vid,
                    "vod_name": title,
                    "vod_pic": img,
                    "vod_remarks": remark
                })
        elif cid.startswith('UP主&&&'):
            mid = cid[6:]
            params = {'mid': mid, 'ps': 30, 'pn': page}
            if imgKey and subKey:
                params = self.encWbi(params, imgKey, subKey)
            url = 'https://api.bilibili.com/x/space/wbi/arc/search?'
            for key in params:
                url += f'&{key}={quote(str(params[key]))}'
            r = self.fetch(url, cookies=cookie, headers=self.header, timeout=5)
            data = json.loads(self.cleanText(r.text))
            if data.get('code') != 0 or 'data' not in data or not data['data']:
                return result
            if page < data['data']['page']['count']:
                pagecount = page + 1
            else:
                pagecount = page
            if page == 1:
                videos = [{"vod_id": f'UP主&&&{mid}', "vod_name": '播放列表'}]
            vodList = data['data']['list']['vlist']
            for vod in vodList:
                vid = str(vod['aid']).strip()
                title = self.removeHtmlTags(vod['title']).replace("&quot;", '"')
                img = vod['pic'].strip()
                remarkinfos = vod['length'].split(':')
                minutes = int(remarkinfos[0])
                if minutes >= 60:
                    hours = str(minutes // 60)
                    minutes = str(minutes % 60)
                    if len(hours) == 1:
                        hours = '0' + hours
                    if len(minutes) == 1:
                        minutes = '0' + minutes
                    remark = hours + ':' + minutes + ':' + remarkinfos[1]
                else:
                    remark = vod['length']
                videos.append({
                    "vod_id": vid,
                    "vod_name": title,
                    "vod_pic": img,
                    "vod_remarks": remark
                })
        elif cid == '历史记录':
            url = f'http://api.bilibili.com/x/v2/history?pn={page}'
            r = self.fetch(url, cookies=cookie, headers=self.header, timeout=5)
            data = json.loads(self.cleanText(r.text))
            if len(data['data']) == 300:
                pagecount = page + 1
            else:
                pagecount = page
            vodList = data['data']
            for vod in vodList:
                if vod['duration'] <= 0:
                    continue
                vid = str(vod["aid"]).strip()
                img = vod["pic"].strip()
                title = self.removeHtmlTags(vod["title"]).replace("&quot;", '"')
                if vod['progress'] != -1:
                    process = time.strftime('%H:%M:%S', time.gmtime(vod['progress']))
                    totalTime = time.strftime('%H:%M:%S', time.gmtime(vod['duration']))
                    if process.startswith('00:'):
                        process = process[3:]
                    if totalTime.startswith('00:'):
                        totalTime = totalTime[3:]
                    remark = process + '|' + totalTime
                    videos.append({
                        "vod_id": vid,
                        "vod_name": title,
                        "vod_pic": img,
                        "vod_remarks": remark
                    })
        else:
            url = 'https://api.bilibili.com/x/web-interface/wbi/search/type?search_type=video&keyword={}&page={}'
            for key in ext:
                if key == 'tid':
                    cid = ext[key]
                    continue
                url += f'&{key}={ext[key]}'
            url = url.format(quote(cid), page)
            r = self.fetch(url, cookies=cookie, headers=self.header, timeout=5)
            data = json.loads(self.cleanText(r.text))
            pagecount = data['data']['numPages']
            vodList = data['data']['result']
            for vod in vodList:
                if vod['type'] != 'video':
                    continue
                vid = str(vod['aid']).strip()
                title = self.removeHtmlTags(self.cleanText(vod['title']))
                img = 'https:' + vod['pic'].strip()
                remarkinfo = vod['duration'].split(':')
                minutes = int(remarkinfo[0])
                seconds = remarkinfo[1]
                if len(seconds) == 1:
                    seconds = '0' + seconds
                if minutes >= 60:
                    hour = str(minutes // 60)
                    minutes = str(minutes % 60)
                    if len(hour) == 1:
                        hour = '0' + hour
                    if len(minutes) == 1:
                        minutes = '0' + minutes
                    remark = f'{hour}:{minutes}:{seconds}'
                else:
                    minutes = str(minutes)
                    if len(minutes) == 1:
                        minutes = '0' + minutes
                    remark = f'{minutes}:{seconds}'
                videos.append({
                    "vod_id": vid,
                    "vod_name": title,
                    "vod_pic": img,
                    "vod_remarks": remark
                })
        lenvideos = len(videos)
        result['list'] = videos
        result['page'] = page
        result['pagecount'] = pagecount
        result['limit'] = lenvideos
        result['total'] = lenvideos
        return result

    def detailContent(self, did):
        aid = did[0]
        if aid.startswith('UP主&&&'):
            mid = aid[6:]
            # 使用 UP 主投稿列表接口（原 medialist/resource/list 传 mid 无效，media_list 恒为 null）
            cookie = ''
            if 'cookie' in self.extendDict:
                cookie = self.extendDict['cookie']
            if 'json' in self.extendDict:
                r = self.fetch(self.extendDict['json'], timeout=10)
                if 'cookie' in r.json():
                    cookie = r.json()['cookie']
            if cookie == '':
                cookie = '{}'
            elif type(cookie) == str and cookie.startswith('http'):
                cookie = self.fetch(cookie, timeout=10).text.strip()
            try:
                if type(cookie) == dict:
                    cookie = json.dumps(cookie, ensure_ascii=False)
            except:
                pass
            cookie, imgKey, subKey = self.getCookie(cookie)
            params = {'mid': mid, 'ps': 50, 'pn': 1}
            if imgKey and subKey:
                params = self.encWbi(params, imgKey, subKey)
            url = 'https://api.bilibili.com/x/space/wbi/arc/search?'
            for key in params:
                url += f'&{key}={quote(str(params[key]))}'
            r = self.fetch(url, headers=self.header, cookies=cookie, timeout=5)
            try:
                vdata = r.json()['data']
                videoList = vdata['list']['vlist']
            except Exception:
                return {'list': []}
            vod = {
                "vod_id": aid,
                "vod_name": '播放列表',
                'vod_play_from': 'B站视频'
            }
            playUrl = ''
            for video in videoList:
                remark = time.strftime('%H:%M:%S', time.gmtime(video['length']))
                name = self.removeHtmlTags(video['title']).strip().replace("#", "-").replace('$', '*')
                if remark.startswith('00:'):
                    remark = remark[3:]
                playUrl += f"[{remark}]/{name}$bvid&&&{video['bvid']}#"
            vod['vod_play_url'] = playUrl.strip('#')
            result = {'list': [vod]}
            return result
        url = f"https://api.bilibili.com/x/web-interface/view?aid={aid}"
        r = self.fetch(url, headers=self.header, timeout=10)
        data = json.loads(self.cleanText(r.text))
        if "staff" in data['data']:
            director = ''
            for staff in data['data']['staff']:
                director += '[a=cr:{{"id":"UP主&&&{}","name":"{}"}}/]{}[/a],'.format(staff['mid'], staff['name'], staff['name'])
        else:
            director = '[a=cr:{{"id":"UP主&&&{}","name":"{}"}}/]{}[/a]'.format(data['data']['owner']['mid'], data['data']['owner']['name'], data['data']['owner']['name'])
        vod = {
            "vod_id": aid,
            "vod_name": self.removeHtmlTags(data['data']['title']),
            "vod_pic": data['data']['pic'],
            "type_name": data['data']['tname'],
            "vod_year": datetime.fromtimestamp(data['data']['pubdate']).strftime('%Y-%m-%d %H:%M:%S'),
            "vod_content": data['data']['desc'].replace('\xa0', ' ').replace('\n\n', '\n').strip(),
            "vod_director": director
        }
        videoList = data['data']['pages']
        playUrl = ''
        for video in videoList:
            remark = time.strftime('%H:%M:%S', time.gmtime(video['duration']))
            name = self.removeHtmlTags(video['part']).strip().replace("#", "-").replace('$', '*')
            if remark.startswith('00:'):
                remark = remark[3:]
            playUrl = playUrl + f"[{remark}]/{name}${aid}_{video['cid']}#"
        url = f'https://api.bilibili.com/x/web-interface/archive/related?aid={aid}'
        r = self.fetch(url, headers=self.header, timeout=5)
        data = json.loads(self.cleanText(r.text))
        videoList = data['data']
        playUrl = playUrl.strip('#') + '$$$'
        for video in videoList:
            remark = time.strftime('%H:%M:%S', time.gmtime(video['duration']))
            if remark.startswith('00:'):
                remark = remark[3:]
            name = self.removeHtmlTags(video['title']).strip().replace("#", "-").replace('$', '*')
            playUrl = playUrl + '[{}]/{}${}_{}#'.format(remark, name, video['aid'], video['cid'])
        vod['vod_play_from'] = 'B站视频$$$相关视频'
        vod['vod_play_url'] = playUrl.strip('#')
        result = {
            'list': [
                vod
            ]
        }
        return result

    def searchContent(self, key, quick, pg=1):
        videos = []
        
        if quick:
            return {'list': []}
        
        cookie = ''
        if 'cookie' in self.extendDict:
            cookie = self.extendDict['cookie']
        if 'json' in self.extendDict:
            r = self.fetch(self.extendDict['json'], timeout=10)
            if 'cookie' in r.json():
                cookie = r.json()['cookie']
        if cookie == '':
            cookie = '{}'
        elif type(cookie) == str and cookie.startswith('http'):
            cookie = self.fetch(cookie, timeout=10).text.strip()
        try:
            if type(cookie) == dict:
                cookie = json.dumps(cookie, ensure_ascii=False)
        except:
            pass
        
        cookie, _, _ = self.getCookie(cookie)
        
        page = int(pg) if pg else 1
        url = f'https://api.bilibili.com/x/web-interface/wbi/search/type?search_type=video&keyword={key}&page={page}'
        r = self.fetch(url, headers=self.header, cookies=cookie, timeout=5)
        jo = json.loads(self.cleanText(r.text))
        
        if 'result' not in jo['data']:
            return {
                'list': [],
                'page': page,
                'pagecount': 1,
                'limit': 0,
                'total': 0
            }
        
        vodList = jo['data']['result']
        for vod in vodList:
            if vod.get('type') != 'video':
                continue
                
            aid = str(vod.get('aid', '')).strip()
            title = self.removeHtmlTags(self.cleanText(vod.get('title', '')))
            img = 'https:' + vod.get('pic', '').strip() if vod.get('pic') else ''
            
            try:
                remarkinfo = vod.get('duration', '0:00').split(':')
                minutes = int(remarkinfo[0]) if remarkinfo[0].isdigit() else 0
                seconds = remarkinfo[1] if len(remarkinfo) > 1 else '00'
            except:
                continue
            
            if len(seconds) == 1:
                seconds = '0' + seconds
            if minutes >= 60:
                hour = str(minutes // 60)
                minutes = str(minutes % 60)
                if len(hour) == 1:
                    hour = '0' + hour
                if len(minutes) == 1:
                    minutes = '0' + minutes
                remark = f'{hour}:{minutes}:{seconds}'
            else:
                minutes = str(minutes)
                if len(minutes) == 1:
                    minutes = '0' + minutes
                remark = f'{minutes}:{seconds}'
            
            videos.append({
                "vod_id": aid,
                "vod_name": title,
                "vod_pic": img,
                "vod_remarks": remark
            })
        
        numResults = jo['data'].get('numResults', 0)
        numPages = jo['data'].get('numPages', 1)
        
        return {
            'list': videos,
            'page': page,
            'pagecount': numPages,
            'limit': len(videos),
            'total': numResults
        }

    def playerContent(self, flag, pid, vipFlags):
        result = {}
        
        # 1. 解析aid和cid
        if pid.startswith('bvid&&&'):
            url = "https://api.bilibili.com/x/web-interface/view?bvid={}".format(pid[7:])
            r = self.fetch(url, headers=self.header, timeout=10)
            data = r.json()['data']
            aid = data['aid']
            cid = data['cid']
        else:
            idList = pid.split("_")
            aid = idList[0]
            cid = idList[1]
        
        # 2. 获取cookie
        cookie = ''
        extendDict = self.extendDict
        if 'cookie' in extendDict:
            cookie = extendDict['cookie']
        if 'json' in self.extendDict:
            r = self.fetch(extendDict['json'], timeout=10)
            if 'cookie' in r.json():
                cookie = r.json()['cookie']
        if cookie == '':
            cookie = '{}'
        elif type(cookie) == str and cookie.startswith('http'):
            cookie = self.fetch(cookie, timeout=10).text.strip()
        try:
            if type(cookie) == dict:
                cookie = json.dumps(cookie, ensure_ascii=False)
        except:
            pass
        cookiesDict, _, _ = self.getCookie(cookie)
        
        # 3. 首选 MP4 直链（durl）：不依赖 DASH/本地代理，任何播放器都能播
        #    先探测一次拿到服务端真实可用的档位列表（accept_quality），再逐档取真实直链
        mp4_list = []
        try:
            timestamp = int(time.time() * 1000)
            probe_url = f'https://api.bilibili.com/x/player/playurl?avid={aid}&cid={cid}&qn=80&fnval=1&fnver=0&fourk=0&_={timestamp}'
            r = self.fetch(probe_url, cookies=cookiesDict, headers=self.header, timeout=5)
            probe_data = json.loads(self.cleanText(r.text))
            if probe_data.get('code') == 0 and 'data' in probe_data:
                pdata = probe_data['data']
                if 'durl' in pdata and pdata['durl']:
                    accept_quality = pdata.get('accept_quality', [])
                    accept_desc = pdata.get('accept_description', [])
                    # 无 accept 字段时用探测返回的这档兜底
                    if not accept_quality:
                        accept_quality = [pdata.get('quality', 64)]
                        accept_desc = ['高清 720P']
                    name_map = dict(zip(accept_quality, accept_desc))
                    for qn in accept_quality:
                        if qn in name_map and len(mp4_list) >= 2 and name_map[qn] in mp4_list:
                            continue
                        try:
                            qurl = f'https://api.bilibili.com/x/player/playurl?avid={aid}&cid={cid}&qn={qn}&fnval=1&fnver=0&fourk=0'
                            r2 = self.fetch(qurl, cookies=cookiesDict, headers=self.header, timeout=5)
                            qdata = json.loads(self.cleanText(r2.text))
                            if qdata.get('code') != 0 or 'data' not in qdata:
                                continue
                            ddata = qdata['data']
                            if 'durl' not in ddata or not ddata['durl']:
                                continue
                            du = ddata['durl'][0]['url']
                            for cand in [du] + ddata['durl'][0].get('backup_url', []):
                                if cand and 'mcdn.bilivideo.cn' not in cand:
                                    du = cand
                                    break
                            if not du:
                                continue
                            qname = name_map.get(qn, f'质量{qn}')
                            if qname in mp4_list:
                                continue
                            mp4_list.append(qname)
                            mp4_list.append(du)
                        except Exception:
                            continue
        except Exception:
            pass
        if mp4_list:
            result["parse"] = 0
            result["url"] = mp4_list
            result["header"] = self.header
            result["format"] = 'video/mp4'
            return result
        
        # 4. 后备：DASH 方案（需要播放器支持 DASH + 本地代理）
        #    测试哪个qn能获得最高画质（使用随机无效值避免缓存记忆）
        random_qn = random.randint(900, 999)  # 每次生成不同的随机数
        test_qn_values = [random_qn, 126, 120]  # 随机值优先，避免被服务器记忆
        
        best_qn = 120
        max_height = 0
        best_data = None
        
        for test_qn in test_qn_values:
            # 添加时间戳参数强制刷新，避免缓存
            timestamp = int(time.time() * 1000)
            test_url = f'https://api.bilibili.com/x/player/playurl?avid={aid}&cid={cid}&qn={test_qn}&fnval=4048&fnver=0&fourk=1&_={timestamp}'
            r = self.fetch(test_url, cookies=cookiesDict, headers=self.header, timeout=5)
            test_data = json.loads(self.cleanText(r.text))
            
            if test_data.get('code') == 0 and 'data' in test_data:
                if 'dash' in test_data['data']:
                    videos = test_data['data']['dash'].get('video', [])
                    if videos:
                        # 获取该画质下的最高分辨率
                        current_height = max([v.get('height', 0) for v in videos])
                        if current_height > max_height:
                            max_height = current_height
                            best_qn = test_qn
                            best_data = test_data
                else:
                    # 非dash格式，直接使用
                    best_qn = test_qn
                    best_data = test_data
                    break
        
        # 5. 使用测试出的最佳qn获取数据
        if best_data is None:
            timestamp = int(time.time() * 1000)
            api_url = f'https://api.bilibili.com/x/player/playurl?avid={aid}&cid={cid}&qn=120&fnval=4048&fnver=0&fourk=1&_={timestamp}'
            r = self.fetch(api_url, cookies=cookiesDict, headers=self.header, timeout=5)
            best_data = json.loads(self.cleanText(r.text))
        
        data = best_data
        
        if data.get('code') != 0 or 'data' not in data:
            return result
        
        # 5. 构建画质选项列表
        play_list = []
        
        if 'accept_quality' in data['data'] and 'accept_description' in data['data']:
            accept_quality = data['data']['accept_quality']
            accept_description = data['data']['accept_description']
            
            added_qualities = set()
            cookies = quote(json.dumps(cookiesDict))
            thread = str(extendDict.get('thread', '0'))
            
            for i, qn in enumerate(accept_quality):
                if i < len(accept_description):
                    quality_name = accept_description[i]
                    
                    if quality_name in added_qualities:
                        continue
                    
                    # 对最高画质使用测试出的最佳qn，其他画质保持原样
                    actual_qn = qn
                    if i == 0:
                        actual_qn = best_qn
                    
                    proxy_url = f'http://127.0.0.1:9978/proxy?do=py&type=mpd&qn={actual_qn}&aid={aid}&cid={cid}&thread={thread}'
                    
                    play_list.append(quality_name)
                    play_list.append(proxy_url)
                    added_qualities.add(quality_name)
            
            if play_list:
                result["parse"] = 0
                result["url"] = play_list
                result["header"] = self.header
                result['danmaku'] = 'https://api.bilibili.com/x/v1/dm/list.so?oid={}'.format(cid)
                result["format"] = 'application/dash+xml'
                return result
        
        return result

    def localProxy(self, params):
        if params['type'] == "mpd":
            return self.proxyMpd(params)
        if params['type'] == "media":
            return self.proxyMedia(params)
        return None

    def destroy(self):
        pass

    def proxyMpd(self, params):
        content, dashinfos, mediaType = self.getDash(params)
        if mediaType == 'mpd':
            return [200, "application/dash+xml", content]
        else:
            url = ''
            urlList = [content] + dashinfos['durl'][0]['backup_url'] if 'backup_url' in dashinfos['durl'][0] and dashinfos['durl'][0]['backup_url'] else [content]
            for url in urlList:
                if 'mcdn.bilivideo.cn' not in url:
                    break
            header = self.header.copy()
            if 'range' in params:
                header['Range'] = params['range']
            if '127.0.0.1:7777' in url:
                header["Location"] = url
                return [302, "video/MP2T", None, header]
            r = requests.get(url, headers=header, stream=True)
            return [206, "application/octet-stream", r.content]

    def proxyMedia(self, params, forceRefresh=False):
        _, dashinfos, _ = self.getDash(params)
        
        qn = params.get('qn', '120')
        
        if 'videoid' in params:
            videoid = int(params['videoid'])
            for video in dashinfos['video']:
                if str(video.get('id', '')) == str(qn):
                    dashinfo = video
                    break
            else:
                dashinfo = dashinfos['video'][videoid]
        elif 'audioid' in params:
            audioid = int(params['audioid'])
            dashinfo = dashinfos['audio'][audioid]
        else:
            return [404, "text/plain", ""]
        
        url = ''
        urlList = [dashinfo['baseUrl']] + dashinfo.get('backupUrl', []) if 'backupUrl' in dashinfo and dashinfo['backupUrl'] else [dashinfo['baseUrl']]
        for url in urlList:
            if 'mcdn.bilivideo.cn' not in url:
                break
        if url == "":
            return [404, "text/plain", ""]
        
        header = self.header.copy()
        if 'range' in params:
            header['Range'] = params['range']
        
        r = requests.get(url, headers=header, stream=True)
        return [206, "application/octet-stream", r.content]

    def getDash(self, params, forceRefresh=False):
        aid = params['aid']
        cid = params['cid']
        
        qn = params.get('qn', '120')
        
        api_url = f'https://api.bilibili.com/x/player/playurl?avid={aid}&cid={cid}&qn={qn}&fnval=4048&fnver=0&fourk=1'
        
        if 'thread' in params:
            thread = params['thread']
        else:
            thread = 0
            
        header = self.header.copy()
        
        if 'cookies' in params:
            cookieDict = json.loads(params['cookies'])
        else:
            cookieDict = {}
        
        key = f'bilivdmpdcache_{aid}_{cid}_{qn}'
        
        if forceRefresh:
            self.delCache(key)
        else:
            data = self.getCache(key)
            if data:
                return data['content'], data['dashinfos'], data['type']

        cookies = cookieDict.copy()
        
        r = self.fetch(api_url, cookies=cookies, headers=header, timeout=5)
        data = json.loads(self.cleanText(r.text))
        
        if data['code'] != 0:
            return '', {}, ''
            
        if not 'dash' in data['data']:
            purl = data['data']['durl'][0]['url']
            try:
                expiresAt = int(re.search(r'deadline=(\d+)', purl).group(1)) - 60
            except:
                expiresAt = int(time.time()) + 600
            if int(thread) > 0:
                try:
                    self.fetch('http://127.0.0.1:7777')
                except:
                    self.fetch('http://127.0.0.1:9978/go')
                purl = f'http://127.0.0.1:7777?url={quote(purl)}&thread={thread}'
            self.setCache(key, {'content': purl, 'type': 'mp4', 'dashinfos':  data['data'], 'expiresAt': expiresAt})
            return purl,  data['data'], 'mp4'

        dashinfos = data['data']['dash']
        duration = dashinfos['duration']
        minBufferTime = dashinfos['minBufferTime']
        
        videoinfo = ''
        videoid = 0
        deadlineList = []
        
        selected_video = None
        for video in dashinfos['video']:
            if str(video.get('id', '')) == str(qn):
                selected_video = video
                break
        
        if not selected_video and len(dashinfos['video']) > 0:
            selected_video = dashinfos['video'][0]
        
        if selected_video:
            try:
                deadline = int(re.search(r'deadline=(\d+)', selected_video['baseUrl']).group(1))
            except:
                deadline = int(time.time()) + 600
            deadlineList.append(deadline)
            
            codecs = selected_video['codecs']
            bandwidth = selected_video['bandwidth']
            frameRate = selected_video['frameRate']
            height = selected_video['height']
            width = selected_video['width']
            void = selected_video['id']
            
            baseUrl = f'http://127.0.0.1:9978/proxy?do=py&type=media&cookies={quote(json.dumps(cookies))}&qn={qn}&aid={aid}&cid={cid}&videoid={videoid}'
            videoinfo = f"""      <Representation bandwidth="{bandwidth}" codecs="{codecs}" frameRate="{frameRate}" height="{height}" id="{void}" width="{width}">
        <BaseURL>{baseUrl}</BaseURL>
        <SegmentBase indexRange="{selected_video['SegmentBase']['indexRange']}">
        <Initialization range="{selected_video['SegmentBase']['Initialization']}"/>
        </SegmentBase>
      </Representation>"""
            videoid += 1
        
        audioinfo = ''
        audioid = 0
        for audio in dashinfos['audio']:
            try:
                deadline = int(re.search(r'deadline=(\d+)', audio['baseUrl']).group(1))
            except:
                deadline = int(time.time()) + 600
            deadlineList.append(deadline)
            bandwidth = audio['bandwidth']
            codecs = audio['codecs']
            aoid = audio['id']
            baseUrl = f'http://127.0.0.1:9978/proxy?do=py&type=media&cookies={quote(json.dumps(cookies))}&qn={qn}&aid={aid}&cid={cid}&audioid={audioid}'
            audioinfo = audioinfo + f"""      <Representation audioSamplingRate="44100" bandwidth="{bandwidth}" codecs="{codecs}" id="{aoid}">
        <BaseURL>{baseUrl}</BaseURL>
        <SegmentBase indexRange="{audio['SegmentBase']['indexRange']}">
        <Initialization range="{audio['SegmentBase']['Initialization']}"/>
        </SegmentBase>
      </Representation>\n"""
            audioid += 1
        
        mpd = f"""<?xml version="1.0" encoding="UTF-8"?>
<MPD xmlns="urn:mpeg:dash:schema:mpd:2011" profiles="urn:mpeg:dash:profile:isoff-on-demand:2011" type="static" mediaPresentationDuration="PT{duration}S" minBufferTime="PT{minBufferTime}S">
  <Period>
    <AdaptationSet mimeType="video/mp4" startWithSAP="1" scanType="progressive" segmentAlignment="true">
      {videoinfo}
    </AdaptationSet>
    <AdaptationSet mimeType="audio/mp4" startWithSAP="1" segmentAlignment="true" lang="und">
      {audioinfo.strip()}
    </AdaptationSet>
  </Period>
</MPD>"""
        
        expiresAt = min(deadlineList) - 60
        self.setCache(key, {'type': 'mpd', 'content': mpd.replace('&', '&amp;'), 'dashinfos': dashinfos, 'expiresAt': expiresAt})
        return mpd.replace('&', '&amp;'), dashinfos, 'mpd'

    def getCookie(self, cookie):
        if '{' in cookie and '}' in cookie:
            cookies = json.loads(cookie)
        else:
            cookies = dict([co.strip().split('=', 1) for co in cookie.strip(';').split(';')])
        bblogin = self.getCache('bblogin')
        if bblogin:
            imgKey = bblogin['imgKey']
            subKey = bblogin['subKey']
            return cookies, imgKey, subKey

        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"
        }
        r = requests.get("http://api.bilibili.com/x/web-interface/nav", cookies=cookies, headers=header, timeout=10)
        data = json.loads(r.text)
        code = data["code"]
        if code == 0:
            imgKey = data['data']['wbi_img']['img_url'].rsplit('/', 1)[1].split('.')[0]
            subKey = data['data']['wbi_img']['sub_url'].rsplit('/', 1)[1].split('.')[0]
            self.setCache('bblogin', {'imgKey': imgKey, 'subKey': subKey, 'expiresAt': int(time.time()) + 1200})
            return cookies, imgKey, subKey
        r = self.fetch("https://www.bilibili.com/", headers=header, timeout=5)
        cookies = r.cookies.get_dict()
        imgKey = ''
        subKey = ''
        return cookies, imgKey, subKey

    def getUserid(self, cookie):
        url = 'http://api.bilibili.com/x/space/myinfo'
        r = self.fetch(url, cookies=cookie, headers=self.header, timeout=5)
        data = json.loads(self.cleanText(r.text))
        if data['code'] == 0:
            return data['data']['mid']

    def removeHtmlTags(self, src):
        from re import sub, compile
        clean = compile('<.*?>')
        return sub(clean, '', src)

    def encWbi(self, params, imgKey, subKey):
        from hashlib import md5
        from functools import reduce
        from urllib.parse import urlencode
        if not imgKey or not subKey:
            return params
        mixinKeyEncTab = [46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52]
        orig = imgKey + subKey
        mixinKey = reduce(lambda s, i: s + orig[i], mixinKeyEncTab, '')[:32]
        params['wts'] = round(time.time())
        params = dict(sorted(params.items()))
        params = {
            k: ''.join(filter(lambda chr: chr not in "!'()*", str(v)))
            for k, v
            in params.items()
        }
        query = urlencode(params)
        params['w_rid'] = md5((query + mixinKey).encode()).hexdigest()
        return params