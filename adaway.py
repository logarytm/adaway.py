#!/usr/bin/env python
import argparse
import sys
import urllib2
import os, os.path
import re
import shutil

backup_hosts_file = 'hosts.orig'
default_host_sources = [
    'http://adaway.org/hosts.txt',
    'http://winhelp2002.mvps.org/hosts.txt']

class HostsEntry:
    def __init__(self, ip, domain):
        self.ip = ip
        self.domain = domain

    @staticmethod
    def parse(row):
        row = row.strip()
        ip, domain = re.split(r'[\t ]+', row)
        return HostsEntry(ip, domain)

    def stringify(self):
        return "%s\t%s" % (self.ip, self.domain)

def download_hosts_file(url):
    response = urllib2.urlopen(url)
    return response.read()

def get_default_hosts_file():
    if os.name == 'nt':
        return 'C:\\Windows\\system32\\drivers\\etc\\hosts'
    else:
        return '/etc/hosts'

def split_lines(s):
    return re.split(r'\r?\n', s)

def read_file(filename):
    return open(filename).read()

def debug(msg):
    print('debug: %s' % msg)

def info(msg):
    print(msg)

def error(msg):
    sys.stderr.write('error: %s\n' % msg)
    sys.stderr.write()

def main(args):
    if args.dump_default_sources:
        for source in default_host_sources:
            print(source)
        return 0

    if args.sources_file:
        if not os.path.isfile(args.sources_file):
            error('%s does not exist or is not a file' % args.sources_file)
            return 1
        host_sources = split_lines(read_file(args.sources_file))
    else:
        host_sources = default_host_sources

    if os.path.exists(backup_hosts_file):
        debug('hosts.orig file already exists, not copying')
    else:
        info('copying hosts file %s to %s' % (args.hosts_file, backup_hosts_file))
        shutil.copy(args.hosts_file, backup_hosts_file)

    out = ['# --BEGIN: original hosts file --', read_file(backup_hosts_file), '# --END: original hosts file --']

    for source in host_sources:
        if source.strip() == '' or source[0] == '#':
            continue
        info('downloading hosts file %s' % source)
        data = download_hosts_file(source)
        out.append('# -- BEGIN: %s --' % source)
        debug('merging %s' % source)
        rows = split_lines(data)
        for row in rows:
            if row.strip() == '' or '#' in row:
                continue
            entry = HostsEntry.parse(row)
            entry.ip = args .target_ip
            out.append(entry.stringify())
        debug('%s successfully merged' % source)
        out.append('# -- END: %s --' % source)

    merged = os.linesep.join(out)
    outfile = open(args.hosts_file, 'w')
    outfile.write(merged)
    outfile.close()
    info('wrote hosts file to %s' % args.hosts_file)
    info('\nPlease note that every change you do to %s may be\noverwritten, edit %s and run adaway instead.' %
            (args.hosts_file, os.path.realpath(backup_hosts_file)))

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target-ip', dest='target_ip',
            default='127.0.0.1')
    parser.add_argument('-o', '--hosts-file', dest='hosts_file',
            default=get_default_hosts_file())
    parser.add_argument('-d', '--dump-default-sources',
            dest='dump_default_sources', default=False, action='store_true')
    parser.add_argument('-l', '--load-sources',
            dest='sources_file', default=None)
    args = parser.parse_args()

    sys.exit(main(args))
else:
    raise Exception, 'This file cannot be imported. It\'s not a module.'
