
rec = f'''def get_{name}(self, **args):
        """
        Get {name} parameters
        :param name: name
        :param uuid: uuid 
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.get{name}(**args)

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']['{returned}']
            return result

        except Fault as error:
            result['error'] = error
            return result'''