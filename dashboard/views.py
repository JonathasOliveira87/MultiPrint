from django.shortcuts import render
from django.contrib.auth.decorators import login_required



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from documents.models import Document, PrintKit

@login_required
def dashboard(request):
    user = request.user
    total_documents = Document.objects.filter(user=user).count()
    total_kits = PrintKit.objects.filter(user=user).count()
    kits = PrintKit.objects.filter(user=user)

    return render(request, "dashboard/index.html", {
        "total_documents": total_documents,
        "total_kits": total_kits,
        "kits": kits
    })
