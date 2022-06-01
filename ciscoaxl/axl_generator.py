import xml.etree.cElementTree as ET  # nosec
import os
import pathlib
import re

cucm_version = "12.5"

cwd = os.path.dirname(os.path.abspath(__file__))
xsd = pathlib.PurePosixPath(f"{cwd}/schema/{cucm_version}/AXLSoap.xsd")


def camel_to_snake(name):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


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

    with open("get123.txt", "a") as filehandle:
        filehandle.write(rec)
        filehandle.write("\n")


tree = ET.ElementTree(file=xsd)
root = tree.getroot()


def parse_get(child):
    for sub in child:
        if "complexContent" in sub.tag:
            for a in sub:
                if "extension" in a.tag:
                    for b in a:
                        if "sequence" in b.tag:
                            for c in b:
                                if "element" in c.tag:
                                    for d in c:
                                        if "complexType" in d.tag:
                                            for e in d:
                                                if "sequence" in e.tag:
                                                    for f in e:
                                                        if "element" in f.tag:
                                                            create_def_get(
                                                                child.attrib[
                                                                    "name"
                                                                ].split("Res")[0],
                                                                f.attrib["name"],
                                                            )


def create_params(reqs):
    res = ""
    for each in reqs:
        res = res + ":param " + each.attrib["name"] + ": " + each.attrib["name"] + "\n"
    return res + ":return: result list of dictionaries"


def create_params_new(reqs):
    res = ""
    for each in reqs:
        res = res + ":param " + each + ": " + each + "\n\t"
    return res + ":return: API Response message"


def create_def_list(name, params, returning):
    # print(name)
    # print(reqs)
    # params = create_params(reqs)
    rec = f'''def {camel_to_snake(name)}(self, name=''):
        """
        {camel_to_snake(name)} parameters
        :param uuid: uuid
        {params}
        """
        result = {{
            'success': False,
            'response': '',
            'error': '',
        }}
        try:
            resp = self.client.list{name[4:]}(
                {{'name': '%'+name}}, returnedTags={returning}
            )

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']['{get_res_from_req(name)}']
            return result

        except Fault as error:
            result['error'] = error
            return result
        '''
    with open("list.txt", "a") as filehandle:
        filehandle.write(rec)
        filehandle.write("\n")


def find_return(child):
    for sub in child:
        if "complexContent" in sub.tag:
            for a in sub:
                if "extension" in a.tag:
                    for b in a:
                        if "sequence" in b.tag:
                            for c in b:
                                if "element" in c.tag:
                                    for d in c:
                                        if "complexType" in d.tag:
                                            for e in d:
                                                if "sequence" in e.tag:
                                                    for f in e:
                                                        if "element" in f.tag:
                                                            # print(f.attrib['name'])
                                                            return f.attrib["name"]
                                        # create_def_list(child.attrib['name'].split('Req')[0], c)


def get_res_from_req(req):
    for child in root:
        if "complexType" in child.tag:
            # if 'Get' in child.attrib['name'][:3] and 'Res' in child.attrib['name']:
            #     parse_get(child)
            # if 'Remove' in child.attrib['name'][:6] and 'Req' in child.attrib['name']:
            #     parse_remove(child)

            if req in child.attrib["name"][:-3] and "Res" in child.attrib["name"]:
                return find_return(child)


def create_def_update(child, reqs):
    params = create_params_new(reqs)
    rec = f'''def {camel_to_snake(child)}(self, **args):
    """
    {camel_to_snake(child)} parameters
    {params}
    """
    result = {{
        'success': False,
        'response': '',
        'error': '',
    }}
    try:
        resp = self.client.update{child[6:]}(**args)

        if resp['return']:
            result['success'] = True
            result['response'] = resp['return']
        return result

    except Fault as error:
        result['error'] = error
        return result
    '''
    with open("update.txt", "a") as filehandle:
        filehandle.write(rec)
        filehandle.write("\n")


def create_def_add(child, reqs):
    params = create_params_new(reqs)
    rec = f'''def {camel_to_snake(child)}(self, **args):
    """
    {camel_to_snake(child)} parameters
    {params}
    """
    result = {{
        'success': False,
        'response': '',
        'error': '',
    }}
    try:
        resp = self.client.add{child[3:]}(**args)

        if resp['return']:
            result['success'] = True
            result['response'] = resp['return']
        return result

    except Fault as error:
        result['error'] = error
        return result
    '''

    with open("add.txt", "a") as filehandle:
        filehandle.write(rec)
        filehandle.write("\n")


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

    with open("remove.txt", "a") as filehandle:
        filehandle.write(rec)
        filehandle.write("\n")


def get_res(name):
    returned = {}
    for child in root:
        if "complexType" in child.tag:
            if "L" + name[4:] in child.attrib["name"]:
                for sub in child:
                    if "sequence" in sub.tag:
                        for a in sub:
                            if "element" in a.tag:
                                returned[a.attrib["name"]] = ""
    return returned


def get_add_params(name):
    returned = []
    for child in root:
        if "complexType" in child.tag:
            if name in child.attrib["name"]:
                for sub in child:
                    if "sequence" in sub.tag:
                        for a in sub:
                            if "element" in a.tag:
                                returned.append(a.attrib["name"])
    return returned

    # print(child.attrib)
    # and 'L'+name[4:] in child.attrib:
    # print(child)
    # for sub in child:
    #     print(sub)
    #     if sub.attrib['name'] is 'L'+name[4:]:
    #         print(sub)


def parse_list(child):
    # print(child.attrib['name'].split('Req')[0])
    params = ""
    req_params = ""
    for sub in child:
        if "sequence" in sub.tag:
            for a in sub:
                if "element" in a.tag:
                    for b in a:
                        if "complexType" in b.tag:
                            for c in b:
                                if "sequence" in c.tag:
                                    for d in c:
                                        if "element" in d.tag:
                                            # print(d.attrib['name'])
                                            # for each in d:
                                            #     print(each)
                                            params = (
                                                params
                                                + ":param "
                                                + d.attrib["name"]
                                                + ": "
                                                + d.attrib["name"]
                                                + "\n\t\t"
                                            )
    returning = get_res(child.attrib["name"].split("Req")[0])
    create_def_list(child.attrib["name"].split("Req")[0], params.strip(), returning)
    # print(child.attrib['name'].split('Req')[0],'\n',res)
    # return res+':return: result list of dictionaries'
    # create_def_list(child.attrib['name'].split('Req')[0], res)
    # if 'element' in d.tag:

    # print(d.attrib['name'])
    # print(e.attrib['name'])
    # print(d)
    # print(c.attrib['name'])
    # create_def_remove(child.attrib['name'].split('Req')[0], b)


def parse_add(child):
    for sub in child:
        if "complexContent" in sub.tag:
            for a in sub:
                if "extension" in a.tag:
                    for b in a:
                        if "sequence" in b.tag:
                            for c in b:
                                if "element" in c.tag:
                                    elem_type = c.attrib["type"].split("axlapi:")[1]
                                    # elem_name = c.attrib['name']
                                    add_params = get_add_params(elem_type)
                                    create_def_add(
                                        child.attrib["name"].split("Req")[0], add_params
                                    )


def parse_update(child):
    update_params = []
    for sub in child:
        if "complexContent" in sub.tag:
            for a in sub:
                if "extension" in a.tag:
                    for b in a:
                        if "sequence" in b.tag:
                            for c in b:
                                if "element" in c.tag:
                                    print(c.attrib["name"])
                                    # elem_type = c.attrib['type'].split('axlapi:')[1]
                                    # elem_name = c.attrib['name']
                                    update_params.append(c.attrib["name"])
    create_def_update(child.attrib["name"].split("Req")[0], update_params)


def parse_remove(child):
    for sub in child:
        if "sequence" in sub.tag:
            for a in sub:
                if "choice" in a.tag:
                    for b in a:
                        if "sequence" in b.tag:
                            create_def_remove(child.attrib["name"].split("Req")[0], b)
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
    if "complexType" in child.tag:
        if "Get" in child.attrib["name"][:3] and "Res" in child.attrib["name"]:
            parse_get(child)
        # if 'Remove' in child.attrib['name'][:6] and 'Req' in child.attrib['name']:
        #     parse_remove(child)
        # if 'List' in child.attrib['name'][:4] and 'Req' in child.attrib['name']:
        #     parse_list(child)
        # if 'Add' in child.attrib['name'][:3] and 'Req' in child.attrib['name']:
        #     parse_add(child)
        # if 'Update' in child.attrib['name'][:6] and 'Req' in child.attrib['name']:
        #     parse_update(child)
