import PyPDF2

from upload_app.models import ModelFileCost


class FileProcessor:
        
    def __init__(self, selected_object: ModelFileCost) -> None:
        self.selected_object = selected_object
        self.access_file()
        self.extract_text_by_pdf_file()

    def access_file(self):
        with self.selected_object.file.open(mode="rb") as openned_file:
            self.pdf_content = PyPDF2.PdfReader(openned_file)

    def extract_text_by_pdf_file(self):
        if self.selected_object.type_file == 'AN':
            print(self.pdf_content.pages[4501].extract_text())
            # print(type(pdf_content.pages[4501].extract_text()))
        else:
            for page in self.pdf_content.pages:
                print(page.extract_text())