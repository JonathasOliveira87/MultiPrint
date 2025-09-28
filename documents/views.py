import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Document, PrintKit
from django.contrib import messages



@login_required
def document_list(request):
    documents = Document.objects.filter(user=request.user).order_by("-uploaded_at")
    return render(request, "documents/list.html", {"documents": documents})


@login_required
def upload_document(request):
    if request.method == "POST":
        files = request.FILES.getlist('files')
        for f in files:
            Document.objects.create(file=f, user=request.user)
        return redirect('document_list')
    return render(request, 'documents/upload.html')


@login_required
def document_delete(request, pk):
    doc = get_object_or_404(Document, pk=pk, user=request.user)

    # Verifica se o documento está em algum kit
    kits_with_doc = PrintKit.objects.filter(user=request.user, documents=doc)
    if kits_with_doc.exists():
        kit_names = ", ".join(k.name for k in kits_with_doc)  # pega os nomes dos kits
        messages.error(request, f"Não é possível deletar este documento, pois ele está nos seguintes kits: {kit_names}.")
        return redirect("document_list")

    # Se não estiver em nenhum kit, pode deletar
    if doc.file:
        import os
        from django.conf import settings
        file_path = os.path.join(settings.MEDIA_ROOT, str(doc.file))
        if os.path.exists(file_path):
            os.remove(file_path)
    doc.delete()
    messages.success(request, "Documento deletado com sucesso.")
    return redirect("document_list")


@login_required
def create_kit(request, kit_id=None):
    if kit_id:
        kit = get_object_or_404(PrintKit, id=kit_id, user=request.user)
    else:
        kit = None

    if request.method == "POST":
        name = request.POST.get("name")
        doc_ids = request.POST.getlist("documents")

        if name and doc_ids:
            if kit:
                kit.name = name
                kit.documents.set(Document.objects.filter(id__in=doc_ids, user=request.user))
                kit.save()
            else:
                kit = PrintKit.objects.create(user=request.user, name=name)
                kit.documents.set(Document.objects.filter(id__in=doc_ids, user=request.user))
            return redirect("create_kit")  # redireciona para a mesma página

    documents = Document.objects.filter(user=request.user)
    kits = PrintKit.objects.filter(user=request.user)  # <-- pega todos os kits do usuário
    return render(request, "documents/create_kit.html", {
        "documents": documents,
        "kit": kit,
        "kits": kits  # <-- passa para o template
    })


@login_required
def kit_delete(request, kit_id):
    kit = get_object_or_404(PrintKit, id=kit_id, user=request.user)
    # Se não tiver documentos, pode deletar
    kit.delete()
    messages.success(request, "Kit deletado com sucesso.")
    return redirect("create_kit")


@login_required
def edit_kit(request, kit_id):
    """
    Edita um kit existente.
    """
    kit = get_object_or_404(PrintKit, id=kit_id, user=request.user)

    if request.method == "POST":
        name = request.POST.get("name")
        doc_ids = request.POST.getlist("documents")

        if name and doc_ids:
            kit.name = name
            kit.documents.set(Document.objects.filter(id__in=doc_ids, user=request.user))
            kit.save()
            return redirect("create_kit")  # volta para a lista de kits

    documents = Document.objects.filter(user=request.user)
    kits = PrintKit.objects.filter(user=request.user)
    return render(request, "documents/create_kit.html", {
        "documents": documents,
        "kit": kit,
        "kits": kits
    })
