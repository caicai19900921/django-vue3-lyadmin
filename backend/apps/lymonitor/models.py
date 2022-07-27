from django.db import models
from utils.modles import CoreModel,BaseModel
# Create your models here.

# ================================================= #
# ************** 服务端监控信息 model************** #
# ================================================= #

class MonitorManage(CoreModel):
    ip = models.CharField(max_length=50, verbose_name="服务器IP", null=True,blank=True)
    name = models.CharField(max_length=50,verbose_name="名称",null=True,blank=True)
    os = models.CharField(max_length=50, verbose_name="系统名称", null=True, blank=True)#windows、centos、小写
    online = models.BooleanField(default=False,verbose_name="在线状态")
    status = models.BooleanField(default=True,verbose_name="监控状态")#True开启 False关闭
    days = models.SmallIntegerField(default=30, verbose_name="日志保留天数")
    interval = models.SmallIntegerField(default=5, verbose_name="监控日志刷新间隔")
    islocal = models.BooleanField(default=False,verbose_name="是否是本机监控")

    class Meta:
        db_table = 'tb_monitor'
        verbose_name = "服务监控"
        verbose_name_plural = verbose_name
