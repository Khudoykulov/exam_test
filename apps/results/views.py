from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ExamResult


@login_required
def result_list(request):
    """Natijalar ro'yxati"""
    results = ExamResult.objects.filter(
        student=request.user
    ).select_related('exam', 'exam__subject').order_by('-created_at')
    
    context = {
        'results': results
    }
    
    return render(request, 'results/result_list.html', context)


@login_required
def result_detail(request, result_id):
    """Natija tafsilotlari"""
    # O'qituvchi va admin barcha natijalarni ko'ra oladi
    if request.user.user_type in ('teacher', 'admin'):
        result = get_object_or_404(ExamResult, id=result_id)
    else:
        result = get_object_or_404(
            ExamResult,
            id=result_id,
            student=request.user
        )
    
    context = {
        'result': result
    }
    
    return render(request, 'results/result_detail.html', context)
