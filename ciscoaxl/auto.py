import xml.etree.cElementTree as ET
import os
import pathlib
import re

cucm_version = '12.5'

cwd = os.path.dirname(os.path.abspath(__file__))
xsd = pathlib.PurePosixPath(f"{cwd}/schema/{cucm_version}/AXLSoap.xsd")

def camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def create_def_get(name, returned):
    rec = f'''def {camel_to_snake(name)}(self, **args):
            """
            {camel_to_snake(name)} parameters
            :param name: name
            :param uuid: uuid 
            :return: result dictionary
            """
            result = {{
                'success': False,
                'response': '',
                'error': '',
            }}
            try:
                resp = self.client.get{name[3:]}(**args)

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['{returned}']
                return result

            except Fault as error:
                result['error'] = error
                return result
            '''

    with open('get.txt', 'a') as filehandle:  
        filehandle.write(rec)
        filehandle.write('\n')
        filehandle.close()

tree = ET.ElementTree(file=xsd)
root = tree.getroot()

def parse_get(child):
    for sub in child:
        if 'complexContent' in sub.tag:
            for a in sub:
                if 'extension' in a.tag:
                    for b in a:
                        if 'sequence' in b.tag:
                            for c in b:
                                if 'element' in c.tag:
                                    for d in c:
                                        if 'complexType' in d.tag:
                                            for e in d:
                                                if 'sequence' in e.tag:
                                                    for f in e:
                                                        if 'element' in f.tag:
                                                            create_def_get(child.attrib['name'].split('Res')[0], f.attrib['name'])

def create_params(reqs):
    res = ''
    for each in reqs:
        res = res+':param '+each.attrib['name']+': '+each.attrib['name']+'\n'
    return res+':return: result dictionary'


def create_def_remove(child, reqs):
    params = create_params(reqs)
    rec = f'''def {camel_to_snake(child)}(self, **args):
    """
    {camel_to_snake(child)} parameters
    :param uuid: uuid
    {params}
    """
    result = {{
        'success': False,
        'response': '',
        'error': '',
    }}
    try:
        resp = self.client.remove{child[6:]}(**args)

        if resp['return']:
            result['success'] = True
            result['response'] = resp['return']
        return result

    except Fault as error:
        result['error'] = error
        return result
    '''

    with open('remove.txt', 'a') as filehandle:  
        filehandle.write(rec)
        filehandle.write('\n')
        filehandle.close()

def parse_remove(child):
    for sub in child:
        if 'sequence' in sub.tag:
            for a in sub:
                if 'choice' in a.tag:
                    for b in a:
                        if 'sequence' in b.tag:
                            create_def_remove(child.attrib['name'].split('Req')[0], b)
                    #         for c in b:
                    #             print(c.attrib['name'])
                    #     #print(b.attrib['name'])
                    # #print(a.attrib['base'])
                    # if a.attrib['base'] is 'axlapi:StandardResponse':
                    #     print(child.attrib['name'].split('Res')[0])
                    # else:
                    #     for b in a:
                    #         if 'sequence' in b.tag:
                    #             for c in b:
                    #                 if 'element' in c.tag:
                    #                     for d in c:
                    #                         if 'complexType' in d.tag:
                    #                             for e in d:
                    #                                 if 'sequence' in e.tag:
                    #                                     for f in e:
                    #                                         print(child.attrib['name'].split('Res')[0])
                    #                                         print(f.attrib)
                    #                                         #if 'element' in f.tag:
                    #                                             #create_def_do_complex(camel_to_snake(child.attrib['name'].split('Res')[0]), f.attrib['name'])
                    #                         elif 'simpleType' in d.tag:
                    #                             for e in d:
                    #                                 print(child.attrib['name'].split('Res')[0])
                    #                                 print(e.attrib)
                    #                                 #create_def_do_simple(camel_to_snake(child.attrib['name'].split('Res')[0]))

for child in root:
    if 'complexType' in child.tag:
        # if 'Get' in child.attrib['name'][:3] and 'Res' in child.attrib['name']:
        #     parse_get(child)
        if 'Remove' in child.attrib['name'][:6] and 'Req' in child.attrib['name']:
            parse_remove(child)

