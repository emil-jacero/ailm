import urllib.request
import os
import re
import uuid
import requests
from bs4 import BeautifulSoup



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


def download_image(url):
    result = dict()
    print('Begin download [{}]'.format(url))
    uuid_image_name = uuid.uuid4()  # Generate unique id and send to caller later

    # Define storage locations on the filesystem
    file_destination = '{dest}tmp_images/'.format(dest=root_path)
    temp_destination_file = '{temp_dest}{img_name}'.format(temp_dest=file_destination,
                                                                   img_name=uuid_image_name)
    try:
        urllib.request.urlretrieve(url, temp_destination_file, reporthook)
    except Exception as e:
        raise e
    result['uuid'] = '{}'.format(uuid_image_name)
    result['path'] = temp_destination_file
    return result


def update_image(conn, distro, release):
    image_dict = dict()
    distro = distro
    release = release
    image_md5 = ""
    image_sha1 = ""
    image_sha256 = ""

    # Check if there is a new image and downloading
    latest_release = get_latest_release(conn, distro, release)
    compare = DatabaseFunctions.compare_img(conn, latest_release['sha256'])
    # Define variables from the scan function
    image_name = latest_release['name']
    image_sha256 = latest_release['sha256']
    image_url = latest_release['url']
    image_build = latest_release['build']
    image_suffix = latest_release['suffix']

    if compare:
        print('Image exist [NAME: {}]'.format(compare))
    else:
        print('Image not found for [{} - {}]'.format(distro, release))
        # Downloading image into temp dir
        file = download_image(image_url)
        image_path = file['path']
        image_uuid = file['uuid']

        # Moving image to final storage
        print('')
        print('Moving image to final location')
        source_file = '{path}tmp_images/{uuid}'.format(path=image_path, uuid=image_uuid)
        source_file = image_path
        dest_file = '{path}{distro}/{uuid}'.format(path=root_path, distro=distro, uuid=image_uuid)
        os.rename(source_file, dest_file)

        # Updating database
        print('Updating database')

        image_dict['distro'] = distro
        image_dict['release'] = release
        image_dict['build'] = image_build
        image_dict['uuid'] = image_uuid
        image_dict['name'] = image_name
        # Handle empty MD5 string
        if image_md5:
            image_dict['md5'] = image_md5
        else:
            image_dict['md5'] = ""
        # Handle empty SHA1 string
        if image_sha1:
            image_dict['sha1'] = image_sha1
        else:
            image_dict['sha1'] = ""
        # Handle empty SHA256 string
        if image_sha256:
            image_dict['sha256'] = image_sha256
        else:
            image_dict['sha256'] = ""
        image_dict['file'] = dest_file
        image_dict['url'] = image_url
        image_dict['suffix'] = image_suffix
        DatabaseFunctions.post_new_image(conn, image_dict)