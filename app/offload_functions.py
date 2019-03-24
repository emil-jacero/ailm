import urllib.request
import os
import re
import requests
from bs4 import BeautifulSoup


def download_image(url, destination, uuid):
    result = dict()
    print('Begin download [{}]'.format(url))
    #uuid_image_name = uuid.uuid4()  # Generate unique id and send to caller later
    uuid_image_name = uuid  # Get uuid from caller

    # Define storage locations on the filesystem
    file_destination = '{dest}tmp_images/'.format(dest=destination)
    temp_destination_file = '{temp_dest}{img_name}'.format(temp_dest=file_destination,
                                                                   img_name=uuid_image_name)
    try:
        urllib.request.urlretrieve(url, temp_destination_file)
    except Exception as e:
        raise e
    #result['uuid'] = '{}'.format(uuid_image_name)
    result['path'] = temp_destination_file
    return result


def get_latest_release(distro, release):
    result = dict()
    if distro == 'ubuntu':
        # Define URL & other variables (defines all because of clarity)
        url = 'https://cloud-images.ubuntu.com/releases/{rel}/'.format(rel=release, )
        hashfile_url = 'SHA256SUMS'
        image_hash = ""
        image_name = ""
        image_url = ""
        latest_build = ""
        image_suffix = ""

        # Retrieve the latest image url
        match_list = []  # Define match_list for later use
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        compile_string = 'release-'
        builds = soup.find_all(href=re.compile(compile_string))
        for build in builds:
            match_list.append(build.string.replace('/', ''))  # Remove forward slash in the strings
        # Sort Alphanumericly
        sorted_builds = sorted(match_list, key=lambda item: (int(item.partition(' ')[0])
                                                             if item[0].isdigit() else float('inf'), item))
        latest_build = sorted_builds[-1]  # It is nicer to set a variable that is the last in the list
        if release <= '16.04':
            # We want to send back the image name
            image_name = 'ubuntu-{release}-server-cloudimg-amd64-disk1.img'.format(release=release)
            # We also want to send back the url that was used
            image_url = '{url}{build}/ubuntu-{release}-server-cloudimg-amd64-disk1.img'.format(url=url,
                                                                                               build=latest_build,
                                                                                               release=release)
            image_suffix = 'img'
        elif release >= '18.04':
            # We want to send back the image name
            image_name = 'ubuntu-{release}-server-cloudimg-amd64.img'.format(release=release)
            # We also want to send back the url that was used
            image_url = '{url}{build}/ubuntu-{release}-server-cloudimg-amd64.img'.format(url=url,
                                                                                         build=latest_build,
                                                                                         release=release)
            image_suffix = 'img'

        # Get sha256 to compare with database
        page = requests.get('{url}{build}/{hashfile}'.format(url=url, build=latest_build, hashfile=hashfile_url))
        soup = BeautifulSoup(page.text, 'html.parser')
        hash_list = soup.decode().split("\n")
        hash_list.pop(-1)
        for hash in hash_list:
            search_string = '{}$'.format(image_name)
            if re.search(search_string, hash):
                image_hash = hash.split(' ')[0]

        result['name'] = image_name
        result['sha256'] = image_hash
        result['url'] = image_url
        result['build'] = latest_build
        result['suffix'] = image_suffix

    elif distro == 'centos':
        # Define URL & other variables (defines all because of clarity)
        url = 'http://cloud.centos.org/centos/{rel}/images/'.format(rel=release)
        hashfile_url = 'sha256sum.txt'
        image_name = ""
        image_hash = ""
        image_url = ""
        latest_build = ""

        # Retrieve the latest image url
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        builds = soup.find_all(href=re.compile('CentOS-[0-9]-x86_64-GenericCloud-[0-9]{4}.qcow2'))

        match_list = []
        for build in builds:
            pattern1 = re.compile(r'(CentOS-[0-9]-x86_64-GenericCloud-[0-9]{4}.qcow2c)|CentOS-[0-9]-x86_64-GenericCloud-[0-9]{4}.qcow2.xz')
            match_all_other_files = pattern1.match(build.contents[0])

            if match_all_other_files:
                continue
                #print('DELETE {}'.format(match_all_other_files.group(0)))
            else:
                match_list.append(build.contents[0])
        # Sort Alphanumericly
        sorted_builds = sorted(match_list, key=lambda item: (int(item.partition(' ')[0])
                                                            if item[0].isdigit() else float('inf'), item))
        # It is nicer to set a variable that is the last in the list
        latest_build = sorted_builds[-1].split('-')[4].replace('.qcow2', '')
        image_url = '{url}CentOS-{release}-x86_64-GenericCloud-{build}.qcow2'.format(url=url,
                                                                                     release=release,
                                                                                     build=latest_build)
        image_suffix = 'qcow2'
        # Get sha256 to compare with database
        page = requests.get('{url}{hashfile}'.format(url=url, hashfile=hashfile_url))
        soup = BeautifulSoup(page.text, 'html.parser')
        hash_list = soup.decode().split("\n")
        hash_list.pop(-1)
        for hash in hash_list:
            search_string = 'CentOS-{release}-x86_64-GenericCloud-{build}.qcow2$'.format(release=release, build=latest_build)
            if re.search(search_string, hash):
                image_hash = hash.split('  ')[0]
                image_name = hash.split('  ')[1]
        result['name'] = image_name
        result['sha256'] = image_hash
        result['url'] = image_url
        result['build'] = latest_build
        result['suffix'] = image_suffix

    return result