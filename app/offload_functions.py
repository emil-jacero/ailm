import urllib.request
import os
import re
import requests
from bs4 import BeautifulSoup
import uuid


class ImageObject:
    def __init__(self):
        self.build = None
        self.uuid = uuid.uuid4()
        self.name = None
        self.sha256 = None
        self.archive_path = None
        self.archive_filename = None
        self.file_suffix = None
        self.source_url = None


def download_image(image, archive_path):
    # v2: ImageObject
    url = image.source_url
    uuid_image_name = image.uuid

    # v2: Update archive_path & archive_filename
    image.archive_path = archive_path
    image.archive_filename = "{}.temp_img".format(uuid_image_name)

    print('Begin download [{}]'.format(url))
    # Define storage locations on the filesystem
    #file_destination = '{dest}tmp_images/'.format(dest=archive_path)
    temp_destination_file = '{dest}tmp_images/{img_name}'.format(dest=archive_path, img_name=image.archive_filename)
    try:
        urllib.request.urlretrieve(url, temp_destination_file)
    except Exception as e:
        raise e

    result = image
    return result


def get_latest_release(distro, release):
    # Instantiate ImageObject
    image = ImageObject()
    if distro == 'ubuntu':
        # Define URL & other variables (defines all because of clarity)
        url = 'https://cloud-images.ubuntu.com/releases/{rel}/'.format(rel=release, )
        hashfile_url = 'SHA256SUMS'
        image_hash = None
        image_name = None
        image_url = None
        latest_build = None
        image_suffix = None

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

        # v2: ImageObject
        image.name = image_name
        image.sha256 = image_hash
        image.source_url = image_url
        image.build = latest_build
        image.file_suffix = image_suffix

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

        # v2: ImageObject
        image.name = image_name
        image.sha256 = image_hash
        image.source_url = image_url
        image.build = latest_build
        image.file_suffix = image_suffix

    return image

def upload_to_glance(conn, image):
    """
    Receive openstacksdk connection and image object.
    Upload to glance
    :param conn: Openstacksdk connection object
    :param image:
    :return:
    """
    image_name = image.name
    image_filename = image.archive_path
    disk_format = "qcow2"
    #--property os_type=linux --property os_version="16.04" --property hw_firmware_type=bios
    conn.create_image()
    """
    name, filename=None,
            container=None,
            md5=None, sha256=None,
            disk_format=None, container_format=None,
            disable_vendor_agent=True,
            wait=False, timeout=3600,
            allow_duplicates=False, meta=None, volume=None, **kwargs):
    """

#latest_image = get_latest_release("ubuntu", "18.04")
#print(latest_image.source_url)
#download_image(latest_image, "/home/emil/Development/Project_ailo/images/")
