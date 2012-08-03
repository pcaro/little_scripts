#!/usr/bin/python
# -*- coding: utf-8 -*-
import ConfigParser
import sys
import logging
from optparse import OptionParser
from os.path import isfile
from string import letters
import StringIO


def write_sentence(title, operator, rules, actions, output):
    logging.debug(u'%s %s %s %s' % (title.decode('utf-8'), operator, str(rules), str(actions)))
    sieve_rules = filter(None,[rule(*r) for r in rules])
    sieve_actions = filter(None,[action(*a) for a in actions])

    if sieve_rules and sieve_actions:
        print >>output, '## %s ##' % title
        print >>output, 'if ',
        if len(sieve_rules) > 1:
            if operator == 'or':
                print >>output, 'anyof ('
            elif operator == 'and':
                print >>output, 'allof ('
        print >>output, ',\n'.join(sieve_rules)
        if len(sieve_rules) > 1:
            print >>output, ')'
        
        print >>output, '{ '
        print >>output, '\n;'.join(sieve_actions)
        print >>output, '}\n'
    else:
        logging.error(u'Saltamos "%s"' % title.decode('utf-8'))

def action(name, args):
    if name == 'transfer':
        # args example
        # in: .1620556498.directory/.INBOX.directory/.listas_internas.directory/yaco-informacion
        # out: INBOX.listas_internas.yaco-informacion
        start = args.find('INBOX')
        if start != -1:
            box = args[start:]
            box =  box.replace('.directory/.','.')
            box =  box.replace('.directory/','.')
        else:
            # IMBOX es requerido para las cuenas IMAP
            return None
        return 'fileinto "%s";\nstop;' % box
    else:
        logging.error('Action "%s" (%s) no processed  ' % (name, args))

def rule(field, func, contents):
    if func == 'contains':
        if field == 'List-Id':
            contents = contents.replace('@','.')
        if contents[0] == '<':
            contents = contents[1:]
        if contents[-1] == '>':
            contents = contents[:-1]
        return 'header :contains ["%s"] "%s"' % (field, contents)
    elif func == 'regexp':
        return 'header :regex ["%s"] "%s"' % (field, contents)
    elif field == '<size>':
        argument = ':over'
        if field == 'less-or-equal':
            argument = ':under'
        return 'size  %s "%s"' % (argument, contents)
    else:
        logging.error('Rule "%s" %s "%s" no processed  ' % (field, func, contents))

def main(file_name, options):
    p = ConfigParser.ConfigParser()
    p.read(file_name)
    
    output = StringIO.StringIO()
    print >>output, 'require ["fileinto", "regex"];'

    num_filters = p.getint('General', 'filters')
    logging.debug('Numero de filtros %i' % num_filters)
    for i in range(num_filters):
        section_name = 'Filter #%s' % i
        title = p.get(section_name,'ToolbarName')
        actions_number = p.getint(section_name,'actions')
        rules_number = p.getint(section_name,'rules')
        operator = p.get(section_name,'operator')
        rules = []
        for r in range(rules_number):
            field = p.get(section_name,'field%s' % letters[r])
            func = p.get(section_name,'func%s' % letters[r])
            contents = p.get(section_name,'contents%s' % letters[r])
            rules.append((field,func,contents))
        actions = []
        for a in range(actions_number):
            name = p.get(section_name,'action-name-%i' % a)
            args = p.get(section_name,'action-args-%i' % a)
            actions.append((name, args))
        write_sentence(title, operator, rules, actions, output)
    print >>sys.stdout, output.getvalue()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    parser = OptionParser(usage="Uso: %prog [options] filtros.ini > filtros.sieve")
    parser.add_option('-d', '--debug',
                  dest='debug',
                  help='Modo depuracion',
                  default=False,
                  action='store_true')
    (options, args) = parser.parse_args()

    if len(args) !=  1:
        parser.error("Numero incorrecto de parametros")

    if options.debug:
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

    filename = args[0]
    if not isfile(filename):
        parser.error("No existe el fichero '%s'" % filename)

    main(filename, options)
