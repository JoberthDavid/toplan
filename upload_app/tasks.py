from upload_app.usefuls.processing_file import FileProcessor
from upload_app.models import ModelFileCost

from celery import shared_task
from celery.utils.log import get_task_logger

from PyPDF2 import PdfReader

from io import BytesIO


logger = get_task_logger(__name__)


def get_list_of_inputs_of_composition( pdf_content, page_selected: int ) -> list:
    return pdf_content.pages[page_selected].extract_text().split('\n')

def extract_text_from_pdf_file( selected_object: ModelFileCost, page_dict: dict, num_pages: int ) -> FileProcessor:
    result = FileProcessor( selected_object=selected_object, page_dict=page_dict, num_pages=num_pages )
    return result

def save_status_file( selected_object: ModelFileCost ) -> bool:
    try:
        selected_object.status=True
        selected_object.save()
        return True
    except:
        return False

@shared_task
def process_file_in_background( id: int ) -> bool:

    selected_object = ModelFileCost.objects.get(id=id)
    
    with selected_object.file.open(mode="rb") as opened_file:
        bytes_stream = BytesIO(opened_file.read())
        pdf_content = PdfReader(bytes_stream)

    num_pages = len(pdf_content.pages)
    page_dict = {}

    for page_selected in range(num_pages):
        page_dict[page_selected] = get_list_of_inputs_of_composition( pdf_content, page_selected )

    result = extract_text_from_pdf_file( selected_object=selected_object, page_dict=page_dict, num_pages=num_pages )

    status_file = save_status_file( selected_object= selected_object )

    return status_file