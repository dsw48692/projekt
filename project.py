import json
import yaml
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Konwerter plików")
        self.geometry("400x200")

        self.input_file = None
        self.output_file = None

        self.create_widgets()

    def create_widgets(self):
        self.input_label = tk.Label(self, text="Plik wejściowy:")
        self.input_label.pack()

        self.input_entry = tk.Entry(self, width=40)
        self.input_entry.pack()

        self.input_button = tk.Button(self, text="Wybierz plik", command=self.choose_input_file)
        self.input_button.pack()

        self.output_label = tk.Label(self, text="Plik wyjściowy:")
        self.output_label.pack()

        self.output_entry = tk.Entry(self, width=40)
        self.output_entry.pack()

        self.output_button = tk.Button(self, text="Wybierz plik", command=self.choose_output_file)
        self.output_button.pack()

        self.convert_button = tk.Button(self, text="Konwertuj", command=self.convert_files)
        self.convert_button.pack()

    def choose_input_file(self):
        self.input_file = filedialog.askopenfilename(
            filetypes=(("XML files", "*.xml"), ("JSON files", "*.json"), ("YAML files", "*.yaml"))
        )
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, self.input_file)

    def choose_output_file(self):
        self.output_file = filedialog.asksaveasfilename(
            filetypes=(("XML files", "*.xml"), ("JSON files", "*.json"), ("YAML files", "*.yaml"))
        )
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, self.output_file)

    def convert_files(self):
        if not self.input_file or not self.output_file:
            messagebox.showerror("Błąd", "Proszę wybrać plik wejściowy i plik wyjściowy.")
            return

        input_file_extension = self.get_file_extension(self.input_file)
        output_file_extension = self.get_file_extension(self.output_file)

        if input_file_extension == "xml" and (output_file_extension == "json" or output_file_extension == "yaml"):
            self.xml_to_json_or_yaml(self.input_file, self.output_file, output_file_extension)
        elif input_file_extension == "json" and (output_file_extension == "xml" or output_file_extension == "yaml"):
            self.json_to_xml_or_yaml(self.input_file, self.output_file, output_file_extension)
        elif input_file_extension == "yaml" and (output_file_extension == "xml" or output_file_extension == "json"):
            self.yaml_to_xml_or_json(self.input_file, self.output_file, output_file_extension)
        else:
            messagebox.showerror("Błąd", "Nieobsługiwana kombinacja konwersji.")

    def get_file_extension(self, filename):
        return filename.split(".")[-1].lower()

    def xml_to_json_or_yaml(self, xml_file, output_file, output_file_extension):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        data = self.xml_to_dict(root)

        if output_file_extension == "json":
            with open(output_file, "w") as file:
                json.dump(data, file, indent=4)
            messagebox.showinfo("Sukces", "Plik XML został pomyślnie skonwertowany do JSON.")
        elif output_file_extension == "yaml":
            with open(output_file, "w") as file:
                yaml.dump(data, file)
            messagebox.showinfo("Sukces", "Plik XML został pomyślnie skonwertowany do YAML.")

    def json_to_xml_or_yaml(self, json_file, output_file, output_file_extension):
        with open(json_file, "r") as file:
            data = json.load(file)

        if output_file_extension == "xml":
            root = self.dict_to_xml(data)
            tree = ET.ElementTree(root)
            tree.write(output_file, encoding="utf-8", xml_declaration=True)
            messagebox.showinfo("Sukces", "Plik JSON został pomyślnie skonwertowany do XML.")
        elif output_file_extension == "yaml":
            with open(output_file, "w") as file:
                yaml.dump(data, file)
            messagebox.showinfo("Sukces", "Plik JSON został pomyślnie skonwertowany do YAML.")

    def yaml_to_xml_or_json(self, yaml_file, output_file, output_file_extension):
        with open(yaml_file, "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

        if output_file_extension == "xml":
            root = self.dict_to_xml(data)
            tree = ET.ElementTree(root)
            tree.write(output_file, encoding="utf-8", xml_declaration=True)
            messagebox.showinfo("Sukces", "Plik YAML został pomyślnie skonwertowany do XML.")
        elif output_file_extension == "json":
            with open(output_file, "w") as file:
                json.dump(data, file, indent=4)
            messagebox.showinfo("Sukces", "Plik YAML został pomyślnie skonwertowany do JSON.")

    def xml_to_dict(self, element):
        if len(element) == 0:
            return element.text
        result = {}
        for child in element:
            child_data = self.xml_to_dict(child)
            if child.tag in result:
                if type(result[child.tag]) is list:
                    result[child.tag].append(child_data)
                else:
                    result[child.tag] = [result[child.tag], child_data]
            else:
                result[child.tag] = child_data
        return result

    def dict_to_xml(self, data):
        if isinstance(data, dict):
            root = ET.Element("root")
            for key, value in data.items():
                sub_element = self.dict_to_xml(value)
                if isinstance(value, list):
                    for item in value:
                        root.append(self.dict_to_xml({key: item}))
                else:
                    element = ET.SubElement(root, key)
                    element.append(sub_element)
            return root
        else:
            return ET.Element("item", attrib={"value": str(data)})


if __name__ == "__main__":
    app = Application()
    app.mainloop()
