import yaml

from django.http import HttpResponse, FileResponse
from django.shortcuts import redirect, render

from rdmo.projects.exports import Export

class CffExport(Export):
    
    def render(self):
        cff_data = self.get_cff_data()
        cff_data = self.remove_none_values(cff_data)
        yaml_content = yaml.dump(cff_data)
        response = HttpResponse(yaml_content, content_type='text/plain')
        response['Content-Disposition'] = 'filename="CITATION.cff"'
        return response

    def get_cff_data(self) -> dict:
        return {
            'abstract': self.project.description,
            'authors': self.get_persons(self.project.member),
            'date-released': self.project.updated.strftime("%Y-%m-%d"),
            'cff-version': '1.2.0',
            'message': "If you use this software, please cite it using these metadata.",
            'contact': self.get_persons(self.project.owners),
            'title' : self.get_text('project/title'),
            'keywords': [text.value for text in self.get_values('project/research_field')],
            'license': self.get_software_license('smp/software-license'),
            'type': 'software',
            'identifiers': self.get_software_identifiers('smp/software-pid')
        }    

    def remove_none_values(self, data: dict) -> dict:
        return {k:v for k,v in data.items() if v}   

    def get_persons(self, members):
        persons = []
        for m in members:
            persons.append({
                'family-names': m.last_name,
                'given-names': m.first_name,
                'email': m.email,
            })
        return persons

    def get_software_identifiers(self, attribute: str): 

        IDENTIFIER = {
            'DOI': 'doi',
            'URL': 'url',
            'Software Heritage Identifier': 'swh',
            'Other': 'other',
            'Sonstige': 'other'
        }

        identifier_text = self.get_values(attribute)
        data = []
        for item in identifier_text:
            identifier_type = item.value[0:item.value.find(':')]
            identifier_value = item.value[item.value.find(':')+1:].strip()
            if identifier_type == "DOI":
                identifier_value = identifier_value.strip('https://doi.org/')
            
            data.append({
                'value': identifier_value,
                'type': IDENTIFIER[identifier_type]
            })
        return data
    
    def get_software_license(self, attribute: str):
        LICENSES = [
            'AGPL-3.0-only',
            'Apache-2.0',
            'BSD-3-Clause',
            'CDDL-1.0',
            'GPL-3.0-only',
            'LGPL-3.0-only',
            'MIT',
        ]

        licenses_text = self.get_values(attribute)
        data = [item.value for item in licenses_text if item.value in LICENSES]
        return data if len(data) > 1 else data[0]
