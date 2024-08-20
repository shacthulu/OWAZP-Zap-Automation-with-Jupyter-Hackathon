import json
import time
from pprint import pprint
from zapv2 import ZAPv2

# Replace values in braces

target = 'https://public-firing-range.appspot.com'
apiKey = '{apikey}'
spiderTimeout = 120 # seconds

zap = ZAPv2(apikey=apiKey, proxies={'http': 'http://{IP}:{Port}', 'https': 'http://{IP}:{Port}'})

def spiderScan(target, zap):
    print('Spidering target {}'.format(target))
    scanID = zap.spider.scan(target)
    timeout = time.time() + spiderTimeout
    while int(zap.spider.status(scanID)) < 100:
        if time.time() > timeout:
            break
        print('Spider progress %: {}'.format(zap.spider.status(scanID)))
        time.sleep(1)
    print('Spider has completed!')
    print('\n'.join(map(str, zap.spider.results(scanID))))
    
def ajaxSpiderScan(target, zap):
    print('AJAX Spidering target {}'.format(target))
    scanID = zap.ajaxSpider.scan(target)
    timeout = time.time() + spiderTimeout
    while zap.ajaxSpider.status == 'running':
        if time.time() > timeout:
            break
        print('AJAX Spider progress: {}'.format(zap.ajaxSpider.status))
        time.sleep(1)
    print('AJAX Spider has completed!')
    print(zap.ajaxSpider.results(start=0, count=10))
    
def activeScan(target, zap):
    print('Active Scanning target {}'.format(target))
    scanID = zap.ascan.scan(target)
    while int(zap.ascan.status(scanID)) < 100:
        print('Scan progress %: {}'.format(zap.ascan.status(scanID)))
        time.sleep(5)

    print('Active Scan completed')
    print('Hosts: {}'.format(', '.join(zap.core.hosts)))


def getTotalAlerts(target, zap):
    st = 0
    pg = 5000
    alert_dict = []
    alert_count = 0
    all_info_alerts = []
    all_low_alerts = []
    all_medium_alerts = []
    all_high_alerts = []
    alerts = zap.alert.alerts(baseurl=target, start=st, count=pg)
    blacklist = [1,2]
    print("in totes")
    while len(alerts) > 0:
        print("in loop")
        print('Reading ' + str(pg) + ' alerts from ' + str(st))
        alert_count += len(alerts)
        for alert in alerts:
            plugin_id = alert.get('pluginId')
            if plugin_id in blacklist:
                continue
            if alert.get('risk') == 'High':
                if(all_high_alerts.count(alert.get('alert')) == 0):
                    pprint(alert)
                    all_high_alerts.append(alert)
                    print(len(all_high_alerts))
                continue
            if alert.get('risk') == 'Medium':
                # Trigger any relevant postprocessing
                continue
            if alert.get('risk') == 'Low':
                # Trigger any relevant postprocessing
                continue
            if alert.get('risk') == 'Informational':
                continue
        st += pg
        alerts = zap.alert.alerts(start=st, count=pg)
    print('Total number of alerts: ' + str(alert_count))
    
def getAllAlerts(target, zap):
    print('Alerts: ')
    pprint(zap.core.alerts(baseurl=target))
    
def getAlertSummary(target, zap):
    print('Alerts Summary')
    pprint(zap.core.alerts_summary(baseurl=target))

spiderScan(target, zap)
#ajaxSpiderScan(target, zap)
activeScan(target,zap)
getTotalAlerts(target, zap)
# getAlertSummary(target, zap)
