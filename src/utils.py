import os, logging, unicodedata, re
from pprint import pformat

logger = logging.getLogger('root.' + __name__)


def log_multiline(log_function, log_text, title=None, prefix=''):
    """Function to log multi-line text
    """
    logger.debug('log_multiline(%s, %s, %s, %s) called', log_function, repr(log_text), repr(title), repr(prefix))

    if type(log_text) == str:
        logger.debug('log_text is type str')
        log_list = log_text.splitlines()
    elif type(log_text) == list and type(log_text[0]) == str:
        logger.debug('log_text is type list with first element of type text')
        log_list = log_text
    else:
        logger.debug('log_text is type ' + type(log_text).__name__)
        log_list = pformat(log_text).splitlines()

    log_function(prefix + '=' * 80)
    if title:
        log_function(prefix + title)
        log_function(prefix + '-' * 80)

    for line in log_list:
        log_function(prefix + line)

    log_function(prefix + '=' * 80)


def unicode_to_ascii(instring):
    """Convert unicode to char string if required and strip any leading/trailing whitespaces
    ToDO: Investigate whether we can just change the encoding of the DOM tree
    """
    result = instring
    if type(result) == unicode:
        result = unicodedata.normalize('NFKD', result).encode('ascii','ignore').strip(""" "'\n\t""")
    return result


def find_files(root_dir, filename_pattern='.*', case_insensitive = True):
    """
    List files matching a specified pattern (regex) anywhere under a root directory

    :param root_dir:
        Root directory to search within.

    :param filename_pattern:
        RegEx string for finding files.

    :param case_insensitive:
        Flag specifying whether name matching should be case insensitive.

    :return:
        List containing absolute pathnames of found files or empty list if none found.
    """
    if case_insensitive:
        file_regex = re.compile(filename_pattern, re.IGNORECASE)
    else:
        file_regex = re.compile(filename_pattern)

    filename_list = []

    for root, _dirs, files in os.walk(root_dir):
        for file_path in sorted(files):
            file_path = os.path.abspath(os.path.join(root, file_path))
            m = re.search(file_regex, file_path)
            if m:
                filename_list.append(file_path)

    return filename_list

