from embedia.layers.data_layer import DataLayer
from embedia.model_generator.project_options import ModelDataType

class SVC_layer(DataLayer):
        
    def __init__(self, model, layer, options=None, **kwargs):
        super().__init__(model, layer, options, **kwargs)
        self.struct_data_type = 'svc_layer_t'
    
    def functions_init(self):

        struct_type = self.struct_data_type
        name = self.name
    
        init_svc_layer = f'''
        {struct_type} init_{name}_data(void){{
        uint16_t nr_class = {self.layer.classes_.size};
        uint16_t nr_SV = {len(self.layer.support_)};
        uint16_t label[] = {'{' + ', '.join(map(str, self.layer.classes_)) + '}'};
        char * kernel_type = "{self.layer.kernel.lower()}";
        uint16_t degree = {self.layer.degree};
        float gamma = {self.layer.gamma};
        float  coef0 = {self.layer.coef0};
        float rho[] = {'{' + ', '.join(map(str, self.layer.intercept_)) + '}'};
        uint16_t nSV[] = {'{' + ', '.join(map(str, self.layer.n_support_)) + '}'};
        float SV[][{self.layer.n_features_in_}]] = {{'''
        for vector in self.layer.support_vectors_:
            init_svc_layer += f'        {{' + ', '.join(map(str, vector)) + '},\n'
        init_svc_layer += f'''        }};
        float dual_coef[][{self.layer.dual_coef_[:1].size}] = {{ '''
        for row in self.layer.dual_coef_:
            init_svc_layer += f'        {{' + ', '.join(map(str, row)) + '},\n'
        init_svc_layer += f'''        }};

        svc_layer_t layer = {{
                nr_class,
                nr_SV,
                kernel_type,
                degree,
                gamma,
                coef0,
                label,
                rho,
                nSV,
                SV,
                dual_coef
        }};
            return layer;
        }}
        '''
        return init_svc_layer
    
    def predict(self, input_name, output_name):
        return f'''svc_layer({self.name}_data, {input_name}, &{output_name});'''