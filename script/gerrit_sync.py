#!/usr/bin/python3
# -*- coding: utf-8 -*-
# import yaml
import shutil
import sys
import os
import subprocess
import fnmatch
import xml.dom.minidom
import sh

#import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET
#Python code to illustrate parsing of XML files
# importing the required modules
import csv
import requests
import xml.etree.ElementTree as ET

from subprocess import call
from distutils.dir_util import copy_tree, remove_tree
import re
from jinja2 import Environment, FileSystemLoader

repo_bin = "/home/DIGITAL/yangkang/user_bin/repo"


# dict save repo projects info


def repo(args):
    args[:0] = [repo_bin]
    stderr = ""
    if args[-1] == '':
        del (args[-1])
    print(args)
    r = subprocess.check_output(args, encoding='UTF-8')
    # r = subprocess.check_output(['/home/DIGITAL/yangkang/user_bin/repo', 'init', '-u', 'git@github.com:YangKangSky/gerrit_sync_sz_uk.git', '-m', 'sz.xml', '-b', 'master'], shell=False)
    print('repo:r is %s' % r)
    return r


def repo_init(url, manifest, revision, args):
    args[:0] = ['init', '-u', url, '-m', manifest, '-b', revision]
    print('repo_init:args is %s' % args)
    r = repo(args)
    return r


def repo_sync(project, args):
    if project == '':
        args[:0] = ['sync']
    else:
        args[:0] = ['sync', project]
    print('repo_sync:args is %s' % args)
    r = repo(args)
    return r


# get project list, repo_list(['-p'])
def repo_list(args):
    args[:0] = ['list']
    print('repo_list:args is %s' % args)
    r = repo(args)
    return r


def print_dict(dict):
    for key, value in dict.items():
        print('keyitem:' + key)
        for single in value:
            print(single.__str__())


def print_rows(rows):
    for keyitem in rows:
        print(keyitem[0].__str__() + ':')
        for subitem in keyitem:
            print('--------' + subitem.__str__())


def saveDictToXLS(dict, filename):
    # specifying the fields for csv file
    #header = ['project', 'local', 'remote', 'remotename', 'branch', 'version', 'last_version']
    header = ['project',  'remote',  'branch']
    rows_num, cols_num = (15, 3)
    rows = [[0] * cols_num] * rows_num
    tmp_row = []
    index=0
    rows = []
    for keyItem in dict:
        print('keyItem is:' + keyItem)
        tmp_row.append(keyItem)
        #tmp_row.extend(dict[keyItem])
        #rows[index] = tmp_row
        index += 1
        tmp_row += dict[keyItem]
        print('tmp_row is: ' + tmp_row.__str__())
        print('dict is: ' + dict[keyItem].__str__())
        rows.append(tmp_row)
        tmp_row = []
    print("rows 0 is:")
    #print_rows(rows)
    print(rows)

    # header = ['Project', 'sz_branch', 'sz_version', 'sz_last_version', 'uk_branch', 'uk_version', 'uk_last_version']
    # data = [['sk-realtek-rtl8852bs', 'master', '75ad6fcd1f95092d156a0b58fc325536daad7c87',
    #          '26712e74d93b45f677c43df54c31698f3fd5385e', 'master', '75ad6fcd1f95092d156a0b58fc325536daad7c87',
    #          '26712e74d93b45f677c43df54c31698f3fd5385e']]
    # with open(filename, 'w') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(header)
    #     writer.writerows(rows)

    #df = pd.DataFrame(rows, columns=header)
    df = pd.DataFrame(data=rows, columns=header)
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='welcome', index=False)
    writer.save()


    # writing to csv file
    # with open('countries.csv', 'w', encoding='UTF8') as f:
    #     # creating a csv dict writer object
    #     writer = csv.DictWriter(filename, fieldnames=field_names)
    #
    #     # writing headers (field names)
    #     writer.writeheader()
    #     rows = [['sk-realtek-rtl8852bs', 'master', '75ad6fcd1f95092d156a0b58fc325536daad7c87', '26712e74d93b45f677c43df54c31698f3fd5385e', 'master', '75ad6fcd1f95092d156a0b58fc325536daad7c87', '26712e74d93b45f677c43df54c31698f3fd5385e']]
    #     print("rows is:")
    #     print(rows)
    #     test = [['a', 1]]
    #     # writing data rows
    #     writer.writerows(rows)


def fill_item_to_dict(sub_dict_project, dict_project):
    tmp_dict = dict()
    new_key = 0
    for keySub in sub_dict_project:
        if keySub == 'Mount path':
            new_key = sub_dict_project[keySub]
            # generate empty list
            tmp_dict.setdefault(new_key, [0, 0])
        elif keySub == 'Manifest revision':
            #tmp_dict[new_key].append(sub_dict_project[keySub])
            tmp_dict[new_key][0] = sub_dict_project[keySub]
        elif keySub == "Current revision":
            #tmp_dict[new_key].append(sub_dict_project[keySub])
            tmp_dict[new_key][1] = sub_dict_project[keySub]
    print('tmp_dict is ' + tmp_dict.__str__())
    for key in dict_project:
        if len(tmp_dict) > 0:
            if key == list(tmp_dict)[0]:
                dict_project[key][3] = tmp_dict[new_key][0]
                dict_project[key][4] = tmp_dict[new_key][1]
                #print(tmp_dict[key][0] + '---' + tmp_dict[key][1])


    return 0

def parsexml_to_dict(dict_project, xmlname):
    print("parsexml_to_dict xml:" + xmlname)
    # use the parse() function to load and parse an XML file
    # create element tree object
    tree = ET.parse(xmlname)

    # get root element
    root = tree.getroot()
    print('root.tag:' + root.tag)
    for child in root:
        print("child.tag={0}, child.attrib={1}".format(child.tag, child.attrib))
        if child.tag == "project":
            print("child.name={0}, child.remote={1}".format(child.get('name'), child.get('remote')))

            dict_project_match_key = child.get('path')
            if dict_project_match_key is not None:
                print("dict_project_match_key:"+dict_project_match_key)
            if dict_project_match_key is None:
                dict_project_match_key = child.get('name')

            print('dict_project[dict_project_match_key]:')
            #print(dict_project)
            print(dict_project_match_key, type(dict_project_match_key))
            dict_project[dict_project_match_key][5] = child.get('revision')


def checkUpdate(dict_project,repoType):
    return 0




def repo_download(workDir, repoURL, manifest,branch):
    if not os.path.exists(workDir):
        os.mkdir(workDir)
    print('repo_sz_dir is %s' % workDir)
    #backup current dir
    tmpDir = os.getcwd()
    print('curdir is %s' % tmpDir)

    # cd workDir
    os.chdir(workDir)
    #download code by repo
    #repo_init(repoURL, manifest, branch, [''])
    repo_sync("", ['-j8'])
    repo_list(['-p'])

    #return to last default dir
    os.chdir(tmpDir)


def repo_prj_info_get(repo_sz_dir,project_dict_Type):

    new_key = 0
    #backup current dir
    tmpDir = os.getcwd()
    print('curdir is %s' % tmpDir)

    os.chdir(repo_sz_dir)
    output = subprocess.check_output('repo forall -p -c git remote -v', shell=True, encoding='UTF-8')
    print('output is \n' + output.__str__())
    result = {}
    for row in output.split('\n'):
        print('row is : ' + row.__str__())
        if bool(re.search(r"^project.*/$", row)):
            print('123')
            if new_key == 0:
                key = row.split(' ')[1][:-1]
                #check the key is invalid
                if key in project_dict_Type.keys():
                    new_key = 1
        else:
            if new_key == 1:
                #value = re.split(r"[ ]+", row)[1]
                value = row.split()[1]
                remote_name = row.split()[0]
                #print('value:' + value+',row:'+row)
                #tmp_dict.setdefault(key, []).append(value)
                project_dict_Type[key][0] = repo_sz_dir + '/' +key
                project_dict_Type[key][1] = value
                project_dict_Type[key][2] = remote_name

                new_key = 0

    #return to last default dir
    os.chdir(tmpDir)
    return project_dict_Type

# output: projectlist
def repo_list_get(projectaDir, projectbDir):
    projectlist_t = []
    projectlist_a = []
    projectlist_b = []

    #backup current dir
    tmpDir = os.getcwd()
    print('curdir is %s' % tmpDir)

    os.chdir(projectaDir)
    cmd = subprocess.Popen('repo list -p', shell=True, stdout=subprocess.PIPE,  encoding='UTF-8')
    for line in cmd.stdout:
        print(line, type(line))
        # remove \n
        projectlist_a.append(line.strip())
        # if "Wget" in line:
        #     print(line)
    print("projectlist_a is " + projectlist_a.__str__())


    os.chdir(projectbDir)
    cmd = subprocess.Popen('repo list -p', shell=True, stdout=subprocess.PIPE,  encoding='UTF-8')
    for line in cmd.stdout:
        print(line, type(line))
        projectlist_b.append(line.strip())
        # if "Wget" in line:
        #     print(line)
    print("projectlist_b is " + projectlist_b.__str__())

    # combined project_a and project_b
    projectlist_t = sorted(list(set(projectlist_a + projectlist_b)))
    print('projectlist_t in:' + projectlist_t.__str__())

    #return to last default dir
    os.chdir(tmpDir)
    return projectlist_t

def project_dict_init(project_dict, projectlist):
    for line in projectlist:
        print("line is " + line.__str__())
        project_dict[line] = ['0', '0', '0', '0', '0', '0']
    print(project_dict)
    print("##################")
    for key, value in project_dict.items():
        print(key,type(key))
        print(key + ' : ' + value.__str__())
    print("##################")
    return project_dict

def project_dict_fill(project_dict,project_repo_dir):
    #backup current dir
    tmpDir = os.getcwd()
    print('curdir is %s' % tmpDir)

    os.chdir(project_repo_dir)
    output = subprocess.check_output('repo info', shell=True, encoding='UTF-8')
    print('output is \n' + output.__str__())
    #define empty dict
    result = {}
    for row in output.split('\n'):
        print('row is : ' + row.__str__())
        if ':' in row:
            key, value = row.split(':')
            # print('key :' + key + '      value:' + value)
            # print('key :' + key + '      value:' + value)
            if key == 'Project' or key == 'Mount path':
                result[key.strip(' .')] = os.path.basename(value.strip())
            elif key == 'Manifest revision' or key == 'Current revision':
                result[key.strip(' .')] = value.strip()
        if '-----' in row:
            print("result is:" + result.__str__())
            # file project dict
            fill_item_to_dict(result, project_dict)
            result.clear()

    # return to last default dir
    os.chdir(tmpDir)
    return project_dict

def project_dict_fill_lastversion(project_dict,project_repo_dir,repoType):
    #backup current dir
    tmpDir = os.getcwd()
    print('curdir is %s' % tmpDir)

    # handle sz xml
    manifest_backup_dir = project_repo_dir + '/.repo/manifests/backup'
    print('manifest_backup_dir is ' + manifest_backup_dir)
    backupfile = []
    if repoType == 'SZ':
        match_pattern = '*_sz.xml'
    elif repoType == 'UK':
        match_pattern = '*_uk.xml'
    else:
        print("Invalid type")
    for file in os.listdir(manifest_backup_dir):
        if fnmatch.fnmatch(file, match_pattern):
            backupfile.append(file)

    print(backupfile)
    backupfile.sort()
    print(backupfile[0])
    backupfile.sort(reverse=True)
    print(backupfile[0])

    latest_backup = backupfile[0]
    #parse manifest
    parsexml_to_dict(project_dict, manifest_backup_dir + '/' + latest_backup)

    # return to last default dir
    os.chdir(tmpDir)
    return project_dict

def project_dict_diff(project_dict):
    #remote_path | branch |sz_version | sz_last_version |
    temp = {}
    for key, value in project_dict.items():
        version = value[4]
        last_version = value[5]
        if version != last_version:
            temp[key] = value
    return temp

def project_patch_generate(project_dict,patch_dir, repo_dir):

    #enpty dict, just return
    if len(project_dict) == 0:
        return 0
    #backup current dir
    tmpDir = os.getcwd()
    print('curdir is %s' % tmpDir)
    os.chdir(repo_dir)

    # http://amoffat.github.io/sh/
    #git format-path a...b -o
    for key, value in project_dict.items():
        module_patch_dir = patch_dir + '/' + key
        git_dir = repo_dir + '/' + key
        print('git_dir:'+git_dir)
        git = sh.git.bake(_cwd=git_dir)
        git.status()

        hash_version = value[4]
        hash_last_version = value[5]

        if hash_version != hash_last_version:
            if not os.path.exists(module_patch_dir):
                os.makedirs(module_patch_dir)
            git("format-patch", hash_last_version + '...' + hash_version, '-o', module_patch_dir)
        module_patch_list = next(os.walk(module_patch_dir))[2]
        if len(module_patch_list):
            value.append(module_patch_list)
        else:
            value.append("none")
    # return to last default dir
    os.chdir(tmpDir)


def apply_patch_list(project_dict_update_a, patch_b_dir):
    #enpty dict, just return
    if len(project_dict_update_a) == 0:
        return 0
    #backup current dir
    tmpDir = os.getcwd()
    print('curdir is %s' % tmpDir)

    patch_dir_list = os.listdir(patch_b_dir)
    if len(patch_dir_list) == 0:
        print('empty patch dir:' + patch_b_dir)
        return 0
    print('project_dict_update_a:' + project_dict_update_a.__str__())


    for key in patch_dir_list:
        #patch_dir_list.extend(dir)
        dir_to_patch = project_dict_update_a[key][0]
        remote = project_dict_update_a[key][1]
        remote_name = project_dict_update_a[key][2]
        branch = project_dict_update_a[key][3]

        patch_location = patch_b_dir + '/' + key
        print('dir_to_patch:' + dir_to_patch.__str__())
        print('patch_location:' + patch_location.__str__())
        git = sh.git.bake(_cwd=dir_to_patch)
        patch_list = os.listdir(patch_location)
        for patch in patch_list:
            patch_full_name = patch_location + '/' + patch
            #git am --3way --ignore-space-change
            git_param = '--3way --ignore-space-change'
            print('git am ' + patch_full_name)
            git("am", patch_full_name)
            #git("push", remote_name, 'HEAD:refs/for/'+branch)

    print('patch_dir_list:' + patch_dir_list.__str__())

    # return to last default dir
    os.chdir(tmpDir)

def generate_prj_list_info_show(project_dict_SZ):
    tmp_dict = dict()
    tmp_list = []
    for key, value in project_dict_SZ.items():
        tmp_dict[key] = [value[1], value[3]]
    return tmp_dict
    return 0

def generate_prj_upgrade_info_show(project_dict_SZ):
    tmp_dict = dict()
    tmp_list = []
    for key, value in project_dict_SZ.items():
        if len(value) == 7:
            tmp_dict[key] = [value[4], value[5], value[6]]
        else:
            tmp_dict[key] = [value[4], value[5]]
    return tmp_dict
    return 0


def saveDictToHtml(sz_project_list_info_show, xls_filename):
    df = pd.read_excel(xls_filename, engine='openpyxl')
    #df['project'] = df['project'].astype(str)
    #df['remote'] = df['remote'].astype(str)
    #df['branch'] = df['branch'].astype(str)
    data = df.to_dict('records')

    results = {}
    results.update({'strategy_name': 'straight',
                    'start_time': '2020-01-01',
                    'end_time': '2021-06-01',
                    'money': 20000,
                    'items': data})
    print("html result is {0}".format(results))

    env = Environment(loader=FileSystemLoader(os.path.dirname(xls_filename)))
    template = env.get_template('./report_template.html')

    with open(os.path.dirname(xls_filename)+"/out.html", 'w+') as f:
        out = template.render(strategy_name=results['strategy_name'],
                              start_time=results['start_time'],
                              end_time=results['end_time'],
                              money=results['money'],
                              items=results['items'])
        #out = template.render(items=results['items'])

        f.write(out)
        f.close()



    return 0


# Hint: to automatically insert a Change-Id, install the hook:
# gitdir=$(git rev-parse --git-dir); scp -p -P 29418 kang.yang@dev.caldero.com:hooks/commit-msg ${gitdir}/hooks/
# git commit --amend --no-edit

def checkAndInsertChangeID():
    return 0

def main(argv=None):
    '''
    sync the code between repo A and Repo B
    '''

    if argv is None:
        argv = sys.argv

    # get current dir
    rootdir = os.getcwd()
    print('curdir is %s' % rootdir)


    workdir = rootdir + '/workdir'

    #prepare work dir
    # repo_sz_dir = curdir.join('repo_SZ')
    repo_sz_dir = workdir + '/repo_SZ'
    if not os.path.exists(repo_sz_dir):
        os.mkdir(repo_sz_dir)

    repo_uk_dir = workdir + '/repo_UK'
    if not os.path.exists(repo_uk_dir):
        os.mkdir(repo_uk_dir)

    SZ_REPO_URI='git@github.com:YangKangSky/gerrit_sync_sz_uk.git'
    SZ_REPO_XML='sz.xml'
    SZ_REPO_BRANCH='master'
    repo_download(repo_sz_dir, SZ_REPO_URI, SZ_REPO_XML, SZ_REPO_BRANCH)


    UK_REPO_URI='git@github.com:YangKangSky/gerrit_sync_sz_uk.git'
    UK_REPO_XML='uk.xml'
    UK_REPO_BRANCH='master'
    repo_download(repo_uk_dir, UK_REPO_URI, UK_REPO_XML, UK_REPO_BRANCH)

    #create empty dict
    #   key              value
    # +==========+===========+============+=================+===========+===========+
    # | Project1 |           |            |                 |           |           |
    # +----------+-----------+------------+-----------------+-----------+-----------+
    # | Project2 |           |            |                 |           |           |
    # +----------+-----------+------------+-----------------+-----------+-----------+

    # +==========+=============+=========+==========+===============+
    # | Project  | local_path  | remote_path |remote_name|  branch |  version |  last_version |
    # +==========+=============+=========+==========+===============+
    # | Project1 |             |         |          |               |
    # +----------+-------------+---------+----------+---------------+
    # | Project2 |             |         |          |               |
    # +----------+-------------+---------+----------+---------------+

    # {Project,[ remote_path，branch, version, last_version  ] }

    projectlist = []

    #generate project list as the first column
    projectlist = repo_list_get(repo_sz_dir, repo_uk_dir)


    # +==========+=============+=========+==========+===============+
    # | Project1 |             |         |          |               |
    # +----------+-------------+---------+----------+---------------+
    # | Project2 |             |         |          |               |
    # +----------+-------------+---------+----------+---------------+
    project_dict_SZ = dict()
    project_dict_SZ = project_dict_init(project_dict_SZ, projectlist)

    project_dict_UK = dict()
    project_dict_UK = project_dict_init(project_dict_UK, projectlist)

    #fill remote_path from repo info
    project_dict_SZ = repo_prj_info_get(repo_sz_dir, project_dict_SZ)

    project_dict_UK = repo_prj_info_get(repo_uk_dir, project_dict_UK)

    print('projectInfoDict_SZ:' + project_dict_SZ.__str__())
    print('projectInfoDict_UK:' + project_dict_UK.__str__())


    # refer to https://stackoverflow.com/questions/16175192/command-output-parsing-in-python
    #fill  branch and current  version
    project_dict_SZ = project_dict_fill(project_dict_SZ, repo_sz_dir)
    project_dict_UK = project_dict_fill(project_dict_UK, repo_uk_dir)


    #fill last version
    project_dict_SZ = project_dict_fill_lastversion(project_dict_SZ, repo_sz_dir, 'SZ')
    project_dict_UK = project_dict_fill_lastversion(project_dict_UK, repo_uk_dir, 'UK')


    print("project_dict_SZ is {0}".format(project_dict_SZ))

    #dict for only project which has upgrade
    project_dict_update_SZ = project_dict_diff(project_dict_SZ)
    project_dict_update_UK = project_dict_diff(project_dict_UK)

    print_dict(project_dict_update_SZ)
    print_dict(project_dict_update_UK)
    #project_dict = project_dict_update

    #prepare work dir
    # repo_sz_dir = curdir.join('repo_SZ')
    patch_sz_dir = workdir + '/patch_SZ'

    if os.path.exists(patch_sz_dir):
        shutil.rmtree(patch_sz_dir)

    os.mkdir(patch_sz_dir)

    patch_uk_dir = workdir + '/patch_UK'
    if not os.path.exists(patch_uk_dir):
        os.mkdir(patch_uk_dir)


    # +==========+=============+=========+==========+===============+===============+
    # | Project  | local_path  | remote_path |remote_name|  branch |  version |  last_version |
    # +==========+=============+=========+==========+===============+===============+
    # | Project1 |             |         |          |               |               |
    # +----------+-------------+---------+----------+---------------+---------------+
    # | Project2 |             |         |          |               |               |
    # +----------+-------------+---------+----------+---------------+---------------+
    project_dict_update_SZ = project_patch_generate(project_dict_update_SZ, patch_sz_dir, repo_sz_dir)
    project_dict_update_UK = project_patch_generate(project_dict_update_UK, patch_uk_dir, repo_uk_dir)



    #SZ的patch合入到UK对应的仓库上;UK的patch合入到SZ对应的patch上
    #we must to make sure that the uk repo do not have any update,so we can sync the patch automatic

    apply_patch_list(project_dict_UK, patch_sz_dir)
    apply_patch_list(project_dict_SZ, patch_uk_dir)

    print('project_dict_SZ' + project_dict_SZ.__str__())

    #define 4 different dict for show
    sz_project_list_info_show = generate_prj_list_info_show(project_dict_SZ)
    uk_project_list_info_show = generate_prj_list_info_show(project_dict_UK)

    print('sz_project_list_info_show' + sz_project_list_info_show.__str__())

    sz_project_upgrade_info_show = generate_prj_upgrade_info_show(project_dict_SZ)
    uk_project_upgrade_info_show = generate_prj_upgrade_info_show(project_dict_UK)

    print('sz_project_upgrade_info_show' + sz_project_upgrade_info_show.__str__())
    print_dict(sz_project_upgrade_info_show)

    print('workdir is ' + workdir)
    #suffix must be .xlsx
    saveDictToXLS(sz_project_list_info_show, workdir + '/excel_sz.xlsx')
    saveDictToXLS(uk_project_list_info_show, workdir + '/excel_uk.xlsx')

    saveDictToHtml(sz_project_list_info_show, workdir + '/excel_sz.xlsx')



    checkAndInsertChangeID()
    print("--------------------")


    # render dataframe as html
    #html = df.to_html()


    #df = pd.DataFrame(project_dict)
    #
    # # save dataframe
    #df.to_csv('site.csv')

    # git app patch
    #git am --3way --ignore-space-change


    return 0


if __name__ == "__main__":
    sys.exit(main())
