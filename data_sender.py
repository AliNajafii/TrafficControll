"""
This module is for sending test data to the server.
it reads json files 
(all_nodes.json,owners.json,roads.json,tollStations.json)
it uses multi threading approach to send data faster.
"""
import re
import json
import sys
import os
import requests
import threading


POSITION_REGEX = r'\d+\.\d*'
log_file = open('log.txt','a',encoding='utf-8')

def make_lat_long(positions:list):
    """
    it gives list of positions and 
    return in the format of [(lat,long),()]
    if empty list given it returns empty list.
    """
    res = []
    #positions list length number should be even
    # because we have lat and long points as a single point
    if len(positions) % 2 == 1 :
        raise ValueError('some positions are missing.') 
    if not positions:
        return positions
    step = 0
    for _ in range(int(len(positions)/2)):
        lat,lng = positions[step:step+2] 
        res.append((lat,lng))
        step += 2
    return res

def extract_lat_long(data:str):
    """
    extracting lat and long from
    a string data and returns
    list of points dictionary.
    it returns in a format like [
        {
            "lat":...,
            "lng":..,
        }
        ,...
        ]
    """
    positions = re.findall(POSITION_REGEX,data)
    points = make_lat_long(positions)
    finall_results = []
    for lat,lng in points:
        finall_results.append(
            {
                'lat':lat,
                'lng':lng
            }
        )
    return finall_results

def data_formatter(data_list:list):
    """
    standardize the format of data
    and return cleaned data.
    for example extract lat and long.
    """
    for data in data_list:
        if data.get('geom'):
            raw_data = data.pop('geom')
            route_set = extract_lat_long(raw_data)
            data['route_set'] = route_set
        elif data.get('location'):
            raw_data = data.pop('location')
            point = extract_lat_long(raw_data)[0]
            data['lat'] = point['lat']
            data['lng'] = point['lng']
    
    return data_list
        
        



def file_handler(file_num:int,format='json'):
    """
    return list of files
    and their number of workers 
    and other info like url
    is stored in a dictionary.
    ex: [
        {
            'resource':file1,
            'workers': 5,
            'url': exampl.com
            'method' : post        
        }
        ,...
        ] 
    this means file1has 4 
    worker threads.and the content of
    this file should be send to url with method.
    """ 
    file_path = None
    files = []
    for n in range(file_num):
        workers_num = None
        url = None
        method=None
        file_info = {}
        while True:
            file_path = input(f'Enter {format} file {n+1} path:\t')
            try:
                workers_num = int(input('number of workers for this file:\t'))
                raw_inp = input('should sento url with method(seprate with , ex:home.com,post):\t')
                url,method = raw_inp.split(',')
                file_info['workers'] = workers_num
                file_info['url'] = url.strip()
                file_info['method'] = method.strip()
            except TypeError as e:
                print('Type Error:',*e.args)
                continue
            if not os.path.isfile(file_path):
                print('it\'s not a file')
                continue
            if file_path.endswith(f'.{format}'):
                break
            print('it\'s not f{json} file')
        file = open(file_path,'r',encoding='utf-8')
        file_info['resource'] = file
        files.append(file_info)
    return files

def http_request(url:str,data,method='post',**headers):
    """
    this function is the main logic
    of sending request to the server
    """
    print('prepare to send...')
    headers.update({
        'Content-Type': 'application/json'
    })
    data = data_formatter(data)
    data = json.dumps(data)
    print('-----------------------',file=log_file)
    print(data,file=log_file)
    
    response = requests.post(url,data=data,headers=headers)
    print(response.status_code)
    print(response.reason)
    num = threading.current_thread().name
    html_file = open(f'responselogs_{num}.html','w',encoding='utf-8')
    print(response.text,file=html_file)
    print('-----------------------',file=log_file,end='\n\n\n')


def thread_handler(url,file,method='post',thread_num=4,**request_headers):
    """
    this function handels the work
    between threads and run them 
    for each resource.
    """
    threads = []
    raw_data = file.read()
    data = json.loads(raw_data)
    if isinstance(data,list):
        #data contains multiple items
        print(file.name,'-->',len(data),'items to send')
        chunk = int(len(data)/thread_num)
        offset=0 #start of data set for each worker
        limit = chunk #end of data set for each worker
        for i in range(thread_num):
            #parttioning data for each worker
            worker_data = data[offset:limit]
            threads.append(
                threading.Thread(
                    target=http_request,
                    args=(url,worker_data,method),
                    kwargs=request_headers
                    )
                )
            offset = limit
            limit += chunk + 1

        for th in threads:
            th.start()
        for th in threads:
            th.join()
        #file content sent successfully
        print(file.name,'sent successfully.')
        
            
    else :
        #data is just one item
        print(file.name,'--> one item to send')
        worker = threading.Thread(
            target=http_request,
            args=(url,data,method),
            kwargs=request_headers
        )
        worker.start()
        worker.join()
    
    file.close()

def resource_handler(resources):
    """
    excute workers for each resource
    """
    for file_info in resources:
        thread_handler(
            file_info['url'],
            file_info['resource'],
            file_info['method'],
            file_info['workers']
        )

def get_defualt_files():
    """
    returns defualt files
    insted of adding manually.
    it returns files like file_handler
    function.
    """
    defualt_setting = {
        "all_nodes.json":{
            'workers':4,
            "url" : 'http://127.0.0.1:8000/system/traffics/',
            "method":"post"
        },
        "owners.json":{
            'workers':1,
            "url" : 'http://127.0.0.1:8000/system/owners/',
            "method":"post"
        },
        "roads.json":{
            'workers':4,
            "url" : 'http://127.0.0.1:8000/geo/roads/',
            "method":"post"
        },
        "tollStations.json":{
            'workers':1,
            "url" : 'http://127.0.0.1:8000/geo/toll-stations/',
            "method":"post"
        }
    }
    files = []
    for f_name in defualt_setting:
        file = open(f_name,'r',encoding='utf-8')
        files.append(
           {
               'resource':file,
               'method':defualt_setting[f_name]['method'],
               'url':defualt_setting[f_name]['url'],
               'workers':defualt_setting[f_name]['workers'],
           }
        )
    return files

def main():
    user_inpu = input('Do you want to process default files?(y/n): ')
    if user_inpu in ('yes','y'):
        files = get_defualt_files()
    else :
        files_num = int(input('How many json files?:\t'))
        files = file_handler(files_num)
    rep = input('execute?(y/n)')
    if rep in ('yes','y'):
        resource_handler(files)
    print('all done.')
    log_file.close()

if __name__ == "__main__":
    main()

    
    