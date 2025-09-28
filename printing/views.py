from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from documents.models import Document, PrintKit
import os, tempfile
from PyPDF2 import PdfMerger
from docx2pdf import convert
import win32api

@login_required
def print_documents(request):
    message = ""
    kits = PrintKit.objects.filter(user=request.user)
    documents = Document.objects.filter(user=request.user)

    if request.method == "POST":
        selected_kit_ids = request.POST.getlist("kits")
        selected_doc_ids = request.POST.getlist("documents")
        from_dashboard = request.POST.get("from_dashboard")  # verifica se veio do dashboard

        # Começa com documentos selecionados manualmente
        documents_to_print = Document.objects.filter(id__in=selected_doc_ids, user=request.user)

        # Adiciona documentos dos kits selecionados
        if selected_kit_ids:
            for kit_id in selected_kit_ids:
                try:
                    kit = PrintKit.objects.get(id=kit_id, user=request.user)
                    documents_to_print = documents_to_print | kit.documents.all()
                except PrintKit.DoesNotExist:
                    continue

        documents_to_print = documents_to_print.distinct()

        # Converter para PDF e criar PDF único
        temp_pdfs = []
        for doc in documents_to_print:
            try:
                if doc.file.name.lower().endswith(".docx"):
                    temp_pdf = os.path.join(tempfile.gettempdir(), os.path.basename(doc.file.name).replace(".docx", ".pdf"))
                    convert(doc.file.path, temp_pdf)
                    temp_pdfs.append(temp_pdf)
                elif doc.file.name.lower().endswith(".pdf"):
                    temp_pdfs.append(doc.file.path)
            except Exception:
                message += f"Erro ao converter {os.path.basename(doc.file.name)}. Verifique se o Word está instalado."

        # Abrir PDF final para impressão
        if temp_pdfs:
            final_pdf = os.path.join(tempfile.gettempdir(), "Documentos_Para_Impressao.pdf")
            merger = PdfMerger()
            for pdf in temp_pdfs:
                merger.append(pdf)
            merger.write(final_pdf)
            merger.close()
            win32api.ShellExecute(0, "open", final_pdf, None, ".", 1)

        # Redireciona apenas se veio do dashboard
        if from_dashboard:
            return redirect("dashboard")

    return render(request, "printing/print_documents.html", {
        "documents": documents,
        "kits": kits,
        "message": message
    })
