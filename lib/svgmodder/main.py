import os
import xml.etree.ElementTree as etree
import pprint,json
ROOT = "C:/Users/jrabd/OneDrive/Documents/PYTHON_PROJECTS/School-Notes/data"

# Specify the desired directory pattern
DIAGRAMS_PATH_PATTERN = 'chapters\\diagrams\\'

special_color_configs = {
    "jjthomsoncathodediscovery.svg":{
    # BG, FILL COLOR, BORDER COLOR, ARROW COLOR, TEXT COLOR
    "light": {
        "initial_colors": ["#1e1e1e", "#2d2d2d", "#4fc3f7", "#4fc3f7", "#ffffff", "#3a3f5a", "#ccfdff", "rgb(204, 253, 255)", "rgb(255, 255, 255)","rgb(216, 216, 216)"],
        "target_colors": ["#1e1e1e", "#b0c4de", "#5a9bd5", "#5a9bd5", "#333333", "#b0c4de", "#333333", "#333333", "#333333","rgb(180, 180, 180)"],
        
    },
    "dark": {
        "initial_colors": ["#1e1e1e", "#2d2d2d", "#4fc3f7", "#ffffff", "#d0e3f5","rgb(51, 51, 51)","rgb(186, 186, 186)"],
        "target_colors": ["#1e1e1e", "#3a3f5a", "#5a9bd5", "#ffffff", "#1e1e1e","#FFFFFF","rgb(100, 100, 100)"],
    }
}
}

color_configs = {
    # BG, FILL COLOR, BORDER COLOR, ARROW COLOR, TEXT COLOR
    "light": {
        "initial_colors": ["#1e1e1e", "#2d2d2d", "#4fc3f7", "#4fc3f7", "#ffffff", "#3a3f5a", "#ccfdff", "rgb(204, 253, 255)", "rgb(255, 255, 255)","rgb(216, 216, 216)"],
        "target_colors": ["#d8eaf7", "#b0c4de", "#5a9bd5", "#5a9bd5", "#333333", "#b0c4de", "#333333", "#333333", "#333333","rgb(180, 180, 180)"]
    },
    "dark": {
        "initial_colors": ["#1e1e1e", "#2d2d2d", "#4fc3f7", "#ffffff", "#d0e3f5"],
        "target_colors": ["#1e1e1e", "#3a3f5a", "#5a9bd5", "#ffffff", "#1e1e1e"],
    }
}
gathered_colors = {
    "light": {},
    "dark": {}
}
def special_style_edits(element,style_property,style_value):
    if style_property == 'stroke':
        if element.tag in ["{http://www.w3.org/2000/svg}path","{http://www.w3.org/2000/svg}rect"]:
            if style_value == "rgb(0, 0, 0)":
                style_value = "rgb(171, 171, 171)"
    return style_property,style_value
class InjectMode:
    @staticmethod
    def create_light_mode_version(svg, svg_data, initial_colors, target_colors):
        print("Inject Method: Create Light Mode Version of Dark Diagrams")
        root = etree.fromstring(svg_data)
  
        for element in root.iter():
            if 'fill' in element.attrib:
                print("Found element: "+element.tag)
                fill_color = element.attrib['fill'].lower()
                if fill_color in initial_colors:
                    target_color = target_colors[initial_colors.index(fill_color)]
                    print(f"Changing fill color from {fill_color} to {target_color} in {etree.tostring(element)}")
                    element.attrib['fill'] = target_color
            if 'style' in element.attrib:

                    styles = element.attrib['style'].split(';')
                    new_styles = []
                    for style in styles:
                
                        if ':' in style:
                            style_property, style_value = style.split(':')
                            style_property = style_property.strip()
                            style_value = style_value.strip().lower()
                            if any([style_property == 'color',style_property == 'fill']) and (style_value.strip().lower() in initial_colors):
                                new_value = target_colors[initial_colors.index(style_value)]
                                new_styles.append(f'{style_property}: {new_value}')

                                print(f"Changed style {style_property} from {style_value} to {new_value} in element {element.tag}")
                            else:
                                prop,val = special_style_edits(element,style_property,style_value)
                                new_styles.append('%s: %s' %(prop,val))
                        else:
                            new_styles.append(style)
                    element.attrib['style'] = '; '.join(new_styles)
            if 'data-drawio-colors' in element.attrib:

                    styles = element.attrib['data-drawio-colors'].split(';')
                    new_styles = []
                    for style in styles:
                        if ':' in style:
                            style_property, style_value = style.split(':')
                            style_property = style_property.strip()
                            style_value = style_value.strip().lower()
                            if style_property == 'color' and style_value in initial_colors:
                                new_value = target_colors[initial_colors.index(style_value)]
                                new_styles.append(f'{style_property}: {new_value}')
                                print(f"Changed style color from {style_value} to {new_value} in element {element.tag}")
                            else:
                                new_styles.append(style)
                        else:
                            new_styles.append(style)
                    element.attrib['style'] = '; '.join(new_styles)

        svg_light_mode_data = etree.tostring(root).decode("utf-8")
        if not svg.endswith("_light.svg"):
            svg = svg.replace(".svg", "_light.svg")
        print("Writing modified file: " + svg)
        with open(svg, "w") as svg_light_mode:
            svg_light_mode.write(svg_light_mode_data)
    
    @staticmethod
    def inject_dark_mode(svg, svg_data, initial_colors, target_colors):
        if not svg.endswith("_light.svg"):
            print("Inject Method: Update Dark Mode Version")
            root = etree.fromstring(svg_data)
            
            for element in root.iter():
                print("Found element: "+element.tag)
                if 'fill' in element.attrib:
                    fill_color = element.attrib['fill'].lower()
                    if fill_color in initial_colors:
                        target_color = target_colors[initial_colors.index(fill_color)]
                        print(f"Changing fill color from {fill_color} to {target_color} in {etree.tostring(element)}")
                        element.attrib['fill'] = target_color
                if 'style' in element.attrib:

                        styles = element.attrib['style'].split(';')
                        new_styles = []
                        for style in styles:

                            if ':' in style:
                                style_property, style_value = style.split(':')
                                style_property = style_property.strip()
                                style_value = style_value.strip().lower()

                                if any([style_property == 'color',style_property == 'fill',style_property=="stroke"]) and (style_value.strip().lower() in initial_colors):
                                    
                                    new_value = target_colors[initial_colors.index(style_value)]
                                    new_styles.append(f'{style_property}: {new_value}')

                                    print(f"Changed style {style_property} from {style_value} to {new_value} in element {element.tag}")
                                else:
                                    prop,val = special_style_edits(element,style_property,style_value)
                                    new_styles.append('%s: %s' %(prop,val))
                            else:
                                new_styles.append(style)
                        element.attrib['style'] = '; '.join(new_styles)
                if 'data-drawio-colors' in element.attrib:

                        styles = element.attrib['data-drawio-colors'].split(';')
                        new_styles = []
                        for style in styles:
                            if ':' in style:
                                style_property, style_value = style.split(':')
                                style_property = style_property.strip()
                                style_value = style_value.strip().lower()
                                if style_property == 'color' and style_value in initial_colors:
                                    new_value = target_colors[initial_colors.index(style_value)]
                                    new_styles.append(f'{style_property}: {new_value}')
                                    print(f"Changed style color from {style_value} to {new_value} in element {element.tag}")
                                else:
                                    new_styles.append(style)
                            else:
                                new_styles.append(style)
                        element.attrib['style'] = '; '.join(new_styles)            
            svg_dark_mode_data = etree.tostring(root).decode("utf-8")
            print("Writing modified file: " + svg)
            with open(svg, "w") as svg_dark_mode:
                svg_dark_mode.write(svg_dark_mode_data)  
    @staticmethod
    def collect_data(svg, svg_data, mode, initial_colors, target_colors):
            colors = {
                # BG, FILL COLOR, BORDER COLOR, ARROW COLOR, TEXT COLOR
                "light": [],
                "dark": []
            }
            callback = None
            root = etree.fromstring(svg_data)      
            requirements_met = False
            def data_collection_end(colors,callback,*args,**kwargs):
                
                for k,v in gathered_colors[mode].copy().items():
                    v = list(set(v))
                    
                    gathered_colors[mode][k] = v
                print("Gathered colors: ",end="")
                pprint.pprint(gathered_colors)
                if callback:callback(*args,**kwargs)
                with open(r"C:\Users\jrabd\OneDrive\Documents\PYTHON_PROJECTS\School-Notes\lib\svgmodder\used_colors.json","w") as f:
                    f.write(json.dumps(gathered_colors))
            if mode == "dual":
                mode = "dark"
                callback = (InjectMode.collect_data ,svg, svg_data, "light", initial_colors, target_colors)
            if mode == "dark":
                    if not svg.endswith("_light.svg"):
                        requirements_met = True
                        print("Gather Data: Dark colors")
            elif mode == "light":
                    if svg.endswith("_light.svg"):
                        requirements_met = True
                        print("Gather Data: Light colors")                
            for element in root.iter():
                print("Found element: "+element.tag)
                if requirements_met:
                    for color_related_attr in ["fill","stroke","color"]:


                        if color_related_attr in element.attrib:
                            value = element.attrib[color_related_attr].lower()
                            if value != "none":
                                if element.tag not in gathered_colors[mode]:
                                    gathered_colors[mode][element.tag] = [value]   
                                else:                             
                                    gathered_colors[mode][element.tag].append(value)
                                print("    - %s:%s"%(color_related_attr, value))
            if callback:data_collection_end(colors,callback[0],*callback[1:])
            else:data_collection_end(colors,None)
def inject(method, *args):
    
    files_to_modify = []
    print("Gathering svg files to modify...")
    for root, sdirs, files in os.walk(ROOT):
        # Check if the current directory path matches the desired pattern
        if DIAGRAMS_PATH_PATTERN in os.path.relpath(root, ROOT):
            for file in files:
                svg = os.path.join(root, file)
                if svg.endswith(".svg"):
                    print("Adding file: " + svg.split("diagrams\\")[1])
                    files_to_modify.append(svg)
    print("Gathered svgs...")
    print("Preparing to dark mode variants...")

    for svg in files_to_modify:
        svg_data = ""
        print("Reading svg file: " + svg)
        with open(svg, "r") as svg_dark_mode:
            svg_data = svg_dark_mode.read()
        print("Modifying parameters...")
        if os.path.basename(svg) in special_color_configs:
            args = list(args)
            if mode == InjectMode.inject_dark_mode:
                args[len(args)-2],args[len(args)-1] = special_color_configs[os.path.basename(svg)]["dark"]["initial_colors"],special_color_configs[os.path.basename(svg)]["dark"]["target_colors"]
            elif mode == InjectMode.create_light_mode_version:
                args[len(args)-2],args[len(args)-1] = special_color_configs[os.path.basename(svg)]["light"]["initial_colors"],special_color_configs[os.path.basename(svg)]["light"]["target_colors"]

        method(svg, svg_data, *args)

        

def clean_accidents(delete_injects=False):
    files_to_delete = []
    print("Gathering svg files to delete...")
    for root, sdirs, files in os.walk(ROOT):
        # Check if the current directory path matches the desired pattern
        if DIAGRAMS_PATH_PATTERN in os.path.relpath(root, ROOT):
            for file in files:
                svg = os.path.join(root, file)
                if not delete_injects:
                    if svg.endswith("_light_light.svg"):
                        print("Deleting file: " + svg.split("diagrams\\")[1])
                        files_to_delete.append(svg)
                else:
                    if input("Are you sure you want delete all injected files[Y/n]? ").lower() == "y":
                        if svg.endswith("_light.svg"):
                            print("Deleting file: " + svg.split("diagrams\\")[1])
                            files_to_delete.append(svg)                    
    if len(files_to_delete) > 0:
        print("Gathered svgs...")
        print("Deleting accidental files...")
        for file in files_to_delete:
            os.remove(file)
    else:
        print("No accidents found!")

mode = InjectMode.inject_dark_mode
if mode == InjectMode.inject_dark_mode:
    initial_colors,target_colors = color_configs["dark"]["initial_colors"], color_configs["dark"]["target_colors"]
else:
    initial_colors,target_colors = color_configs["light"]["initial_colors"], color_configs["light"]["target_colors"]

if mode == InjectMode.collect_data:
    inject(mode, "dual", initial_colors,target_colors)
else:
    inject(mode, initial_colors,target_colors)

clean_accidents()
