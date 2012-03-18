__author__ = 'xxshutong'

class Utils:
    @staticmethod
    def generate_options(model_list):
        value_array = []
        label_array = []
        for model_obj in model_list:
            value_array.append(model_obj.id)
            label_array.append(model_obj.name)
        result = {'value':value_array, 'label':label_array}
        return result