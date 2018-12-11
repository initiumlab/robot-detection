from __future__ import print_function

import sys, os.path, codecs, re
import six

robot_useragents = [
        'appie',
        'architext',
        'jeeves',
        'bjaaland',
        'contentmatch',
        'ferret',
        'googlebot',
        'google\-sitemaps',
        'gulliver',
        'virus[_+ ]detector',		# Must be before harvest
        'harvest',
        'htdig',
        'linkwalker',
        'lilina',
        'lycos[_+ ]',
        'moget',
        'muscatferret',
        'myweb',
        'nomad',
        'scooter',
        'slurp',
        '^voyager\/',
        'weblayers',
        # Common robots (Not in robot file)
        'antibot',
        'bruinbot',
        'digout4u',
        'echo!',
        'fast\-webcrawler',
        'ia_archiver\-web\.archive\.org', # Must be before ia_archiver to avoid confusion with alexa
        'ia_archiver',
        'jennybot',
        'mercator',
        'netcraft',
        'msnbot\-media',
        'msnbot',
        'petersnews',
        'relevantnoise\.com',
        'unlost_web_crawler',
        'voila',
        'webbase',
        'webcollage',
        'cfetch',
        'zyborg',	# Must be before wisenut 
        'wisenutbot'

        # Less common robots (In robot file)
        'getbot',
        'geturl',
        'sogou',
        'inspectorwww',
        'irobot',
        'javabee',
        'jbot',
        'jcrawler',
        'linkidator',
        'linkscan',
        'mwdsearch',
        'ndspider',
        'openfind',
        'perlcrawler',
        'phantom',
        'phpdig',
        'python',
        'robbie',
        'robi',
        'robocrawl',
        'robofox',
        'robozilla',
        'roverbot',
        'rules',
        'search\-info',
        'simbot',
        'site\-valet',
        'sitetech',
        'skymob',
        'slcrawler',
        'smartspider',
        'snooper',
        'solbot',
        'speedy',
        'spider[_+ ]monkey',
        'spiderbot',
        'spiderline',
        'spiderman',
        'spiderview',
        'tlspider',
        'w3index',
        'w3m2',
        'wallpaper',
        'wanderer',
        'wapspIRLider',
        'webbandit',
        'webcatcher',
        'webfetcher',
        'webfoot',
        'webinator',
        'weblinker',
        'webmirror',
        'webquest',
        'webreader',
        'webreaper',
        'webspider',
        'webwalk',
        'webwalker',
        'webwatch',
        # Other robots reported by users
        'baiduspider',
        'bloglines',
        'blogpulse',
        'blogsearch',
        'blogshares',
        'bookmark\-manager',
        'checkweb_link_validator',
        'converamultimediacrawler',
        'converacrawler',
        'cscrawler',
        'deepindex',
        'dulance',
        'dumbot',
        'enteprise',
        'facebook',
        'favicon',
        'feedburner',
        'feedfetcher\-google',
        'feedflow',
        'feedster',
        'feedsky',
        'feedvalidator',
        'htmlparser',
        'libcrawl',
        'linkbot',
        'metager\-linkchecker',	# Must be before linkchecker
        'linkchecker',
        'microsoft[_+ ]url[_+ ]control',
        'misterbot',
        'mj12bot',
        'mojeekbot',
        'msiecrawler',
        'opentaggerbot',
        'openwebspider',
        'oracle_ultra_search',
        'orbiter',
        'yodaobot',
        'qihoobot',
        'peerbot',
        'pyquery',
        'sohu\-search',
        'sohu',
        'twiceler',
        'w3c\-checklink',
        'w3c[_+ ]css[_+ ]validator[_+ ]jfouffa',
        'w3c_validator',
        'webdup',
        'webfilter',
        'webindexer',
        'webminer',
        'yacy',
        'yahoo\-blogs',
        'yahoo\-verticalcrawler',
        'yahoofeedseeker',
        'yahooseeker\-testing',
        'yahooseeker',
        'yahoo\-mmcrawler',
        'yahoo!_mindset',
        # Other id that are 99% of robots
        'wget',
        'libwww',
        'java\/[0-9]'   # put at end to avoid false positive

        # Generic robot
        'robot',
        'checker',
        'crawl',
        'discovery',
        'hunter',
        'scanner',
        'spider',
        'sucker',
        'bot[\s_+:,\.\;\/\\\-]',
        '[\s_+:,\.\;\/\\\-]bot',
        'no_user_agent',

        # manually added
        'whatsapp',
        'linebot',
        'telegram',
        'jike',
        ]

robot_useragents = [re.compile(x) for x in robot_useragents]

def is_robot(user_agent):
    if not isinstance(user_agent, six.string_types):
        raise TypeError
    if len(user_agent) == 0:
        raise ValueError

    try:
        # See if any one matches
        return any(robot_ua.search(user_agent.lower()) for robot_ua in robot_useragents)
    except UnicodeDecodeError:
        # Unicode error, robot_useragents is unicode strings. user_agent might have malformed bytes, so try looking at boring ascii
        return any(robot_ua.search(user_agent.lower().encode('ascii', 'ignore')) for robot_ua in robot_useragents)



def _parse_db_export(filename):
    assert os.path.isfile(filename)

    lines = codecs.open(filename, encoding="latin1").readlines()

    exclude_ua = set()
    for line in lines:
        if line.startswith("robot-exclusion-useragent:"):
            line = line.strip()
            dont_care, ua = line.split(":", 1)
            ua = ua.strip()
            if ' or ' in ua:
                uas = ua.split(" or ")
                # remove quotes
                uas = [x[1:-1] if (x[0] in ['"', "'"] and x[-1] in ['"', "'"]) else x for x in uas]
            else:
                uas = [ua]
            for ua in uas:
                # don't include nonsense stuff
                if ua.lower() not in ['', '*', 'n/a', 'none', 'yes', 'no', "due to a deficiency in java it's not currently possible to set the user-agent."]:
                    exclude_ua.add(ua)

    if robot_useragents != exclude_ua:
        print("robot_detection is out of date. Here's the new robot_useragents variable:")
        print(exclude_ua)
    else:
        print("No changes, robot_detection is up to date")


if __name__ == '__main__' and len(sys.argv) == 2:
    _parse_db_export(sys.argv[1])

