import re
import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

class CustomSyntaxExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {'debug': [False, 'Enable debug logging']}
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        md.preprocessors.register(CustomSyntaxPreprocessor(md, debug=self.getConfig('debug')), 'custom_syntax_pre', 200)

class CustomSyntaxPreprocessor(Preprocessor):
    def __init__(self, md, debug=False):
        super().__init__(md)
        self.debug = debug

    def run(self, lines):
        new_lines = []
        for line in lines:
            if self.debug:
                print(f"Preprocessor input line: {line}")

            # Handle highlighted text
            line = re.sub(r'==(.+?)==', r'<strong><span class="highlighted_text">\1</span></strong>', line)

            # Handle Q&A
            line = re.sub(r'<Q::(.+?)::(.+?)>', 
                r'<div class="question"><p>\1</p><button class="q_and_a_button" onclick="">Show Answer</button><p class="q_and_a_answer">\2</p></div>', 
                line)

            if self.debug:
                print(f"Preprocessor output line: {line}")

            new_lines.append(line)
        return new_lines

    def handle_properties(self, match):
        if self.debug:
            print(f"Handling properties for: {match.group(0)}")

        content = match.group(1)
        props = match.group(2)

        attributes = self.parse_properties(props)
        result = f'{content}<element-props {attributes}></element-props>'

        if self.debug:
            print(f"Result of handle_properties: {result}")

        return result

    def parse_properties(self, props):
        properties = {}
        for prop in props.split(','):
            key, value = prop.split(':')
            properties[key.strip()] = value.strip().strip('"')
        
        return ' '.join([f'{k}="{v}"' for k, v in properties.items()])

def finalize_post_processing_md(html):
    # This regex finds the element and its properties and merges them into one tag
    print("\nHTML: Before 1st sub: "+html)
    html = re.sub(r'(<(\w+))(>[^<]*<element-props (.*?)></element-props>)', r'\1 \4\3', html)
    print("\nHTML: Before 2nd sub: "+html)
    html = re.sub(r'<element-props (.*?)></element-props>', r'', html)  # Clean up any remaining <element-props>
    
    
    return html

if __name__ == "__main__":
    md = markdown.Markdown(extensions=[CustomSyntaxExtension(debug=True)])

    sample_text = """
## Difference between Living and Non living
---

| Living        | Non Living       |
| ------------- | ---------------- |
| Growth        | No Growth        |
| Reproduction  | No Reproduction  |
| Metabolism    | No Metabolism    |
| Consciousness | No Consciousness |

## Taxonomy
---
Taxonomy is the branch of science that deals with the identification, naming and classification of organisms. **Carolus Linnaeus** is the **father of taxonomy**

## Binomial Nomenclature
---
It is the scientific naming of organisms having two parts, The first part represents genus and the second part represents species. It was introduced by **Carolus Linnaeus**
#### Scientific names of some organisms:

| Organisms | Scientific Name     |
| --------- | ------------------- |
| Man       | *Homo sapien*       |
| Housefly  | *Musca domestica*   |
| Mango     | *Mangifera indica*  |
| Wheat     | *Triticum aestivum* |

### Rules of Scientific Naming
-  Scientific names are in latin
-  First should be genus and second name, species
-  There should be a gap between the genus and species
-  If printed, it is in italic, If handwritten it is seperately underlined

## Taxonomic Category
---

-  It is the classification of organisms into different taxons (Rank/Levels)

![Taxons](Taxons.svg)
- In taxonomic category, taxas are arranged from lower levels to higher levels called taxonomic hierarchy

### Taxonomic Category of Man and Housefly

| Taxon   | Man       | Housefly     |
| ------- | --------- | ------------ |
| Kingdom | Animalia  | Animalia<br> |
| Phylum  | chordata  | Antropoda    |
| Class   | Mammalia  | Insecta      |
| Order   | Primata   | Diptera      |
| Family  | Hominidae | Muscidae     |
| Genus   | Homo      | Musca        |
| Species | sapien    | domestica    |


"""

    html = md.convert(sample_text)
    print("Final HTML output:")
    print(html)

    # Post-processing to convert element properties to actual attributes
    html = finalize_post_processing_md(html)

    print("\nFinal HTML output after post-processing:")
    print(html)
