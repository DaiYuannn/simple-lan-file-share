from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden

from .models import SharedFile


def _is_admin_client(request: HttpRequest) -> bool:
	"""判断当前请求是否来自“服务器端或管理员端”。

	当前实现策略：仅允许来自本机的请求执行管理操作：
	- 访问地址为 127.0.0.1/localhost
	- 或 REMOTE_ADDR 为 127.0.0.1

	如需更复杂的策略（例如特定 IP 白名单 / 简单口令），可在此扩展。
	"""
	host = request.get_host().split(":")[0]
	remote_addr = request.META.get("REMOTE_ADDR", "")
	return host in {"127.0.0.1", "localhost"} or remote_addr == "127.0.0.1"


def index(request: HttpRequest) -> HttpResponse:
	if request.method == "POST" and request.FILES.get("file"):
		upload = request.FILES["file"]
		name = request.POST.get("name", "")
		SharedFile.objects.create(name=name, file=upload)
		return redirect("fileshare:index")

	files = SharedFile.objects.order_by("-uploaded_at")
	is_admin = _is_admin_client(request)
	return render(request, "fileshare/index.html", {"files": files, "is_admin": is_admin})


def delete_file(request: HttpRequest, pk: int) -> HttpResponse:
	if not _is_admin_client(request):
		return HttpResponseForbidden("仅允许在服务器端/管理员端删除文件。")

	file_obj = get_object_or_404(SharedFile, pk=pk)
	file_obj.file.delete(save=False)
	file_obj.delete()
	return redirect("fileshare:index")
